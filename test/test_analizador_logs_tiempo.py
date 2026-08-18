from datetime import datetime

import pytest

from core.analizador_logs import (
    convertir_fecha_log,
    extraer_fecha_log,
)


def test_extraer_fecha_log_valida():
    # ARRANGE
    linea = (
        '192.168.1.20 - - '
        '[16/Aug/2026:09:01:16] '
        '"POST /login HTTP/1.1" 401'
    )

    # ACT
    resultado = extraer_fecha_log(linea)

    # ASSERT
    assert resultado == "16/Aug/2026:09:01:16"


def test_extraer_fecha_log_sin_fecha():
    # ARRANGE
    linea = "192.168.1.20 Failed password"

    # ACT
    resultado = extraer_fecha_log(linea)

    # ASSERT
    assert resultado is None


def test_convertir_fecha_log_valida():
    # ARRANGE
    fecha_texto = "16/Aug/2026:09:01:16"

    # ACT
    resultado = convertir_fecha_log(fecha_texto)

    # ASSERT
    # El resultado esperado es naive porque
    # el log de origen no contiene zona horaria.
    assert resultado == datetime(  # noqa: DTZ001
        2026,
        8,
        16,
        9,
        1,
        16,
    )


def test_convertir_fecha_log_none():
    # ACT
    resultado = convertir_fecha_log(None)

    # ASSERT
    assert resultado is None


def test_convertir_fecha_log_invalida():
    # ARRANGE
    fecha_texto = "fecha-invalida"

    # ACT + ASSERT
    with pytest.raises(ValueError):
        convertir_fecha_log(fecha_texto)
