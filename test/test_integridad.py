import pytest

from core.hash import calcular_sha256
from core.integridad import generar_snapshot


def test_generar_snapshot_un_archivo(tmp_path):
    # ARRANGE
    archivo = tmp_path / "factura.pdf"
    archivo.write_bytes(b"contenido de prueba")

    # ACT
    snapshot = generar_snapshot(tmp_path)

    # ASSERT
    assert snapshot["ruta_base"] == str(tmp_path)

    assert snapshot["archivos"]["factura.pdf"] == calcular_sha256(archivo)


def test_generar_snapshot_subdirectorio(tmp_path):
    # ARRANGE
    carpeta = tmp_path / "Trabajo"
    carpeta.mkdir()

    archivo = carpeta / "informe.txt"
    archivo.write_bytes(b"informe interno")

    # ACT
    snapshot = generar_snapshot(tmp_path)

    # ASSERT
    assert snapshot["archivos"]["Trabajo/informe.txt"] == calcular_sha256(archivo)


def test_generar_snapshot_carpeta_vacia(tmp_path):
    # ACT
    snapshot = generar_snapshot(tmp_path)

    # ASSERT
    assert snapshot["ruta_base"] == str(tmp_path)
    assert snapshot["archivos"] == {}


def test_generar_snapshot_ruta_inexistente(tmp_path):
    # ARRANGE
    ruta_inexistente = tmp_path / "no_existe"

    # ACT / ASSERT
    with pytest.raises(FileNotFoundError):
        generar_snapshot(ruta_inexistente)


def test_generar_snapshot_ruta_es_archivo(tmp_path):
    # ARRANGE
    archivo = tmp_path / "factura.pdf"
    archivo.write_bytes(b"contenido")

    # ACT / ASSERT
    with pytest.raises(NotADirectoryError):
        generar_snapshot(archivo)
