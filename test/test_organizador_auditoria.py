from organizador import mostrar_auditoria_seguridad


def test_mostrar_auditoria_seguridad_muestra_resultado(
    monkeypatch,
    capsys,
):
    # ARRANGE
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "/tmp/baseline.json",
    )

    monkeypatch.setattr(
        "organizador.ejecutar_auditoria",
        lambda carpeta, baseline: {
            "resumen": {
                "seguridad": {
                    "ok": 5,
                    "sospechosos": 1,
                    "no_verificados": 0,
                },
                "integridad": {
                    "sin_cambios": 4,
                    "modificados": 1,
                    "nuevos": 0,
                    "eliminados": 0,
                },
            },
            "nivel": "ALERTA",
            "informe": "INFORME DE PRUEBA",
        },
    )

    # ACT
    mostrar_auditoria_seguridad("/tmp/vigilada")

    # ASSERT
    salida = capsys.readouterr().out

    assert "INFORME DE PRUEBA" in salida


def test_mostrar_auditoria_seguridad_maneja_error(
    monkeypatch,
    capsys,
):
    # ARRANGE
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "/tmp/baseline.json",
    )

    def auditoria_simulada(_carpeta, _baseline):
        raise FileNotFoundError("Baseline no encontrada")

    monkeypatch.setattr(
        "organizador.ejecutar_auditoria",
        auditoria_simulada,
    )

    # ACT
    mostrar_auditoria_seguridad("/tmp/vigilada")

    # ASSERT
    salida = capsys.readouterr().out

    assert "Baseline no encontrada" in salida


def test_mostrar_auditoria_seguridad_guarda_informe(
    tmp_path,
    monkeypatch,
):
    # ARRANGE
    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "/tmp/baseline.json",
    )

    monkeypatch.setattr(
        "organizador.ejecutar_auditoria",
        lambda carpeta, baseline: {
            "resumen": {
                "seguridad": {
                    "ok": 5,
                    "sospechosos": 0,
                    "no_verificados": 0,
                },
                "integridad": {
                    "sin_cambios": 5,
                    "modificados": 0,
                    "nuevos": 0,
                    "eliminados": 0,
                },
            },
            "nivel": "OK",
            "informe": "INFORME GUARDADO",
        },
    )

    # ACT
    mostrar_auditoria_seguridad("/tmp/vigilada")

    # ASSERT
    informe = tmp_path / "reports" / "auditoria.txt"

    assert informe.exists()
    assert informe.read_text(encoding="utf-8") == "INFORME GUARDADO"


def test_main_incluye_opcion_auditoria(monkeypatch, capsys):
    # ARRANGE
    respuestas = iter(
        [
            "12",
        ]
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(respuestas),
    )

    # ACT
    from organizador import main

    main()

    # ASSERT
    salida = capsys.readouterr().out

    assert "11) Ejecutar auditoría de seguridad" in salida
    assert "12) Salir" in salida


def test_main_ejecuta_auditoria(monkeypatch):
    # ARRANGE
    respuestas = iter(
        [
            "11",
            "/tmp/vigilada",
            "12",
        ]
    )

    carpeta_recibida = {}

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(respuestas),
    )

    def auditoria_simulada(carpeta):
        carpeta_recibida["ruta"] = carpeta

    monkeypatch.setattr(
        "organizador.mostrar_auditoria_seguridad",
        auditoria_simulada,
    )

    from organizador import main

    # ACT
    main()

    # ASSERT
    assert carpeta_recibida["ruta"] == "/tmp/vigilada"
