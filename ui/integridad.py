from pathlib import Path

from core.integridad import (
    cargar_baseline,
    comparar_integridad,
    generar_snapshot,
    guardar_baseline,
)


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
