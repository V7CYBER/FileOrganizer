def crear_evento_seguridad(
    linea,
    ip,
    regla,
    contenido,
    fecha=None,
):
    campos_obligatorios = {
        "id",
        "tipo",
        "severidad",
        "descripcion",
    }

    if not campos_obligatorios <= regla.keys():
        raise ValueError("Regla incompleta")

    if not isinstance(linea, int):
        raise TypeError("Línea inválida")

    if linea < 1:
        raise ValueError("Línea inválida")

    if not isinstance(contenido, str):
        raise TypeError("Contenido inválido")

    return {
        "linea": linea,
        "ip": ip,
        "tipo": regla["tipo"],
        "severidad": regla["severidad"],
        "regla": regla["id"],
        "descripcion": regla["descripcion"],
        "contenido": contenido,
        "fecha": fecha,
    }
