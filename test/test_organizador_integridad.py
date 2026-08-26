import json

from ui.integridad import crear_baseline_integridad, verificar_integridad


def test_crear_baseline_integridad(tmp_path, monkeypatch):
    # ARRANGE
    carpeta = tmp_path / "vigilada"
    carpeta.mkdir()

    archivo = carpeta / "documento.txt"
    archivo.write_bytes(b"contenido")

    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(
        "builtins.input",
        lambda _: str(carpeta),
    )

    # ACT
    crear_baseline_integridad()

    # ASSERT
    baseline = tmp_path / "baselines" / "baseline.json"

    assert baseline.exists()
    contenido = json.loads(baseline.read_text(encoding="utf-8"))

    assert contenido["ruta_base"] == str(carpeta.resolve())
    assert "documento.txt" in contenido["archivos"]


def test_verificar_integridad_detecta_modificado(
    tmp_path,
    monkeypatch,
    capsys,
):
    # ARRANGE
    carpeta = tmp_path / "vigilada"
    carpeta.mkdir()

    archivo = carpeta / "documento.txt"
    archivo.write_bytes(b"contenido original")

    monkeypatch.chdir(tmp_path)

    respuestas = iter(
        [
            str(carpeta),
            str(tmp_path / "baselines" / "baseline.json"),
        ]
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(respuestas),
    )

    crear_baseline_integridad()

    archivo.write_bytes(b"contenido modificado")

    # ACT
    verificar_integridad()

    # ASSERT
    salida = capsys.readouterr().out

    assert "Modificados : 1" in salida
    assert "Nuevos      : 0" in salida
    assert "Eliminados  : 0" in salida


def test_crear_baseline_integridad_maneja_ruta_invalida(
    monkeypatch,
    capsys,
):
    # ARRANGE
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "/ruta/inexistente",
    )

    # ACT
    crear_baseline_integridad()

    # ASSERT
    salida = capsys.readouterr().out

    assert "✗" in salida


def test_verificar_integridad_maneja_baseline_invalida(
    monkeypatch,
    capsys,
):
    # ARRANGE
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "/baseline/inexistente.json",
    )

    # ACT
    verificar_integridad()

    # ASSERT
    salida = capsys.readouterr().out

    assert "✗" in salida
