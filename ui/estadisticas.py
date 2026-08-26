from core.estadisticas import (
    calcular_resumen_estadisticas,
    filtrar_historial,
    leer_estadisticas,
)


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
