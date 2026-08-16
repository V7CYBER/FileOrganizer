from pathlib import Path
import re


PATRONES_SEGURIDAD = {
    "SQL_INJECTION": [
        re.compile(r"\bunion\s+select\b", re.IGNORECASE),
        re.compile(r"\bor\s+1\s*=\s*1\b", re.IGNORECASE),
        re.compile(r"\band\s+1\s*=\s*1\b", re.IGNORECASE),
        re.compile(r"\bor\s+'[^']*'\s*=\s*'[^']*'\b", re.IGNORECASE),
        re.compile(r"\bsleep\s*\(\s*\d+\s*\)", re.IGNORECASE),
        re.compile(r"\bbenchmark\s*\(", re.IGNORECASE),
        re.compile(r"\bdrop\s+table\b", re.IGNORECASE),
        re.compile(r"\binformation_schema\b", re.IGNORECASE),
    ],

    "FUERZA_BRUTA": [
        re.compile(r"\bfailed\s+password\b", re.IGNORECASE),
        re.compile(r"\bfailed\s+login\b", re.IGNORECASE),
        re.compile(r"\bauthentication\s+failure\b", re.IGNORECASE),
        re.compile(r"\binvalid\s+user\b", re.IGNORECASE),
        re.compile(r"\bmaximum\s+authentication\s+attempts\b", re.IGNORECASE),
        re.compile(r"\btoo\s+many\s+authentication\s+failures\b", re.IGNORECASE),
    ],
}


SEVERIDADES = {
    "SQL_INJECTION": "ALTA",
    "FUERZA_BRUTA": "MEDIA",
}


PATRON_IP = re.compile(
    r"\b(?:"
    r"(?:25[0-5]|2[0-4]\d|1?\d?\d)\."
    r"){3}"
    r"(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"
)


def extraer_ip(linea):
    """
    Extrae la primera dirección IPv4 válida
    encontrada en una línea de log.
    """

    coincidencia = PATRON_IP.search(linea)

    if coincidencia:
        return coincidencia.group()

    return None


def analizar_linea(linea, numero_linea):
    """
    Analiza una línea de log y devuelve los eventos
    de seguridad detectados.
    """

    eventos = []

    for tipo, patrones in PATRONES_SEGURIDAD.items():

        for patron in patrones:

            if patron.search(linea):

                eventos.append({
                    "linea": numero_linea,
                    "ip": extraer_ip(linea),
                    "tipo": tipo,
                    "severidad": SEVERIDADES[tipo],
                    "contenido": linea.rstrip("\n"),
                })

                break

    return eventos


def analizar_log(ruta_archivo):
    """
    Analiza un archivo de texto línea por línea.
    """

    ruta = Path(ruta_archivo)

    if not ruta.exists():
        raise FileNotFoundError(
            f"No existe el archivo: {ruta}"
        )

    if not ruta.is_file():
        raise ValueError(
            f"La ruta no es un archivo: {ruta}"
        )

    eventos = []

    with open(
        ruta,
        "r",
        encoding="utf-8",
        errors="replace",
    ) as archivo:

        for numero_linea, linea in enumerate(
            archivo,
            start=1,
        ):

            eventos.extend(
                analizar_linea(
                    linea,
                    numero_linea,
                )
            )

    return eventos


def generar_resumen_logs(eventos):
    """
    Genera un resumen de los eventos detectados.
    """

    resumen = {
        "eventos": len(eventos),
        "sql_injection": 0,
        "fuerza_bruta": 0,
        "alta": 0,
        "media": 0,
    }

    for evento in eventos:

        if evento["tipo"] == "SQL_INJECTION":
            resumen["sql_injection"] += 1

        elif evento["tipo"] == "FUERZA_BRUTA":
            resumen["fuerza_bruta"] += 1

        if evento["severidad"] == "ALTA":
            resumen["alta"] += 1

        elif evento["severidad"] == "MEDIA":
            resumen["media"] += 1

    return resumen


def agrupar_eventos_por_ip(eventos):
    """
    Agrupa eventos de seguridad por dirección IP.
    """

    agrupados = {}

    for evento in eventos:

        ip = evento.get("ip")

        if ip is None:
            continue

        if ip not in agrupados:
            agrupados[ip] = []

        agrupados[ip].append(evento)

    return agrupados


def detectar_fuerza_bruta_por_ip(eventos, umbral=3):
    """
    Detecta posibles ataques de fuerza bruta cuando
    una misma IP genera varios eventos de autenticación fallida.
    """

    agrupados = agrupar_eventos_por_ip(eventos)

    alertas = []

    for ip, eventos_ip in agrupados.items():

        intentos = [
            evento
            for evento in eventos_ip
            if evento["tipo"] == "FUERZA_BRUTA"
        ]

        if len(intentos) >= umbral:

            alertas.append({
                "ip": ip,
                "tipo": "POSIBLE_FUERZA_BRUTA",
                "severidad": "ALTA",
                "intentos": len(intentos),
                "lineas": [
                    evento["linea"]
                    for evento in intentos
                ],
            })

    return alertas


PATRON_FECHA_LOG = re.compile(
    r"\[(\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2})\]"
)


def extraer_fecha_log(linea):
    """
    Extrae la fecha y hora de una línea de log
    con formato tipo Apache.
    """

    coincidencia = PATRON_FECHA_LOG.search(linea)

    if coincidencia:
        return coincidencia.group(1)

    return None


from datetime import datetime


def convertir_fecha_log(fecha_texto):
    """
    Convierte una fecha de log Apache en datetime.
    """

    if fecha_texto is None:
        return None

    return datetime.strptime(
        fecha_texto,
        "%d/%b/%Y:%H:%M:%S",
    )


def detectar_fuerza_bruta_temporal(
    eventos,
    umbral=3,
    ventana_segundos=60,
):
    """
    Detecta posibles ataques de fuerza bruta
    correlacionando IP, número de intentos y tiempo.
    """

    agrupados = agrupar_eventos_por_ip(eventos)

    alertas = []

    for ip, eventos_ip in agrupados.items():

        intentos = []

        for evento in eventos_ip:

            if evento["tipo"] != "FUERZA_BRUTA":
                continue

            fecha_texto = extraer_fecha_log(
                evento["contenido"]
            )

            fecha = convertir_fecha_log(
                fecha_texto
            )

            if fecha is None:
                continue

            intentos.append({
                "fecha": fecha,
                "linea": evento["linea"],
            })

        intentos.sort(
            key=lambda intento: intento["fecha"]
        )

        for indice in range(
            len(intentos) - umbral + 1
        ):

            ventana = intentos[
                indice:indice + umbral
            ]

            diferencia = (
                ventana[-1]["fecha"]
                - ventana[0]["fecha"]
            ).total_seconds()

            if diferencia <= ventana_segundos:

                alertas.append({
                    "ip": ip,
                    "tipo": "POSIBLE_FUERZA_BRUTA",
                    "severidad": "ALTA",
                    "intentos": umbral,
                    "ventana_segundos": diferencia,
                    "lineas": [
                        intento["linea"]
                        for intento in ventana
                    ],
                })

                break

    return alertas
