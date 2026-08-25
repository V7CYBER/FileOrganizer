from pathlib import Path

from core.integridad import cargar_baseline, comparar_integridad, generar_snapshot
from core.seguridad import generar_resumen_seguridad, verificar_archivos


def generar_resumen_auditoria(seguridad, integridad):
    return {
        "seguridad": {
            "ok": seguridad["ok"],
            "sospechosos": seguridad["sospechosos"],
            "no_verificados": seguridad["no_verificados"],
        },
        "integridad": {
            "sin_cambios": len(integridad["sin_cambios"]),
            "modificados": len(integridad["modificados"]),
            "nuevos": len(integridad["nuevos"]),
            "eliminados": len(integridad["eliminados"]),
        },
    }


def determinar_nivel_auditoria(resumen):
    seguridad = resumen["seguridad"]
    integridad = resumen["integridad"]

    if seguridad["sospechosos"] > 0:
        return "ALERTA"

    if (
        seguridad["no_verificados"] > 0
        or integridad["modificados"] > 0
        or integridad["nuevos"] > 0
        or integridad["eliminados"] > 0
    ):
        return "ADVERTENCIA"

    return "OK"


def generar_informe_auditoria(resumen, nivel):
    seguridad = resumen["seguridad"]
    integridad = resumen["integridad"]

    return (
        "===== AUDITORÍA DE SEGURIDAD =====\n"
        f"Nivel: {nivel}\n"
        "\n"
        "SEGURIDAD\n"
        f"OK: {seguridad['ok']}\n"
        f"Sospechosos: {seguridad['sospechosos']}\n"
        f"No verificados: {seguridad['no_verificados']}\n"
        "\n"
        "INTEGRIDAD\n"
        f"Sin cambios: {integridad['sin_cambios']}\n"
        f"Modificados: {integridad['modificados']}\n"
        f"Nuevos: {integridad['nuevos']}\n"
        f"Eliminados: {integridad['eliminados']}\n"
    )


def guardar_informe_auditoria(informe, destino):
    ruta = Path(destino)

    ruta.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if ruta.exists():
        contador = 1

        while True:
            candidato = ruta.with_name(f"{ruta.stem}_{contador}{ruta.suffix}")

            if not candidato.exists():
                ruta = candidato
                break

            contador += 1

    ruta.write_text(
        informe,
        encoding="utf-8",
    )

    return ruta


def ejecutar_auditoria(carpeta, ruta_baseline):
    baseline = cargar_baseline(ruta_baseline)

    ruta_carpeta = Path(carpeta).resolve()
    ruta_base = Path(baseline["ruta_base"]).resolve()

    if ruta_carpeta != ruta_base:
        raise ValueError(
            "La carpeta a auditar no coincide "
            "con la ruta base de la baseline."
        )

    resultados_seguridad = verificar_archivos(carpeta)

    resumen_seguridad = generar_resumen_seguridad(
        resultados_seguridad,
    )

    snapshot_actual = generar_snapshot(
        baseline["ruta_base"],
    )

    resultado_integridad = comparar_integridad(
        baseline,
        snapshot_actual,
    )

    resumen = generar_resumen_auditoria(
        resumen_seguridad,
        resultado_integridad,
    )

    nivel = determinar_nivel_auditoria(resumen)

    informe = generar_informe_auditoria(
        resumen,
        nivel,
    )

    return {
        "resumen": resumen,
        "nivel": nivel,
        "informe": informe,
    }
