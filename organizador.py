#!/usr/bin/env python3

from pathlib import Path
from core.analizador import analizar_carpeta
from core.clasificador import clasificar_archivos
from core.movimientos import mover_archivos
from core.deshacer import deshacer_ultima_organizacion
from core.mensajes import mostrar_error, mostrar_error_ruta
from core.duplicados import buscar_duplicados
from core.duplicados_hash import buscar_duplicados_hash
from datetime import datetime
from core.estadisticas import (
    guardar_estadisticas,
    leer_estadisticas,
    calcular_resumen_estadisticas,
    filtrar_historial
)

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

    resumen = calcular_resumen_estadisticas(historial)

    print(f"\nOrganizaciones........ {resumen['organizaciones']}")
    print(f"Archivos analizados... {resumen['analizados']}")
    print(f"Archivos movidos...... {resumen['movidos']}")
    print(f"Archivos omitidos..... {resumen['omitidos']}")

    print("\n----------------------------------------")
    print("Categorías acumuladas\n")

    for categoria, cantidad in sorted(
        resumen["categorias"].items()
    ):
        print(f"{categoria:<24} {cantidad}")

    ultima = resumen["ultima_operacion"]

    print("\n----------------------------------------")
    print("ÚLTIMA OPERACIÓN")
    print("----------------------------------------")

    print(f"\nFecha................ {ultima['fecha']}")
    print(f"Ruta................. {ultima['ruta']}")
    print(f"Archivos analizados.. {ultima['analizados']}")
    print(f"Archivos movidos..... {ultima['movidos']}")
    print(f"Archivos omitidos.... {ultima['omitidos']}")

    print("\nCategorías\n")

    for categoria, cantidad in sorted(
        ultima["categorias"].items()
    ):
        print(f"{categoria:<24} {cantidad}")

    print("\n----------------------------------------")

def mostrar_historial():

    historial = leer_estadisticas()

    while True:

        print("\n========================================")
        print("       HISTORIAL DE ORGANIZACIONES")
        print("========================================")
        print("1) Mostrar todo el historial")
        print("2) Filtrar por ruta")
        print("3) Volver")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":

            resultados = filtrar_historial(historial)

        elif opcion == "2":

            ruta = input("\nIntroduzca la ruta a buscar: ").strip()
            resultados = filtrar_historial(historial, ruta)

        elif opcion == "3":

            return

        else:

            print("\n✗ Opción no válida.\n")
            continue

        print("\n========================================")
        print("       RESULTADOS DEL HISTORIAL")
        print("========================================")

        if not resultados:

            print("\nNo se encontraron organizaciones.")
            print("----------------------------------------")
            continue

        print(f"\nOrganizaciones encontradas: {len(resultados)}")

        for numero, registro in enumerate(resultados, start=1):

            print(f"\nOrganización #{numero}")
            print("----------------------------------------")

            print(f"Fecha................ {registro.get('fecha', 'N/D')}")
            print(f"Ruta................. {registro.get('ruta', 'N/D')}")
            print(f"Archivos analizados.. {registro.get('analizados', 0)}")
            print(f"Archivos movidos..... {registro.get('movidos', 0)}")
            print(f"Archivos omitidos.... {registro.get('omitidos', 0)}")

            print("\nCategorías\n")

            for categoria, cantidad in sorted(
                registro.get("categorias", {}).items()
            ):
                print(f"{categoria:<24} {cantidad}")

            print("\n----------------------------------------")

def mostrar_duplicados_hash():

    ruta = input("¿Qué carpeta quieres analizar? ").strip()

    duplicados = buscar_duplicados_hash(ruta)

    print("\n========================================")
    print(" DUPLICADOS POR CONTENIDO (SHA-256)")
    print("========================================")

    print(f"\nGrupos encontrados..... {len(duplicados)}")

    if not duplicados:

        print("\nNo se encontraron archivos duplicados.")
        print("----------------------------------------")
        return

    contador = 1

    for hash_archivo, lista in duplicados.items():

        print(f"\nGrupo {contador}\n")
        if hash_archivo == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855":

            print("⚠ Archivos vacíos")

        else:

            print("Hash")
            print(f"{hash_archivo[:16]}...")

        print(f"Archivos encontrados: {len(lista)}")
        print("\nArchivos\n")

        for archivo in lista:

            fecha = datetime.fromtimestamp(
                archivo["fecha"]
            ).strftime("%d/%m/%Y %H:%M:%S")

            print(f"Nombre               : {archivo['nombre']}")
            print(f"Ruta                 : {archivo['ruta']}")
            print(f"Tamaño               : {archivo['tamano']} bytes")
            print(f"Última modificación  : {fecha}")
            print()

            print("----------------------------------------")

            
        contador += 1

def mostrar_duplicados():

    ruta = input("¿Qué carpeta quieres analizar? ").strip()

    carpeta = Path(ruta)

    if not carpeta.exists() or not carpeta.is_dir():
        mostrar_error_ruta(carpeta)
        return

    duplicados = buscar_duplicados(carpeta)

    print("\n========================================")
    print("      ARCHIVOS DUPLICADOS")
    print("========================================")

    print(f"\nGrupos encontrados..... {len(duplicados)}")

    if not duplicados:
        print("\nNo se encontraron archivos duplicados.")
        print("----------------------------------------")
        return

    for nombre, lista in duplicados.items():

        print(f"\n{nombre}")

        for archivo in lista:
            print(f"   {archivo}")

        print("----------------------------------------")

def main():

    while True:

        print("=" * 40)
        print("        FILE ORGANIZER v2.12")
        print("=" * 40)
        print("1) Organizar carpeta")
        print("2) Modo simulación")
        print("3) Deshacer última organización")
        print("4) Ver estadisticas")
        print("5) Buscar archivos duplicados por nombre")
        print("6) Buscar archivos duplicados por contenido (SHA-256)")
        print("7) Ver historial de organizaciones")
        print("8) Salir")

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

            mostrar_duplicados()  

        elif opcion == "6":

            mostrar_duplicados_hash() 

        elif opcion == "7":

            mostrar_historial()

        elif opcion == "8":

            print("\n¡Hasta la próxima!")
            break

        else:

            print("\n✗ Opción no válida.\n")



if __name__ == "__main__":
     main()        

