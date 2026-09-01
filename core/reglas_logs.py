import re

REGLAS_DETECCION = [
    {
        "id": "WEB_SQL_001",
        "tipo": "SQL_INJECTION",
        "severidad": "ALTA",
        "descripcion": "Posible intento de SQL Injection",
        "patrones": [
            re.compile(
                r"\bunion\s+select\b",
                re.IGNORECASE,
            ),
            re.compile(
                r"\bor\s+1\s*=\s*1\b",
                re.IGNORECASE,
            ),
            re.compile(
                r"\band\s+1\s*=\s*1\b",
                re.IGNORECASE,
            ),
            re.compile(
                r"\bor\s+'[^']*'\s*=\s*'[^']*'",
                re.IGNORECASE,
            ),
            re.compile(
                r"\bsleep\s*\(\s*\d+\s*\)",
                re.IGNORECASE,
            ),
            re.compile(
                r"\bbenchmark\s*\(",
                re.IGNORECASE,
            ),
            re.compile(
                r"\bdrop\s+table\b",
                re.IGNORECASE,
            ),
            re.compile(
                r"\binformation_schema\b",
                re.IGNORECASE,
            ),
        ],
    },
    {
        "id": "AUTH_FAIL_001",
        "tipo": "FUERZA_BRUTA",
        "severidad": "MEDIA",
        "descripcion": "Intento de autenticación fallido",
        "patrones": [
            re.compile(
                r"\bfailed\s+password\b",
                re.IGNORECASE,
            ),
            re.compile(
                r"\bfailed\s+login\b",
                re.IGNORECASE,
            ),
            re.compile(
                r"\bauthentication\s+failure\b",
                re.IGNORECASE,
            ),
            re.compile(
                r"\binvalid\s+user\b",
                re.IGNORECASE,
            ),
            re.compile(
                r"\bmaximum\s+authentication\s+attempts\b",
                re.IGNORECASE,
            ),
            re.compile(
                r"\btoo\s+many\s+authentication\s+failures\b",
                re.IGNORECASE,
            ),
        ],
    },
    {
        "id": "WEB_PATH_001",
        "tipo": "PATH_TRAVERSAL",
        "severidad": "ALTA",
        "descripcion": "Posible intento de Path Traversal",
        "patrones": [
            re.compile(
                r"\.\./",
                re.IGNORECASE,
            ),
            re.compile(
                r"%2e%2e%2f",
                re.IGNORECASE,
            ),
            re.compile(
                r"%2e%2e/",
                re.IGNORECASE,
            ),
            re.compile(
                r"\.\.%2f",
                re.IGNORECASE,
            ),
        ],
    },
    {
        "id": "WEB_CMD_001",
        "tipo": "COMMAND_INJECTION",
        "severidad": "ALTA",
        "descripcion": "Posible intento de Command Injection",
        "patrones": [
            re.compile(
                r";\s*whoami\b",
                re.IGNORECASE,
            ),
            re.compile(
                r"&&\s*id\b",
                re.IGNORECASE,
            ),
        ],
    },
]


def evaluar_regla(regla, linea):
    for patron in regla["patrones"]:
        if patron.search(linea):
            return True

    return False


def evaluar_linea_con_reglas(linea, reglas):
    coincidencias = []

    for regla in reglas:
        if evaluar_regla(regla, linea):
            coincidencias.append(regla)

    return coincidencias
