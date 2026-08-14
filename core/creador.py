from pathlib import Path

from core.configuracion import cargar_configuracion


def crear_carpetas(ruta):

    carpeta = Path(ruta)
    configuracion = cargar_configuracion()

    categorias = [
        nombre
        for nombre in configuracion
        if nombre != "ignorar"
    ]

    for nombre in categorias:

        destino = carpeta / nombre

        if not destino.exists():
            destino.mkdir()
            print(f"✓ Creada carpeta: {nombre}")

        else:
            print(f"• Ya existe: {nombre}")
