from datetime import datetime, timezone
from pathlib import Path


def generar_informe_duplicados(carpeta, duplicados):

    carpeta_reports = Path("reports")
    carpeta_reports.mkdir(exist_ok=True)

    fecha = datetime.now(timezone.utc).astimezone()

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
    total_archivos = 0
    espacio_duplicados = 0
    espacio_recuperable = 0
    grupos_vacios = 0

    for hash_archivo, lista in duplicados.items():

        total_archivos += len(lista)

        tamano_grupo = sum(
            archivo["tamano"]
            for archivo in lista
        )

        espacio_duplicados += tamano_grupo

        if lista[0]["tamano"] == 0:
            grupos_vacios += 1
        else:
            espacio_recuperable += (
                tamano_grupo - lista[0]["tamano"]
            )

    lineas.append(
        f"Archivos duplicados.... {total_archivos}"
    )

    lineas.append(
        f"Espacio ocupado....... {espacio_duplicados} bytes"
    )

    lineas.append(
        f"Espacio recuperable... {espacio_recuperable} bytes"
    )

    lineas.append(
        f"Grupos de vacíos...... {grupos_vacios}"
    )
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
                archivo["fecha"],
                tz=timezone.utc,
            ).astimezone().strftime("%d/%m/%Y %H:%M:%S")

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
