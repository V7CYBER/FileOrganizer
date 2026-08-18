from datetime import datetime, timezone

from core.rutas import ARCHIVO_LOG_MOVIMIENTOS, LOGS


def guardar_log(nombre_archivo, ruta_original, categoria):

    LOGS.mkdir(exist_ok=True)

    fecha = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S")

    with open(ARCHIVO_LOG_MOVIMIENTOS, "a", encoding="utf-8") as log:

        log.write(
            f"[{fecha}] {nombre_archivo} | {ruta_original} | {categoria}\n"
        )
