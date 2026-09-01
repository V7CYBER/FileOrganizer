from pathlib import Path

import organizador
import ui.logs


def test_mostrar_analisis_logs_muestra_resumen(
    monkeypatch,
    capsys,
):
    # ARRANGE
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "/tmp/seguridad.log",
    )

    monkeypatch.setattr(
        Path,
        "exists",
        lambda _: True,
    )

    monkeypatch.setattr(
        Path,
        "is_file",
        lambda _: True,
    )

    eventos = [
        {
            "linea": 1,
            "ip": "192.168.1.10",
            "tipo": "SQL_INJECTION",
            "severidad": "ALTA",
            "regla": "WEB_SQL_001",
            "descripcion": "Posible intento de SQL Injection",
            "contenido": "UNION SELECT",
        }
    ]

    monkeypatch.setattr(
        ui.logs,
        "analizar_log",
        lambda _: eventos,
    )

    monkeypatch.setattr(
        ui.logs,
        "generar_resumen_logs",
        lambda _: {
            "eventos": 1,
            "sql_injection": 1,
            "fuerza_bruta": 0,
            "alta": 1,
            "media": 0,
        },
    )

    monkeypatch.setattr(
        ui.logs,
        "detectar_fuerza_bruta_temporal",
        lambda *_args, **_kwargs: [],
    )

    # ACT
    organizador.mostrar_analisis_logs()

    # ASSERT
    salida = capsys.readouterr().out

    assert "ANÁLISIS DE SEGURIDAD" in salida
    assert "Eventos detectados... 1" in salida
    assert "SQL Injection........ 1" in salida
    assert "192.168.1.10" in salida
    assert "UNION SELECT" in salida
    assert "WEB_SQL_001" in salida
    assert "Posible intento de SQL Injection" in salida


def test_mostrar_analisis_logs_sin_eventos(
    monkeypatch,
    capsys,
):
    # ARRANGE
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "/tmp/seguridad.log",
    )

    monkeypatch.setattr(
        Path,
        "exists",
        lambda _: True,
    )

    monkeypatch.setattr(
        Path,
        "is_file",
        lambda _: True,
    )

    monkeypatch.setattr(
        ui.logs,
        "analizar_log",
        lambda _: [],
    )

    monkeypatch.setattr(
        ui.logs,
        "generar_resumen_logs",
        lambda _: {
            "eventos": 0,
            "sql_injection": 0,
            "fuerza_bruta": 0,
            "alta": 0,
            "media": 0,
        },
    )

    monkeypatch.setattr(
        ui.logs,
        "detectar_fuerza_bruta_temporal",
        lambda *_args, **_kwargs: [],
    )

    # ACT
    organizador.mostrar_analisis_logs()

    # ASSERT
    salida = capsys.readouterr().out

    assert "Eventos detectados... 0" in salida
    assert "No se detectaron eventos de seguridad." in salida


def test_mostrar_analisis_logs_ruta_invalida(
    monkeypatch,
    capsys,
):
    # ARRANGE
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "/tmp/inexistente.log",
    )

    monkeypatch.setattr(
        Path,
        "exists",
        lambda _: False,
    )

    # ACT
    organizador.mostrar_analisis_logs()

    # ASSERT
    salida = capsys.readouterr().out

    assert "no existe o no es válido" in salida


def test_mostrar_analisis_logs_maneja_error_lectura(
    monkeypatch,
    capsys,
):
    # ARRANGE
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "/tmp/seguridad.log",
    )

    monkeypatch.setattr(
        Path,
        "exists",
        lambda _: True,
    )

    monkeypatch.setattr(
        Path,
        "is_file",
        lambda _: True,
    )

    def analizar_log_simulado(_archivo):
        raise PermissionError("Permiso denegado")

    monkeypatch.setattr(
        ui.logs,
        "analizar_log",
        analizar_log_simulado,
    )

    # ACT
    organizador.mostrar_analisis_logs()

    # ASSERT
    salida = capsys.readouterr().out

    assert "No se pudo analizar el archivo" in salida
    assert "Permiso denegado" in salida
