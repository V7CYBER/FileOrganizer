from pathlib import Path

from ui.organizacion import mostrar_alertas_seguridad


def test_alertas_vacias_no_imprimen(capsys):
    # ARRANGE
    sospechosos = []

    # ACT
    mostrar_alertas_seguridad(sospechosos)

    # ASSERT
    salida = capsys.readouterr().out

    assert salida == ""


def test_mostrar_alerta_sospechoso(capsys):
    # ARRANGE
    sospechosos = [
        {
            "archivo": Path("/tmp/programa.jpg"),
            "extension": ".jpg",
            "tipo_real": "PE/Windows executable",
            "estado": "SOSPECHOSO",
        }
    ]

    # ACT
    mostrar_alertas_seguridad(sospechosos)

    # ASSERT
    salida = capsys.readouterr().out

    assert "ALERTA DE SEGURIDAD" in salida
    assert "programa.jpg" in salida
    assert ".jpg" in salida
    assert "PE/Windows executable" in salida
    assert "SOSPECHOSO" in salida
    assert "CUARENTENA" in salida


def test_alerta_en_modo_simulacion(capsys):
    # ARRANGE
    sospechosos = [
        {
            "archivo": Path("/tmp/programa.jpg"),
            "extension": ".jpg",
            "tipo_real": "PE/Windows executable",
            "estado": "SOSPECHOSO",
        }
    ]

    # ACT
    mostrar_alertas_seguridad(
        sospechosos,
        simulacion=True,
    )

    # ASSERT
    salida = capsys.readouterr().out

    assert "Modo simulación" in salida
    assert (
        "Los archivos sospechosos NO serán enviados "
        "a cuarentena."
    ) in salida
