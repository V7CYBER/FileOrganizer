from pathlib import Path

import ui.organizacion


def test_seleccionar_carpeta_ruta_invalida(
    monkeypatch,
    capsys,
):
    # ARRANGE
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "/tmp/inexistente",
    )

    monkeypatch.setattr(
        Path,
        "exists",
        lambda _: False,
    )

    # ACT
    ui.organizacion.seleccionar_carpeta()

    # ASSERT
    salida = capsys.readouterr().out

    assert "ERROR" in salida.upper() or "no existe" in salida.lower()


def test_seleccionar_carpeta_cancelada(
    tmp_path,
    monkeypatch,
    capsys,
):
    # ARRANGE
    carpeta = tmp_path / "prueba"
    carpeta.mkdir()

    respuestas = iter(
        [
            str(carpeta),
            "N",
        ]
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(respuestas),
    )

    monkeypatch.setattr(
        ui.organizacion,
        "analizar_carpeta",
        lambda _: {
            "ruta": carpeta,
            "archivos": 1,
            "carpetas": 0,
            "extensiones": {
                ".txt": 1,
            },
        },
    )

    monkeypatch.setattr(
        ui.organizacion,
        "verificar_archivos",
        lambda _: [],
    )

    monkeypatch.setattr(
        ui.organizacion,
        "obtener_sospechosos",
        lambda _: [],
    )

    monkeypatch.setattr(
        ui.organizacion,
        "clasificar_archivos",
        lambda _: [
            ("documento.txt", "Documentos"),
        ],
    )

    # ACT
    ui.organizacion.seleccionar_carpeta()

    # ASSERT
    salida = capsys.readouterr().out

    assert "Operación cancelada por el usuario." in salida


def test_seleccionar_carpeta_modo_simulacion(
    tmp_path,
    monkeypatch,
    capsys,
):
    # ARRANGE
    carpeta = tmp_path / "prueba"
    carpeta.mkdir()

    respuestas = iter(
        [
            str(carpeta),
            "S",
        ]
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(respuestas),
    )

    monkeypatch.setattr(
        ui.organizacion,
        "analizar_carpeta",
        lambda _: {
            "ruta": carpeta,
            "archivos": 2,
            "carpetas": 0,
            "extensiones": {
                ".jpg": 1,
                ".pdf": 1,
            },
        },
    )

    monkeypatch.setattr(
        ui.organizacion,
        "verificar_archivos",
        lambda _: [],
    )

    monkeypatch.setattr(
        ui.organizacion,
        "obtener_sospechosos",
        lambda _: [],
    )

    monkeypatch.setattr(
        ui.organizacion,
        "clasificar_archivos",
        lambda _: [
            ("foto.jpg", "Fotos"),
            ("documento.pdf", "Documentos"),
        ],
    )

    llamadas_mover = []

    monkeypatch.setattr(
        ui.organizacion,
        "mover_archivos",
        lambda *_args, **_kwargs: llamadas_mover.append(True),
    )

    # ACT
    ui.organizacion.seleccionar_carpeta(simulacion=True)

    # ASSERT
    salida = capsys.readouterr().out

    assert "RESUMEN SIMULACIÓN" in salida
    assert "Archivos analizados..... 2" in salida
    assert "Fotos" in salida
    assert "Documentos" in salida
    assert "No se ha movido ningún archivo." in salida

    assert llamadas_mover == []


def test_seleccionar_carpeta_organizacion_real(
    tmp_path,
    monkeypatch,
    capsys,
):
    # ARRANGE
    carpeta = tmp_path / "prueba"
    carpeta.mkdir()

    respuestas = iter(
        [
            str(carpeta),
            "S",
        ]
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(respuestas),
    )

    monkeypatch.setattr(
        ui.organizacion,
        "analizar_carpeta",
        lambda _: {
            "ruta": carpeta,
            "archivos": 1,
            "carpetas": 0,
            "extensiones": {
                ".txt": 1,
            },
        },
    )

    monkeypatch.setattr(
        ui.organizacion,
        "verificar_archivos",
        lambda _: [],
    )

    monkeypatch.setattr(
        ui.organizacion,
        "obtener_sospechosos",
        lambda _: [],
    )

    monkeypatch.setattr(
        ui.organizacion,
        "clasificar_archivos",
        lambda _: [
            ("documento.txt", "Documentos"),
        ],
    )

    monkeypatch.setattr(
        ui.organizacion,
        "mover_archivos",
        lambda _clasificacion, _carpeta: {
            "analizados": 1,
            "movidos": 1,
            "omitidos": 0,
            "categorias": {
                "Documentos": 1,
            },
        },
    )

    estadisticas_guardadas = {}

    def guardar_estadisticas_simulado(ruta, estadisticas):
        estadisticas_guardadas["ruta"] = ruta
        estadisticas_guardadas["estadisticas"] = estadisticas

    monkeypatch.setattr(
        ui.organizacion,
        "guardar_estadisticas",
        guardar_estadisticas_simulado,
    )

    # ACT
    ui.organizacion.seleccionar_carpeta()

    # ASSERT
    salida = capsys.readouterr().out

    assert "RESUMEN FINAL" in salida
    assert "Archivos analizados..... 1" in salida
    assert "Archivos movidos........ 1" in salida
    assert "Archivos omitidos....... 0" in salida
    assert "Proceso finalizado correctamente." in salida

    assert estadisticas_guardadas["ruta"] == carpeta
    assert estadisticas_guardadas["estadisticas"]["movidos"] == 1
