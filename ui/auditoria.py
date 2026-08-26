from pathlib import Path

from core.auditoria import ejecutar_auditoria, guardar_informe_auditoria


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
