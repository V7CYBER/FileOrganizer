from pathlib import Path

import pytest

import core.cuarentena as cuarentena


def preparar_cuarentena_temporal(tmp_path, monkeypatch):
    carpeta_cuarentena = tmp_path / "quarantine"

    monkeypatch.setattr(
        cuarentena,
        "CUARENTENA",
        carpeta_cuarentena,
    )

    monkeypatch.setattr(
        cuarentena,
        "REGISTRO_CUARENTENA",
        carpeta_cuarentena / "alertas.log",
    )

    return carpeta_cuarentena


def test_poner_en_cuarentena_mueve_y_registra(
    tmp_path,
    monkeypatch,
):
    # ARRANGE
    carpeta_cuarentena = preparar_cuarentena_temporal(
        tmp_path,
        monkeypatch,
    )

    origen = tmp_path / "programa.jpg"
    origen.write_bytes(
        b"MZ\x90\x00\x03\x00\x00\x00"
    )

    # ACT
    destino = cuarentena.poner_en_cuarentena(
        origen,
        "PE/Windows executable",
        ".jpg",
    )

    # ASSERT
    assert not origen.exists()
    assert destino.exists()
    assert destino == carpeta_cuarentena / "programa.jpg"

    registro = carpeta_cuarentena / "alertas.log"

    assert registro.exists()

    contenido = registro.read_text(
        encoding="utf-8"
    )

    assert "programa.jpg" in contenido
    assert "Extensión: .jpg" in contenido
    assert "Tipo real: PE/Windows executable" in contenido
    assert "Origen:" in contenido
    assert "Destino:" in contenido


def test_cuarentena_evitar_colision_nombre(
    tmp_path,
    monkeypatch,
):
    # ARRANGE
    carpeta_cuarentena = preparar_cuarentena_temporal(
        tmp_path,
        monkeypatch,
    )

    carpeta_cuarentena.mkdir()

    existente = carpeta_cuarentena / "programa.jpg"
    existente.write_bytes(b"archivo existente")

    origen = tmp_path / "programa.jpg"
    origen.write_bytes(
        b"MZ\x90\x00\x03\x00\x00\x00"
    )

    # ACT
    destino = cuarentena.poner_en_cuarentena(
        origen,
        "PE/Windows executable",
        ".jpg",
    )

    # ASSERT
    assert destino.name == "programa_1.jpg"
    assert destino.exists()
    assert existente.exists()


def test_cuarentena_archivo_inexistente(
    tmp_path,
    monkeypatch,
):
    # ARRANGE
    preparar_cuarentena_temporal(
        tmp_path,
        monkeypatch,
    )

    archivo = tmp_path / "no_existe.jpg"

    # ACT + ASSERT
    with pytest.raises(FileNotFoundError):
        cuarentena.poner_en_cuarentena(
            archivo,
            "PE/Windows executable",
            ".jpg",
        )


def test_generar_alerta():
    # ARRANGE
    archivo = Path("/tmp/programa.jpg")

    # ACT
    alerta = cuarentena.generar_alerta(
        archivo,
        "PE/Windows executable",
        ".jpg",
    )

    # ASSERT
    assert "programa.jpg" in alerta
    assert ".jpg" in alerta
    assert "PE/Windows executable" in alerta
    assert "SOSPECHOSO" in alerta
    assert "CUARENTENA" in alerta
