#!/usr/bin/env python3

from pathlib import Path
from core.analizador import analizar_carpeta
from core.clasificador import clasificar_archivos
from core.creador import crear_carpetas
from core.movimientos import mover_archivos

def seleccionar_carpeta():

    ruta = input("¿Qué carpeta quieres organizar? ")

    carpeta = Path(ruta).expanduser()

    if carpeta.exists() and carpeta.is_dir():

        datos = analizar_carpeta(carpeta)

        print("\n----------------------------------------")
        print(f"Ruta............... {datos['ruta']}")
        print(f"Archivos........... {datos['archivos']}")
        print(f"Subcarpetas........ {datos['carpetas']}")

        print("\nTipos de archivo encontrados:")

        for extension, cantidad in sorted(datos["extensiones"].items()):
            print(f"  {extension:<15} {cantidad}")

        print("\nClasificación prevista:")

        clasificacion = clasificar_archivos(carpeta)

        if clasificacion:

            for nombre, categoria in clasificacion:
                print(f"  {nombre:<35} → {categoria}")

        else:

            print("  No se encontraron archivos para organizar.")

        print("\nPreparando estructura de carpetas...\n")

        crear_carpetas(carpeta)

        print("\nMoviendo archivos...\n")

        mover_archivos(clasificacion, carpeta)

        print("----------------------------------------")

    else:

        print("\n✗ La carpeta no existe.")


def main():

    print("=" * 40)
    print("        FILE ORGANIZER v1.0")
    print("=" * 40)

    seleccionar_carpeta()


if __name__ == "__main__":
    main()