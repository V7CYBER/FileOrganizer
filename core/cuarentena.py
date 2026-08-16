from datetime import datetime
from pathlib import Path
import shutil

from core.rutas import PROYECTO


CUARENTENA = PROYECTO / "quarantine"
REGISTRO_CUARENTENA = CUARENTENA / "alertas.log"


def generar_nombre_cuarentena(ruta_archivo):
    ruta = Path(ruta_archivo)

    contador = 1
    destino = CUARENTENA / ruta.name

    while destino.exists():
        destino = CUARENTENA / f"{ruta.stem}_{contador}{ruta.suffix}"
        contador += 1

    return destino


def poner_en_cuarentena(
    ruta_archivo,
    tipo_real,
    extension,
):
    ruta = Path(ruta_archivo)

    if not ruta.exists():
        raise FileNotFoundError(
            f"No existe el archivo: {ruta}"
        )

    CUARENTENA.mkdir(parents=True, exist_ok=True)

    destino = generar_nombre_cuarentena(ruta)

    shutil.move(str(ruta), str(destino))

    fecha = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        REGISTRO_CUARENTENA,
        "a",
        encoding="utf-8"
    ) as log:

        log.write(
            f"[{fecha}] "
            f"{ruta.name} | "
            f"Origen: {ruta.parent} | "
            f"Destino: {destino} | "
            f"Extensión: {extension} | "
            f"Tipo real: {tipo_real}\n"
        )

    return destino


def generar_alerta(
    ruta_archivo,
    tipo_real,
    extension,
):
    ruta = Path(ruta_archivo)

    return (
        "\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "        ⚠ ALERTA DE SEGURIDAD\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Archivo........: {ruta.name}\n"
        f"Extensión......: {extension}\n"
        f"Tipo real......: {tipo_real}\n"
        "Estado.........: SOSPECHOSO\n"
        "Acción.........: CUARENTENA\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
