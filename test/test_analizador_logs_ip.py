import pytest

from core.analizador_logs import extraer_ip


@pytest.mark.parametrize(
    ("linea", "esperado"),
    [
        (
            "Login failed from 192.168.1.20",
            "192.168.1.20",
        ),
        (
            "Origen 10.0.0.15 autenticación fallida",
            "10.0.0.15",
        ),
        (
            "IP mínima 0.0.0.0",
            "0.0.0.0",
        ),
        (
            "IP máxima 255.255.255.255",
            "255.255.255.255",
        ),
        (
            "Sin dirección IP en esta línea",
            None,
        ),
        (
            "999.999.999.999 Failed login",
            None,
        ),
        (
            "256.1.1.1 Failed login",
            None,
        ),
        (
            "Primera 192.168.1.10 segunda 10.0.0.5",
            "192.168.1.10",
        ),
    ],
)
def test_extraer_ip(linea, esperado):
    # ACT
    resultado = extraer_ip(linea)

    # ASSERT
    assert resultado == esperado
