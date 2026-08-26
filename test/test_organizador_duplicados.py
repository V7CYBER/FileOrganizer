from pathlib import Path

import organizador
import ui.duplicados


def test_mostrar_duplicados_muestra_resultados(
    monkeypatch,
    capsys,
):
    # ARRANGE
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "/tmp/prueba",
    )

    monkeypatch.setattr(
        Path,
        "exists",
        lambda _: True,
    )

    monkeypatch.setattr(
        Path,
        "is_dir",
        lambda _: True,
    )

    monkeypatch.setattr(
        ui.duplicados,
        "buscar_duplicados",
        lambda _: {
            "foto.jpg": [
                "foto.jpg",
                "foto (1).jpg",
            ],
        },
    )

    # ACT
    organizador.mostrar_duplicados()

    # ASSERT
    salida = capsys.readouterr().out

    assert "ARCHIVOS DUPLICADOS" in salida
    assert "Grupos encontrados..... 1" in salida
    assert "foto.jpg" in salida
    assert "foto (1).jpg" in salida


def test_mostrar_duplicados_sin_resultados(
    monkeypatch,
    capsys,
):
    # ARRANGE
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "/tmp/prueba",
    )

    monkeypatch.setattr(
        Path,
        "exists",
        lambda _: True,
    )

    monkeypatch.setattr(
        Path,
        "is_dir",
        lambda _: True,
    )

    monkeypatch.setattr(
        ui.duplicados,
        "buscar_duplicados",
        lambda _: {},
    )

    # ACT
    organizador.mostrar_duplicados()

    # ASSERT
    salida = capsys.readouterr().out

    assert "Grupos encontrados..... 0" in salida
    assert "No se encontraron archivos duplicados." in salida


def test_mostrar_duplicados_ruta_invalida(
    monkeypatch,
    capsys,
):
    # ARRANGE
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "/tmp/inexistente",
    )

    monkeypatch.setattr(
        Path,
        "exists",
        lambda _: False,
    )

    # ACT
    organizador.mostrar_duplicados()

    # ASSERT
    salida = capsys.readouterr().out

    assert "ERROR" in salida.upper() or "no existe" in salida.lower()


def test_mostrar_duplicados_hash_muestra_resultados(
    monkeypatch,
    capsys,
):
    # ARRANGE
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "/tmp/prueba",
    )

    monkeypatch.setattr(
        ui.duplicados,
        "buscar_duplicados_hash",
        lambda _: {
            "a"
            * 64: [
                {
                    "nombre": "uno.txt",
                    "ruta": "/tmp/prueba/uno.txt",
                    "tamano": 10,
                    "fecha": 0,
                },
                {
                    "nombre": "dos.txt",
                    "ruta": "/tmp/prueba/dos.txt",
                    "tamano": 10,
                    "fecha": 0,
                },
            ],
        },
    )

    # ACT
    organizador.mostrar_duplicados_hash()

    # ASSERT
    salida = capsys.readouterr().out

    assert "DUPLICADOS POR CONTENIDO" in salida
    assert "Grupos encontrados..... 1" in salida
    assert "uno.txt" in salida
    assert "dos.txt" in salida
