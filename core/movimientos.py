from pathlib import Path
import shutil

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