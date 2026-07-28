from pathlib import Path
import shutil
from core.logger import guardar_log
from core.mensajes import mostrar_error


def mostrar_progreso(actual, total):

    ancho = 20

    progreso = int((actual / total) * ancho)

    barra = "#" * progreso + "-" * (ancho - progreso)

    print(f"[{barra}] {actual}/{total}")


def obtener_destino_libre(destino):

    if not destino.exists():
        return destino

    contador = 1

    while True:

        nuevo_nombre = f"{destino.stem} ({contador}){destino.suffix}"
        nuevo_destino = destino.parent / nuevo_nombre

        if not nuevo_destino.exists():
            return nuevo_destino

        contador += 1


def mover_fotos(ruta):

    carpeta = Path(ruta)
    destino = carpeta / "Fotos"


    extensiones_fotos = [".jpg", ".jpeg", ".png", ".gif"]

    for archivo in carpeta.iterdir():

        if archivo.is_file():

            if archivo.suffix.lower() in extensiones_fotos:

                nuevo_destino = obtener_destino_libre(destino / archivo.name)

                shutil.move(str(archivo), str(nuevo_destino))

                print(f"📷 {archivo.name} → Fotos/")


def mover_archivos(clasificacion, ruta):

    carpeta = Path(ruta)
    estadisticas = {}

    total = len(clasificacion)
    actual = 0

    for nombre, categoria in clasificacion:

        origen = carpeta / nombre
        destino = carpeta / categoria / nombre

        destino = obtener_destino_libre(destino)

        if origen.exists():

            try:

                shutil.move(str(origen), "/ruta/que/no/existe/" + nombre)
                guardar_log(nombre, str(carpeta), categoria)


                estadisticas[categoria] = estadisticas.get(categoria, 0) + 1
                actual += 1
                mostrar_progreso(actual, total)
                print(f"📦 {nombre} → {categoria}/")

            except PermissionError:

                mostrar_error(
                    nombre,
                    "Permiso denegado."
                )

            except FileNotFoundError:

                mostrar_error(
                    nombre,
                    "Archivo o carpeta no encontrada."
                )

            except OSError as error:

                mostrar_error(
                    nombre,
                    f"Error del sistema: {error}"
                )

            except Exception as error:

                mostrar_error(
                    nombre,
                    f"Error inesperado: {error}"
                )
      

    return estadisticas
