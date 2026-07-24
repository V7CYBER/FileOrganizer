from pathlib import Path

CATEGORIAS = {
    ".jpg": "Fotos",
    ".jpeg": "Fotos",
    ".png": "Fotos",
    ".gif": "Fotos",

    ".pdf": "Documentos",
    ".doc": "Documentos",
    ".docx": "Documentos",
    ".txt": "Documentos",

    ".mp3": "Música",
    ".wav": "Música",

    ".mp4": "Vídeos",
    ".avi": "Vídeos",
    ".mkv": "Vídeos",

    ".zip": "Comprimidos",
    ".rar": "Comprimidos",
    ".7z": "Comprimidos"
}


def clasificar_archivos(ruta):

    carpeta = Path(ruta)

    resultado = []

    for archivo in carpeta.iterdir():

        if archivo.is_file():

            extension = archivo.suffix.lower()

            categoria = CATEGORIAS.get(extension, "Otros")

            resultado.append((archivo.name, categoria))

    return resultado