#!/usr/bin/env python3

from pathlib import Path
from core.analizador import analizar_carpeta
from core.clasificador import clasificar_archivos
from core.movimientos import mover_archivos
from core.deshacer import deshacer_ultima_organizacion


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

            estadisticas = mover_archivos(clasificacion, carpeta)

            print("\n========================================")
            print("           RESUMEN FINAL")
            print("========================================")

            total = sum(estadisticas.values())

            print(f"\nArchivos movidos........ {total}\n")

            for categoria, cantidad in estadisticas.items():
                print(f"{categoria:<22} {cantidad}")

            print("\nProceso finalizado correctamente.")

        else:

            print("\n*** MODO SIMULACIÓN ***")
            print("No se ha movido ningún archivo.")

        print("----------------------------------------")

    else:

        print("\n✗ La carpeta no existe.")


def main():

    while True:

        print("=" * 40)
        print("        FILE ORGANIZER v1.6")
        print("=" * 40)
        print("1) Organizar carpeta")
        print("2) Deshacer última organización")
        print("3) Salir")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":

            seleccionar_carpeta()

        elif opcion == "2":

            deshacer_ultima_organizacion()

        elif opcion == "3":

            print("\n¡Hasta la próxima!")
            break

        else:

            print("\n✗ Opción no válida.\n")


if __name__ == "__main__":
    main()        