#!/usr/bin/env python3

from pathlib import Path

from core.analizador import analizar_carpeta
from core.clasificador import clasificar_archivos
from core.cuarentena import generar_alerta, poner_en_cuarentena
from core.deshacer import deshacer_ultima_organizacion
from core.estadisticas import guardar_estadisticas
from core.mensajes import mostrar_error_ruta
from core.movimientos import mover_archivos
from core.seguridad import obtener_sospechosos, verificar_archivos
from ui.auditoria import mostrar_auditoria_seguridad
from ui.duplicados import mostrar_duplicados, mostrar_duplicados_hash
from ui.estadisticas import mostrar_estadisticas, mostrar_historial
from ui.integridad import crear_baseline_integridad, verificar_integridad
from ui.logs import mostrar_analisis_logs
from ui.organizacion import mostrar_analisis_carpeta, mostrar_clasificacion


def mostrar_alertas_seguridad(sospechosos, simulacion=False):

    if not sospechosos:
        return

    print("\n========================================")
    print("       ⚠ ALERTAS DE SEGURIDAD")
    print("========================================")

    for resultado in sospechosos:

        print(
            generar_alerta(
                resultado["archivo"],
                resultado["tipo_real"],
                resultado["extension"],
            )
        )

    if simulacion:

        print("\nModo simulación:")
        print("Los archivos sospechosos NO serán enviados " "a cuarentena.")

    print("\n========================================")


def enviar_sospechosos_cuarentena(sospechosos):

    if not sospechosos:
        return

    print("\nEnviando archivos sospechosos " "a cuarentena...")

    for resultado in sospechosos:

        destino = poner_en_cuarentena(
            resultado["archivo"],
            resultado["tipo_real"],
            resultado["extension"],
        )

        print(f"✓ {resultado['archivo'].name} → " f"{destino}")

    print("\n========================================")


def seleccionar_carpeta(simulacion=False):

    ruta = input("¿Qué carpeta quieres organizar? ").strip()

    carpeta = Path(ruta)

    if not carpeta.exists() or not carpeta.is_dir():
        mostrar_error_ruta(carpeta)
        return

    datos = analizar_carpeta(carpeta)

    resultados_seguridad = verificar_archivos(carpeta)
    sospechosos = obtener_sospechosos(resultados_seguridad)

    mostrar_alertas_seguridad(
        sospechosos,
        simulacion=simulacion,
    )

    mostrar_analisis_carpeta(datos)

    clasificacion = clasificar_archivos(carpeta)

    if not mostrar_clasificacion(clasificacion):
        return

    confirmacion = (
        input("\n¿Desea continuar con la organización? (S/N): ").strip().upper()
    )

    if confirmacion != "S":

        print("\nOperación cancelada por el usuario.")
        print("----------------------------------------")
        return

    # La cuarentena solamente se ejecuta después
    # de la confirmación del usuario.
    if sospechosos and not simulacion:

        enviar_sospechosos_cuarentena(sospechosos)

    if simulacion:

        resumen = {}

        for _, categoria in clasificacion:
            resumen[categoria] = resumen.get(categoria, 0) + 1

        print("\n========================================")
        print("      RESUMEN SIMULACIÓN")
        print("========================================")

        print(f"\nArchivos analizados..... " f"{len(clasificacion)}")

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

    print(f"\nArchivos analizados..... " f"{estadisticas['analizados']}")

    print(f"Archivos movidos........ " f"{estadisticas['movidos']}")

    print(f"Archivos omitidos....... " f"{estadisticas['omitidos']}")

    print("\n----------------------------------------\n")

    for categoria, cantidad in estadisticas["categorias"].items():
        print(f"{categoria:<24} {cantidad}")

    print("\n----------------------------------------")
    print("Proceso finalizado correctamente.")


def main():

    while True:

        print("=" * 40)
        print("        FILE ORGANIZER v3.4")
        print("=" * 40)
        print("1) Organizar carpeta")
        print("2) Modo simulación")
        print("3) Deshacer última organización")
        print("4) Ver estadisticas")
        print("5) Buscar archivos duplicados por nombre")
        print("6) Buscar archivos duplicados por contenido (SHA-256)")
        print("7) Ver historial de organizaciones")
        print("8) Analizar archivo de logs")
        print("9) Crear baseline de integridad")
        print("10) Verificar integridad")
        print("11) Ejecutar auditoría de seguridad")
        print("12) Salir")

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

            mostrar_analisis_logs()

        elif opcion == "9":

            crear_baseline_integridad()

        elif opcion == "10":

            verificar_integridad()

        elif opcion == "11":

            carpeta = input("\nCarpeta a auditar: ").strip()
            mostrar_auditoria_seguridad(carpeta)

        elif opcion == "12":

            print("\n¡Hasta la próxima!")
            break

        else:

            print("\n✗ Opción no válida.\n")


if __name__ == "__main__":
    main()
