from datetime import datetime

import pytest

from core.alertas import crear_alerta_seguridad


def test_crear_alerta_seguridad_genera_estructura_normalizada():
    # ARRANGE
    ip = "192.168.1.20"
    intentos = 3
    ventana_segundos = 20.0
    lineas = [1, 2, 3]

    # ACT
    alerta = crear_alerta_seguridad(
        ip=ip,
        intentos=intentos,
        ventana_segundos=ventana_segundos,
        lineas=lineas,
    )

    # ASSERT
    assert alerta == {
        "ip": "192.168.1.20",
        "tipo": "POSIBLE_FUERZA_BRUTA",
        "severidad": "ALTA",
        "intentos": 3,
        "ventana_segundos": 20.0,
        "lineas": [1, 2, 3],
        "fecha": None,
    }


def test_crear_alerta_seguridad_incluye_fecha():
    # ARRANGE
    fecha = datetime(  # noqa: DTZ001
        2026,
        8,
        16,
        9,
        1,
        16,
    )

    # ACT
    alerta = crear_alerta_seguridad(
        ip="192.168.1.20",
        intentos=3,
        ventana_segundos=20,
        lineas=[1, 2, 3],
        fecha=fecha,
    )

    # ASSERT
    assert alerta["fecha"] == fecha


def test_crear_alerta_seguridad_rechaza_intentos_invalidos():
    # ACT / ASSERT
    with pytest.raises(
        ValueError,
        match="Intentos inválidos",
    ):
        crear_alerta_seguridad(
            ip="192.168.1.20",
            intentos=0,
            ventana_segundos=20.0,
            lineas=[1, 2, 3],
        )


def test_crear_alerta_seguridad_rechaza_tipo_intentos_invalido():
    # ACT / ASSERT
    with pytest.raises(
        TypeError,
        match="Intentos inválidos",
    ):
        crear_alerta_seguridad(
            ip="192.168.1.20",
            intentos="3",
            ventana_segundos=20.0,
            lineas=[1, 2, 3],
        )
