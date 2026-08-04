#!/usr/bin/env python3

from pathlib import Path
from core.analizador import analizar_carpeta
from core.clasificador import clasificar_archivos
from core.movimientos import mover_archivos
from core.deshacer import deshacer_ultima_organizacion
from core.mensajes import mostrar_error, mostrar_error_ruta
from core.estadisticas import guardar_estadisticas, leer_estadisticas

def seleccionar_carpeta(simulacion=False):

    ruta = input("¿Qué carpeta quieres organizar? ").strip()

    carpeta = Path(ruta)

    if not carpeta.exists() or not carpeta.is_dir():
        mostrar_error_ruta(carpeta)
        return

    datos = analizar_carpeta(carpeta)

    print("\n----------------------------------------")
    print(f"Ruta............... {datos['ruta']}")
    print(f"Archivos........... {datos['archivos']}")
    print(f"Subcarpetas........ {datos['carpetas']}")

    print("\nTipos de archivo encontrados:")

    if datos["extensiones"]:
        for extension, cantidad in sorted(datos["extensiones"].items()):
            print(f"  {extension:<15} {cantidad}")
    else:
        print("  No se encontraron archivos.")

    clasificacion = clasificar_archivos(carpeta)

    print("\n\nClasificación prevista:")

    if clasificacion:
        for nombre, categoria in clasificacion:
            print(f"  {nombre:<35} → {categoria}")
    else:
        print("  No se encontraron archivos para organizar.")
        return

    confirmacion = input(
        "\n¿Desea continuar con la organización? (S/N): "
    ).strip().upper()

    if confirmacion != "S":
        print("\nOperación cancelada por el usuario.")
        print("----------------------------------------")
        return

    if simulacion:

        resumen = {}

        for _, categoria in clasificacion:
            resumen[categoria] = resumen.get(categoria, 0) + 1

        print("\n========================================")
        print("      RESUMEN SIMULACIÓN")
        print("========================================")

        print(f"\nArchivos analizados..... {len(clasificacion)}")

        print("\nSe moverían:\n")

        for categoria, cantidad in resumen.items():
            print(f"{categoria:<24} {cantidad}")

        print("\n----------------------------------------")
        print("No se ha movido ningún archivo.")
        print("----------------------------------------")

        return

    print("\nMoviendo archivos...\n")

    estadisticas = mover_archivos(clasificacion, carpeta)

    guardar_estadisticas(carpeta, estadisticas)

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

def mostrar_estadisticas():

    historial = leer_estadisticas()

    print("\n========================================")
    print("           ESTADÍSTICAS")
    print("========================================")

    if not historial:
        print("\nNo existen estadísticas guardadas.")
        print("----------------------------------------")
        return

    total_organizaciones = len(historial)

    total_analizados = 0
    total_movidos = 0
    total_omitidos = 0

    categorias = {}

    for registro in historial:

        total_analizados += registro["analizados"]
        total_movidos += registro["movidos"]
        total_omitidos += registro["omitidos"]

        for categoria, cantidad in registro["categorias"].items():
            categorias[categoria] = (
                categorias.get(categoria, 0) + cantidad
            )

    print(f"\nOrganizaciones........ {total_organizaciones}")
    print(f"Archivos analizados... {total_analizados}")
    print(f"Archivos movidos...... {total_movidos}")
    print(f"Archivos omitidos..... {total_omitidos}")

    print("\n----------------------------------------")
    print("Categorías\n")

    for categoria, cantidad in sorted(categorias.items()):
        print(f"{categoria:<24} {cantidad}")

    print("\n----------------------------------------")

def main():

    while True:

        print("=" * 40)
        print("        FILE ORGANIZER v2.4")
        print("=" * 40)
        print("1) Organizar carpeta")
        print("2) Modo simulación")
        print("3) Deshacer última organización")
        print("4) Ver estadisticas")
        print("5) Salir")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
           seleccionar_carpeta()

        elif opcion == "2":
                
            seleccionar_carpeta(simulacion=True)


        elif opcion == "3":
             
             deshacer_ultima_organizacion()


        elif opcion == "4":
            
           mostrar_estadisticas()


        elif opcion == "5":

            print("\n¡Hasta la próxima!")
            break

        else:

            print("\n✗ Opción no válida.\n")



if __name__ == "__main__":
     main()        

