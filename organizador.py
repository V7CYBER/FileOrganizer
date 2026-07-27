#!/usr/bin/env python3

from pathlib import Path
from core.analizador import analizar_carpeta
from core.clasificador import clasificar_archivos
from core.creador import crear_carpetas
from core.movimientos import mover_archivos

def seleccionar_carpeta():

    ruta = input("¿Qué carpeta quieres organizar? ")
    carpeta = Path(ruta).expanduser()

    while True:

        simulacion = input("¿Mover los archivos? (S/N): ").strip().upper()

        if simulacion in ("S", "N"):
            break

        print("✗ Respuesta no válida. Escribe únicamente S o N.\n")

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

        if not clasificacion:

            print("  No se encontraron archivos para organizar.")

        else:

            for nombre, categoria in clasificacion:
                print(f"  {nombre:<35} → {categoria}")

        if simulacion == "S":

            print("\nMoviendo archivos...\n")

            mover_archivos(clasificacion, carpeta)

        else:

            print("\n*** MODO SIMULACIÓN ***")
            print("No se ha movido ningún archivo.")

        print("----------------------------------------")

    else:

        print("\n✗ La carpeta no existe.")


def main():

    print("=" * 40)
    print("        FILE ORGANIZER v1.2")
    print("=" * 40)

    seleccionar_carpeta()


if __name__ == "__main__":
    main()