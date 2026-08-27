from pathlib import Path

import ui.organizacion


def test_enviar_sospechosos_vacio_no_hace_nada(
    monkeypatch,
    capsys,
):
    # ARRANGE
    llamadas = []

    def cuarentena_falsa(*args, **kwargs):
        llamadas.append((args, kwargs))

    monkeypatch.setattr(
        ui.organizacion,
        "poner_en_cuarentena",
        cuarentena_falsa,
    )

    # ACT
    ui.organizacion.enviar_sospechosos_cuarentena([])

    # ASSERT
    salida = capsys.readouterr().out

    assert llamadas == []
    assert salida == ""


def test_enviar_sospechosos_llama_cuarentena(
    monkeypatch,
    capsys,
):
    # ARRANGE
    sospechosos = [
        {
            "archivo": Path("/tmp/programa.jpg"),
            "extension": ".jpg",
            "tipo_real": "PE/Windows executable",
            "estado": "SOSPECHOSO",
        },
        {
            "archivo": Path("/tmp/documento.pdf"),
            "extension": ".pdf",
            "tipo_real": "PE/Windows executable",
            "estado": "SOSPECHOSO",
        },
    ]

    llamadas = []

    def cuarentena_falsa(
        ruta_archivo,
        tipo_real,
        extension,
    ):
        llamadas.append(
            (
                ruta_archivo,
                tipo_real,
                extension,
            )
        )

        return Path("/tmp/quarantine") / Path(ruta_archivo).name

    monkeypatch.setattr(
        ui.organizacion,
        "poner_en_cuarentena",
        cuarentena_falsa,
    )

    # ACT
    ui.organizacion.enviar_sospechosos_cuarentena(sospechosos)

    # ASSERT
    salida = capsys.readouterr().out

    assert len(llamadas) == 2

    assert llamadas[0] == (
        Path("/tmp/programa.jpg"),
        "PE/Windows executable",
        ".jpg",
    )

    assert llamadas[1] == (
        Path("/tmp/documento.pdf"),
        "PE/Windows executable",
        ".pdf",
    )

    assert "Enviando archivos sospechosos" in salida
    assert "programa.jpg" in salida
    assert "documento.pdf" in salida
    assert "/tmp/quarantine/programa.jpg" in salida
    assert "/tmp/quarantine/documento.pdf" in salida
