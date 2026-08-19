from pathlib import Path

from core.hash import calcular_sha256


def generar_snapshot(carpeta):
    ruta_base = Path(carpeta)

    if not ruta_base.exists():
        raise FileNotFoundError(f"No existe la ruta: {ruta_base}")

    if not ruta_base.is_dir():
        raise NotADirectoryError(f"La ruta no es un directorio: {ruta_base}")

    archivos = {}

    for archivo in ruta_base.rglob("*"):
        if archivo.is_file():
            ruta_relativa = archivo.relative_to(ruta_base)

            archivos[str(ruta_relativa)] = calcular_sha256(archivo)

    return {
        "ruta_base": str(ruta_base),
        "archivos": archivos,
    }
