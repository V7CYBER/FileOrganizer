from organizador import mostrar_clasificacion


def test_mostrar_clasificacion_con_archivos(capsys):
    # ARRANGE
    clasificacion = [
        ("foto.jpg", "Fotos"),
        ("documento.pdf", "Documentos"),
    ]

    # ACT
    resultado = mostrar_clasificacion(clasificacion)

    # ASSERT
    salida = capsys.readouterr().out

    assert resultado is True
    assert "Clasificación prevista:" in salida
    assert "foto.jpg" in salida
    assert "Fotos" in salida
    assert "documento.pdf" in salida
    assert "Documentos" in salida


def test_mostrar_clasificacion_vacia(capsys):
    # ARRANGE
    clasificacion = []

    # ACT
    resultado = mostrar_clasificacion(clasificacion)

    # ASSERT
    salida = capsys.readouterr().out

    assert resultado is False
    assert "Clasificación prevista:" in salida
    assert (
        "No se encontraron archivos para organizar."
        in salida
    )
