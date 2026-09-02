def crear_alerta_seguridad(
    ip,
    intentos,
    ventana_segundos,
    lineas,
    fecha=None,
):
    if not isinstance(intentos, int):
        raise TypeError("Intentos inválidos")
    if intentos < 1:
        raise ValueError("Intentos inválidos")

    return {
        "ip": ip,
        "tipo": "POSIBLE_FUERZA_BRUTA",
        "severidad": "ALTA",
        "intentos": intentos,
        "ventana_segundos": ventana_segundos,
        "lineas": lineas,
        "fecha": fecha,
    }
