import shutil
from pathlib import Path

from core.rutas import ARCHIVO_LOG_MOVIMIENTOS


def deshacer_ultima_organizacion():

    archivo_log = ARCHIVO_LOG_MOVIMIENTOS

    if not archivo_log.exists():

        print("✗ No existe ningún historial de movimientos.")
        return

    print("✓ Historial encontrado.")

    with open(archivo_log, "r", encoding="utf-8") as log:
        lineas = log.readlines()

    if not lineas:

        print("No hay movimientos para deshacer.")
        return

    print(f"Se han encontrado {len(lineas)} movimientos.\n")

    restaurados = 0

    for linea in lineas:

        linea = linea.strip()

        partes = linea.split(" | ")

        if len(partes) != 3:
            print(f"✗ Registro de log inválido: {linea}")
            continue

        registro = partes[0]
        ruta_original = partes[1]
        categoria = partes[2]

        nombre_archivo = registro.split("] ", 1)[1]

        origen = Path(ruta_original) / categoria / nombre_archivo
        destino = Path(ruta_original) / nombre_archivo

        if origen.exists():

            shutil.move(str(origen), str(destino))

            restaurados += 1

            print(f"✓ Restaurado: {nombre_archivo}")

        else:

            print(f"✗ No encontrado: {origen}")

    print("\n========================================")
    print("      RESUMEN DE RESTAURACIÓN")
    print("========================================")
    print(f"Archivos restaurados..... {restaurados}")

    if restaurados > 0:

        with open(archivo_log, "w", encoding="utf-8"):
            pass

        print("✓ Historial borrado.")
