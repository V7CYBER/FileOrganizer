from pathlib import Path

import pytest

from core.analizador_logs import (
    analizar_log,
    generar_resumen_logs,
    agrupar_eventos_por_ip,
    detectar_fuerza_bruta_por_ip,
)


def test_analizar_log_detecta_eventos(tmp_path):
    # ARRANGE
    archivo = tmp_path / "access.log"

    archivo.write_text(
        "\n".join(
            [
                '192.168.1.10 "GET /index.html HTTP/1.1" 200',
                "192.168.1.20 Failed login",
                "192.168.1.30 UNION SELECT username FROM users",
            ]
        ),
        encoding="utf-8",
    )

    # ACT
    eventos = analizar_log(archivo)

    # ASSERT
    assert len(eventos) == 2

    assert eventos[0]["tipo"] == "FUERZA_BRUTA"
    assert eventos[0]["ip"] == "192.168.1.20"

    assert eventos[1]["tipo"] == "SQL_INJECTION"
    assert eventos[1]["ip"] == "192.168.1.30"


def test_analizar_log_archivo_inexistente(tmp_path):
    # ARRANGE
    archivo = tmp_path / "no_existe.log"

    # ACT + ASSERT
    with pytest.raises(FileNotFoundError):
        analizar_log(archivo)


def test_analizar_log_ruta_no_archivo(tmp_path):
    # ACT + ASSERT
    with pytest.raises(ValueError):
        analizar_log(tmp_path)


def test_generar_resumen_logs():
    # ARRANGE
    eventos = [
        {
            "tipo": "SQL_INJECTION",
            "severidad": "ALTA",
        },
        {
            "tipo": "SQL_INJECTION",
            "severidad": "ALTA",
        },
        {
            "tipo": "FUERZA_BRUTA",
            "severidad": "MEDIA",
        },
    ]

    # ACT
    resumen = generar_resumen_logs(eventos)

    # ASSERT
    assert resumen == {
        "eventos": 3,
        "sql_injection": 2,
        "fuerza_bruta": 1,
        "alta": 2,
        "media": 1,
    }


def test_agrupar_eventos_por_ip():
    # ARRANGE
    eventos = [
        {
            "ip": "192.168.1.20",
            "tipo": "FUERZA_BRUTA",
        },
        {
            "ip": "192.168.1.20",
            "tipo": "FUERZA_BRUTA",
        },
        {
            "ip": "192.168.1.30",
            "tipo": "SQL_INJECTION",
        },
        {
            "ip": None,
            "tipo": "SQL_INJECTION",
        },
    ]

    # ACT
    agrupados = agrupar_eventos_por_ip(eventos)

    # ASSERT
    assert set(agrupados) == {
        "192.168.1.20",
        "192.168.1.30",
    }

    assert len(agrupados["192.168.1.20"]) == 2
    assert len(agrupados["192.168.1.30"]) == 1


def test_detectar_fuerza_bruta_por_ip():
    # ARRANGE
    eventos = [
        {
            "linea": 1,
            "ip": "192.168.1.20",
            "tipo": "FUERZA_BRUTA",
        },
        {
            "linea": 2,
            "ip": "192.168.1.20",
            "tipo": "FUERZA_BRUTA",
        },
        {
            "linea": 3,
            "ip": "192.168.1.20",
            "tipo": "FUERZA_BRUTA",
        },
        {
            "linea": 4,
            "ip": "192.168.1.30",
            "tipo": "FUERZA_BRUTA",
        },
    ]

    # ACT
    alertas = detectar_fuerza_bruta_por_ip(
        eventos,
        umbral=3,
    )

    # ASSERT
    assert len(alertas) == 1

    alerta = alertas[0]

    assert alerta["ip"] == "192.168.1.20"
    assert alerta["tipo"] == "POSIBLE_FUERZA_BRUTA"
    assert alerta["severidad"] == "ALTA"
    assert alerta["intentos"] == 3
    assert alerta["lineas"] == [1, 2, 3]
