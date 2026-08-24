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
