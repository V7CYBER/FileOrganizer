from datetime import datetime
from pathlib import Path


def guardar_log(nombre_archivo, ruta_original, categoria):

    carpeta_logs = Path("logs")

    carpeta_logs.mkdir(exist_ok=True)

    archivo_log = carpeta_logs / "movimientos.log"

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(archivo_log, "a", encoding="utf-8") as log:

        log.write(
            f"[{fecha}] {nombre_archivo} | {ruta_original} | {categoria}\n"
)