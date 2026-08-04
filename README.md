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
│   ├── creador.py
│   ├── deshacer.py
│   ├── estadisticas.py
│   ├── logger.py
│   ├── mensajes.py
│   └── movimientos.py
├── docs/
├── logs/
├── stats/
│   └── estadisticas.json
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
# 📂 FileOrganizer
```text
========================================
        FILE ORGANIZER v2.4
========================================
1) Organizar carpeta
2) Modo simulación
3) Deshacer última organización
4) Ver estadísticas
5) Salir
```
FileOrganizer es una aplicación desarrollada en Python para organizar archivos automáticamente según su extensión.

## Funciones actuales

- ✅ Análisis de carpetas
- ✅ Clasificación por categorías mediante `config.json`
- ✅ Creación automática de carpetas
- ✅ Organización de archivos
- ✅ Barra de progreso
- ✅ Resumen final
- ✅ Historial de movimientos
- ✅ Deshacer última organización
- ✅ Menú interactivo
- ✅ Manejo de errores
- ✅ Carpetas configurables mediante JSON
- ✅ Modo simulación (v2.1)
- 📈 Consulta de estadísticas desde el menú.
---

# Versiones

## v2.1

### Novedades

- Nuevo **Modo Simulación**.
- Vista previa de la organización sin mover archivos.
- Resumen específico para la simulación.
- Refactorización de `seleccionar_carpeta()`.
- Código reorganizado para facilitar futuras mejoras.

---

## Próximas mejoras (v2.2)

- Utilizar la sección `"ignorar"` de `config.json`.
- Evitar analizar las carpetas creadas por el propio programa.
- Mejorar la velocidad en ejecuciones repetidas.
- 📊 Registro automático de estadísticas de cada organización.
## Características

- Organización automática de archivos por categorías.
- Configuración mediante `config.json`.
- Creación automática de carpetas.
- Historial de movimientos.
- Deshacer última organización.
- Modo simulación.
- Sistema de carpetas ignoradas.
- 📊 Registro automático de estadísticas de cada organización.
## Estadísticas

A partir de la versión **v2.4**, FileOrganizer registra automáticamente todas las organizaciones realizadas y permite consultarlas desde el menú principal.

Las estadísticas se almacenan en:

```text
stats/estadisticas.json
```

Actualmente se muestran:

- Número de organizaciones realizadas.
- Archivos analizados.
- Archivos movidos.
- Archivos omitidos.
- Total de archivos organizados por categoría.

Esta funcionalidad servirá como base para futuras consultas e informes más avanzados.

Las estadísticas se almacenan en:

```text
stats/estadisticas.json
```

Cada registro contiene:

- Fecha y hora.
- Carpeta organizada.
- Archivos analizados.
- Archivos movidos.
- Archivos omitidos.
- Número de archivos por categoría.
- 📊 Registro automático de estadísticas de cada organización.

Este historial servirá de base para futuras funciones de consulta y generación de informes.

