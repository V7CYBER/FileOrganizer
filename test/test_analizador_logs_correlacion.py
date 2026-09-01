from datetime import datetime

from core.analizador_logs import detectar_fuerza_bruta_temporal


def crear_evento(ip, fecha, linea):
    """
    Crea un evento de autenticación fallida
    para las pruebas de correlación temporal.
    """

    return {
        "linea": linea,
        "ip": ip,
        "tipo": "FUERZA_BRUTA",
        "severidad": "MEDIA",
        "contenido": (
            f"{ip} - - [{fecha}] " '"POST /login HTTP/1.1" 401 Failed password'
        ),
    }


def test_detectar_fuerza_bruta_en_ventana_temporal():
    # ARRANGE
    eventos = [
        crear_evento(
            "192.168.1.20",
            "16/Aug/2026:09:01:16",
            3,
        ),
        crear_evento(
            "192.168.1.20",
            "16/Aug/2026:09:01:17",
            4,
        ),
        crear_evento(
            "192.168.1.20",
            "16/Aug/2026:09:01:18",
            5,
        ),
    ]

    # ACT
    alertas = detectar_fuerza_bruta_temporal(
        eventos,
        umbral=3,
        ventana_segundos=60,
    )

    # ASSERT
    assert len(alertas) == 1

    alerta = alertas[0]

    assert alerta["ip"] == "192.168.1.20"
    assert alerta["tipo"] == "POSIBLE_FUERZA_BRUTA"
    assert alerta["severidad"] == "ALTA"
    assert alerta["intentos"] == 3
    assert alerta["ventana_segundos"] == 2.0
    assert alerta["lineas"] == [3, 4, 5]


def test_no_alerta_si_intentos_estan_separados():
    # ARRANGE
    eventos = [
        crear_evento(
            "192.168.1.20",
            "16/Aug/2026:09:00:00",
            1,
        ),
        crear_evento(
            "192.168.1.20",
            "16/Aug/2026:09:02:00",
            2,
        ),
        crear_evento(
            "192.168.1.20",
            "16/Aug/2026:09:04:00",
            3,
        ),
    ]

    # ACT
    alertas = detectar_fuerza_bruta_temporal(
        eventos,
        umbral=3,
        ventana_segundos=60,
    )

    # ASSERT
    assert alertas == []


def test_no_alerta_si_ips_son_diferentes():
    # ARRANGE
    eventos = [
        crear_evento(
            "192.168.1.10",
            "16/Aug/2026:09:00:00",
            1,
        ),
        crear_evento(
            "192.168.1.20",
            "16/Aug/2026:09:00:01",
            2,
        ),
        crear_evento(
            "192.168.1.30",
            "16/Aug/2026:09:00:02",
            3,
        ),
    ]

    # ACT
    alertas = detectar_fuerza_bruta_temporal(
        eventos,
        umbral=3,
        ventana_segundos=60,
    )

    # ASSERT
    assert alertas == []


def test_no_alerta_por_debajo_del_umbral():
    # ARRANGE
    eventos = [
        crear_evento(
            "192.168.1.20",
            "16/Aug/2026:09:00:00",
            1,
        ),
        crear_evento(
            "192.168.1.20",
            "16/Aug/2026:09:00:01",
            2,
        ),
    ]

    # ACT
    alertas = detectar_fuerza_bruta_temporal(
        eventos,
        umbral=3,
        ventana_segundos=60,
    )

    # ASSERT
    assert alertas == []


def test_correlacion_temporal_utiliza_fecha_normalizada():
    # ARRANGE
    eventos = [
        {
            "linea": 1,
            "ip": "192.168.1.20",
            "tipo": "FUERZA_BRUTA",
            "severidad": "MEDIA",
            "contenido": "sin fecha en contenido",
            "fecha": datetime(  # noqa: DTZ001
                2026,
                8,
                16,
                9,
                0,
                0,
            ),
        },
        {
            "linea": 2,
            "ip": "192.168.1.20",
            "tipo": "FUERZA_BRUTA",
            "severidad": "MEDIA",
            "contenido": "sin fecha en contenido",
            "fecha": datetime(  # noqa: DTZ001
                2026,
                8,
                16,
                9,
                0,
                10,
            ),
        },
        {
            "linea": 3,
            "ip": "192.168.1.20",
            "tipo": "FUERZA_BRUTA",
            "severidad": "MEDIA",
            "contenido": "sin fecha en contenido",
            "fecha": datetime(  # noqa: DTZ001
                2026,
                8,
                16,
                9,
                0,
                20,
            ),
        },
    ]

    # ACT
    alertas = detectar_fuerza_bruta_temporal(
        eventos,
        umbral=3,
        ventana_segundos=60,
    )

    # ASSERT
    assert len(alertas) == 1
    assert alertas[0]["ip"] == "192.168.1.20"
    assert alertas[0]["intentos"] == 3
