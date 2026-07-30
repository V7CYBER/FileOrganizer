# FileOrganizer

Organizador automático de archivos desarrollado en Python.

## Objetivo

Organizar automáticamente los archivos de una carpeta según su extensión, utilizando una configuración externa mediante `config.json`.

## Características

- Análisis previo de la carpeta.
- Clasificación automática por extensión.
- Creación automática de carpetas.
- Barra de progreso.
- Confirmación antes de mover archivos.
- Historial de movimientos.
- Deshacer la última organización.
- Configuración mediante `config.json`.
- Carpeta `Sin_clasificar` para extensiones desconocidas.
- Exclusión automática de carpetas configuradas mediante la lista `ignorar`.

---

## Estructura del proyecto

```text
FileOrganizer/
├── core/
│   ├── analizador.py
│   ├── clasificador.py
│   ├── movimientos.py
│   ├── deshacer.py
│   ├── logger.py
│   ├── mensajes.py
│   └── creador.py
├── logs/
├── docs/
├── test/
├── utils/
├── config.json
├── organizador.py
└── README.md
```

---

## Versiones

### v1.0
- Primer organizador funcional.

### v1.8
- Configuración externa mediante `config.json`.
- Carpeta `Sin_clasificar`.

### v1.9
- Nuevo resumen final.
- Estadísticas de archivos analizados, movidos y omitidos.

### v2.0
- Lista `ignorar` en `config.json`.
- El analizador ignora automáticamente las carpetas configuradas.
- El clasificador elimina la clave `ignorar` antes de clasificar.
- Carga de `config.json` mediante rutas absolutas con `Path(__file__)`.
- Arquitectura más modular y configurable.

---

## Tecnologías utilizadas

- Python 3
- pathlib
- shutil
- json

---

## Estado del proyecto

En desarrollo.
