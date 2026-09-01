from core.reglas_logs import (
    REGLAS_DETECCION,
    evaluar_linea_con_reglas,
    evaluar_regla,
)


def test_reglas_deteccion_tienen_estructura_valida():
    # ARRANGE
    campos_obligatorios = {
        "id",
        "tipo",
        "severidad",
        "descripcion",
        "patrones",
    }

    # ACT + ASSERT
    assert REGLAS_DETECCION

    for regla in REGLAS_DETECCION:
        assert campos_obligatorios <= regla.keys()

        assert isinstance(regla["id"], str)
        assert regla["id"].strip()

        assert isinstance(regla["tipo"], str)
        assert regla["tipo"].strip()

        assert isinstance(regla["severidad"], str)
        assert regla["severidad"].strip()

        assert isinstance(regla["descripcion"], str)
        assert regla["descripcion"].strip()

        assert isinstance(regla["patrones"], list)
        assert regla["patrones"]


def test_reglas_deteccion_incluyen_reglas_base():
    # ARRANGE
    reglas_por_id = {regla["id"]: regla for regla in REGLAS_DETECCION}

    # ACT
    sql_injection = reglas_por_id["WEB_SQL_001"]
    fuerza_bruta = reglas_por_id["AUTH_FAIL_001"]

    # ASSERT
    assert sql_injection["tipo"] == "SQL_INJECTION"
    assert sql_injection["severidad"] == "ALTA"

    assert fuerza_bruta["tipo"] == "FUERZA_BRUTA"
    assert fuerza_bruta["severidad"] == "MEDIA"

    assert len(sql_injection["patrones"]) == 8
    assert len(fuerza_bruta["patrones"]) == 6


def test_evaluar_regla_detecta_coincidencia():
    # ARRANGE
    regla = REGLAS_DETECCION[0]

    linea = "192.168.1.30 " "UNION SELECT username FROM users"

    # ACT
    resultado = evaluar_regla(
        regla,
        linea,
    )

    # ASSERT
    assert resultado is True


def test_evaluar_regla_sin_coincidencia():
    # ARRANGE
    regla = REGLAS_DETECCION[0]

    linea = "192.168.1.10 " "GET /index.html HTTP/1.1 200"

    # ACT
    resultado = evaluar_regla(
        regla,
        linea,
    )

    # ASSERT
    assert resultado is False


def test_evaluar_linea_con_reglas_devuelve_coincidencias():
    # ARRANGE
    linea = "192.168.1.30 " "UNION SELECT username FROM users"

    # ACT
    coincidencias = evaluar_linea_con_reglas(
        linea,
        REGLAS_DETECCION,
    )

    # ASSERT
    assert len(coincidencias) == 1

    regla = coincidencias[0]

    assert regla["id"] == "WEB_SQL_001"
    assert regla["tipo"] == "SQL_INJECTION"
    assert regla["severidad"] == "ALTA"


def test_evaluar_linea_con_reglas_sin_coincidencias():
    # ARRANGE
    linea = "192.168.1.10 " "GET /index.html HTTP/1.1 200"

    # ACT
    coincidencias = evaluar_linea_con_reglas(
        linea,
        REGLAS_DETECCION,
    )

    # ASSERT
    assert coincidencias == []


def test_evaluar_linea_con_reglas_varias_coincidencias():
    # ARRANGE
    linea = "192.168.1.30 " "Failed password " "UNION SELECT username FROM users"

    # ACT
    coincidencias = evaluar_linea_con_reglas(
        linea,
        REGLAS_DETECCION,
    )

    # ASSERT
    ids = {regla["id"] for regla in coincidencias}

    assert ids == {
        "WEB_SQL_001",
        "AUTH_FAIL_001",
    }


def test_reglas_deteccion_incluyen_path_traversal():
    # ARRANGE
    reglas_por_id = {regla["id"]: regla for regla in REGLAS_DETECCION}

    # ACT
    regla = reglas_por_id["WEB_PATH_001"]

    # ASSERT
    assert regla["tipo"] == "PATH_TRAVERSAL"
    assert regla["severidad"] == "ALTA"
    assert regla["descripcion"] == "Posible intento de Path Traversal"
    assert regla["patrones"]


def test_reglas_deteccion_incluyen_command_injection():
    # ARRANGE
    reglas_por_id = {regla["id"]: regla for regla in REGLAS_DETECCION}

    # ACT
    regla = reglas_por_id["WEB_CMD_001"]

    # ASSERT
    assert regla["tipo"] == "COMMAND_INJECTION"
    assert regla["severidad"] == "ALTA"
    assert regla["descripcion"] == "Posible intento de Command Injection"
    assert regla["patrones"]
