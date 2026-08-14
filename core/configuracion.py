import json

from core.rutas import CONFIGURACION


def cargar_configuracion():

    with open(CONFIGURACION, "r", encoding="utf-8") as f:
        configuracion = json.load(f)

    if not validar_configuracion(configuracion):
        raise ValueError("La configuración de config.json no es válida.")

    return configuracion


def validar_configuracion(configuracion):

    if not isinstance(configuracion, dict):
        return False

    if "Sin_clasificar" not in configuracion:
        return False

    if "ignorar" not in configuracion:
        return False

    for nombre, valores in configuracion.items():

        if not isinstance(valores, list):
            return False

        if nombre == "ignorar":

            for carpeta in valores:

                if not isinstance(carpeta, str):
                    return False

        else:

            for extension in valores:

                if not isinstance(extension, str):
                    return False

                if extension and not extension.startswith("."):
                    return False

    return True


def obtener_carpetas_ignoradas(configuracion):

    return configuracion.get("ignorar", [])
