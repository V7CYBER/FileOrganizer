from pathlib import Path

from core.analizador import analizar_carpeta
from core.clasificador import clasificar_archivos
from core.cuarentena import generar_alerta, poner_en_cuarentena
from core.estadisticas import guardar_estadisticas
from core.mensajes import mostrar_error_ruta
from core.movimientos import mover_archivos
from core.seguridad import obtener_sospechosos, verificar_archivos


def mostrar_analisis_carpeta(datos):
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


def mostrar_clasificacion(clasificacion):
    print("\n\nClasificación prevista:")

    if not clasificacion:
        print("  No se encontraron archivos para organizar.")
        return False

    for nombre, categoria in clasificacion:
        print(f"  {nombre:<35} → {categoria}")

    return True


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

    estadisticas = mover_archivos(
        clasificacion,
        carpeta,
    )

    guardar_estadisticas(
        carpeta,
        estadisticas,
    )

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
