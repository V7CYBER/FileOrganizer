import pytest

from core.magic_numbers import identificar_tipo_real


def test_firma_valida_con_contenido_posterior(tmp_path):
    # ARRANGE
    archivo = tmp_path / "documento.pdf"
    archivo.write_bytes(
        b"%PDF-1.7 contenido posterior arbitrario"
    )

    # ACT
    resultado = identificar_tipo_real(archivo)

    # ASSERT
    assert resultado == "PDF"


def test_firma_incompleta(tmp_path):
    # ARRANGE
    archivo = tmp_path / "incompleto.bin"
    archivo.write_bytes(b"\xFF\xD8")

    # ACT
    resultado = identificar_tipo_real(archivo)

    # ASSERT
    assert resultado == "Desconocido"


def test_archivo_de_un_solo_byte(tmp_path):
    # ARRANGE
    archivo = tmp_path / "minimo.bin"
    archivo.write_bytes(b"M")

    # ACT
    resultado = identificar_tipo_real(archivo)

    # ASSERT
    assert resultado == "Desconocido"


def test_nombre_unicode_y_espacios(tmp_path):
    # ARRANGE
    archivo = tmp_path / "mi fíchéró 日本.png"
    archivo.write_bytes(
        b"\x89PNG\r\n\x1a\n"
    )

    # ACT
    resultado = identificar_tipo_real(archivo)

    # ASSERT
    assert resultado == "PNG"


def test_directorio_en_lugar_de_archivo(tmp_path):
    # ARRANGE
    directorio = tmp_path / "carpeta"
    directorio.mkdir()

    # ACT + ASSERT
    with pytest.raises(IsADirectoryError):
        identificar_tipo_real(directorio)
