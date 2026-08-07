import hashlib


def calcular_sha256(ruta):

    sha256 = hashlib.sha256()

    with open(ruta, "rb") as archivo:

        while True:

            bloque = archivo.read(4096)

            if not bloque:
                break

            sha256.update(bloque)

    return sha256.hexdigest()
