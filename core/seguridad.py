from pathlib import Path

from core.verificador import verificar_archivo


def verificar_archivos(carpeta):
    """
    Verifica los archivos de una carpeta comparando
    su extensión con su firma real.
    """

    ruta = Path(carpeta)

    if not ruta.exists():
        raise FileNotFoundError(
            f"No existe la carpeta: {ruta}"
        )

    if not ruta.is_dir():
        raise NotADirectoryError(
            f"La ruta no es una carpeta: {ruta}"
        )

    resultados = []

    for archivo in sorted(ruta.iterdir()):

        if not archivo.is_file():
            continue

        resultado = verificar_archivo(archivo)

        resultados.append(resultado)

    return resultados


def obtener_sospechosos(resultados):
    """
    Devuelve únicamente los archivos detectados
    como sospechosos.
    """

    return [
        resultado
        for resultado in resultados
        if resultado["estado"] == "SOSPECHOSO"
    ]


def obtener_no_verificados(resultados):
    """
    Devuelve los archivos cuya extensión todavía
    no está contemplada por el verificador.
    """

    return [
        resultado
        for resultado in resultados
        if resultado["estado"] == "NO_VERIFICADO"
    ]


def obtener_archivos_ok(resultados):
    """
    Devuelve los archivos cuya extensión coincide
    con su tipo real detectado.
    """

    return [
        resultado
        for resultado in resultados
        if resultado["estado"] == "OK"
    ]


def generar_resumen_seguridad(resultados):
    """
    Genera un resumen estadístico de la verificación.
    """

    resumen = {
        "verificados": len(resultados),
        "ok": 0,
        "sospechosos": 0,
        "no_verificados": 0,
    }

    for resultado in resultados:

        estado = resultado["estado"]

        if estado == "OK":
            resumen["ok"] += 1

        elif estado == "SOSPECHOSO":
            resumen["sospechosos"] += 1

        elif estado == "NO_VERIFICADO":
            resumen["no_verificados"] += 1

    return resumen
