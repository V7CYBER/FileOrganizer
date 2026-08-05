from pathlib import Path
import re


def buscar_duplicados(ruta):

    carpeta = Path(ruta)

    grupos = {}

    for archivo in carpeta.rglob("*"):

        if archivo.is_file():

            nombre_base = re.sub(
                r" \(\d+\)",
                "",
                archivo.name
            )

            grupos.setdefault(nombre_base, []).append(archivo.name)

    duplicados = {}

    for nombre, lista in grupos.items():

        if len(lista) > 1:
            duplicados[nombre] = sorted(lista)

    return duplicados
