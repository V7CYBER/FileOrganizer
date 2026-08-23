import json
from pathlib import Path

from core.hash import calcular_sha256


def generar_snapshot(carpeta):
    ruta_base = Path(carpeta).resolve()
    if not ruta_base.exists():
        raise FileNotFoundError(f"No existe la ruta: {ruta_base}")

    if not ruta_base.is_dir():
        raise NotADirectoryError(f"La ruta no es un directorio: {ruta_base}")

    archivos = {}

    for archivo in ruta_base.rglob("*"):
        if archivo.is_symlink():
            continue

        if archivo.is_file():
            ruta_relativa = archivo.relative_to(ruta_base)

            try:
                archivos[str(ruta_relativa)] = calcular_sha256(archivo)

            except FileNotFoundError:
                continue

    return {
        "ruta_base": str(ruta_base),
        "archivos": archivos,
    }


def guardar_baseline(snapshot, ruta):
    destino = Path(ruta)

    if destino.exists():
        contador = 1

        while True:
            candidato = destino.with_name(f"{destino.stem}_{contador}{destino.suffix}")

            if not candidato.exists():
                destino = candidato
                break

            contador += 1

    destino.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        destino,
        "w",
        encoding="utf-8",
    ) as archivo:
        json.dump(
            snapshot,
            archivo,
            indent=4,
            ensure_ascii=False,
        )

    return destino


def cargar_baseline(ruta):
    archivo = Path(ruta)

    if not archivo.exists():
        raise FileNotFoundError(f"No existe la baseline: {archivo}")

    with open(
        archivo,
        "r",
        encoding="utf-8",
    ) as f:
        baseline = json.load(f)

    if "ruta_base" not in baseline:
        raise ValueError("La baseline no contiene 'ruta_base'.")

    if "archivos" not in baseline:
        raise ValueError("La baseline no contiene 'archivos'.")

    if not isinstance(baseline["ruta_base"], str):
        raise TypeError("'ruta_base' debe ser una cadena de texto.")

    if not baseline["ruta_base"].strip():
        raise ValueError("'ruta_base' no puede estar vacía.")

    if not Path(baseline["ruta_base"]).is_absolute():
        raise ValueError("'ruta_base' debe ser una ruta absoluta.")

    if not isinstance(baseline["archivos"], dict):
        raise TypeError("'archivos' debe ser un diccionario.")

    for hash_archivo in baseline["archivos"].values():
        if not isinstance(hash_archivo, str):
            raise TypeError("Los hashes de 'archivos' deben ser cadenas de texto.")

        if len(hash_archivo) != 64 or any(
            caracter not in "0123456789abcdef" for caracter in hash_archivo.lower()
        ):
            raise ValueError("Los hashes de 'archivos' deben ser SHA-256 válidos.")

    return baseline


def comparar_integridad(baseline, actual):
    if baseline["ruta_base"] != actual["ruta_base"]:
        raise ValueError(
            "La baseline y el snapshot actual " "pertenecen a rutas diferentes."
        )

    resultado = {
        "sin_cambios": [],
        "modificados": [],
        "nuevos": [],
        "eliminados": [],
    }

    for ruta, hash_anterior in baseline["archivos"].items():
        hash_actual = actual["archivos"].get(ruta)

        if hash_actual == hash_anterior:
            resultado["sin_cambios"].append(ruta)

        elif hash_actual is not None:
            resultado["modificados"].append(ruta)

        else:
            resultado["eliminados"].append(ruta)

    for ruta in actual["archivos"]:
        if ruta not in baseline["archivos"]:
            resultado["nuevos"].append(ruta)

    return resultado
