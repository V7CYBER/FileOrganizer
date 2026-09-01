from datetime import datetime

import pytest

from core.eventos import crear_evento_seguridad


def test_crear_evento_seguridad_genera_estructura_normalizada():
    # ARRANGE
    regla = {
        "id": "WEB_SQL_001",
        "tipo": "SQL_INJECTION",
        "severidad": "ALTA",
        "descripcion": "Posible intento de SQL Injection",
    }

    # ACT
    evento = crear_evento_seguridad(
        linea=10,
        ip="192.168.1.30",
        regla=regla,
        contenido="UNION SELECT username FROM users",
    )

    # ASSERT
    assert evento == {
        "linea": 10,
        "ip": "192.168.1.30",
        "tipo": "SQL_INJECTION",
        "severidad": "ALTA",
        "regla": "WEB_SQL_001",
        "descripcion": "Posible intento de SQL Injection",
        "contenido": "UNION SELECT username FROM users",
        "fecha": None,
    }


def test_crear_evento_seguridad_permite_ip_ausente():
    # ARRANGE
    regla = {
        "id": "AUTH_FAIL_001",
        "tipo": "FUERZA_BRUTA",
        "severidad": "MEDIA",
        "descripcion": "Intento de autenticación fallido",
    }

    # ACT
    evento = crear_evento_seguridad(
        linea=5,
        ip=None,
        regla=regla,
        contenido="Failed login",
    )

    # ASSERT
    assert evento["ip"] is None
    assert evento["regla"] == "AUTH_FAIL_001"
    assert evento["tipo"] == "FUERZA_BRUTA"


def test_crear_evento_seguridad_rechaza_regla_incompleta():
    # ARRANGE
    regla = {
        "id": "WEB_SQL_001",
        "tipo": "SQL_INJECTION",
        "severidad": "ALTA",
    }

    # ACT / ASSERT
    with pytest.raises(
        ValueError,
        match="Regla incompleta",
    ):
        crear_evento_seguridad(
            linea=10,
            ip="192.168.1.30",
            regla=regla,
            contenido="UNION SELECT",
        )


def test_crear_evento_seguridad_rechaza_linea_invalida():
    # ARRANGE
    regla = {
        "id": "WEB_SQL_001",
        "tipo": "SQL_INJECTION",
        "severidad": "ALTA",
        "descripcion": "Posible intento de SQL Injection",
    }

    # ACT / ASSERT
    with pytest.raises(
        ValueError,
        match="Línea inválida",
    ):
        crear_evento_seguridad(
            linea=0,
            ip="192.168.1.30",
            regla=regla,
            contenido="UNION SELECT",
        )


def test_crear_evento_seguridad_rechaza_contenido_invalido():
    # ARRANGE
    regla = {
        "id": "WEB_SQL_001",
        "tipo": "SQL_INJECTION",
        "severidad": "ALTA",
        "descripcion": "Posible intento de SQL Injection",
    }

    # ACT / ASSERT
    with pytest.raises(
        TypeError,
        match="Contenido inválido",
    ):
        crear_evento_seguridad(
            linea=10,
            ip="192.168.1.30",
            regla=regla,
            contenido=None,
        )


def test_crear_evento_seguridad_rechaza_tipo_linea_invalido():
    # ARRANGE
    regla = {
        "id": "WEB_SQL_001",
        "tipo": "SQL_INJECTION",
        "severidad": "ALTA",
        "descripcion": "Posible intento de SQL Injection",
    }

    # ACT / ASSERT
    with pytest.raises(
        TypeError,
        match="Línea inválida",
    ):
        crear_evento_seguridad(
            linea="10",
            ip="192.168.1.30",
            regla=regla,
            contenido="UNION SELECT",
        )


def test_crear_evento_seguridad_incluye_fecha():
    # ARRANGE
    regla = {
        "id": "AUTH_FAIL_001",
        "tipo": "FUERZA_BRUTA",
        "severidad": "MEDIA",
        "descripcion": "Intento de autenticación fallido",
    }

    fecha = datetime(  # noqa: DTZ001
        2026,
        8,
        16,
        9,
        1,
        16,
    )

    # ACT
    evento = crear_evento_seguridad(
        linea=5,
        ip="192.168.1.20",
        regla=regla,
        contenido="Failed password",
        fecha=fecha,
    )

    # ASSERT
    assert evento["fecha"] == fecha
