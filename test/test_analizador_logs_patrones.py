import pytest

from core.analizador_logs import analizar_linea


@pytest.mark.parametrize(
    "contenido",
    [
        "UNION SELECT username,password FROM users",
        "OR 1=1",
        "AND 1=1",
        "OR 'a' = 'a'",
        "SLEEP(5)",
        "BENCHMARK(1000, MD5('test'))",
        "DROP TABLE users",
        "information_schema",
    ],
)
def test_detectar_sql_injection(contenido):
    # ARRANGE
    linea = f"192.168.1.30 {contenido}"

    # ACT
    eventos = analizar_linea(linea, 10)

    # ASSERT
    assert len(eventos) == 1

    evento = eventos[0]

    assert evento["linea"] == 10
    assert evento["ip"] == "192.168.1.30"
    assert evento["tipo"] == "SQL_INJECTION"
    assert evento["severidad"] == "ALTA"


@pytest.mark.parametrize(
    "contenido",
    [
        "Failed password",
        "Failed login",
        "Authentication failure",
        "Invalid user",
        "Maximum authentication attempts",
        "Too many authentication failures",
    ],
)
def test_detectar_fallos_autenticacion(contenido):
    # ARRANGE
    linea = f"192.168.1.20 {contenido}"

    # ACT
    eventos = analizar_linea(linea, 5)

    # ASSERT
    assert len(eventos) == 1

    evento = eventos[0]

    assert evento["linea"] == 5
    assert evento["ip"] == "192.168.1.20"
    assert evento["tipo"] == "FUERZA_BRUTA"
    assert evento["severidad"] == "MEDIA"


def test_linea_legitima_no_genera_eventos():
    # ARRANGE
    linea = (
        '192.168.1.10 - - '
        '"GET /index.html HTTP/1.1" 200'
    )

    # ACT
    eventos = analizar_linea(linea, 1)

    # ASSERT
    assert eventos == []
