import core.analizador_logs


def test_correlacion_utiliza_constructor_alertas(
    monkeypatch,
):
    # ARRANGE
    alerta_creada = {
        "ip": "192.168.1.20",
        "tipo": "POSIBLE_FUERZA_BRUTA",
        "severidad": "ALTA",
        "intentos": 3,
        "ventana_segundos": 20.0,
        "lineas": [1, 2, 3],
        "fecha": None,
    }

    monkeypatch.setattr(
        core.analizador_logs,
        "crear_alerta_seguridad",
        lambda **_kwargs: alerta_creada,
    )

    eventos = [
        {
            "linea": 1,
            "ip": "192.168.1.20",
            "tipo": "FUERZA_BRUTA",
            "severidad": "MEDIA",
            "contenido": (
                "192.168.1.20 - - "
                "[16/Aug/2026:09:00:00] "
                "Failed password"
            ),
        },
        {
            "linea": 2,
            "ip": "192.168.1.20",
            "tipo": "FUERZA_BRUTA",
            "severidad": "MEDIA",
            "contenido": (
                "192.168.1.20 - - "
                "[16/Aug/2026:09:00:10] "
                "Failed password"
            ),
        },
        {
            "linea": 3,
            "ip": "192.168.1.20",
            "tipo": "FUERZA_BRUTA",
            "severidad": "MEDIA",
            "contenido": (
                "192.168.1.20 - - "
                "[16/Aug/2026:09:00:20] "
                "Failed password"
            ),
        },
    ]

    # ACT
    alertas = core.analizador_logs.detectar_fuerza_bruta_temporal(
        eventos,
        umbral=3,
        ventana_segundos=60,
    )

    # ASSERT
    assert alertas == [alerta_creada]
