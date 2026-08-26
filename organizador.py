#!/usr/bin/env python3

from datetime import datetime, timezone
from pathlib import Path

from core.analizador import analizar_carpeta
from core.analizador_logs import (
    analizar_log,
    detectar_fuerza_bruta_temporal,
    generar_resumen_logs,
)
from core.auditoria import ejecutar_auditoria, guardar_informe_auditoria
from core.clasificador import clasificar_archivos
from core.cuarentena import generar_alerta, poner_en_cuarentena
from core.deshacer import deshacer_ultima_organizacion
from core.duplicados import buscar_duplicados
from core.duplicados_hash import buscar_duplicados_hash
from core.estadisticas import (
    guardar_estadisticas,
)
from core.integridad import (
    cargar_baseline,
    comparar_integridad,
    generar_snapshot,
    guardar_baseline,
)
from core.mensajes import mostrar_error_ruta
from core.movimientos import mover_archivos
from core.seguridad import obtener_sospechosos, verificar_archivos
from ui.estadisticas import mostrar_estadisticas, mostrar_historial
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
        if (
            hash_archivo
            == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        ):

            print("⚠ Archivos vacíos")

        else:

            print("Hash")
            print(f"{hash_archivo[:16]}...")

        print(f"Archivos encontrados: {len(lista)}")
        print("\nArchivos\n")

        for archivo in lista:

            fecha = (
                datetime.fromtimestamp(
                    archivo["fecha"],
                    tz=timezone.utc,
                )
                .astimezone()
                .strftime("%d/%m/%Y %H:%M:%S")
            )

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


def mostrar_analisis_logs():

    ruta = input("¿Qué archivo de log quieres analizar? ").strip()

    archivo = Path(ruta)

    if not archivo.exists() or not archivo.is_file():
        print("\n✗ El archivo indicado no existe o no es válido.")
        return

    try:

        eventos = analizar_log(archivo)

    except (PermissionError, OSError) as error:

        print(f"\n✗ No se pudo analizar el archivo: {error}")
        return

    resumen = generar_resumen_logs(eventos)

    alertas_fuerza_bruta = detectar_fuerza_bruta_temporal(
        eventos,
        umbral=3,
        ventana_segundos=60,
    )

    print("\n========================================")
    print("       ANÁLISIS DE SEGURIDAD")
    print("========================================")

    print(f"\nArchivo.............. {archivo}")
    print(f"Eventos detectados... {resumen['eventos']}")
    print(f"SQL Injection........ {resumen['sql_injection']}")
    print(f"Fuerza bruta......... {resumen['fuerza_bruta']}")
    print(f"Severidad ALTA....... {resumen['alta']}")
    print(f"Severidad MEDIA...... {resumen['media']}")

    if eventos:

        print("\n===== EVENTOS DETECTADOS =====")

        for evento in eventos:

            ip = evento["ip"] or "N/D"

            print(
                f"\nLínea........ {evento['linea']}"
                f"\nIP........... {ip}"
                f"\nTipo......... {evento['tipo']}"
                f"\nSeveridad.... {evento['severidad']}"
                f"\nContenido.... {evento['contenido']}"
            )

    else:

        print("\nNo se detectaron eventos de seguridad.")

    if alertas_fuerza_bruta:

        print("\n========================================")
        print("       ⚠ ALERTAS CORRELACIONADAS")
        print("========================================")

        for alerta in alertas_fuerza_bruta:

            print(
                f"\nIP.............. {alerta['ip']}"
                f"\nTipo............ {alerta['tipo']}"
                f"\nSeveridad....... {alerta['severidad']}"
                f"\nIntentos........ {alerta['intentos']}"
                f"\nVentana......... "
                f"{alerta['ventana_segundos']} segundos"
                f"\nLíneas.......... {alerta['lineas']}"
            )

    print("\n----------------------------------------")
    print("Análisis finalizado.")


def crear_baseline_integridad():
    print("\n========================================")
    print("       CREAR BASELINE DE INTEGRIDAD")
    print("========================================")

    ruta = input("\nCarpeta a vigilar: ").strip()

    try:
        snapshot = generar_snapshot(ruta)

        destino = Path("baselines") / "baseline.json"

        archivo_guardado = guardar_baseline(
            snapshot,
            destino,
        )

    except (FileNotFoundError, NotADirectoryError) as error:
        print(f"\n✗ {error}")
        return

    print("\n✓ Baseline creada correctamente.")
    print(f"Ruta: {archivo_guardado}")
    print(f"Archivos registrados: " f"{len(snapshot['archivos'])}")


def verificar_integridad():
    print("\n========================================")
    print("       VERIFICAR INTEGRIDAD")
    print("========================================")

    ruta_baseline = input("\nRuta de la baseline: ").strip()

    try:
        baseline = cargar_baseline(ruta_baseline)

        snapshot_actual = generar_snapshot(baseline["ruta_base"])

        resultado = comparar_integridad(
            baseline,
            snapshot_actual,
        )

    except (
        FileNotFoundError,
        NotADirectoryError,
        ValueError,
        TypeError,
    ) as error:
        print(f"\n✗ {error}")
        return

    print("\n===== RESULTADO DE INTEGRIDAD =====")
    print(f"Sin cambios : {len(resultado['sin_cambios'])}")
    print(f"Modificados : {len(resultado['modificados'])}")
    print(f"Nuevos      : {len(resultado['nuevos'])}")
    print(f"Eliminados  : {len(resultado['eliminados'])}")


def mostrar_auditoria_seguridad(carpeta):
    print("\n========================================")
    print("       AUDITORÍA DE SEGURIDAD")
    print("========================================")

    ruta_baseline = input("\nRuta de la baseline: ").strip()

    try:
        resultado = ejecutar_auditoria(
            carpeta,
            ruta_baseline,
        )

        destino = Path("reports") / "auditoria.txt"

        archivo_guardado = guardar_informe_auditoria(
            resultado["informe"],
            destino,
        )

    except (
        FileNotFoundError,
        NotADirectoryError,
        ValueError,
        TypeError,
    ) as error:
        print(f"\n✗ {error}")
        return

    print()
    print(resultado["informe"])
    print(f"\nInforme guardado en: {archivo_guardado}")


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
