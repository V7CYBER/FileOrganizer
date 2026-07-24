from pathlib import Path

def analizar_carpeta(ruta):
    carpeta = Path(ruta)

    archivos = 0
    carpetas = 0
    extensiones = {}

    for elemento in carpeta.iterdir():
        if elemento.is_file():
            archivos += 1

            extension = elemento.suffix.lower()
            if extension == "":
                extension = "[sin extensión]"

            extensiones[extension] = extensiones.get(extension, 0) + 1

        elif elemento.is_dir():
            carpetas += 1

    return {
        "ruta": carpeta.resolve(),
        "archivos": archivos,
        "carpetas": carpetas,
        "extensiones": extensiones
    }