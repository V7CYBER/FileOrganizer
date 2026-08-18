from pathlib import Path

from core.configuracion import cargar_configuracion, obtener_carpetas_ignoradas


def analizar_carpeta(ruta):

    carpeta = Path(ruta)

    archivos = 0
    carpetas = 0
    extensiones = {}

    config = cargar_configuracion()
    ignorar = obtener_carpetas_ignoradas(config)

    for elemento in carpeta.iterdir():

        if elemento.is_file():

            archivos += 1

            extension = elemento.suffix.lower()

            if extension == "":
                extension = "[sin extensión]"

            extensiones[extension] = extensiones.get(extension, 0) + 1

        elif elemento.is_dir():

            if elemento.name in ignorar:
                continue

            carpetas += 1

    return {
        "ruta": carpeta.resolve(),
        "archivos": archivos,
        "carpetas": carpetas,
        "extensiones": extensiones
    }
