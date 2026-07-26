from pathlib import Path
from config import CATEGORIAS


def clasificar_archivos(ruta):

    carpeta = Path(ruta)

    resultado = []

    for archivo in carpeta.iterdir():

        if archivo.is_file():

            extension = archivo.suffix.lower()

            categoria = "Otros"

            for nombre_categoria, extensiones in CATEGORIAS.items():

                if extension in extensiones:

                    categoria = nombre_categoria
                    break

            resultado.append((archivo.name, categoria))

    return resultado