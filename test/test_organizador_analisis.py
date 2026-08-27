from pathlib import Path

from ui.organizacion import mostrar_analisis_carpeta


def test_mostrar_analisis_con_extensiones(capsys):
    # ARRANGE
    datos = {
        "ruta": Path("/tmp/prueba"),
        "archivos": 3,
        "carpetas": 1,
        "extensiones": {
            ".jpg": 2,
            ".pdf": 1,
        },
    }

    # ACT
    mostrar_analisis_carpeta(datos)

    # ASSERT
    salida = capsys.readouterr().out

    assert "Ruta............... /tmp/prueba" in salida
    assert "Archivos........... 3" in salida
    assert "Subcarpetas........ 1" in salida
    assert ".jpg" in salida
    assert "2" in salida
    assert ".pdf" in salida
    assert "1" in salida


def test_mostrar_analisis_sin_extensiones(capsys):
    # ARRANGE
    datos = {
        "ruta": Path("/tmp/vacia"),
        "archivos": 0,
        "carpetas": 0,
        "extensiones": {},
    }

    # ACT
    mostrar_analisis_carpeta(datos)

    # ASSERT
    salida = capsys.readouterr().out

    assert "Ruta............... /tmp/vacia" in salida
    assert "Archivos........... 0" in salida
    assert "Subcarpetas........ 0" in salida
    assert "No se encontraron archivos." in salida


def test_extensiones_se_muestran_ordenadas(capsys):
    # ARRANGE
    datos = {
        "ruta": Path("/tmp/orden"),
        "archivos": 3,
        "carpetas": 0,
        "extensiones": {
            ".zip": 1,
            ".jpg": 1,
            ".pdf": 1,
        },
    }

    # ACT
    mostrar_analisis_carpeta(datos)

    # ASSERT
    salida = capsys.readouterr().out

    posicion_jpg = salida.index(".jpg")
    posicion_pdf = salida.index(".pdf")
    posicion_zip = salida.index(".zip")

    assert posicion_jpg < posicion_pdf < posicion_zip
