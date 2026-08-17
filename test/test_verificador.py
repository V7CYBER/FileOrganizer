from core.verificador import verificar_archivo


def test_archivo_jpeg_correcto(tmp_path):
    # ARRANGE
    archivo = tmp_path / "foto.jpg"
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


def test_archivo_jpg_disfrazado_de_ejecutable(tmp_path):
    # ARRANGE
    archivo = tmp_path / "programa.jpg"
    archivo.write_bytes(
        b"MZ\x90\x00\x03\x00\x00\x00"
    )

    # ACT
    resultado = verificar_archivo(archivo)

    # ASSERT
    assert resultado["archivo"] == archivo
    assert resultado["extension"] == ".jpg"
    assert resultado["tipo_real"] == "PE/Windows executable"
    assert resultado["estado"] == "SOSPECHOSO"


def test_extension_no_verificada(tmp_path):
    # ARRANGE
    archivo = tmp_path / "archivo.xyz"
    archivo.write_bytes(
        b"contenido sin firma conocida"
    )

    # ACT
    resultado = verificar_archivo(archivo)

    # ASSERT
    assert resultado["archivo"] == archivo
    assert resultado["extension"] == ".xyz"
    assert resultado["tipo_real"] == "Desconocido"
    assert resultado["estado"] == "NO_VERIFICADO"
