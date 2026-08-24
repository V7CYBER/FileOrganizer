from pathlib import Path


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
            candidato = ruta.with_name(
                f"{ruta.stem}_{contador}{ruta.suffix}"
            )

            if not candidato.exists():
                ruta = candidato
                break

            contador += 1

    ruta.write_text(
        informe,
        encoding="utf-8",
    )

    return ruta
