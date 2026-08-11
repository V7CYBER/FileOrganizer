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

def calcular_resumen_estadisticas(historial):

    if not historial:
        return {
            "organizaciones": 0,
            "analizados": 0,
            "movidos": 0,
            "omitidos": 0,
            "categorias": {},
            "ultima_operacion": None
        }

    total_analizados = 0
    total_movidos = 0
    total_omitidos = 0
    categorias = {}

    for registro in historial:

        total_analizados += registro.get("analizados", 0)
        total_movidos += registro.get("movidos", 0)
        total_omitidos += registro.get("omitidos", 0)

        for categoria, cantidad in registro.get("categorias", {}).items():
            categorias[categoria] = (
                categorias.get(categoria, 0) + cantidad
            )

    return {
        "organizaciones": len(historial),
        "analizados": total_analizados,
        "movidos": total_movidos,
        "omitidos": total_omitidos,
        "categorias": categorias,
        "ultima_operacion": historial[-1]
    }
