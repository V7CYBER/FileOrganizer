from pathlib import Path

from core.hash import calcular_sha256


def buscar_duplicados_hash(ruta):

    carpeta = Path(ruta)

    grupos = {}

    for archivo in carpeta.rglob("*"):

        if archivo.is_file():

            hash_archivo = calcular_sha256(archivo)

            grupos.setdefault(hash_archivo, []).append(archivo.name)

    duplicados = {}

    for hash_archivo, lista in grupos.items():

        if len(lista) > 1:

            duplicados[hash_archivo] = sorted(lista)

    return duplicados
