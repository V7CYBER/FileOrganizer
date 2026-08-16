from pathlib import Path

from core.magic_numbers import identificar_tipo_real


EXTENSIONES_ESPERADAS = {
    ".jpg": {"JPEG"},
    ".jpeg": {"JPEG"},
    ".png": {"PNG"},
    ".gif": {"GIF"},
    ".pdf": {"PDF"},
    ".zip": {"ZIP"},
    ".gz": {"GZIP"},
    ".exe": {"PE/Windows executable"},
    ".dll": {"PE/Windows executable"},
    ".bin": {"ELF"},
}


def verificar_archivo(ruta_archivo):
    ruta = Path(ruta_archivo)

    extension = ruta.suffix.lower()
    tipo_real = identificar_tipo_real(ruta)

    tipos_esperados = EXTENSIONES_ESPERADAS.get(extension)

    if tipos_esperados is None:
        return {
            "archivo": ruta,
            "extension": extension,
            "tipo_real": tipo_real,
            "estado": "NO_VERIFICADO",
        }

    if tipo_real in tipos_esperados:
        estado = "OK"
    else:
        estado = "SOSPECHOSO"

    return {
        "archivo": ruta,
        "extension": extension,
        "tipo_real": tipo_real,
        "estado": estado,
    }
