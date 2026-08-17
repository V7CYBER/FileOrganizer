import pytest

from core.verificador import verificar_archivo


def test_archivo_sin_extension(tmp_path):
    # ARRANGE
    archivo = tmp_path / "archivo"
    archivo.write_bytes(b"contenido sin firma conocida")

    # ACT
    resultado = verificar_archivo(archivo)

    # ASSERT
    assert resultado["archivo"] == archivo
    assert resultado["extension"] == ""
    assert resultado["tipo_real"] == "Desconocido"
    assert resultado["estado"] == "NO_VERIFICADO"


def test_extension_mayusculas(tmp_path):
    # ARRANGE
    archivo = tmp_path / "FOTO.JPG"
    archivo.write_bytes(
        b"\xFF\xD8\xFF\xE0\x00\x10\x4A\x46"
    )

    # ACT
    resultado = verificar_archivo(archivo)

    # ASSERT
    assert resultado["extension"] == ".jpg"
    assert resultado["tipo_real"] == "JPEG"
    assert resultado["estado"] == "OK"


def test_nombre_unicode(tmp_path):
    # ARRANGE
    archivo = tmp_path / "fótó_ñ_日本.jpg"
    archivo.write_bytes(
        b"\xFF\xD8\xFF\xE0\x00\x10\x4A\x46"
    )

    # ACT
    resultado = verificar_archivo(archivo)

    # ASSERT
    assert resultado["archivo"] == archivo
    assert resultado["extension"] == ".jpg"
    assert resultado["tipo_real"] == "JPEG"
    assert resultado["estado"] == "OK"


def test_archivo_vacio_con_extension_conocida(tmp_path):
    # ARRANGE
    archivo = tmp_path / "vacio.jpg"
    archivo.write_bytes(b"")

    # ACT
    resultado = verificar_archivo(archivo)

    # ASSERT
    assert resultado["extension"] == ".jpg"
    assert resultado["tipo_real"] == "Desconocido"
    assert resultado["estado"] == "SOSPECHOSO"


def test_pdf_disfrazado_de_ejecutable(tmp_path):
    # ARRANGE
    archivo = tmp_path / "documento.pdf"
    archivo.write_bytes(
        b"MZ\x90\x00\x03\x00\x00\x00"
    )

    # ACT
    resultado = verificar_archivo(archivo)

    # ASSERT
    assert resultado["extension"] == ".pdf"
    assert resultado["tipo_real"] == "PE/Windows executable"
    assert resultado["estado"] == "SOSPECHOSO"


def test_archivo_con_varias_extensiones(tmp_path):
    # ARRANGE
    archivo = tmp_path / "foto.backup.JPG"
    archivo.write_bytes(
        b"\xFF\xD8\xFF\xE0\x00\x10\x4A\x46"
    )

    # ACT
    resultado = verificar_archivo(archivo)

    # ASSERT
    assert resultado["extension"] == ".jpg"
    assert resultado["tipo_real"] == "JPEG"
    assert resultado["estado"] == "OK"
