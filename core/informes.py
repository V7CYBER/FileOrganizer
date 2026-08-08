from pathlib import Path
from datetime import datetime


def generar_informe_duplicados(carpeta, duplicados):

    carpeta_reports = Path("reports")
    carpeta_reports.mkdir(exist_ok=True)

    fecha = datetime.now()

    nombre_archivo = (
        f"duplicados_{fecha.strftime('%Y%m%d_%H%M%S')}.txt"
    )

    ruta_informe = carpeta_reports / nombre_archivo
    lineas = []

    lineas.append("=" * 60)
    lineas.append("           FILE ORGANIZER — INFORME")
    lineas.append("=" * 60)
    lineas.append("")
    lineas.append("Tipo de análisis..... Duplicados por contenido (SHA-256)")
    lineas.append(f"Fecha................ {fecha.strftime('%d/%m/%Y %H:%M:%S')}")
    lineas.append(f"Carpeta analizada.... {Path(carpeta).resolve()}")
    lineas.append("")
    lineas.append("-" * 60)
    lineas.append("RESUMEN")
    lineas.append("-" * 60)
    lineas.append("")
    lineas.append(f"Grupos encontrados.... {len(duplicados)}")

    contador = 1

    for hash_archivo, lista in duplicados.items():

        lineas.append("")
        lineas.append("-" * 60)
        lineas.append(f"GRUPO {contador}")
        lineas.append("-" * 60)
        lineas.append("")
        lineas.append(f"SHA-256: {hash_archivo}")
        lineas.append(f"Archivos encontrados: {len(lista)}")
        lineas.append("")

        for numero, archivo in enumerate(lista, start=1):

            fecha_archivo = datetime.fromtimestamp(
                archivo["fecha"]
            ).strftime("%d/%m/%Y %H:%M:%S")

            lineas.append(f"{numero}. {archivo['nombre']}")
            lineas.append(f"   Ruta: {archivo['ruta']}")
            lineas.append(f"   Tamaño: {archivo['tamano']} bytes")
            lineas.append(
                f"   Modificado: {fecha_archivo}"
            )
            lineas.append("")

        contador += 1

    with ruta_informe.open("w", encoding="utf-8") as archivo:

        archivo.write("\n".join(lineas))

    return ruta_informe
