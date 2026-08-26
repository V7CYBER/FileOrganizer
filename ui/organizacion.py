def mostrar_analisis_carpeta(datos):
    print("\n----------------------------------------")
    print(f"Ruta............... {datos['ruta']}")
    print(f"Archivos........... {datos['archivos']}")
    print(f"Subcarpetas........ {datos['carpetas']}")

    print("\nTipos de archivo encontrados:")

    if datos["extensiones"]:
        for extension, cantidad in sorted(
            datos["extensiones"].items()
        ):
            print(f"  {extension:<15} {cantidad}")

    else:
        print("  No se encontraron archivos.")


def mostrar_clasificacion(clasificacion):
    print("\n\nClasificación prevista:")

    if not clasificacion:
        print(
            "  No se encontraron archivos para organizar."
        )
        return False

    for nombre, categoria in clasificacion:
        print(
            f"  {nombre:<35} → {categoria}"
        )

    return True
