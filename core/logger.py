from datetime import datetime

from core.rutas import LOGS, ARCHIVO_LOG_MOVIMIENTOS


def guardar_log(nombre_archivo, ruta_original, categoria):

    LOGS.mkdir(exist_ok=True)

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(ARCHIVO_LOG_MOVIMIENTOS, "a", encoding="utf-8") as log:

        log.write(
            f"[{fecha}] {nombre_archivo} | {ruta_original} | {categoria}\n"
        )
