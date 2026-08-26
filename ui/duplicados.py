from datetime import datetime, timezone
from pathlib import Path

from core.duplicados import buscar_duplicados
from core.duplicados_hash import buscar_duplicados_hash
from core.mensajes import mostrar_error_ruta


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
            == "e3b0c44298fc1c149afbf4c8996fb924"
            "27ae41e4649b934ca495991b7852b855"
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
