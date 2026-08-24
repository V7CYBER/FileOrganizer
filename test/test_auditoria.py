from core.auditoria import determinar_nivel_auditoria, generar_resumen_auditoria


def test_generar_resumen_auditoria():
    # ARRANGE
    seguridad = {
        "ok": 8,
        "sospechosos": 2,
        "no_verificados": 1,
    }

    integridad = {
        "sin_cambios": ["documento.txt"],
        "modificados": ["config.json"],
        "nuevos": ["extraño.exe"],
        "eliminados": [],
    }

    # ACT
    resultado = generar_resumen_auditoria(
        seguridad,
        integridad,
    )

    # ASSERT
    assert resultado == {
        "seguridad": {
            "ok": 8,
            "sospechosos": 2,
            "no_verificados": 1,
        },
        "integridad": {
            "sin_cambios": 1,
            "modificados": 1,
            "nuevos": 1,
            "eliminados": 0,
        },
    }


def test_determinar_nivel_auditoria_ok():
    # ARRANGE
    resumen = {
        "seguridad": {
            "ok": 8,
            "sospechosos": 0,
            "no_verificados": 0,
        },
        "integridad": {
            "sin_cambios": 8,
            "modificados": 0,
            "nuevos": 0,
            "eliminados": 0,
        },
    }

    # ACT
    nivel = determinar_nivel_auditoria(resumen)

    # ASSERT
    assert nivel == "OK"


def test_determinar_nivel_auditoria_advertencia():
    # ARRANGE
    resumen = {
        "seguridad": {
            "ok": 8,
            "sospechosos": 0,
            "no_verificados": 0,
        },
        "integridad": {
            "sin_cambios": 7,
            "modificados": 1,
            "nuevos": 0,
            "eliminados": 0,
        },
    }

    # ACT
    nivel = determinar_nivel_auditoria(resumen)

    # ASSERT
    assert nivel == "ADVERTENCIA"


def test_determinar_nivel_auditoria_alerta():
    # ARRANGE
    resumen = {
        "seguridad": {
            "ok": 7,
            "sospechosos": 1,
            "no_verificados": 0,
        },
        "integridad": {
            "sin_cambios": 8,
            "modificados": 0,
            "nuevos": 0,
            "eliminados": 0,
        },
    }

    # ACT
    nivel = determinar_nivel_auditoria(resumen)

    # ASSERT
    assert nivel == "ALERTA"


def test_determinar_nivel_auditoria_alerta_tiene_prioridad():
    # ARRANGE
    resumen = {
        "seguridad": {
            "ok": 5,
            "sospechosos": 1,
            "no_verificados": 0,
        },
        "integridad": {
            "sin_cambios": 5,
            "modificados": 1,
            "nuevos": 1,
            "eliminados": 1,
        },
    }

    # ACT
    nivel = determinar_nivel_auditoria(resumen)

    # ASSERT
    assert nivel == "ALERTA"


def test_determinar_nivel_auditoria_no_verificados():
    # ARRANGE
    resumen = {
        "seguridad": {
            "ok": 7,
            "sospechosos": 0,
            "no_verificados": 1,
        },
        "integridad": {
            "sin_cambios": 8,
            "modificados": 0,
            "nuevos": 0,
            "eliminados": 0,
        },
    }

    # ACT
    nivel = determinar_nivel_auditoria(resumen)

    # ASSERT
    assert nivel == "ADVERTENCIA"
