from pathlib import Path


MAGIC_NUMBERS = {
    b"\xFF\xD8\xFF": "JPEG",
    b"\x89PNG": "PNG",
    b"GIF8": "GIF",
    b"%PDF": "PDF",
    b"PK\x03\x04": "ZIP",
    b"\x1F\x8B": "GZIP",
    b"\x7FELF": "ELF",
    b"MZ": "PE/Windows executable",
}


def identificar_tipo_real(ruta_archivo):
    ruta = Path(ruta_archivo)

    with open(ruta, "rb") as archivo:
        cabecera = archivo.read(8)

    for firma, tipo in MAGIC_NUMBERS.items():

        if cabecera.startswith(firma):
            return tipo

    return "Desconocido"
