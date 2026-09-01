import core.analizador_logs


def test_analizar_linea_utiliza_motor_de_reglas(
    monkeypatch,
):
    # ARRANGE
    regla = {
        "id": "TEST_001",
        "tipo": "EVENTO_PRUEBA",
        "severidad": "ALTA",
        "descripcion": "Regla utilizada para probar la integración.",
        "patrones": [],
    }

    monkeypatch.setattr(
        core.analizador_logs,
        "evaluar_linea_con_reglas",
        lambda _linea, _reglas: [regla],
    )

    # ACT
    eventos = core.analizador_logs.analizar_linea(
        "192.168.1.50 contenido de prueba",
        10,
    )

    # ASSERT
    assert len(eventos) == 1

    evento = eventos[0]

    assert evento["linea"] == 10
    assert evento["ip"] == "192.168.1.50"
    assert evento["tipo"] == "EVENTO_PRUEBA"
    assert evento["severidad"] == "ALTA"


def test_analizar_linea_incluye_metadatos_de_regla(
    monkeypatch,
):
    # ARRANGE
    regla = {
        "id": "TEST_002",
        "tipo": "EVENTO_PRUEBA",
        "severidad": "MEDIA",
        "descripcion": "Detección de prueba.",
        "patrones": [],
    }

    monkeypatch.setattr(
        core.analizador_logs,
        "evaluar_linea_con_reglas",
        lambda _linea, _reglas: [regla],
    )

    # ACT
    eventos = core.analizador_logs.analizar_linea(
        "10.0.0.25 contenido",
        7,
    )

    # ASSERT
    evento = eventos[0]

    assert evento["regla"] == "TEST_002"
    assert evento["descripcion"] == "Detección de prueba."


def test_analizar_linea_real_incluye_metadatos_regla():
    # ARRANGE
    linea = "192.168.1.30 " "UNION SELECT username FROM users"

    # ACT
    eventos = core.analizador_logs.analizar_linea(
        linea,
        12,
    )

    # ASSERT
    assert len(eventos) == 1

    evento = eventos[0]

    assert evento["regla"] == "WEB_SQL_001"
    assert evento["descripcion"] == "Posible intento de SQL Injection"


def test_analizar_linea_detecta_path_traversal_real():
    # ARRANGE
    linea = "192.168.1.50 " "GET /../../etc/passwd HTTP/1.1"

    # ACT
    eventos = core.analizador_logs.analizar_linea(
        linea,
        20,
    )

    # ASSERT
    assert len(eventos) == 1

    evento = eventos[0]

    assert evento["regla"] == "WEB_PATH_001"
    assert evento["tipo"] == "PATH_TRAVERSAL"
    assert evento["severidad"] == "ALTA"
    assert evento["descripcion"] == "Posible intento de Path Traversal"


def test_analizar_linea_detecta_path_traversal_codificado():
    # ARRANGE
    linea = "192.168.1.50 " "GET /%2e%2e%2f%2e%2e%2fetc/passwd HTTP/1.1"

    # ACT
    eventos = core.analizador_logs.analizar_linea(
        linea,
        21,
    )

    # ASSERT
    assert len(eventos) == 1

    evento = eventos[0]

    assert evento["regla"] == "WEB_PATH_001"
    assert evento["tipo"] == "PATH_TRAVERSAL"


def test_analizar_linea_detecta_variantes_path_traversal():
    # ARRANGE
    variantes = [
        "/%2e%2e/etc/passwd",
        "/..%2fetc/passwd",
    ]

    # ACT
    resultados = [
        core.analizador_logs.analizar_linea(
            f"192.168.1.50 GET {ruta} HTTP/1.1",
            numero_linea,
        )
        for numero_linea, ruta in enumerate(
            variantes,
            start=30,
        )
    ]

    # ASSERT
    for eventos in resultados:
        assert len(eventos) == 1
        assert eventos[0]["regla"] == "WEB_PATH_001"
        assert eventos[0]["tipo"] == "PATH_TRAVERSAL"
        assert eventos[0]["severidad"] == "ALTA"


def test_analizar_linea_detecta_command_injection_real():
    # ARRANGE
    linea = "192.168.1.60 " "GET /?cmd=;whoami HTTP/1.1"

    # ACT
    eventos = core.analizador_logs.analizar_linea(
        linea,
        40,
    )

    # ASSERT
    assert len(eventos) == 1

    evento = eventos[0]

    assert evento["linea"] == 40
    assert evento["ip"] == "192.168.1.60"
    assert evento["regla"] == "WEB_CMD_001"
    assert evento["tipo"] == "COMMAND_INJECTION"
    assert evento["severidad"] == "ALTA"
    assert evento["descripcion"] == "Posible intento de Command Injection"


def test_analizar_linea_detecta_command_injection_and_id():
    # ARRANGE
    linea = "192.168.1.60 " "GET /?cmd=&&id HTTP/1.1"

    # ACT
    eventos = core.analizador_logs.analizar_linea(
        linea,
        41,
    )

    # ASSERT
    assert len(eventos) == 1

    evento = eventos[0]

    assert evento["regla"] == "WEB_CMD_001"
    assert evento["tipo"] == "COMMAND_INJECTION"
    assert evento["severidad"] == "ALTA"
