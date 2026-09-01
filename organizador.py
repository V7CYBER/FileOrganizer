#!/usr/bin/env python3

from core.deshacer import deshacer_ultima_organizacion
from ui.auditoria import mostrar_auditoria_seguridad
from ui.duplicados import mostrar_duplicados, mostrar_duplicados_hash
from ui.estadisticas import mostrar_estadisticas, mostrar_historial
from ui.integridad import crear_baseline_integridad, verificar_integridad
from ui.logs import mostrar_analisis_logs
from ui.organizacion import seleccionar_carpeta


def main():

    while True:

        print("=" * 40)
        print("        FILE ORGANIZER v3.7")
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
