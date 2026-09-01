from pathlib import Path

from core.analizador_logs import (
    analizar_log,
    detectar_fuerza_bruta_temporal,
    generar_resumen_logs,
)


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
                f"\nRegla........ {evento['regla']}"
                f"\nDescripción.. {evento['descripcion']}"
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
