from pathlib import Path
import json
from datetime import datetime


def guardar_estadisticas(ruta, estadisticas):

    archivo = (
        Path(__file__).resolve().parent.parent
        / "stats"
        / "estadisticas.json"
    )

    if archivo.exists():
        with open(archivo, "r", encoding="utf-8") as f:
            historial = json.load(f)
    else:
        historial = []

    registro = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ruta": str(ruta),
        "analizados": estadisticas["analizados"],
        "movidos": estadisticas["movidos"],
        "omitidos": estadisticas["omitidos"],
        "categorias": estadisticas["categorias"]
    }

    historial.append(registro)

    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(historial, f, indent=4, ensure_ascii=False)


def leer_estadisticas():

    archivo = (
        Path(__file__).resolve().parent.parent
        / "stats"
        / "estadisticas.json"
    )

    if not archivo.exists():
        return []

    with open(archivo, "r", encoding="utf-8") as f:
        return json.load(f)

