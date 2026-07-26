from pathlib import Path

CARPETAS = [
    "Fotos",
    "Documentos",
    "Música",
    "Vídeos",
    "Comprimidos",
    "Otros"
]


def crear_carpetas(ruta):

    carpeta = Path(ruta)

    for nombre in CARPETAS:

        destino = carpeta / nombre

        if not destino.exists():
            destino.mkdir()
            print(f"✓ Creada carpeta: {nombre}")

        else:
            print(f"• Ya existe: {nombre}")