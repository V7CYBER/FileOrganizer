import os

import pytest

from core.magic_numbers import identificar_tipo_real
from core.seguridad import verificar_archivos
from core.verificador import verificar_archivo


@pytest.mark.skipif(
    os.name != "posix",
    reason="Prueba específica de permisos POSIX",
)
def test_magic_numbers_archivo_sin_permiso_lectura(tmp_path):
    # ARRANGE
    archivo = tmp_path / "protegido.jpg"

    archivo.write_bytes(
        b"\xFF\xD8\xFF\xE0\x00\x10\x4A\x46"
    )

    archivo.chmod(0o000)

    try:
        # ACT + ASSERT
        with pytest.raises(PermissionError):
            identificar_tipo_real(archivo)

    finally:
        archivo.chmod(0o600)


@pytest.mark.skipif(
    os.name != "posix",
    reason="Prueba específica de permisos POSIX",
)
def test_verificador_archivo_sin_permiso_lectura(tmp_path):
    # ARRANGE
    archivo = tmp_path / "protegido.jpg"

    archivo.write_bytes(
        b"\xFF\xD8\xFF\xE0\x00\x10\x4A\x46"
    )

    archivo.chmod(0o000)

    try:
        # ACT + ASSERT
        with pytest.raises(PermissionError):
            verificar_archivo(archivo)

    finally:
        archivo.chmod(0o600)


@pytest.mark.skipif(
    os.name != "posix",
    reason="Prueba específica de permisos POSIX",
)
def test_seguridad_directorio_sin_permiso(tmp_path):
    # ARRANGE
    carpeta = tmp_path / "protegida"
    carpeta.mkdir()

    archivo = carpeta / "foto.jpg"
    archivo.write_bytes(
        b"\xFF\xD8\xFF\xE0\x00\x10\x4A\x46"
    )

    carpeta.chmod(0o000)

    try:
        # ACT + ASSERT
        with pytest.raises(PermissionError):
            verificar_archivos(carpeta)

    finally:
        carpeta.chmod(0o700)
