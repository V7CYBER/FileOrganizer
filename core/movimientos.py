from pathlib import Path
import shutil
from core.logger import guardar_log


def obtener_destino_libre(destino):

    if not destino.exists():
        return destino

    contador = 1

    while True:

        nuevo_nombre = (
            f"{destino.stem} ({contador}){destino.suffix}"
        )

        nuevo_destino = destino.parent / nuevo_nombre

        if not nuevo_destino.exists():
            return nuevo_destino

        contador += 1

EXTENSIONES_FOTOS = [".jpg", ".jpeg", ".png", ".gif"]


def mover_fotos(ruta):

    carpeta = Path(ruta)
    destino = carpeta / "Fotos"

    for archivo in carpeta.iterdir():

        if archivo.is_file():

            if archivo.suffix.lower() in EXTENSIONES_FOTOS:

                nuevo_destino = destino / archivo.name

                shutil.move(str(archivo), str(nuevo_destino))

                print(f"📷 {archivo.name} → Fotos/")

def mover_archivos(clasificacion, ruta):

    carpeta = Path(ruta)

    for nombre, categoria in clasificacion:

        origen = carpeta / nombre
        destino = carpeta / categoria / nombre

        destino = obtener_destino_libre(destino)

        if origen.exists():

            shutil.move(str(origen), str(destino))
            guardar_log(nombre, categoria)

            print(f"📦 {nombre} → {categoria}/")