#!/usr/bin/env python3

from pathlib import Path
from core.analizador import analizar_carpeta
from core.clasificador import clasificar_archivos
from core.movimientos import mover_archivos
from core.deshacer import deshacer_ultima_organizacion
from core.mensajes import mostrar_error, mostrar_error_ruta


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

        if not clasificacion:

            print("  No se encontraron archivos para organizar.")

        else:

            for nombre, categoria in clasificacion:
                print(f"  {nombre:<35} → {categoria}")

        if clasificacion:
            confirmacion = input(
            "\n¿Desea continuar con la organización? (S/N): "
            ).strip().upper()

            if confirmacion != "S":

                print("\nOperación cancelada por el usuario.")
                print("----------------------------------------")
                return

            print("\nMoviendo archivos...\n")

            estadisticas = mover_archivos(clasificacion, carpeta)

            print("\n========================================")
            print("           RESUMEN FINAL")
            print("========================================")

            print(f"\nArchivos analizados..... {estadisticas['analizados']}")
            print(f"Archivos movidos........ {estadisticas['movidos']}")
            print(f"Archivos omitidos....... {estadisticas['omitidos']}")

            print("\n----------------------------------------\n")

            for categoria, cantidad in estadisticas["categorias"].items():
                print(f"{categoria:<24} {cantidad}")

            print("\n----------------------------------------")
            print("Proceso finalizado correctamente.")

    else:

        mostrar_error_ruta(carpeta)


def main():

    while True:

        print("=" * 40)
        print("        FILE ORGANIZER v2.0")
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

