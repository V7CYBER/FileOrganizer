from datetime import datetime

import core.analizador_logs


def test_analizar_linea_utiliza_constructor_eventos(
    monkeypatch,
):
    # ARRANGE
    evento_creado = {
        "linea": 99,
        "ip": "10.0.0.10",
        "tipo": "EVENTO_PRUEBA",
        "severidad": "ALTA",
        "regla": "TEST_001",
        "descripcion": "Evento construido por el normalizador",
        "contenido": "contenido",
    }

    monkeypatch.setattr(
        core.analizador_logs,
        "crear_evento_seguridad",
        lambda **_kwargs: evento_creado,
    )

    monkeypatch.setattr(
        core.analizador_logs,
        "evaluar_linea_con_reglas",
        lambda _linea, _reglas: [
            {
                "id": "TEST_001",
                "tipo": "EVENTO_PRUEBA",
                "severidad": "ALTA",
                "descripcion": "Evento de prueba",
                "patrones": [],
            }
        ],
    )

    # ACT
    eventos = core.analizador_logs.analizar_linea(
        "10.0.0.10 contenido",
        5,
    )

    # ASSERT
    assert eventos == [evento_creado]


def test_analizar_linea_incluye_fecha_normalizada():
    # ARRANGE
    linea = "192.168.1.20 - - " "[16/Aug/2026:09:01:16] " "Failed password"

    # ACT
    eventos = core.analizador_logs.analizar_linea(
        linea,
        10,
    )

    # ASSERT
    assert len(eventos) == 1

    evento = eventos[0]

    assert evento["fecha"] == datetime(  # noqa: DTZ001
        2026,
        8,
        16,
        9,
        1,
        16,
    )
