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
core/
|__ hash.py
|__ duplicados_hash.py
|__ .gitignore
├── analizador.py
├── clasificador.py
├── creador.py
├── deshacer.py
├── duplicados.py
├── estadisticas.py
├── logger.py
├── mensajes.py
└── movimientos.py
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
        FILE ORGANIZER v2.5
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
- ✅ Detección de duplicados por contenido (SHA-256).
- ✅ Identificación automática de archivos vacíos.
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
### v2.5

- Detección de archivos duplicados por nombre.
- Búsqueda recursiva en todas las subcarpetas.
- Agrupación automática de duplicados.
- Uso de expresiones regulares para normalizar nombres.
- Resultados ordenados alfabéticamente.
- Informe del número de grupos de duplicados encontrados.
✅ v2.5
- Detección de archivos duplicados.
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

Además, desde la versión 2.5 el programa incorpora:

- 🔍 Detección de archivos duplicados por nombre.
- 📂 Búsqueda recursiva en todas las subcarpetas.
- 🧩 Agrupación automática de archivos con el mismo nombre base.
Este historial servirá de base para futuras funciones de consulta y generación de informes.

## ✅ v2.6

### Novedades

- 🔐 Detección de archivos duplicados mediante SHA-256.
- 📄 Detección de archivos con contenido idéntico aunque tengan distinto nombre.
- ⚠ Identificación automática de archivos vacíos.
- 📊 Número de archivos encontrados en cada grupo de duplicados.
- 🧹 Reestructuración de `organizador.py`.
- 🐍 Creación del entorno virtual `.venv`.
- ⚙ Configuración de Black Formatter para el desarrollo.
- 📝 Creación del archivo `.gitignore`.
## v2.7

### Novedades

* Detección de duplicados por contenido mediante SHA-256.
* Obtención automática de metadatos de cada archivo duplicado.
* Visualización de:

  * Nombre del archivo.
  * Ruta completa.
  * Tamaño.
  * Fecha de última modificación.
* Conversión de timestamps Unix a formato de fecha legible mediante `datetime`.
* Identificación específica de grupos cuyo hash corresponde a archivos vacíos.
* Refactorización del módulo `duplicados_hash.py` para trabajar con estructuras de datos enriquecidas (diccionarios con metadatos), preparando el proyecto para la futura generación de informes.

### Competencias adquiridas

* Uso de `Path.stat()`.
* Obtención de metadatos del sistema de archivos.
* Manejo de timestamps Unix.
* Conversión de fechas con `datetime`.
* Diseño de estructuras de datos basadas en listas de diccionarios.
* Separación entre lógica de negocio (`core/`) y presentación (`organizador.py`).

## v2.9

### Objetivo técnico

Se amplía el sistema de informes de duplicados para incluir un resumen cuantitativo del análisis, facilitando la interpretación de los resultados y preparando el proyecto para futuras funciones de auditoría.

### Novedades

- 📊 Conteo total de archivos duplicados.
- 💾 Cálculo del espacio ocupado por los archivos duplicados.
- ♻️ Cálculo del espacio potencialmente recuperable.
- ⚠️ Conteo de grupos formados exclusivamente por archivos vacíos.
- 📄 Inclusión de estas métricas en los informes `.txt`.
- 🔢 Mantenimiento del detalle individual de cada archivo duplicado.
- 🧾 Actualización de la versión del programa a v2.9.

### Ejemplo de resumen

```text
Grupos encontrados.... 2
Archivos duplicados.... 18
Espacio ocupado....... 22 bytes
Espacio recuperable... 11 bytes
Grupos de vacíos...... 1
```
## v2.10

### Objetivo técnico

Refactorizar el sistema de estadísticas para separar el cálculo de los datos de su presentación, haciendo `organizador.py` más limpio y preparando FileOrganizer para futuras funciones de análisis, auditoría y visualización.

### Cambios realizados

1. **Nueva función de resumen de estadísticas**

   Se añadió `calcular_resumen_estadisticas()` en:

   `core/estadisticas.py`

   Esta función centraliza el cálculo de:

   - Número total de organizaciones.
   - Archivos analizados.
   - Archivos movidos.
   - Archivos omitidos.
   - Categorías acumuladas.
   - Última operación registrada.

2. **Separación entre lógica y presentación**

   Antes, `organizador.py` realizaba directamente los cálculos acumulados de las estadísticas.

   Ahora `core/estadisticas.py` se encarga de procesar el historial y `organizador.py` únicamente presenta los resultados.

3. **Estadísticas acumuladas**

   La opción `4) Ver estadísticas` muestra ahora los datos acumulados de todas las organizaciones realizadas.

   Ejemplo:

   ```text
   Organizaciones........ 1
   Archivos analizados... 2
   Archivos movidos...... 2
   Archivos omitidos..... 0

   ----------------------------------------
   Categorías acumuladas

   Documentos               1
   Fotos                    1

## v2.11

### Objetivo técnico

Añadir un historial consultable de las organizaciones realizadas, reutilizando el historial de estadísticas existente para permitir al usuario revisar las operaciones anteriores sin modificar los datos almacenados.

### Cambios realizados

1. **Nueva función de historial**

   Se añadió `mostrar_historial()` en:

   `organizador.py`

   Esta función recupera el historial mediante `leer_estadisticas()` y presenta cada organización registrada de forma individual.

2. **Nuevo acceso desde el menú**

   Se añadió una nueva opción:

   ```text
   7) Ver historial de organizaciones
   ```

   La opción permite consultar todas las organizaciones almacenadas en `stats/estadisticas.json`.

3. **Información mostrada**

   Para cada organización se muestra:

   * Número de organización.
   * Fecha.
   * Ruta analizada.
   * Archivos analizados.
   * Archivos movidos.
   * Archivos omitidos.
   * Categorías procesadas.

4. **Recorrido del historial**

   Se utiliza `enumerate()` para numerar automáticamente las organizaciones comenzando desde 1.

5. **Acceso seguro a los datos**

   Se utiliza `dict.get()` para acceder a los campos del historial de forma segura, evitando errores si algún registro antiguo no contiene una determinada clave.

6. **Manejo de historial vacío**

   Si no existen organizaciones registradas, el programa muestra un mensaje informativo y vuelve al menú sin producir errores.

7. **Actualización del menú**

   La opción de salida se desplaza a:

   ```text
   8) Salir
   ```

   mientras que la opción 7 queda reservada para consultar el historial.

### Problemas corregidos durante el desarrollo

Durante la implementación se produjo un problema de integración debido a la indentación de `mostrar_historial()`, que inicialmente quedó dentro de `mostrar_estadisticas()`.

Esto provocaba:

```text
NameError: name 'mostrar_historial' is not defined
```

Se corrigió la estructura del código para que `mostrar_historial()` sea una función independiente al mismo nivel que el resto de funciones principales.

También se detectó una discrepancia entre las etiquetas del menú y la lógica de las opciones 7 y 8. La lógica era correcta, pero los textos del menú estaban invertidos.

Finalmente se corrigió para que:

```text
7) Ver historial de organizaciones
8) Salir
```

### Competencias adquiridas

* Uso de `enumerate()`.
* Recorrido de estructuras de datos.
* Uso seguro de `dict.get()`.
* Reutilización de funciones existentes.
* Separación entre almacenamiento y presentación.
* Manejo de historiales.
* Integración de nuevas opciones en un menú interactivo.
* Identificación y corrección de errores de ámbito (`NameError`).
* Corrección de errores de indentación.
* Detección de incoherencias entre interfaz y lógica.
* Pruebas de integración después de modificar el menú.

### Resultado

FileOrganizer dispone ahora de un historial consultable de las organizaciones realizadas.

El historial continúa almacenándose en:

`stats/estadisticas.json`

La nueva función reutiliza `leer_estadisticas()` para recuperar los datos y `organizador.py` se encarga de presentarlos al usuario.

La opción de historial constituye una base para futuras funciones de auditoría, búsqueda y análisis de operaciones.

### Validación

La versión v2.11 ha sido validada mediante:

```bash
python3 -m py_compile core/*.py organizador.py
git diff --check
```

Ambas comprobaciones se completaron correctamente.

## v2.12

### Objetivo técnico

Ampliar el sistema de historial de organizaciones permitiendo consultar todas las operaciones registradas y filtrar el historial por una ruta concreta.

### Cambios realizados

1. **Filtrado del historial**

   Se añadió `filtrar_historial()` en:

   `core/estadisticas.py`

   La función permite recuperar todo el historial o únicamente los registros correspondientes a una ruta determinada.

2. **Nuevo submenú de historial**

   La opción `7) Ver historial de organizaciones` incorpora:

   - Mostrar todo el historial.
   - Filtrar el historial por ruta.
   - Volver al menú principal.

3. **Separación de responsabilidades**

   `core/estadisticas.py` se encarga de procesar y filtrar los datos del historial, mientras que `organizador.py` se ocupa de presentar la información al usuario.

4. **Manejo de búsquedas sin resultados**

   Cuando una ruta no tiene organizaciones registradas, el programa informa al usuario sin producir errores.

### Competencias adquiridas

- Filtrado de listas de diccionarios.
- Uso de funciones reutilizables para procesar datos.
- Separación entre lógica de datos y presentación.
- Integración de nuevas funciones en un menú interactivo.
- Manejo de búsquedas sin resultados.
- Pruebas funcionales de diferentes rutas.
- Mantenimiento de una arquitectura modular en Python.

### Resultado

FileOrganizer dispone ahora de un historial consultable y filtrable por ruta, proporcionando una base para futuras funciones de búsqueda, análisis y auditoría.

### Corrección posterior a las pruebas

Durante las pruebas de integración de la v2.12 se detectó un error en
`organizador.py` al guardar las estadísticas después de una organización.

La llamada utilizada inicialmente era:

`core.estadisticas.guardar_estadisticas(carpeta, estadisticas)`

pero el módulo no había sido importado mediante el nombre `core`.

Se corrigió utilizando directamente la función importada:

`guardar_estadisticas(carpeta, estadisticas)`

La corrección fue validada mediante una organización real de archivos,
comprobando que las estadísticas se registran correctamente en
`stats/estadisticas.json`.

### Datos de estadísticas

El archivo:

`stats/estadisticas.json`

contiene datos generados durante la ejecución del programa y no forma parte
del código fuente. Por este motivo se excluye del control de versiones
mediante `.gitignore`.

La estructura modular de `core/estadisticas.py` se mantiene separada de la
presentación realizada por `organizador.py`.
