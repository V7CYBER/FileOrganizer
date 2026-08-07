from pathlib import Path

from core.hash import calcular_sha256


def buscar_duplicados_hash(ruta):

    carpeta = Path(ruta)

    grupos = {}

    for archivo in carpeta.rglob("*"):

        if archivo.is_file():

            hash_archivo = calcular_sha256(archivo)

            grupos.setdefault(hash_archivo, []).append(
    {
        "nombre": archivo.name,
        "ruta": str(archivo),
        "tamano": archivo.stat().st_size,
        "fecha": archivo.stat().st_mtime,
    }
)

    duplicados = {}

    for hash_archivo, lista in grupos.items():

        if len(lista) > 1:

            duplicados[hash_archivo] = lista

    return duplicados
