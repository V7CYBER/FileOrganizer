import pytest

from core.magic_numbers import identificar_tipo_real


@pytest.mark.parametrize(
    ("nombre", "contenido", "esperado"),
    [
        (
            "foto.jpg",
            b"\xFF\xD8\xFF\xE0\x00\x10\x4A\x46",
            "JPEG",
        ),
        (
            "imagen.png",
            b"\x89PNG\x0D\x0A\x1A\x0A",
            "PNG",
        ),
        (
            "animacion.gif",
            b"GIF89aXX",
            "GIF",
        ),
        (
            "documento.pdf",
            b"%PDF-1.7",
            "PDF",
        ),
        (
            "archivo.zip",
            b"PK\x03\x04\x14\x00\x00\x00",
            "ZIP",
        ),
        (
            "archivo.gz",
            b"\x1F\x8B\x08\x00\x00\x00\x00\x00",
            "GZIP",
        ),
        (
            "programa.elf",
            b"\x7FELF\x02\x01\x01\x00",
            "ELF",
        ),
        (
            "programa.exe",
            b"MZ\x90\x00\x03\x00\x00\x00",
            "PE/Windows executable",
        ),
        (
            "desconocido.xyz",
            b"contenido sin firma conocida",
            "Desconocido",
        ),
        (
            "vacio.bin",
            b"",
            "Desconocido",
        ),
    ],
)
def test_identificar_tipo_real(
    tmp_path,
    nombre,
    contenido,
    esperado,
):
    # ARRANGE
    archivo = tmp_path / nombre
    archivo.write_bytes(contenido)

    # ACT
    resultado = identificar_tipo_real(archivo)

    # ASSERT
    assert resultado == esperado


def test_archivo_inexistente(tmp_path):
    # ARRANGE
    archivo = tmp_path / "no_existe.bin"

    # ACT + ASSERT
    with pytest.raises(FileNotFoundError):
        identificar_tipo_real(archivo)
