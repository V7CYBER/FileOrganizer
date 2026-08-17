import pytest

from core.magic_numbers import identificar_tipo_real
from core.verificador import verificar_archivo


def test_magic_numbers_sigue_symlink(tmp_path):
    # ARRANGE
    original = tmp_path / "original.jpg"
    original.write_bytes(
        b"\xFF\xD8\xFF\xE0\x00\x10\x4A\x46"
    )

    enlace = tmp_path / "enlace.jpg"
    enlace.symlink_to(original)

    # ACT
    resultado = identificar_tipo_real(enlace)

    # ASSERT
    assert resultado == "JPEG"


def test_verificador_sigue_symlink(tmp_path):
    # ARRANGE
    original = tmp_path / "original.jpg"
    original.write_bytes(
        b"\xFF\xD8\xFF\xE0\x00\x10\x4A\x46"
    )

    enlace = tmp_path / "enlace.jpg"
    enlace.symlink_to(original)

    # ACT
    resultado = verificar_archivo(enlace)

    # ASSERT
    assert resultado["archivo"] == enlace
    assert resultado["extension"] == ".jpg"
    assert resultado["tipo_real"] == "JPEG"
    assert resultado["estado"] == "OK"


def test_magic_numbers_archivo_eliminado(tmp_path):
    # ARRANGE
    archivo = tmp_path / "temporal.jpg"

    archivo.write_bytes(
        b"\xFF\xD8\xFF\xE0\x00\x10\x4A\x46"
    )

    archivo.unlink()

    # ACT + ASSERT
    with pytest.raises(FileNotFoundError):
        identificar_tipo_real(archivo)


def test_verificador_archivo_eliminado(tmp_path):
    # ARRANGE
    archivo = tmp_path / "temporal.jpg"

    archivo.write_bytes(
        b"\xFF\xD8\xFF\xE0\x00\x10\x4A\x46"
    )

    archivo.unlink()

    # ACT + ASSERT
    with pytest.raises(FileNotFoundError):
        verificar_archivo(archivo)


def test_symlink_roto(tmp_path):
    # ARRANGE
    destino_inexistente = tmp_path / "no_existe.jpg"

    enlace = tmp_path / "enlace_roto.jpg"
    enlace.symlink_to(destino_inexistente)

    # ACT + ASSERT
    with pytest.raises(FileNotFoundError):
        identificar_tipo_real(enlace)
