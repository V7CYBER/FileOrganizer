import pytest

from core.seguridad import (
    generar_resumen_seguridad,
    obtener_archivos_ok,
    obtener_no_verificados,
    obtener_sospechosos,
    verificar_archivos,
)


def crear_archivos_prueba(carpeta):
    """
    Crea tres archivos con estados diferentes:
    OK, SOSPECHOSO y NO_VERIFICADO.
    """

    (carpeta / "foto.jpg").write_bytes(
        b"\xFF\xD8\xFF\xE0\x00\x10\x4A\x46"
    )

    (carpeta / "programa.jpg").write_bytes(
        b"MZ\x90\x00\x03\x00\x00\x00"
    )

    (carpeta / "archivo.xyz").write_bytes(
        b"contenido sin firma conocida"
    )


def test_verificar_archivos(tmp_path):
    # ARRANGE
    crear_archivos_prueba(tmp_path)

    # ACT
    resultados = verificar_archivos(tmp_path)

    # ASSERT
    assert len(resultados) == 3

    estados = {
        resultado["archivo"].name: resultado["estado"]
        for resultado in resultados
    }

    assert estados["foto.jpg"] == "OK"
    assert estados["programa.jpg"] == "SOSPECHOSO"
    assert estados["archivo.xyz"] == "NO_VERIFICADO"


def test_verificar_archivos_ignora_subdirectorios(tmp_path):
    # ARRANGE
    crear_archivos_prueba(tmp_path)

    subdirectorio = tmp_path / "subcarpeta"
    subdirectorio.mkdir()

    (subdirectorio / "oculto.jpg").write_bytes(
        b"MZ\x90\x00\x03\x00\x00\x00"
    )

    # ACT
    resultados = verificar_archivos(tmp_path)

    # ASSERT
    assert len(resultados) == 3

    nombres = {
        resultado["archivo"].name
        for resultado in resultados
    }

    assert "oculto.jpg" not in nombres


def test_verificar_archivos_ruta_inexistente(tmp_path):
    # ARRANGE
    carpeta = tmp_path / "no_existe"

    # ACT + ASSERT
    with pytest.raises(FileNotFoundError):
        verificar_archivos(carpeta)


def test_verificar_archivos_ruta_no_directorio(tmp_path):
    # ARRANGE
    archivo = tmp_path / "archivo.txt"
    archivo.write_text(
        "contenido",
        encoding="utf-8",
    )

    # ACT + ASSERT
    with pytest.raises(NotADirectoryError):
        verificar_archivos(archivo)


def test_filtrar_resultados_por_estado(tmp_path):
    # ARRANGE
    crear_archivos_prueba(tmp_path)
    resultados = verificar_archivos(tmp_path)

    # ACT
    archivos_ok = obtener_archivos_ok(resultados)
    sospechosos = obtener_sospechosos(resultados)
    no_verificados = obtener_no_verificados(resultados)

    # ASSERT
    assert len(archivos_ok) == 1
    assert len(sospechosos) == 1
    assert len(no_verificados) == 1

    assert archivos_ok[0]["archivo"].name == "foto.jpg"
    assert sospechosos[0]["archivo"].name == "programa.jpg"
    assert no_verificados[0]["archivo"].name == "archivo.xyz"


def test_generar_resumen_seguridad(tmp_path):
    # ARRANGE
    crear_archivos_prueba(tmp_path)
    resultados = verificar_archivos(tmp_path)

    # ACT
    resumen = generar_resumen_seguridad(resultados)

    # ASSERT
    assert resumen == {
        "verificados": 3,
        "ok": 1,
        "sospechosos": 1,
        "no_verificados": 1,
    }
