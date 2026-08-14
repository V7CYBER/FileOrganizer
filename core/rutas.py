from pathlib import Path


PROYECTO = Path(__file__).resolve().parent.parent

CONFIGURACION = PROYECTO / "config.json"

LOGS = PROYECTO / "logs"

ARCHIVO_LOG_MOVIMIENTOS = LOGS / "movimientos.log"
