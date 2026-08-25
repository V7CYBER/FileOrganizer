from core.auditoria import (
    determinar_nivel_auditoria,
    ejecutar_auditoria,
    generar_informe_auditoria,
    generar_resumen_auditoria,
    guardar_informe_auditoria,
)


def test_generar_resumen_auditoria():
    # ARRANGE
    seguridad = {
        "ok": 8,
        "sospechosos": 2,
        "no_verificados": 1,
    }

    integridad = {
        "sin_cambios": ["documento.txt"],
        "modificados": ["config.json"],
        "nuevos": ["extraño.exe"],
        "eliminados": [],
    }

    # ACT
    resultado = generar_resumen_auditoria(
        seguridad,
        integridad,
    )

    # ASSERT
    assert resultado == {
        "seguridad": {
            "ok": 8,
            "sospechosos": 2,
            "no_verificados": 1,
        },
        "integridad": {
            "sin_cambios": 1,
            "modificados": 1,
            "nuevos": 1,
            "eliminados": 0,
        },
    }


def test_determinar_nivel_auditoria_ok():
    # ARRANGE
    resumen = {
        "seguridad": {
            "ok": 8,
            "sospechosos": 0,
            "no_verificados": 0,
        },
        "integridad": {
            "sin_cambios": 8,
            "modificados": 0,
            "nuevos": 0,
            "eliminados": 0,
        },
    }

    # ACT
    nivel = determinar_nivel_auditoria(resumen)

    # ASSERT
    assert nivel == "OK"


def test_determinar_nivel_auditoria_advertencia():
    # ARRANGE
    resumen = {
        "seguridad": {
            "ok": 8,
            "sospechosos": 0,
            "no_verificados": 0,
        },
        "integridad": {
            "sin_cambios": 7,
            "modificados": 1,
            "nuevos": 0,
            "eliminados": 0,
        },
    }

    # ACT
    nivel = determinar_nivel_auditoria(resumen)

    # ASSERT
    assert nivel == "ADVERTENCIA"


def test_determinar_nivel_auditoria_alerta():
    # ARRANGE
    resumen = {
        "seguridad": {
            "ok": 7,
            "sospechosos": 1,
            "no_verificados": 0,
        },
        "integridad": {
            "sin_cambios": 8,
            "modificados": 0,
            "nuevos": 0,
            "eliminados": 0,
        },
    }

    # ACT
    nivel = determinar_nivel_auditoria(resumen)

    # ASSERT
    assert nivel == "ALERTA"


def test_determinar_nivel_auditoria_alerta_tiene_prioridad():
    # ARRANGE
    resumen = {
        "seguridad": {
            "ok": 5,
            "sospechosos": 1,
            "no_verificados": 0,
        },
        "integridad": {
            "sin_cambios": 5,
            "modificados": 1,
            "nuevos": 1,
            "eliminados": 1,
        },
    }

    # ACT
    nivel = determinar_nivel_auditoria(resumen)

    # ASSERT
    assert nivel == "ALERTA"


def test_determinar_nivel_auditoria_no_verificados():
    # ARRANGE
    resumen = {
        "seguridad": {
            "ok": 7,
            "sospechosos": 0,
            "no_verificados": 1,
        },
        "integridad": {
            "sin_cambios": 8,
            "modificados": 0,
            "nuevos": 0,
            "eliminados": 0,
        },
    }

    # ACT
    nivel = determinar_nivel_auditoria(resumen)

    # ASSERT
    assert nivel == "ADVERTENCIA"


def test_generar_informe_auditoria():
    # ARRANGE
    resumen = {
        "seguridad": {
            "ok": 8,
            "sospechosos": 0,
            "no_verificados": 0,
        },
        "integridad": {
            "sin_cambios": 8,
            "modificados": 0,
            "nuevos": 0,
            "eliminados": 0,
        },
    }

    # ACT
    informe = generar_informe_auditoria(resumen, "OK")

    # ASSERT
    assert "AUDITORÍA DE SEGURIDAD" in informe
    assert "Nivel: OK" in informe
    assert "Sospechosos: 0" in informe
    assert "Modificados: 0" in informe


def test_generar_informe_auditoria_incluye_todos_los_resumenes():
    # ARRANGE
    resumen = {
        "seguridad": {
            "ok": 5,
            "sospechosos": 1,
            "no_verificados": 2,
        },
        "integridad": {
            "sin_cambios": 4,
            "modificados": 1,
            "nuevos": 2,
            "eliminados": 1,
        },
    }

    # ACT
    informe = generar_informe_auditoria(
        resumen,
        "ALERTA",
    )

    # ASSERT
    assert "OK: 5" in informe
    assert "Sospechosos: 1" in informe
    assert "No verificados: 2" in informe
    assert "Sin cambios: 4" in informe
    assert "Modificados: 1" in informe
    assert "Nuevos: 2" in informe
    assert "Eliminados: 1" in informe


def test_guardar_informe_auditoria_crea_archivo(tmp_path):
    # ARRANGE
    informe = "Informe de prueba"

    destino = tmp_path / "reports" / "auditoria.txt"

    # ACT
    archivo_guardado = guardar_informe_auditoria(
        informe,
        destino,
    )

    # ASSERT
    assert archivo_guardado.exists()
    assert archivo_guardado.read_text(encoding="utf-8") == informe


def test_guardar_informe_auditoria_evitar_sobrescritura(tmp_path):
    # ARRANGE
    destino = tmp_path / "reports" / "auditoria.txt"

    primer_informe = guardar_informe_auditoria(
        "Informe original",
        destino,
    )

    # ACT
    segundo_informe = guardar_informe_auditoria(
        "Informe nuevo",
        destino,
    )

    # ASSERT
    assert primer_informe != segundo_informe
    assert primer_informe.read_text(encoding="utf-8") == "Informe original"
    assert segundo_informe.read_text(encoding="utf-8") == "Informe nuevo"


def test_guardar_informe_auditoria_multiples_colisiones(tmp_path):
    # ARRANGE
    destino = tmp_path / "reports" / "auditoria.txt"

    primer_informe = guardar_informe_auditoria(
        "Informe 1",
        destino,
    )

    segundo_informe = guardar_informe_auditoria(
        "Informe 2",
        destino,
    )

    # ACT
    tercer_informe = guardar_informe_auditoria(
        "Informe 3",
        destino,
    )

    # ASSERT
    assert primer_informe.name == "auditoria.txt"
    assert segundo_informe.name == "auditoria_1.txt"
    assert tercer_informe.name == "auditoria_2.txt"


def test_ejecutar_auditoria_combina_seguridad_e_integridad(monkeypatch):
    # ARRANGE
    resultados_seguridad = ["resultado_simulado"]

    resumen_seguridad = {
        "ok": 8,
        "sospechosos": 1,
        "no_verificados": 0,
    }

    baseline = {
        "ruta_base": "/tmp/vigilada",
        "archivos": {},
    }

    snapshot_actual = {
        "ruta_base": "/tmp/vigilada",
        "archivos": {},
    }

    resultado_integridad = {
        "sin_cambios": ["uno.txt"],
        "modificados": ["dos.txt"],
        "nuevos": [],
        "eliminados": [],
    }

    monkeypatch.setattr(
        "core.auditoria.verificar_archivos",
        lambda _: resultados_seguridad,
    )

    monkeypatch.setattr(
        "core.auditoria.generar_resumen_seguridad",
        lambda _: resumen_seguridad,
    )

    monkeypatch.setattr(
        "core.auditoria.cargar_baseline",
        lambda _: baseline,
    )

    monkeypatch.setattr(
        "core.auditoria.generar_snapshot",
        lambda _: snapshot_actual,
    )

    monkeypatch.setattr(
        "core.auditoria.comparar_integridad",
        lambda _baseline, _actual: resultado_integridad,
    )

    # ACT
    resultado = ejecutar_auditoria(
        "/tmp/vigilada",
        "/tmp/baseline.json",
    )

    # ASSERT
    assert resultado["resumen"] == {
        "seguridad": {
            "ok": 8,
            "sospechosos": 1,
            "no_verificados": 0,
        },
        "integridad": {
            "sin_cambios": 1,
            "modificados": 1,
            "nuevos": 0,
            "eliminados": 0,
        },
    }

    assert resultado["nivel"] == "ALERTA"


def test_ejecutar_auditoria_usa_ruta_base_de_baseline(monkeypatch):
    # ARRANGE
    baseline = {
        "ruta_base": "/tmp/ruta_baseline",
        "archivos": {},
    }

    ruta_recibida = {}

    monkeypatch.setattr(
        "core.auditoria.verificar_archivos",
        lambda _: [],
    )

    monkeypatch.setattr(
        "core.auditoria.generar_resumen_seguridad",
        lambda _: {
            "ok": 0,
            "sospechosos": 0,
            "no_verificados": 0,
        },
    )

    monkeypatch.setattr(
        "core.auditoria.cargar_baseline",
        lambda _: baseline,
    )

    def snapshot_simulado(ruta):
        ruta_recibida["ruta"] = ruta

        return {
            "ruta_base": ruta,
            "archivos": {},
        }

    monkeypatch.setattr(
        "core.auditoria.generar_snapshot",
        snapshot_simulado,
    )

    monkeypatch.setattr(
        "core.auditoria.comparar_integridad",
        lambda _baseline, _actual: {
            "sin_cambios": [],
            "modificados": [],
            "nuevos": [],
            "eliminados": [],
        },
    )

    # ACT
    ejecutar_auditoria(
        "/tmp/ruta_baseline",
        "/tmp/baseline.json",
    )

    # ASSERT
    assert ruta_recibida["ruta"] == "/tmp/ruta_baseline"


def test_ejecutar_auditoria_incluye_informe(monkeypatch):
    # ARRANGE
    monkeypatch.setattr(
        "core.auditoria.verificar_archivos",
        lambda _: [],
    )

    monkeypatch.setattr(
        "core.auditoria.generar_resumen_seguridad",
        lambda _: {
            "ok": 3,
            "sospechosos": 0,
            "no_verificados": 0,
        },
    )

    monkeypatch.setattr(
        "core.auditoria.cargar_baseline",
        lambda _: {
            "ruta_base": "/tmp/vigilada",
            "archivos": {},
        },
    )

    monkeypatch.setattr(
        "core.auditoria.generar_snapshot",
        lambda ruta: {
            "ruta_base": ruta,
            "archivos": {},
        },
    )

    monkeypatch.setattr(
        "core.auditoria.comparar_integridad",
        lambda _baseline, _actual: {
            "sin_cambios": ["uno.txt"],
            "modificados": [],
            "nuevos": [],
            "eliminados": [],
        },
    )

    # ACT
    resultado = ejecutar_auditoria(
        "/tmp/vigilada",
        "/tmp/baseline.json",
    )

    # ASSERT
    assert "informe" in resultado
    assert "AUDITORÍA DE SEGURIDAD" in resultado["informe"]
    assert "Nivel: OK" in resultado["informe"]


def test_ejecutar_auditoria_rechaza_carpeta_distinta_baseline(
    monkeypatch,
):
    # ARRANGE
    monkeypatch.setattr(
        "core.auditoria.verificar_archivos",
        lambda _: [],
    )

    monkeypatch.setattr(
        "core.auditoria.generar_resumen_seguridad",
        lambda _: {
            "ok": 0,
            "sospechosos": 0,
            "no_verificados": 0,
        },
    )

    monkeypatch.setattr(
        "core.auditoria.cargar_baseline",
        lambda _: {
            "ruta_base": "/tmp/carpeta_baseline",
            "archivos": {},
        },
    )

    # ACT / ASSERT
    import pytest

    with pytest.raises(
        ValueError,
        match="no coincide",
    ):
        ejecutar_auditoria(
            "/tmp/otra_carpeta",
            "/tmp/baseline.json",
        )
