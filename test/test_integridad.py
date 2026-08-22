import json
from pathlib import Path

import pytest

from core.hash import calcular_sha256
from core.integridad import (
    cargar_baseline,
    comparar_integridad,
    generar_snapshot,
    guardar_baseline,
)


def test_generar_snapshot_un_archivo(tmp_path):
    # ARRANGE
    archivo = tmp_path / "factura.pdf"
    archivo.write_bytes(b"contenido de prueba")

    # ACT
    snapshot = generar_snapshot(tmp_path)

    # ASSERT
    assert snapshot["ruta_base"] == str(tmp_path)

    assert snapshot["archivos"]["factura.pdf"] == calcular_sha256(archivo)


def test_generar_snapshot_subdirectorio(tmp_path):
    # ARRANGE
    carpeta = tmp_path / "Trabajo"
    carpeta.mkdir()

    archivo = carpeta / "informe.txt"
    archivo.write_bytes(b"informe interno")

    # ACT
    snapshot = generar_snapshot(tmp_path)

    # ASSERT
    assert snapshot["archivos"]["Trabajo/informe.txt"] == calcular_sha256(archivo)


def test_generar_snapshot_carpeta_vacia(tmp_path):
    # ACT
    snapshot = generar_snapshot(tmp_path)

    # ASSERT
    assert snapshot["ruta_base"] == str(tmp_path)
    assert snapshot["archivos"] == {}


def test_generar_snapshot_ruta_inexistente(tmp_path):
    # ARRANGE
    ruta_inexistente = tmp_path / "no_existe"

    # ACT / ASSERT
    with pytest.raises(FileNotFoundError):
        generar_snapshot(ruta_inexistente)


def test_generar_snapshot_ruta_es_archivo(tmp_path):
    # ARRANGE
    archivo = tmp_path / "factura.pdf"
    archivo.write_bytes(b"contenido")

    # ACT / ASSERT
    with pytest.raises(NotADirectoryError):
        generar_snapshot(archivo)


def test_guardar_baseline_crea_archivo_y_directorio(tmp_path):
    # ARRANGE
    snapshot = {
        "ruta_base": "/home/wakan/Documentos",
        "archivos": {
            "factura.pdf": "AAA111",
        },
    }

    destino = tmp_path / "baselines" / "baseline.json"

    # ACT
    resultado = guardar_baseline(snapshot, destino)

    # ASSERT
    assert resultado == destino
    assert destino.exists()

    contenido = json.loads(destino.read_text(encoding="utf-8"))

    assert contenido == snapshot


def test_guardar_baseline_evitar_sobrescritura(tmp_path):
    # ARRANGE
    destino = tmp_path / "baseline.json"

    snapshot_1 = {
        "ruta_base": "/origen/uno",
        "archivos": {
            "a.txt": "AAA111",
        },
    }

    snapshot_2 = {
        "ruta_base": "/origen/dos",
        "archivos": {
            "b.txt": "BBB222",
        },
    }

    guardar_baseline(snapshot_1, destino)

    # ACT
    resultado = guardar_baseline(snapshot_2, destino)

    # ASSERT
    assert resultado == tmp_path / "baseline_1.json"

    contenido_original = json.loads(destino.read_text(encoding="utf-8"))

    contenido_nuevo = json.loads(resultado.read_text(encoding="utf-8"))

    assert contenido_original == snapshot_1
    assert contenido_nuevo == snapshot_2


def test_guardar_baseline_multiples_colisiones(tmp_path):
    # ARRANGE
    destino = tmp_path / "baseline.json"

    snapshot = {
        "ruta_base": "/origen",
        "archivos": {},
    }

    guardar_baseline(snapshot, destino)
    guardar_baseline(snapshot, destino)

    # ACT
    resultado = guardar_baseline(snapshot, destino)

    # ASSERT
    assert resultado == tmp_path / "baseline_2.json"

    assert destino.exists()
    assert (tmp_path / "baseline_1.json").exists()
    assert (tmp_path / "baseline_2.json").exists()


def test_cargar_baseline_valida(tmp_path):
    # ARRANGE
    snapshot = {
        "ruta_base": "/home/wakan/Documentos",
        "archivos": {
            "factura.pdf": "a" * 64,
        },
    }

    destino = tmp_path / "baseline.json"
    guardar_baseline(snapshot, destino)

    # ACT
    resultado = cargar_baseline(destino)

    # ASSERT
    assert resultado == snapshot


def test_cargar_baseline_inexistente(tmp_path):
    # ARRANGE
    ruta = tmp_path / "no_existe.json"

    # ACT / ASSERT
    with pytest.raises(FileNotFoundError):
        cargar_baseline(ruta)


def test_cargar_baseline_json_corrupto(tmp_path):
    # ARRANGE
    ruta = tmp_path / "baseline.json"
    ruta.write_text(
        "{ esto no es json válido",
        encoding="utf-8",
    )

    # ACT / ASSERT
    with pytest.raises(json.JSONDecodeError):
        cargar_baseline(ruta)


def test_comparar_integridad_sin_cambios():
    # ARRANGE
    baseline = {
        "ruta_base": "/home/wakan/Documentos",
        "archivos": {
            "factura.pdf": "AAA111",
        },
    }

    actual = {
        "ruta_base": "/home/wakan/Documentos",
        "archivos": {
            "factura.pdf": "AAA111",
        },
    }

    # ACT
    resultado = comparar_integridad(baseline, actual)

    # ASSERT
    assert resultado == {
        "sin_cambios": ["factura.pdf"],
        "modificados": [],
        "nuevos": [],
        "eliminados": [],
    }


def test_comparar_integridad_modificado():
    # ARRANGE
    baseline = {
        "ruta_base": "/home/wakan/Documentos",
        "archivos": {
            "factura.pdf": "AAA111",
        },
    }

    actual = {
        "ruta_base": "/home/wakan/Documentos",
        "archivos": {
            "factura.pdf": "BBB222",
        },
    }

    # ACT
    resultado = comparar_integridad(baseline, actual)

    # ASSERT
    assert resultado == {
        "sin_cambios": [],
        "modificados": ["factura.pdf"],
        "nuevos": [],
        "eliminados": [],
    }


def test_comparar_integridad_nuevo():
    # ARRANGE
    baseline = {
        "ruta_base": "/home/wakan/Documentos",
        "archivos": {},
    }

    actual = {
        "ruta_base": "/home/wakan/Documentos",
        "archivos": {
            "nuevo.txt": "CCC333",
        },
    }

    # ACT
    resultado = comparar_integridad(baseline, actual)

    # ASSERT
    assert resultado == {
        "sin_cambios": [],
        "modificados": [],
        "nuevos": ["nuevo.txt"],
        "eliminados": [],
    }


def test_comparar_integridad_eliminado():
    # ARRANGE
    baseline = {
        "ruta_base": "/home/wakan/Documentos",
        "archivos": {
            "viejo.txt": "DDD444",
        },
    }

    actual = {
        "ruta_base": "/home/wakan/Documentos",
        "archivos": {},
    }

    # ACT
    resultado = comparar_integridad(baseline, actual)

    # ASSERT
    assert resultado == {
        "sin_cambios": [],
        "modificados": [],
        "nuevos": [],
        "eliminados": ["viejo.txt"],
    }


def test_comparar_integridad_varios_cambios():
    # ARRANGE
    baseline = {
        "ruta_base": "/home/wakan/Documentos",
        "archivos": {
            "igual.txt": "AAA111",
            "modificado.txt": "BBB222",
            "eliminado.txt": "CCC333",
        },
    }

    actual = {
        "ruta_base": "/home/wakan/Documentos",
        "archivos": {
            "igual.txt": "AAA111",
            "modificado.txt": "ZZZ999",
            "nuevo.txt": "DDD444",
        },
    }

    # ACT
    resultado = comparar_integridad(baseline, actual)

    # ASSERT
    assert resultado == {
        "sin_cambios": ["igual.txt"],
        "modificados": ["modificado.txt"],
        "nuevos": ["nuevo.txt"],
        "eliminados": ["eliminado.txt"],
    }


def test_comparar_integridad_rutas_base_distintas():
    # ARRANGE
    baseline = {
        "ruta_base": "/home/wakan/Documentos",
        "archivos": {
            "archivo.txt": "AAA111",
        },
    }

    actual = {
        "ruta_base": "/home/wakan/Descargas",
        "archivos": {
            "archivo.txt": "AAA111",
        },
    }

    # ACT / ASSERT
    with pytest.raises(ValueError):
        comparar_integridad(baseline, actual)


def test_generar_snapshot_ruta_base_absoluta(tmp_path, monkeypatch):
    # ARRANGE
    monkeypatch.chdir(tmp_path)

    carpeta = Path("vigilada")
    carpeta.mkdir()

    # ACT
    snapshot = generar_snapshot(carpeta)

    # ASSERT
    assert snapshot["ruta_base"] == str(carpeta.resolve())


def test_cargar_baseline_sin_ruta_base(tmp_path):
    # ARRANGE
    ruta = tmp_path / "baseline.json"

    ruta.write_text(
        json.dumps(
            {
                "archivos": {
                    "factura.pdf": "AAA111",
                }
            }
        ),
        encoding="utf-8",
    )

    # ACT / ASSERT
    with pytest.raises(ValueError):
        cargar_baseline(ruta)


def test_cargar_baseline_sin_archivos(tmp_path):
    # ARRANGE
    ruta = tmp_path / "baseline.json"

    ruta.write_text(
        json.dumps(
            {
                "ruta_base": "/home/wakan/Documentos",
            }
        ),
        encoding="utf-8",
    )

    # ACT / ASSERT
    with pytest.raises(ValueError):
        cargar_baseline(ruta)


def test_cargar_baseline_ruta_base_tipo_invalido(tmp_path):
    # ARRANGE
    ruta = tmp_path / "baseline.json"

    ruta.write_text(
        json.dumps(
            {
                "ruta_base": 123,
                "archivos": {},
            }
        ),
        encoding="utf-8",
    )

    # ACT / ASSERT
    with pytest.raises(TypeError):
        cargar_baseline(ruta)


def test_cargar_baseline_archivos_tipo_invalido(tmp_path):
    # ARRANGE
    ruta = tmp_path / "baseline.json"

    ruta.write_text(
        json.dumps(
            {
                "ruta_base": "/home/wakan/Documentos",
                "archivos": [],
            }
        ),
        encoding="utf-8",
    )

    # ACT / ASSERT
    with pytest.raises(TypeError):
        cargar_baseline(ruta)


def test_generar_snapshot_archivo_desaparece_durante_hash(tmp_path, monkeypatch):
    # ARRANGE
    archivo = tmp_path / "temporal.txt"
    archivo.write_bytes(b"contenido temporal")

    def hash_simulado(ruta):
        raise FileNotFoundError(f"Archivo desaparecido: {ruta}")

    monkeypatch.setattr(
        "core.integridad.calcular_sha256",
        hash_simulado,
    )

    # ACT
    snapshot = generar_snapshot(tmp_path)

    # ASSERT
    assert snapshot["archivos"] == {}


def test_generar_snapshot_ignora_symlink(tmp_path):
    # ARRANGE
    real = tmp_path / "real.txt"
    real.write_bytes(b"contenido real")

    enlace = tmp_path / "enlace.txt"
    enlace.symlink_to(real)

    # ACT
    snapshot = generar_snapshot(tmp_path)

    # ASSERT
    assert "real.txt" in snapshot["archivos"]
    assert "enlace.txt" not in snapshot["archivos"]


def test_cargar_baseline_hash_tipo_invalido(tmp_path):
    # ARRANGE
    ruta = tmp_path / "baseline.json"

    ruta.write_text(
        json.dumps(
            {
                "ruta_base": "/home/wakan/Documentos",
                "archivos": {
                    "factura.pdf": 123,
                },
            }
        ),
        encoding="utf-8",
    )

    # ACT / ASSERT
    with pytest.raises(TypeError):
        cargar_baseline(ruta)


def test_cargar_baseline_hash_formato_invalido(tmp_path):
    # ARRANGE
    ruta = tmp_path / "baseline.json"

    ruta.write_text(
        json.dumps(
            {
                "ruta_base": "/home/wakan/Documentos",
                "archivos": {
                    "factura.pdf": "HASH_INVALIDO",
                },
            }
        ),
        encoding="utf-8",
    )

    # ACT / ASSERT
    with pytest.raises(ValueError):
        cargar_baseline(ruta)


def test_cargar_baseline_ruta_base_vacia(tmp_path):
    # ARRANGE
    ruta = tmp_path / "baseline.json"

    ruta.write_text(
        json.dumps(
            {
                "ruta_base": "",
                "archivos": {},
            }
        ),
        encoding="utf-8",
    )

    # ACT / ASSERT
    with pytest.raises(ValueError):
        cargar_baseline(ruta)
