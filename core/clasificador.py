from pathlib import Path

from core.configuracion import cargar_configuracion


def clasificar_archivos(ruta):

    carpeta = Path(ruta)

    categorias = cargar_configuracion()
    categorias.pop("ignorar", None)

    resultado = []

    for archivo in carpeta.iterdir():

        if archivo.is_file():

            extension = archivo.suffix.lower()

            categoria = "Sin_clasificar"

            for nombre_categoria, extensiones in categorias.items():

                if extension in extensiones:

                    categoria = nombre_categoria
                    break

            resultado.append((archivo.name, categoria))

    return resultado
