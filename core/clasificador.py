from pathlib import Path
import json



def cargar_configuracion():

    archivo = Path("config.json")

    with open(archivo, "r", encoding="utf-8") as f:

        return json.load(f)
    


def clasificar_archivos(ruta):

    carpeta = Path(ruta)

    categorias = cargar_configuracion()

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
