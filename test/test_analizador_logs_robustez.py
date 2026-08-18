from core.analizador_logs import (
    analizar_log,
    detectar_fuerza_bruta_temporal,
    generar_resumen_logs,
)


def test_log_vacio(tmp_path):
    # ARRANGE
    archivo = tmp_path / "vacio.log"
    archivo.write_text("", encoding="utf-8")

    # ACT
    eventos = analizar_log(archivo)
    resumen = generar_resumen_logs(eventos)

    # ASSERT
    assert eventos == []

    assert resumen == {
        "eventos": 0,
        "sql_injection": 0,
        "fuerza_bruta": 0,
        "alta": 0,
        "media": 0,
    }


def test_log_con_bytes_invalidos_utf8(tmp_path):
    # ARRANGE
    archivo = tmp_path / "bytes_invalidos.log"

    archivo.write_bytes(
        b"\xff\xfe\xfa contenido corrupto\n"
        b"192.168.1.20 Failed password\n"
    )

    # ACT
    eventos = analizar_log(archivo)

    # ASSERT
    assert len(eventos) == 1
    assert eventos[0]["tipo"] == "FUERZA_BRUTA"
    assert eventos[0]["ip"] == "192.168.1.20"


def test_log_solo_lineas_legitimas(tmp_path):
    # ARRANGE
    archivo = tmp_path / "normal.log"

    archivo.write_text(
        '192.168.1.10 "GET /index.html HTTP/1.1" 200\n'
        '192.168.1.11 "GET /contacto HTTP/1.1" 200\n'
        '192.168.1.12 "POST /formulario HTTP/1.1" 201',
        encoding="utf-8",
    )

    # ACT
    eventos = analizar_log(archivo)

    # ASSERT
    assert eventos == []


def test_correlacion_ignora_evento_sin_fecha():
    # ARRANGE
    eventos = [
        {
            "linea": 1,
            "ip": "192.168.1.20",
            "tipo": "FUERZA_BRUTA",
            "severidad": "MEDIA",
            "contenido": "192.168.1.20 Failed password",
        },
        {
            "linea": 2,
            "ip": "192.168.1.20",
            "tipo": "FUERZA_BRUTA",
            "severidad": "MEDIA",
            "contenido": "192.168.1.20 Failed password",
        },
        {
            "linea": 3,
            "ip": "192.168.1.20",
            "tipo": "FUERZA_BRUTA",
            "severidad": "MEDIA",
            "contenido": "192.168.1.20 Failed password",
        },
    ]

    # ACT
    alertas = detectar_fuerza_bruta_temporal(
        eventos,
        umbral=3,
        ventana_segundos=60,
    )

    # ASSERT
    assert alertas == []
