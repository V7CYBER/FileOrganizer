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
│   ├── alertas.py
│   ├── analizador.py
│   ├── analizador_logs.py
│   ├── auditoria.py
│   ├── clasificador.py
│   ├── configuracion.py
│   ├── creador.py
│   ├── cuarentena.py
│   ├── deshacer.py
│   ├── duplicados.py
│   ├── duplicados_hash.py
│   ├── estadisticas.py
│   ├── eventos.py
│   ├── hash.py
│   ├── informes.py
│   ├── integridad.py
│   ├── logger.py
│   ├── magic_numbers.py
│   ├── mensajes.py
│   ├── movimientos.py
│   ├── rutas.py
│   ├── reglas_logs.py
│   ├── seguridad.py
│   └── verificador.py
├── ui/
│   ├── __init__.py
│   ├── auditoria.py
│   ├── duplicados.py
│   ├── estadisticas.py
│   ├── integridad.py
│   ├── logs.py
│   └── organizacion.py
├── docs/
│   ├── Resumen_v3.1_Seguridad.md
│   ├── Resumen_v3.2_Robustez_Testing.md
│   ├── Resumen_v3.3_Monitor_Integridad.md
│   ├── Resumen_v3.4_Auditoria_Seguridad.md
│   └── Resumen_v3.5_Refactor_Arquitectura.md
│   └── Resumen_v3.6_Motor_Reglas_Logs.md
├── reports/
│   └── .gitkeep
├── test/
│   ├── test_alertas.py
│   ├── test_analizador_logs_alertas.py
│   ├── test_analizador_logs_eventos.py
│   ├── test_analizador_logs_correlacion.py
│   ├── test_analizador_logs_funciones.py
│   ├── test_analizador_logs_ip.py
│   ├── test_analizador_logs_patrones.py
│   ├── test_analizador_logs_reglas.py
│   ├── test_analizador_logs_robustez.py
│   ├── test_analizador_logs_tiempo.py
│   ├── test_auditoria.py
│   ├── test_cuarentena.py
│   ├── test_cuarentena_robustez.py
│   ├── test_eventos.py
│   ├── test_filesystem_robustez.py
│   ├── test_integridad.py
│   ├── test_magic_numbers.py
│   ├── test_magic_numbers_robustez.py
│   ├── test_movimientos_robustez.py
│   ├── test_organizador_alertas.py
│   ├── test_organizador_analisis.py
│   ├── test_organizador_auditoria.py
│   ├── test_organizador_clasificacion.py
│   ├── test_organizador_cuarentena.py
│   ├── test_organizador_duplicados.py
│   ├── test_organizador_integridad.py
│   ├── test_organizador_logs.py
│   ├── test_organizador_seleccion.py
│   ├── test_permisos_robustez.py
│   ├── test_reglas_logs.py
│   ├── test_seguridad.py
│   ├── test_verificador.py
│   └── test_verificador_robustez.py
├── config.json
├── .gitignore
├── organizador.py
├── README.md
├── requirements-dev.txt
└── requirements.txt
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

En desarrollo activo.

# 📂 FileOrganizer

```text
========================================
        FILE ORGANIZER v3.8
========================================
1) Organizar carpeta
2) Modo simulación
3) Deshacer última organización
4) Ver estadisticas
5) Buscar archivos duplicados por nombre
6) Buscar archivos duplicados por contenido (SHA-256)
7) Ver historial de organizaciones
8) Analizar archivo de logs
9) Crear baseline de integridad
10) Verificar integridad
11) Ejecutar auditoría de seguridad
12) Salir
```
FileOrganizer es una aplicación desarrollada en Python para organizar y analizar archivos, incorporando progresivamente mecanismos de seguridad defensiva, integridad, análisis de logs y auditoría.
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

## v3.0

### Objetivo técnico

Centralizar las rutas utilizadas por FileOrganizer para eliminar rutas relativas dependientes del directorio desde el que se ejecuta el programa y mejorar la organización interna del código.

### Cambios realizados

1. **Nuevo módulo de rutas**

   Se añadió:

   `core/rutas.py`

   Este módulo centraliza las rutas principales del proyecto:

   * Ruta raíz del proyecto.
   * Ruta de `config.json`.
   * Carpeta `logs`.
   * Archivo `logs/movimientos.log`.

   Las rutas se construyen a partir de la ubicación real del proyecto mediante `Path(__file__).resolve()`.

2. **Nuevo módulo de configuración**

   Se añadió:

   `core/configuracion.py`

   Este módulo centraliza la carga de `config.json` y la obtención de las carpetas configuradas como ignoradas.

   De esta forma, la gestión de la configuración queda separada de la lógica de clasificación.

3. **Actualización del logger**

   `core/logger.py` deja de construir directamente la ruta de `logs/movimientos.log` y utiliza las rutas definidas en:

   `core/rutas.py`

4. **Actualización del sistema de deshacer**

   `core/deshacer.py` utiliza ahora:

   `ARCHIVO_LOG_MOVIMIENTOS`

   para localizar el historial de movimientos.

   Se añadió además una comprobación para detectar registros de log inválidos antes de procesarlos.

5. **Actualización del clasificador**

   `core/clasificador.py` utiliza la configuración centralizada mediante `core.configuracion`.

   La lógica de clasificación queda separada de la carga de configuración.

6. **Actualización del analizador**

   `core/analizador.py` utiliza la configuración centralizada para determinar las carpetas que deben ignorarse durante el análisis.

7. **Actualización del creador de carpetas**

   `core/creador.py` utiliza la configuración centralizada para trabajar con las categorías definidas en `config.json`.

8. **Eliminación de código obsoleto**

   Se eliminó la función `mover_fotos()` de:

   `core/movimientos.py`

   La función ya no tenía referencias en el proyecto y había quedado obsoleta dentro de la arquitectura actual.

### Pruebas realizadas

La versión v3.0 fue validada mediante:

```bash
python3 -m py_compile core/*.py organizador.py
git diff --check
```

También se comprobaron:

* Carga correcta de `config.json`.
* Obtención de carpetas ignoradas.
* Resolución absoluta de las rutas del proyecto.
* Integración entre `logger.py` y `rutas.py`.
* Integración entre `deshacer.py` y `rutas.py`.
* Ausencia de referencias a las rutas antiguas.
* Organización real de archivos.
* Clasificación de archivos conocidos y desconocidos.
* Creación automática de `Sin_clasificar`.
* Registro correcto de movimientos.

### Resultado

FileOrganizer dispone ahora de una arquitectura más limpia y mantenible, con las rutas y la configuración centralizadas.

La lógica relacionada con:

* configuración,
* rutas,
* clasificación,
* análisis,
* movimientos,
* registros,
* deshacer

queda mejor separada entre los módulos correspondientes.

La versión v3.0 fue confirmada mediante Git con el commit:

`40bc6d7 — v3.0: centraliza configuración y rutas del proyecto`

El commit fue publicado correctamente en GitHub mediante `git push`.

### Competencias adquiridas

* Centralización de rutas mediante `pathlib`.
* Uso de rutas absolutas basadas en `__file__`.
* Separación de responsabilidades entre módulos.
* Refactorización de código existente.
* Eliminación segura de código obsoleto.
* Integración entre módulos Python.
* Validación mediante compilación y comprobaciones de Git.
* Gestión de configuración externa mediante JSON.
* Mantenimiento de compatibilidad con funcionalidades existentes.
* Flujo completo de desarrollo, pruebas, commit y publicación mediante Git.



## v3.1

### Objetivo técnico

Añadir una capa de seguridad a FileOrganizer mediante análisis de firmas binarias, detección de archivos sospechosos, cuarentena y análisis defensivo de logs.

La versión amplía el proyecto desde la organización de archivos hacia funcionalidades relacionadas con ciberseguridad defensiva y análisis de eventos.

### Cambios realizados

1. **Detección mediante Magic Numbers**

   Se añadió:

   `core/magic_numbers.py`

   Este módulo permite analizar los primeros bytes de un archivo para determinar su tipo real mediante firmas conocidas.

   Inicialmente se contemplan:

   - JPEG
   - PNG
   - GIF
   - PDF
   - ZIP
   - GZIP
   - ELF
   - PE / Windows executable

2. **Verificación de extensión frente al contenido real**

   Se añadió:

   `core/verificador.py`

   El módulo compara:

   `extensión declarada ↔ tipo real detectado`

   Los posibles estados son:

   - `OK`
   - `SOSPECHOSO`
   - `NO_VERIFICADO`

   Durante las pruebas se validó el caso de un archivo llamado:

   `programa.jpg`

   cuya firma real correspondía a:

   `PE/Windows executable`

   El archivo fue marcado correctamente como:

   `SOSPECHOSO`

3. **Nueva capa de seguridad**

   Se añadió:

   `core/seguridad.py`

   Este módulo permite:

   - verificar todos los archivos de una carpeta;
   - obtener archivos correctos;
   - obtener archivos sospechosos;
   - identificar archivos no verificados;
   - generar un resumen estadístico de seguridad.

4. **Sistema de cuarentena**

   Se añadió:

   `core/cuarentena.py`

   Los archivos sospechosos pueden trasladarse a:

   `quarantine/`

   El sistema:

   - crea automáticamente la carpeta;
   - evita sobrescribir archivos con el mismo nombre;
   - conserva la ruta original;
   - registra el destino;
   - registra la extensión;
   - registra el tipo real detectado;
   - genera alertas de seguridad.

   El registro se almacena en:

   `quarantine/alertas.log`

   La carpeta `quarantine/` se añadió a `.gitignore` para evitar incorporar muestras potencialmente sospechosas al repositorio.

5. **Confirmación antes de aplicar la cuarentena**

   La capa de seguridad se integró en el flujo de organización.

   El programa:

   1. analiza la carpeta;
   2. verifica los archivos;
   3. muestra las alertas;
   4. presenta la clasificación prevista;
   5. solicita confirmación;
   6. únicamente después de confirmar aplica la cuarentena y organiza los archivos restantes.

   Se validó que responder `N` no modifica los archivos.

   También se comprobó que el modo simulación no mueve archivos a cuarentena.

6. **Nuevo analizador de logs**

   Se añadió:

   `core/analizador_logs.py`

   El módulo analiza archivos de texto línea por línea mediante expresiones regulares.

   Permite detectar inicialmente eventos relacionados con:

   - SQL Injection.
   - Fallos repetidos de autenticación.

7. **Detección de SQL Injection**

   Se añadieron patrones para identificar posibles intentos relacionados con:

   - `UNION SELECT`
   - `OR 1=1`
   - `AND 1=1`
   - comparaciones sospechosas mediante `OR`
   - `SLEEP()`
   - `BENCHMARK()`
   - `DROP TABLE`
   - `information_schema`

   Estos eventos se clasifican inicialmente con severidad:

   `ALTA`

8. **Detección de fallos de autenticación**

   Se añadieron patrones como:

   - `Failed password`
   - `Failed login`
   - `Authentication failure`
   - `Invalid user`
   - `Maximum authentication attempts`
   - `Too many authentication failures`

   Estos eventos se clasifican inicialmente con severidad:

   `MEDIA`

9. **Extracción de direcciones IPv4**

   El analizador permite extraer direcciones IPv4 válidas de las líneas del log.

   Se validan los cuatro octetos dentro del rango:

   `0–255`

   Una dirección inválida como:

   `999.999.999.999`

   no es aceptada.

10. **Agrupación de eventos por IP**

    Los eventos detectados pueden agruparse según la dirección IP de origen.

    Esto permite identificar comportamientos repetitivos procedentes de una misma fuente.

11. **Correlación de fuerza bruta**

    Se añadió una primera correlación basada en:

    - misma dirección IP;
    - múltiples eventos de autenticación fallida;
    - umbral configurable.

    Durante las pruebas:

    `192.168.1.20`

    generó tres eventos de autenticación fallida y fue identificada como:

    `POSIBLE_FUERZA_BRUTA`

12. **Correlación temporal**

    La detección se mejoró incorporando una ventana temporal.

    Configuración validada:

    - Umbral: 3 intentos.
    - Ventana: 60 segundos.

    Caso positivo:

    - IP: `192.168.1.20`
    - Intentos: 3
    - Ventana real: 2.0 segundos
    - Líneas: `[3, 4, 5]`

    Resultado:

    `POSIBLE_FUERZA_BRUTA`

    También se realizó una prueba negativa con tres intentos separados durante varios minutos.

    Resultado:

    `0 alertas correlacionadas`

13. **Integración en el menú principal**

    Se añadió una nueva opción:

    `8) Analizar archivo de logs`

    La opción de salida pasa a ser:

    `9) Salir`

    El análisis muestra:

    - eventos encontrados;
    - SQL Injection;
    - eventos de autenticación;
    - severidades;
    - IP de origen;
    - contenido de la línea;
    - alertas correlacionadas.

### Pruebas realizadas

La versión v3.1 fue validada mediante:

```bash
python3 -m py_compile core/*.py organizador.py
git diff --check
git diff --cached --check
```

### Resultado

La versión v3.1 incorporó una primera capa de seguridad defensiva al proyecto, ampliando FileOrganizer más allá de la organización de archivos.

El proyecto permite:

- verificar el tipo real de determinados archivos mediante magic numbers;
- detectar discrepancias entre extensión y contenido;
- identificar archivos potencialmente sospechosos;
- trasladarlos a una zona de cuarentena controlada;
- registrar alertas de seguridad;
- analizar archivos de logs;
- detectar patrones relacionados con SQL Injection;
- detectar fallos de autenticación;
- extraer y validar direcciones IPv4;
- agrupar eventos por dirección IP;
- detectar posibles ataques de fuerza bruta;
- correlacionar eventos dentro de una ventana temporal.

Estas funcionalidades establecen la base para continuar desarrollando FileOrganizer como proyecto orientado no solo a Python y automatización, sino también a ciberseguridad defensiva.

---

## v3.2

### Objetivo técnico

La versión v3.2 introduce una nueva etapa en el desarrollo de FileOrganizer centrada en la calidad, robustez y mantenibilidad del código.

Hasta esta versión, las funcionalidades del proyecto se validaban principalmente mediante pruebas manuales y comprobaciones de integración. En v3.2 se incorpora testing automático con `pytest` y análisis estático con `Ruff`, permitiendo verificar de forma repetible tanto el comportamiento del programa como determinados aspectos de calidad del código.

El objetivo principal de esta versión no ha sido añadir una gran funcionalidad visible para el usuario, sino reforzar técnicamente el proyecto mediante:

- pruebas automatizadas;
- pruebas de casos límite y condiciones de error;
- pruebas de robustez del sistema de archivos;
- validación de la capa de seguridad;
- validación del analizador de logs;
- refactorización controlada del flujo principal;
- análisis estático del código;
- mejora del tratamiento de excepciones;
- revisión del manejo de fechas y zonas horarias;
- limpieza y normalización del entorno de desarrollo.

Este proceso permite detectar regresiones y errores de forma temprana y proporciona una base más segura para continuar ampliando FileOrganizer en versiones posteriores.
### Cambios realizados

1. **Introducción de testing automático con pytest**

   Se incorporó `pytest` como framework de testing del proyecto.

   El objetivo fue sustituir progresivamente la dependencia de pruebas manuales por una batería automatizada capaz de verificar el comportamiento del código después de cada modificación.

   Los tests se almacenan en:

   `test/`

   Durante el desarrollo de v3.2 la batería alcanzó:

   `101 passed`

   Esto permite ejecutar una validación completa mediante:

   ```bash
   python -m pytest test/
   ```

2. **Tests de identificación mediante magic numbers**

   Se crearon pruebas para verificar `core/magic_numbers.py`.

   La batería comprueba la identificación de firmas correspondientes a distintos formatos, entre ellos:

   - JPEG;
   - PNG;
   - GIF;
   - PDF;
   - ZIP;
   - GZIP;
   - ELF;
   - ejecutables PE/Windows.

   También se añadieron casos para:

   - archivos desconocidos;
   - archivos vacíos;
   - archivos inexistentes;
   - firmas incompletas;
   - archivos de un solo byte;
   - nombres Unicode y espacios;
   - directorios utilizados incorrectamente como archivos.

3. **Tests del verificador de archivos**

   Se automatizó la validación de `core/verificador.py`.

   Las pruebas verifican situaciones como:

   - archivos cuya extensión coincide con su tipo real;
   - archivos JPEG válidos;
   - ejecutables con extensión `.jpg`;
   - archivos PDF disfrazados de ejecutables;
   - extensiones no verificadas;
   - extensiones en mayúsculas;
   - archivos sin extensión;
   - archivos vacíos;
   - nombres Unicode;
   - archivos con múltiples extensiones.

4. **Tests de la capa de seguridad**

   Se añadieron pruebas para `core/seguridad.py` destinadas a comprobar:

   - análisis de archivos;
   - exclusión de subdirectorios;
   - tratamiento de rutas inexistentes;
   - tratamiento de rutas que no son directorios;
   - filtrado de resultados según su estado;
   - generación de resúmenes de seguridad.

5. **Tests del sistema de cuarentena**

   Se automatizó la validación de `core/cuarentena.py`.

   Entre los escenarios comprobados se encuentran:

   - traslado de archivos a cuarentena;
   - registro de la operación;
   - prevención de colisiones de nombres;
   - múltiples colisiones consecutivas;
   - archivos inexistentes;
   - archivos sin extensión;
   - nombres Unicode y espacios;
   - prevención de sobrescrituras;
   - múltiples entradas en el registro de cuarentena.

6. **Pruebas de robustez del sistema de archivos**

   Se incorporaron casos destinados a comprobar el comportamiento ante situaciones menos habituales del sistema de archivos.

   Se validaron escenarios relacionados con:

   - enlaces simbólicos válidos;
   - enlaces simbólicos rotos;
   - archivos eliminados antes de ser procesados;
   - archivos sin permisos de lectura;
   - directorios sin permisos suficientes.

   Estas pruebas permiten verificar no solo el funcionamiento esperado del programa, sino también su comportamiento frente a condiciones anómalas del entorno.
7. **Tests del analizador de logs**

   Se añadió una batería específica para `core/analizador_logs.py`.

   Los tests validan la detección de patrones relacionados con SQL Injection, entre ellos:

   - `UNION SELECT`;
   - `OR 1=1`;
   - `AND 1=1`;
   - comparaciones sospechosas mediante `OR`;
   - `SLEEP()`;
   - `BENCHMARK()`;
   - `DROP TABLE`;
   - `information_schema`.

   También se validaron eventos relacionados con autenticación fallida:

   - `Failed password`;
   - `Failed login`;
   - `Authentication failure`;
   - `Invalid user`;
   - `Maximum authentication attempts`;
   - `Too many authentication failures`.

8. **Corrección de un patrón SQL mediante testing**

   Durante la ejecución de la nueva batería automatizada se detectó que el patrón:

   `OR 'a' = 'a'`

   no era identificado correctamente.

   El fallo estaba relacionado con una frontera de palabra `\b` situada al final de la expresión regular.

   El test permitió reproducir el problema de forma automática, corregir la expresión regular y comprobar posteriormente que toda la batería seguía funcionando.

   Este caso demostró de forma práctica el valor del testing automático para detectar errores que podían pasar desapercibidos durante las pruebas manuales.

9. **Tests de extracción y validación IPv4**

   Se añadieron pruebas para comprobar la extracción de direcciones IPv4.

   Se validaron:

   - direcciones privadas habituales;
   - dirección mínima `0.0.0.0`;
   - dirección máxima `255.255.255.255`;
   - octetos fuera de rango;
   - líneas sin dirección IP;
   - múltiples direcciones en una misma línea.

   Cuando existen varias IP en una línea, el analizador devuelve la primera dirección válida encontrada.

10. **Tests de fechas de logs**

    Se automatizaron pruebas para:

    - extracción de fechas en formato Apache;
    - líneas sin timestamp;
    - conversión de texto a `datetime`;
    - entrada `None`;
    - formatos de fecha inválidos.

    El formato analizado actualmente no incluye información de zona horaria.

    Por este motivo, la función de conversión conserva de forma deliberada un `datetime` sin zona horaria para la correlación interna de eventos.

11. **Tests de correlación de fuerza bruta**

    Se validó automáticamente la correlación temporal de eventos de autenticación fallida.

    Entre los escenarios comprobados se encuentran:

    - tres intentos desde la misma IP dentro de una ventana temporal;
    - intentos separados durante demasiado tiempo;
    - intentos distribuidos entre distintas IP;
    - número de intentos inferior al umbral;
    - eventos sin información temporal.

    La detección positiva validada utiliza:

    - umbral: `3`;
    - ventana máxima: `60 segundos`.

    En el escenario de prueba, tres intentos realizados en una ventana real de `2.0 segundos` generan una alerta:

    `POSIBLE_FUERZA_BRUTA`

12. **Tests de funciones auxiliares del analizador**

    También se añadieron pruebas directas para:

    - `analizar_log()`;
    - `generar_resumen_logs()`;
    - `agrupar_eventos_por_ip()`;
    - `detectar_fuerza_bruta_por_ip()`.

    Se comprobaron además casos como:

    - archivo de log inexistente;
    - ruta que no representa un archivo;
    - log vacío;
    - tráfico legítimo sin eventos de seguridad;
    - contenido con bytes no válidos en UTF-8.

    El analizador utiliza `errors="replace"` durante la lectura, permitiendo continuar el procesamiento de un log aunque contenga determinados bytes no válidos.
13. **Refactorización controlada de `organizador.py`**

    Durante v3.2 se redujo progresivamente la responsabilidad de `seleccionar_carpeta()`.

    Se extrajeron funciones específicas para separar presentación y flujo:

    - `mostrar_alertas_seguridad()`;
    - `mostrar_analisis_carpeta()`;
    - `mostrar_clasificacion()`;
    - `enviar_sospechosos_cuarentena()`.

    El objetivo fue mejorar la legibilidad, mantenibilidad y capacidad de testeo sin alterar el comportamiento general del programa.

    Cada extracción se realizó de forma incremental y se validó ejecutando la batería completa de tests después de cada cambio.

14. **Uso de `capsys` para validar salida por pantalla**

    Se incorporó la fixture `capsys` de `pytest` para comprobar funciones que utilizan `print()`.

    Esto permitió validar automáticamente:

    - mensajes de alerta;
    - información de análisis de carpeta;
    - clasificación prevista;
    - mensajes específicos del modo simulación;
    - salida generada durante operaciones de cuarentena.

    De esta forma, la salida de consola también pasa a formar parte del comportamiento comprobable del programa.

15. **Uso de `monkeypatch` para aislar dependencias**

    Se utilizó `monkeypatch` para sustituir temporalmente dependencias durante los tests.

    Entre otros casos, permitió:

    - redirigir la cuarentena real hacia directorios temporales;
    - sustituir `poner_en_cuarentena()` por una función controlada;
    - simular errores durante `shutil.move()`;
    - comprobar llamadas sin modificar archivos reales del proyecto.

    Esto permite probar funciones con efectos secundarios de forma aislada y segura.

16. **Uso de `tmp_path` para pruebas del sistema de archivos**

    La fixture `tmp_path` se utilizó para generar directorios temporales independientes para cada test.

    Gracias a ello se pudieron comprobar operaciones reales sobre archivos sin utilizar rutas permanentes ni contaminar el entorno del proyecto.

    Se aplicó en pruebas relacionadas con:

    - creación de archivos;
    - eliminación;
    - cuarentena;
    - permisos;
    - enlaces simbólicos;
    - logs;
    - archivos sospechosos.

17. **Detección de una recursión accidental durante el refactor**

    Durante la extracción de `mostrar_analisis_carpeta()` se introdujo accidentalmente una llamada recursiva:

    ```python
    def mostrar_analisis_carpeta(datos):
        mostrar_analisis_carpeta(datos)
    ```

    Los tests específicos detectaron inmediatamente el problema mediante:

    `RecursionError: maximum recursion depth exceeded`

    La función fue corregida y la batería completa volvió a quedar en estado correcto.

    Este caso demostró el valor de disponer de tests de regresión mientras se modifica la arquitectura de código existente.

18. **Mejora del tratamiento de excepciones en movimientos**

    Ruff detectó la regla:

    `BLE001`

    debido al uso de:

    ```python
    except Exception as error:
    ```

    en `core/movimientos.py`.

    Antes de eliminar este bloque se creó un test específico que simulaba un `RuntimeError` inesperado.

    El comportamiento inicial fue:

    `FAILED: DID NOT RAISE RuntimeError`

    Esto confirmó que el `except Exception` estaba ocultando errores que podían corresponder a defectos de programación.

    Tras eliminar el manejador genérico:

    - `PermissionError` continúa gestionándose;
    - `FileNotFoundError` continúa gestionándose;
    - `OSError` continúa gestionándose;
    - las excepciones inesperadas se propagan correctamente.

    El nuevo comportamiento quedó protegido mediante:

    `test/test_movimientos_robustez.py`
19. **Introducción de análisis estático con Ruff**

    Se incorporó `Ruff` como herramienta de análisis estático y calidad de código.

    La versión utilizada durante el desarrollo de v3.2 fue:

    `ruff 0.16.3`

    La primera revisión completa del proyecto detectó:

    `37 avisos`

    En lugar de aplicar una corrección automática masiva, los avisos se revisaron progresivamente por categorías.

    El procedimiento utilizado fue:

    1. seleccionar una regla concreta;
    2. revisar los archivos afectados;
    3. comprender el motivo del aviso;
    4. realizar únicamente las modificaciones necesarias;
    5. ejecutar los tests;
    6. comprobar la compilación;
    7. ejecutar `git diff --check`;
    8. continuar con la siguiente categoría.

    Este procedimiento permitió utilizar el análisis estático como herramienta de aprendizaje y revisión técnica, evitando modificaciones automáticas cuyo impacto no hubiera sido previamente comprendido.

20. **Eliminación de imports no utilizados — F401**

    La regla:

    `F401`

    detectó imports que habían quedado sin utilizar después de diferentes etapas de desarrollo y refactorización.

    Se localizaron inicialmente cuatro casos:

    - `mostrar_error` en `organizador.py`;
    - `Path` en `test/test_analizador_logs_funciones.py`;
    - `Path` en `test/test_cuarentena_robustez.py`;
    - `pytest` en `test/test_verificador_robustez.py`.

    Los imports fueron eliminados manualmente y posteriormente se comprobó:

    `All checks passed!`

    La batería completa continuó funcionando con:

    `100 passed`

21. **Corrección de f-strings innecesarios — F541**

    Ruff detectó mediante la regla:

    `F541`

    dos cadenas marcadas como f-string que no contenían ninguna interpolación.

    En `core/mensajes.py` se sustituyeron expresiones como:

    ```python
    print(f"\nArchivo:")
    ```

    por:

    ```python
    print("\nArchivo:")
    ```

    y se realizó la misma corrección para el mensaje `Motivo:`.

    El cambio no modifica el comportamiento del programa, pero elimina sintaxis innecesaria y mejora la claridad del código.

22. **Normalización de imports — I001**

    La regla:

    `I001`

    permitió detectar bloques de imports desordenados o con un formato no normalizado.

    Inicialmente se localizaron:

    `17 errores`

    La corrección se realizó en dos tandas controladas:

    - módulos de `core/` y `organizador.py`;
    - archivos de tests.

    Entre las mejoras realizadas se encuentran:

    - orden correcto de módulos de la biblioteca estándar;
    - separación entre biblioteca estándar e imports internos;
    - ordenación de nombres importados;
    - simplificación de imports multilínea cuando era apropiado;
    - eliminación de líneas en blanco innecesarias.

    Después de ambas tandas:

    `All checks passed!`

    y la batería completa continuó mostrando:

    `100 passed`

23. **Normalización de imports de módulos — PLR0402**

    Ruff detectó varios imports realizados mediante alias innecesarios, por ejemplo:

    ```python
    import core.cuarentena as cuarentena
    ```

    Se sustituyeron por la forma recomendada:

    ```python
    from core import cuarentena
    ```

    La misma revisión se aplicó al módulo de movimientos utilizado por los tests.

    Los cambios fueron validados nuevamente mediante la batería completa.

24. **Simplificación de construcción de texto en tests — FLY002**

    Ruff detectó construcciones basadas en:

    ```python
    "\n".join([...])
    ```

    que podían expresarse de forma más directa en los datos de prueba.

    Los casos afectados se encontraban en:

    - `test/test_analizador_logs_funciones.py`;
    - `test/test_analizador_logs_robustez.py`.

    Después de la modificación se ejecutaron primero los tests directamente afectados.

    Resultado:

    `10 passed`

    Posteriormente se ejecutó la batería completa:

    `101 passed`

25. **Validación del shebang y permisos de ejecución — EXE001**

    `organizador.py` contiene:

    ```bash
    #!/usr/bin/env python3
    ```

    Ruff detectó mediante:

    `EXE001`

    que el archivo incluía un shebang pero no tenía establecido el permiso de ejecución.

    Se corrigieron los permisos del archivo, pasando en Git de:

    `100644`

    a:

    `100755`

    De esta forma existe coherencia entre el shebang declarado y los permisos reales del programa.

26. **Revisión de fechas y zonas horarias — reglas DTZ**

    Ruff detectó varios usos de `datetime` sin información explícita de zona horaria.

    Se revisaron individualmente los casos presentes en:

    - `core/cuarentena.py`;
    - `core/estadisticas.py`;
    - `core/informes.py`;
    - `core/logger.py`;
    - `organizador.py`;
    - `core/analizador_logs.py`;
    - tests relacionados con fechas.

    Para fechas que representan momentos reales del sistema se adoptó un manejo consciente de zona horaria.

    Por ejemplo:

    ```python
    datetime.now(timezone.utc).astimezone()
    ```

    y los timestamps Unix se convierten proporcionando explícitamente información de zona horaria cuando corresponde.

27. **Excepción deliberada para fechas de logs sin zona horaria**

    El formato de log analizado actualmente por `core/analizador_logs.py` utiliza fechas como:

    `16/Aug/2026:09:01:16`

    Este formato no contiene información sobre zona horaria.

    Por este motivo, convertir automáticamente esa fecha a UTC o a otra zona introduciría información que no existe en el dato original.

    Se decidió conservar deliberadamente un `datetime` sin zona horaria para esta correlación temporal interna.

    La decisión quedó documentada directamente en el código mediante:

    ```python
    # noqa: DTZ007
    ```

    El test correspondiente mantiene igualmente un `datetime` sin zona horaria de forma deliberada mediante:

    ```python
    # noqa: DTZ001
    ```

    De esta forma no se ignora globalmente la regla: se documenta una excepción concreta cuya razón técnica ha sido revisada.

28. **Resultado final del análisis estático**

    Después de revisar y corregir progresivamente las diferentes categorías, se ejecutó Ruff sobre el proyecto completo.

    Resultado final:

    ```text
    All checks passed!
    ```

    La validación se realizó conjuntamente con:

    ```bash
    python -m pytest test/ -q
    python3 -m py_compile core/*.py organizador.py
    git diff --check
    ```

    Resultado de pytest:

    ```text
    101 passed
    ```

    Por tanto, la limpieza realizada mediante análisis estático no introdujo regresiones detectadas por la batería automatizada.

29. **Separación de dependencias del proyecto**

    Durante la revisión final de v3.2 se comprobó que el archivo destinado a las dependencias tenía el nombre:

    `requeriments.txt`

    Se corrigió a la convención estándar:

    `requirements.txt`

    Actualmente FileOrganizer no necesita dependencias externas para ejecutar su funcionalidad principal, por lo que este archivo permanece vacío.

    Las herramientas utilizadas exclusivamente durante el desarrollo se separaron en:

    `requirements-dev.txt`

    con el contenido:

    ```text
    pytest==9.1.1
    ruff==0.16.3
    ```

    Esta separación diferencia las dependencias necesarias para ejecutar la aplicación de las herramientas necesarias para desarrollar, probar y analizar el proyecto.

30. **Mejora de `.gitignore`**

    Durante las ejecuciones de pytest y Ruff se generan automáticamente directorios de caché:

    `.pytest_cache/`

    `.ruff_cache/`

    Se añadieron ambos a `.gitignore`.

    El proyecto ya excluía además elementos que no deben incorporarse normalmente al repositorio:

    - `.venv/`;
    - `__pycache__/`;
    - archivos `*.pyc`;
    - `.vscode/`;
    - logs generados;
    - informes generados;
    - estadísticas generadas;
    - archivos y muestras almacenados en `quarantine/`.

31. **Entorno de desarrollo utilizado**

    La validación final de v3.2 se realizó utilizando:

    ```text
    Python 3.14.4
    pytest 9.1.1
    Ruff 0.16.3
    ```

    Las herramientas de desarrollo se ejecutan desde el entorno virtual `.venv`.

    Un entorno equivalente puede instalar las herramientas de desarrollo mediante:

    ```bash
    python -m pip install -r requirements-dev.txt
    ```

32. **Crecimiento de la batería automatizada**

    La primera batería consolidada de v3.2 alcanzó:

    `100 tests`

    distribuidos inicialmente en:

    `19 archivos`

    Durante la revisión con Ruff se detectó el uso de un manejador excesivamente genérico:

    ```python
    except Exception
    ```

    Antes de modificarlo se añadió un nuevo test de regresión:

    `test/test_movimientos_robustez.py`

    Este nuevo test elevó la batería final a:

    `101 tests`

    y el número de archivos de test a:

    `20`

    Esto demuestra que el análisis estático no se utilizó únicamente para modificar estilo: uno de sus avisos condujo a revisar un comportamiento real del programa y a proteger la corrección mediante un nuevo test automatizado.

### Pruebas realizadas

La versión v3.2 fue sometida de forma continua a pruebas durante todo su desarrollo.

La batería automatizada final se ejecutó mediante:

```bash
python -m pytest test/ -q
```

Resultado:

```text
101 passed
```

El análisis estático completo se realizó mediante Ruff.

Resultado:

```text
All checks passed!
```

También se comprobó que los módulos principales continuaban compilando correctamente:

```bash
python3 -m py_compile core/*.py organizador.py
```

y se verificó la limpieza formal de los cambios mediante:

```bash
git diff --check
```

Durante el desarrollo no se esperó hasta el final para ejecutar estas comprobaciones.

Después de cada grupo de modificaciones se ejecutaron los tests afectados y posteriormente la batería completa, siguiendo un ciclo aproximado de:

```text
modificación
    ↓
test específico
    ↓
batería completa
    ↓
Ruff
    ↓
compilación
    ↓
git diff --check
```

### Competencias adquiridas

El desarrollo de v3.2 permitió trabajar de forma práctica conceptos relacionados con calidad de software y testing.

Entre ellos:

- fundamentos de testing automatizado con `pytest`;
- estructura Arrange / Act / Assert;
- diseño de casos positivos y negativos;
- pruebas de casos límite;
- pruebas de regresión;
- uso de `tmp_path`;
- uso de `capsys`;
- uso de `monkeypatch`;
- uso de `pytest.raises`;
- uso de `pytest.mark.parametrize`;
- simulación controlada de errores;
- testing de operaciones sobre el sistema de archivos;
- testing de código relacionado con seguridad;
- validación automatizada de expresiones regulares;
- testing de extracción y validación de IPv4;
- testing de correlación temporal;
- análisis estático con Ruff;
- interpretación de reglas de linting;
- corrección incremental frente a corrección automática masiva;
- organización y limpieza de imports;
- revisión del tratamiento de excepciones;
- diferencia entre excepciones esperadas y errores inesperados;
- conceptos de `datetime` naive y timezone-aware;
- documentación de excepciones deliberadas mediante `noqa`;
- gestión de permisos ejecutables en Git;
- separación de dependencias de ejecución y desarrollo;
- mantenimiento de `.gitignore`;
- refactorización respaldada por tests.

### Resultado

La versión v3.2 transforma la forma en la que FileOrganizer puede continuar evolucionando.

El proyecto ya no depende únicamente de pruebas manuales para comprobar que sus funcionalidades siguen funcionando.

Dispone de una batería automatizada capaz de validar áreas como:

- identificación de archivos mediante magic numbers;
- verificación de extensión y contenido;
- capa de seguridad;
- cuarentena;
- sistema de archivos;
- permisos;
- análisis de logs;
- detección de patrones de seguridad;
- IPv4;
- fechas;
- correlación temporal;
- fuerza bruta;
- funciones extraídas del flujo principal;
- tratamiento de errores durante movimientos.

La batería final alcanza:

```text
101 passed
```

y el análisis estático del proyecto finaliza con:

```text
All checks passed!
```

Además, la refactorización de `organizador.py` ha comenzado a separar responsabilidades anteriormente concentradas en el flujo principal, facilitando su comprensión y testing.

La eliminación del manejador genérico `except Exception` constituye también una mejora de robustez: los errores esperados continúan siendo gestionados, mientras que errores inesperados ya no quedan ocultos.

Con v3.2, FileOrganizer incorpora una base de control de calidad formada por:

```text
Código
  │
  ├── pytest ─────► comportamiento
  │
  ├── Ruff ───────► análisis estático
  │
  ├── py_compile ─► validación sintáctica
  │
  └── Git ────────► control y trazabilidad
```

Esta versión establece una base más sólida para desarrollar las siguientes funcionalidades del proyecto con mayor seguridad frente a regresiones.

---

## v3.3

### Objetivo técnico

La versión v3.3 incorpora un Monitor de Integridad de Archivos (FIM, File Integrity Monitoring) a FileOrganizer.

El objetivo de esta versión es permitir establecer un estado de referencia de una carpeta mediante hashes SHA-256 y comparar posteriormente ese estado con el contenido actual del sistema de archivos.

Esta funcionalidad acerca FileOrganizer a un caso de uso real de ciberseguridad defensiva, donde los cambios inesperados sobre archivos pueden constituir indicadores de modificación, eliminación o incorporación de contenido.

El desarrollo de v3.3 se ha realizado siguiendo un enfoque incremental basado en TDD:

```text
RED
 ↓
GREEN
 ↓
Refactor
 ↓
Batería completa
```

### Cambios realizados

1. **Nuevo módulo de integridad**

   Se añadió:

   `core/integridad.py`

   El módulo centraliza la lógica relacionada con el monitor de integridad.

   Sus funciones principales permiten:

   - generar snapshots de una carpeta;
   - guardar baselines;
   - cargar y validar baselines;
   - comparar una baseline con el estado actual.

2. **Generación de snapshots mediante SHA-256**

   `generar_snapshot()` recorre recursivamente la carpeta vigilada y calcula el SHA-256 de cada archivo.

   El snapshot utiliza una estructura similar a:

   ```json
   {
       "ruta_base": "/home/usuario/Documentos",
       "archivos": {
           "factura.pdf": "SHA256...",
           "Trabajo/informe.txt": "SHA256..."
       }
   }
   ```

   Las rutas de los archivos se almacenan de forma relativa a la carpeta vigilada.

   `ruta_base` se normaliza como ruta absoluta.

3. **Recorrido recursivo**

   El FIM permite monitorizar archivos situados tanto en la carpeta principal como en sus subdirectorios.

   Ejemplo:

   ```text
   vigilada/
   ├── documento.txt
   └── Trabajo/
       └── informe.pdf
   ```

   El snapshot almacena:

   ```text
   documento.txt
   Trabajo/informe.pdf
   ```

4. **Guardado de baselines**

   Se añadió `guardar_baseline()`.

   La función guarda el snapshot en formato JSON y crea automáticamente el directorio de destino cuando sea necesario.

5. **Prevención de sobrescritura**

   Si ya existe:

   ```text
   baseline.json
   ```

   el sistema genera automáticamente:

   ```text
   baseline_1.json
   baseline_2.json
   baseline_3.json
   ...
   ```

   De esta forma se evita destruir una baseline anterior.

6. **Exclusión de baselines del repositorio**

   La carpeta:

   `baselines/`

   se añadió a `.gitignore`.

   Las baselines contienen información generada durante la ejecución, como rutas y hashes del sistema de archivos, por lo que no forman parte del código fuente del proyecto.

7. **Carga de baselines**

   Se añadió `cargar_baseline()`.

   La función permite recuperar desde JSON una baseline previamente creada y convertirla nuevamente en una estructura de datos Python.

8. **Validación estructural de baselines**

   Una baseline debe contener obligatoriamente:

   ```text
   ruta_base
   archivos
   ```

   Si falta alguna de estas claves se genera un error explícito.

9. **Validación de tipos**

   Se comprueba que:

   ```text
   ruta_base → str
   archivos  → dict
   hashes    → str
   ```

   Los tipos incorrectos generan `TypeError`.

10. **Validación de ruta base**

    `ruta_base` debe:

    - ser una cadena de texto;
    - no estar vacía;
    - no contener únicamente espacios;
    - representar una ruta absoluta.

    Las rutas relativas almacenadas en una baseline son rechazadas.

11. **Validación del formato SHA-256**

    Los hashes almacenados en una baseline deben cumplir el formato esperado para SHA-256:

    - 64 caracteres;
    - representación hexadecimal;
    - caracteres comprendidos entre `0-9` y `a-f`.

    Una cadena cualquiera ya no se acepta como hash válido.

12. **Comparación de integridad**

    Se añadió `comparar_integridad()`.

    La función compara:

    ```text
    baseline
       ↕
    snapshot actual
    ```

    y clasifica los archivos en cuatro grupos:

    ```text
    sin_cambios
    modificados
    nuevos
    eliminados
    ```

13. **Detección de archivos sin cambios**

    Si una ruta existe en ambos snapshots y su SHA-256 coincide:

    ```text
    misma ruta + mismo hash
    → sin_cambios
    ```

14. **Detección de archivos modificados**

    Si una ruta existe en ambos estados pero su hash ha cambiado:

    ```text
    misma ruta + hash diferente
    → modificados
    ```

15. **Detección de archivos nuevos**

    Si un archivo aparece en el snapshot actual pero no existía en la baseline:

    ```text
    no estaba antes + existe ahora
    → nuevos
    ```

16. **Detección de archivos eliminados**

    Si un archivo estaba registrado en la baseline pero ya no aparece en el estado actual:

    ```text
    estaba antes + ya no existe
    → eliminados
    ```

17. **Validación de la carpeta vigilada**

    Antes de comparar dos estados se comprueba que ambos pertenecen a la misma `ruta_base`.

    Intentar comparar snapshots correspondientes a carpetas diferentes genera `ValueError`.

18. **Manejo de archivos que desaparecen durante el escaneo**

    Durante un recorrido del sistema de archivos puede producirse una condición de carrera:

    ```text
    archivo detectado
        ↓
    otro proceso lo elimina
        ↓
    intento de calcular SHA-256
    ```

    Si el archivo desaparece durante el cálculo del hash, el FIM captura específicamente `FileNotFoundError`, omite ese archivo y continúa con el resto del análisis.

    No se utiliza un manejador genérico `except Exception`.

19. **Enlaces simbólicos**

    Los enlaces simbólicos se ignoran deliberadamente durante la generación del snapshot.

    Esto evita seguir automáticamente enlaces que podrían apuntar fuera de la carpeta vigilada.

20. **Integración en el menú principal**

    El monitor de integridad se integró en `organizador.py`.

    El menú de v3.3 incluye:

    ```text
    9) Crear baseline de integridad
    10) Verificar integridad
    11) Salir
    ```

21. **Creación de baseline desde la interfaz**

    La opción:

    ```text
    9) Crear baseline de integridad
    ```

    solicita una carpeta al usuario, genera su snapshot y guarda la baseline.

    La interfaz muestra:

    - ruta donde se ha guardado;
    - número de archivos registrados.

22. **Verificación de integridad desde la interfaz**

    La opción:

    ```text
    10) Verificar integridad
    ```

    permite seleccionar una baseline previamente creada.

    El programa:

    1. carga y valida la baseline;
    2. obtiene su `ruta_base`;
    3. genera un snapshot actual;
    4. compara ambos estados;
    5. muestra el resultado.

    Ejemplo:

    ```text
    ===== RESULTADO DE INTEGRIDAD =====
    Sin cambios : 2
    Modificados : 1
    Nuevos      : 1
    Eliminados  : 1
    ```

23. **Testing específico del FIM**

    Se amplió:

    `test/test_integridad.py`

    y se creó:

    `test/test_organizador_integridad.py`

    Las pruebas cubren tanto la lógica del núcleo como su integración con la interfaz.

24. **TDD aplicado al desarrollo**

    Durante v3.3 las nuevas funcionalidades se desarrollaron mediante ciclos RED/GREEN.

    Entre otros casos, los tests permitieron detectar:

    - ausencia inicial de funciones;
    - rutas relativas almacenadas incorrectamente;
    - falta de clasificación de archivos modificados;
    - falta de detección de nuevos y eliminados;
    - un `return` colocado dentro de un bucle;
    - baselines con estructura inválida;
    - hashes con tipos incorrectos;
    - hashes con formato SHA-256 inválido;
    - rutas base vacías o relativas;
    - tratamiento de symlinks;
    - archivos que desaparecen durante el hashing.

25. **Prueba manual end-to-end**

    Además del testing automatizado se realizó una prueba manual completa sobre una carpeta temporal.

    Se creó una baseline con archivos reales y posteriormente se provocaron simultáneamente los cuatro estados:

    - archivo sin cambios;
    - archivo modificado;
    - archivo nuevo;
    - archivo eliminado.

    El resultado fue:

    ```text
    Sin cambios : 2
    Modificados : 1
    Nuevos      : 1
    Eliminados  : 1
    ```

    El resultado coincidió exactamente con el estado real del sistema de archivos.

### Pruebas realizadas

La auditoría técnica final del FIM se realizó mediante:

```bash
python -m pytest \
    test/test_integridad.py \
    test/test_organizador_integridad.py \
    -q
```

Resultado:

```text
30 passed
```

La batería completa del proyecto se ejecutó mediante:

```bash
python -m pytest test/ -q
```

Resultado:

```text
131 passed
```

El análisis estático completo se realizó mediante:

```bash
python -m ruff check .
```

Resultado:

```text
All checks passed!
```

También se validó la compilación:

```bash
python3 -m py_compile core/*.py organizador.py
```

y la limpieza formal de los cambios:

```bash
git diff --check
```

Todas las comprobaciones se completaron correctamente.

### Competencias adquiridas

El desarrollo de v3.3 permitió trabajar de forma práctica conceptos relacionados con sistemas de archivos, integridad y ciberseguridad defensiva:

- File Integrity Monitoring (FIM);
- creación de estados de referencia o baselines;
- SHA-256 aplicado a monitorización de archivos;
- comparación de estados del sistema de archivos;
- detección de modificaciones;
- detección de archivos nuevos y eliminados;
- rutas absolutas y relativas con `pathlib`;
- recorrido recursivo con `rglob()`;
- serialización y carga mediante JSON;
- validación de estructuras de datos externas;
- diferencia entre `TypeError` y `ValueError`;
- validación de formato hexadecimal;
- manejo de condiciones de carrera;
- tratamiento controlado de `FileNotFoundError`;
- enlaces simbólicos y sus implicaciones de seguridad;
- prevención de sobrescrituras;
- diseño de funciones separadas de la presentación;
- integración de funcionalidades de seguridad en una interfaz existente;
- TDD mediante ciclos RED/GREEN;
- tests de integración mediante `monkeypatch`;
- validación de salida mediante `capsys`;
- pruebas end-to-end;
- mantenimiento de una batería de regresión.

### Resultado

Con v3.3, FileOrganizer incorpora un monitor de integridad funcional capaz de establecer un estado conocido de una carpeta y detectar posteriormente cambios en sus archivos.

El flujo principal puede representarse como:

```text
Carpeta vigilada
      │
      ▼
generar_snapshot()
      │
      ▼
 SHA-256
      │
      ▼
guardar_baseline()
      │
      ▼
 baseline.json
      │
      │   pasa el tiempo
      ▼
generar_snapshot()
      │
      ▼
comparar_integridad()
      │
      ├── sin cambios
      ├── modificados
      ├── nuevos
      └── eliminados
```

La versión v3.3 amplía FileOrganizer hacia un nuevo ámbito de ciberseguridad defensiva y aprovecha la infraestructura de testing introducida en v3.2 para desarrollar las nuevas funcionalidades mediante TDD.

La batería completa del proyecto alcanza:

```text
131 passed
```

y el análisis estático finaliza con:

```text
All checks passed!
```
---

# v3.4 — Auditoría de seguridad

La versión **v3.4** incorpora una capa de auditoría de seguridad que unifica funcionalidades defensivas desarrolladas en versiones anteriores de FileOrganizer.

El nuevo sistema combina:

- verificación de archivos;
- detección de archivos sospechosos;
- archivos no verificados;
- monitorización de integridad mediante FIM;
- clasificación del nivel de auditoría;
- generación de informes;
- almacenamiento de informes sin sobrescritura;
- integración completa en el menú principal.

## Motor de auditoría

Se añadió el módulo:

```text
core/auditoria.py
```

Este módulo centraliza el flujo de auditoría y coordina los componentes de seguridad e integridad existentes.

El flujo principal es:

```text
Carpeta a auditar
      │
      ▼
cargar_baseline()
      │
      ▼
validar coherencia de rutas
      │
      ▼
verificar_archivos()
      │
      ▼
generar_resumen_seguridad()
      │
      ▼
generar_snapshot()
      │
      ▼
comparar_integridad()
      │
      ▼
generar_resumen_auditoria()
      │
      ▼
determinar_nivel_auditoria()
      │
      ▼
generar_informe_auditoria()
```

## Resumen unificado

La auditoría combina dos fuentes de información.

### Seguridad

```text
OK
Sospechosos
No verificados
```

### Integridad

```text
Sin cambios
Modificados
Nuevos
Eliminados
```

De esta forma, FileOrganizer puede ofrecer una visión conjunta del estado de seguridad de una carpeta.

## Niveles de auditoría

v3.4 introduce tres niveles:

```text
OK
ADVERTENCIA
ALERTA
```

El nivel `OK` representa una auditoría sin incidencias detectadas.

`ADVERTENCIA` se utiliza cuando existen situaciones que requieren revisión, como archivos no verificados o cambios de integridad.

`ALERTA` tiene prioridad sobre los demás niveles y se utiliza cuando se detectan archivos sospechosos.

## Informes de auditoría

La auditoría genera informes de texto que incluyen:

- nivel de auditoría;
- archivos OK;
- archivos sospechosos;
- archivos no verificados;
- archivos sin cambios;
- archivos modificados;
- archivos nuevos;
- archivos eliminados.

Los informes se almacenan en:

```text
reports/
```

El sistema evita sobrescribir informes existentes mediante nombres alternativos cuando se producen colisiones.

Ejemplo:

```text
auditoria.txt
auditoria_1.txt
auditoria_2.txt
...
```

## Validación de coherencia de rutas

La auditoría comprueba que la carpeta solicitada coincida con la `ruta_base` almacenada en la baseline.

```text
carpeta a auditar
        │
        ▼
baseline["ruta_base"]
        │
        ├── coincide ─────► continuar auditoría
        │
        └── no coincide ─► ValueError
```

Esta validación evita combinar accidentalmente el análisis de seguridad de una carpeta con el estado de integridad perteneciente a otra.

Las rutas se normalizan mediante `Path.resolve()` antes de realizar la comparación.

## Integración en el menú

El menú principal fue actualizado a:

```text
========================================
        FILE ORGANIZER v3.4
========================================
1) Organizar carpeta
2) Modo simulación
3) Deshacer última organización
4) Ver estadisticas
5) Buscar archivos duplicados por nombre
6) Buscar archivos duplicados por contenido (SHA-256)
7) Ver historial de organizaciones
8) Analizar archivo de logs
9) Crear baseline de integridad
10) Verificar integridad
11) Ejecutar auditoría de seguridad
12) Salir
```

La nueva opción permite ejecutar una auditoría completa desde la interfaz principal.

## Prueba manual end-to-end

Además del testing automatizado se realizó una prueba manual completa utilizando una carpeta temporal.

Primero se creó una baseline con dos archivos.

La primera auditoría obtuvo:

```text
Nivel: ADVERTENCIA

SEGURIDAD
OK: 0
Sospechosos: 0
No verificados: 2

INTEGRIDAD
Sin cambios: 2
Modificados: 0
Nuevos: 0
Eliminados: 0
```

Posteriormente se modificó deliberadamente uno de los archivos.

La segunda auditoría detectó correctamente:

```text
Nivel: ADVERTENCIA

SEGURIDAD
OK: 0
Sospechosos: 0
No verificados: 2

INTEGRIDAD
Sin cambios: 1
Modificados: 1
Nuevos: 0
Eliminados: 0
```

También se verificó la creación automática de informes dentro de `reports/`.

## Testing

v3.4 continúa utilizando desarrollo dirigido por pruebas mediante ciclos RED/GREEN.

Se añadieron y ampliaron:

```text
test/test_auditoria.py
test/test_organizador_auditoria.py
```

Los tests cubren:

- generación del resumen de auditoría;
- nivel `OK`;
- nivel `ADVERTENCIA`;
- nivel `ALERTA`;
- prioridad de `ALERTA`;
- tratamiento de archivos no verificados;
- generación de informes;
- contenido completo de informes;
- almacenamiento de informes;
- prevención de sobrescrituras;
- múltiples colisiones de nombres;
- combinación de seguridad e integridad;
- utilización de la ruta base de la baseline;
- inclusión del informe en el resultado;
- rechazo de carpetas incompatibles con la baseline;
- presentación de resultados desde la interfaz;
- manejo de errores;
- almacenamiento del informe desde la interfaz;
- incorporación de la auditoría al menú;
- ejecución de la auditoría desde el menú.

La validación técnica final alcanzó:

```text
151 passed
```

El análisis estático finalizó con:

```text
All checks passed!
```

También se validaron correctamente:

```bash
python3 -m py_compile core/*.py organizador.py
git diff --check
```

## Resultado

Con v3.4, FileOrganizer deja de presentar por separado parte de sus mecanismos defensivos y comienza a utilizarlos como componentes de un **sistema unificado de auditoría**.

La arquitectura puede resumirse como:

```text
             FILEORGANIZER v3.4
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
      SEGURIDAD             INTEGRIDAD
          │                     │
 verificar_archivos()    generar_snapshot()
          │                     │
          │              comparar_integridad()
          │                     │
          └──────────┬──────────┘
                     ▼
          generar_resumen_auditoria()
                     │
                     ▼
          determinar_nivel_auditoria()
                     │
                     ▼
          generar_informe_auditoria()
                     │
                     ▼
                 reports/
```

La versión v3.4 refuerza así la orientación de FileOrganizer hacia la ciberseguridad defensiva, reutilizando los mecanismos de seguridad de archivos y File Integrity Monitoring desarrollados anteriormente.
---

# v3.5 — Refactor de arquitectura e interfaz

La versión **v3.5** reorganiza la arquitectura interna de FileOrganizer para separar la interacción con el usuario de la lógica funcional del proyecto.

El objetivo principal de esta versión no es añadir nuevas funcionalidades al programa, sino mejorar su **modularidad, mantenibilidad, testabilidad y claridad arquitectónica** sin alterar el comportamiento existente.

## Objetivo del refactor

Antes de v3.5, `organizador.py` concentraba gran parte de la interfaz de terminal y coordinaba directamente funcionalidades pertenecientes a distintas áreas del proyecto.

A medida que FileOrganizer incorporó estadísticas, duplicados, análisis de logs, monitorización de integridad y auditoría de seguridad, este archivo fue creciendo hasta alcanzar aproximadamente **718 líneas**.

v3.5 introduce una nueva capa:

```text
ui/
```

encargada de agrupar las funciones relacionadas con la interacción mediante terminal.

La arquitectura queda conceptualmente dividida en:

```text
FileOrganizer
│
├── organizador.py
│   └── punto de entrada y menú principal
│
├── ui/
│   └── interacción con el usuario
│
└── core/
    └── lógica funcional del programa
```

## Nueva capa `ui/`

La interfaz se distribuye en módulos especializados:

```text
ui/
├── __init__.py
├── auditoria.py
├── duplicados.py
├── estadisticas.py
├── integridad.py
├── logs.py
└── organizacion.py
```

### `ui/organizacion.py`

Contiene el flujo principal de organización:

```text
mostrar_analisis_carpeta()
mostrar_clasificacion()
mostrar_alertas_seguridad()
enviar_sospechosos_cuarentena()
seleccionar_carpeta()
```

Este módulo coordina el análisis, clasificación, comprobaciones de seguridad, confirmación del usuario, simulación, cuarentena, movimiento de archivos y presentación del resumen final.

### `ui/estadisticas.py`

Agrupa:

```text
mostrar_estadisticas()
mostrar_historial()
```

La presentación de estadísticas e historial deja de formar parte del punto de entrada principal.

### `ui/duplicados.py`

Agrupa:

```text
mostrar_duplicados()
mostrar_duplicados_hash()
```

La interfaz de búsqueda de duplicados por nombre y por contenido SHA-256 queda aislada de `organizador.py`.

### `ui/logs.py`

Contiene:

```text
mostrar_analisis_logs()
```

Este módulo gestiona la interacción para el análisis defensivo de logs y la presentación de eventos y alertas correlacionadas.

### `ui/integridad.py`

Agrupa:

```text
crear_baseline_integridad()
verificar_integridad()
```

La interfaz del monitor de integridad queda separada de la lógica FIM implementada en `core/integridad.py`.

### `ui/auditoria.py`

Contiene:

```text
mostrar_auditoria_seguridad()
```

La interfaz de auditoría queda separada de `core/auditoria.py`, responsable de la lógica de análisis y generación del informe.

## Simplificación de `organizador.py`

Uno de los resultados principales de v3.5 es la reducción de `organizador.py`.

Antes del refactor:

```text
organizador.py
≈ 718 líneas
```

Después del refactor:

```text
organizador.py
89 líneas
```

El archivo conserva una única función propia:

```text
main()
```

Su responsabilidad queda reducida esencialmente a:

```text
mostrar menú
     │
     ▼
leer opción
     │
     ▼
delegar en ui/ o core/
     │
     ▼
repetir / salir
```

Esto convierte `organizador.py` en un punto de entrada mucho más pequeño y fácil de mantener.

## Arquitectura resultante

Antes de v3.5:

```text
organizador.py
    │
    ├── menú
    ├── análisis
    ├── clasificación
    ├── seguridad
    ├── cuarentena
    ├── duplicados
    ├── estadísticas
    ├── historial
    ├── análisis de logs
    ├── integridad
    └── auditoría
```

Después de v3.5:

```text
              organizador.py
                  89 líneas
                      │
                    main()
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
        ui/                      core/
          │                       │
 interacción terminal        lógica funcional
          │                       │
          └───────────┬───────────┘
                      ▼
                FileOrganizer
```

La separación permite distinguir con mayor claridad:

- **entrada y navegación** → `organizador.py`;
- **presentación e interacción** → `ui/`;
- **lógica funcional y defensiva** → `core/`.

## Caracterización antes de extraer

Las funciones no se trasladaron directamente sin protección.

Antes de extraer bloques importantes se añadieron o ampliaron tests de caracterización para conservar el comportamiento existente.

Se caracterizaron específicamente:

- análisis de carpetas;
- clasificación;
- alertas de seguridad;
- cuarentena;
- selección y organización de carpetas;
- modo simulación;
- estadísticas;
- historial;
- duplicados;
- análisis de logs;
- integridad;
- auditoría.

Este procedimiento permitió realizar el refactor manteniendo una red de seguridad contra regresiones.

## Tests de selección y organización

v3.5 incorpora `test/test_organizador_seleccion.py`.

Los tests verifican:

- rechazo de rutas inválidas;
- cancelación por parte del usuario;
- funcionamiento del modo simulación;
- ausencia de movimientos reales durante la simulación;
- organización real;
- generación de estadísticas tras mover archivos.

## Validación técnica

La batería completa al finalizar el refactor alcanza:

```text
165 passed
```

El análisis estático finaliza con:

```text
All checks passed!
```

También se validan correctamente:

```bash
python3 -m py_compile core/*.py ui/*.py organizador.py
git diff --check
```

## Commits principales de v3.5

El refactor se desarrolló incrementalmente:

```text
a0f98f6  v3.5: inicia refactor de capa de interfaz
7b19671  v3.5: extrae interfaz de estadisticas e historial
bba4ad3  v3.5: extrae interfaz de duplicados
45765bf  v3.5: extrae interfaz de analisis de logs
35c652c  v3.5: extrae interfaz de integridad
0d3182f  v3.5: extrae interfaz de auditoria
46cf699  v3.5: completa refactor de interfaz de organizacion
```

Cada bloque fue validado antes de continuar con el siguiente.

## Limpieza y hardening

Durante el cierre de v3.5 también se revisaron:

- archivos ignorados por Git;
- directorios generados durante la ejecución;
- cachés de `pytest` y Ruff;
- baselines;
- cuarentena;
- logs;
- informes;
- estadísticas;
- dependencias de desarrollo;
- imports residuales;
- referencias antiguas a funciones trasladadas.

El directorio vacío `utils/` fue eliminado al comprobarse que no contenía código ni referencias activas.

Los artefactos generados durante la ejecución continúan excluidos mediante `.gitignore`.

## Resultado

v3.5 transforma la estructura del proyecto sin modificar su propósito funcional.

FileOrganizer pasa de depender de un archivo principal de gran tamaño a utilizar una arquitectura más claramente separada:

```text
              FILEORGANIZER v3.5
                       │
              ┌────────┴────────┐
              ▼                 ▼
             ui/              core/
              │                 │
        presentación      lógica funcional
              │                 │
              └────────┬────────┘
                       ▼
                organizador.py
                    main()
```

El resultado es una base más adecuada para continuar desarrollando funcionalidades de ciberseguridad, ampliar los tests y evolucionar el proyecto sin volver a concentrar responsabilidades en `organizador.py`.
````markdown
---

# v3.6 — Motor de reglas para análisis defensivo de logs

La versión **v3.6** evoluciona el analizador defensivo de logs de FileOrganizer mediante la introducción de un **motor declarativo de reglas de detección**.

El objetivo principal es separar la definición de amenazas de la lógica encargada de analizar los registros.

Antes de v3.6, los patrones de detección estaban definidos directamente dentro de:

```text
core/analizador_logs.py
```

mediante estructuras específicas para patrones y severidades.

En v3.6 se introduce:

```text
core/reglas_logs.py
```

como módulo dedicado a definir y evaluar reglas de seguridad.

## Arquitectura del motor

El nuevo flujo queda:

```text
línea de log
     │
     ▼
analizar_linea()
     │
     ▼
evaluar_linea_con_reglas()
     │
     ▼
REGLAS_DETECCION
     │
     ▼
evento de seguridad
```

Cada regla utiliza una estructura declarativa:

```text
id
tipo
severidad
descripcion
patrones
```

Esto permite identificar de forma independiente la regla concreta que generó un evento.

## Reglas disponibles

v3.6 incorpora cuatro reglas principales:

```text
WEB_SQL_001
└── SQL_INJECTION

AUTH_FAIL_001
└── FUERZA_BRUTA

WEB_PATH_001
└── PATH_TRAVERSAL

WEB_CMD_001
└── COMMAND_INJECTION
```

### SQL Injection

La detección existente de SQL Injection fue migrada al nuevo sistema de reglas sin modificar su comportamiento.

Se mantienen patrones relacionados con:

```text
UNION SELECT
OR 1=1
AND 1=1
SLEEP()
BENCHMARK()
DROP TABLE
information_schema
```

### Fallos de autenticación

La detección de eventos relacionados con fuerza bruta también fue migrada al motor declarativo.

Se mantienen patrones como:

```text
Failed password
Failed login
Authentication failure
Invalid user
Maximum authentication attempts
Too many authentication failures
```

La correlación temporal ya existente continúa funcionando sobre estos eventos.

## Path Traversal

v3.6 incorpora una nueva detección:

```text
WEB_PATH_001
```

con:

```text
tipo........ PATH_TRAVERSAL
severidad... ALTA
```

La regla reconoce variantes como:

```text
../
%2e%2e%2f
%2e%2e/
..%2f
```

Esto permite identificar intentos básicos de acceso a rutas fuera del directorio esperado, incluyendo algunas variantes codificadas para URL.

## Command Injection

También se incorpora:

```text
WEB_CMD_001
```

con:

```text
tipo........ COMMAND_INJECTION
severidad... ALTA
```

En v3.6 se caracterizan inicialmente patrones como:

```text
;whoami
&&id
```

La finalidad es demostrar que el motor puede incorporar nuevas familias de amenazas sin modificar la lógica central del analizador.

## Eventos enriquecidos

Los eventos de seguridad dejan de incluir únicamente:

```text
linea
ip
tipo
severidad
contenido
```

y pasan a incorporar también:

```text
regla
descripcion
```

Por ejemplo:

```text
Regla........ WEB_PATH_001
Tipo......... PATH_TRAVERSAL
Severidad.... ALTA
Descripción.. Posible intento de Path Traversal
```

La interfaz `ui/logs.py` fue actualizada para mostrar estos metadatos.

## Eliminación de lógica legacy

Después de conectar `analizador_linea()` con el nuevo motor se comprobaron las referencias a:

```text
PATRONES_SEGURIDAD
SEVERIDADES
```

Ambas estructuras quedaron sin uso y fueron eliminadas de `core/analizador_logs.py`.

Esto reduce la duplicación y centraliza las reglas de detección en:

```text
core/reglas_logs.py
```

## Extensibilidad

Una de las principales ventajas de v3.6 es que una nueva amenaza puede añadirse mediante una nueva regla sin reescribir `analizar_linea()`.

El diseño pasa de:

```text
analizador
├── patrones
├── severidades
└── lógica
```

a:

```text
reglas_logs.py
├── definiciones de amenazas
└── evaluación de reglas

analizador_logs.py
└── análisis y generación de eventos
```

## Desarrollo mediante TDD

El motor fue construido incrementalmente mediante ciclos RED/GREEN.

Se probaron:

- estructura obligatoria de las reglas;
- reglas base;
- coincidencia positiva;
- ausencia de coincidencia;
- evaluación de todas las reglas;
- varias reglas sobre una misma línea;
- integración con `analizar_linea()`;
- enriquecimiento de eventos;
- Path Traversal;
- variantes codificadas de Path Traversal;
- Command Injection;
- integración real de las nuevas detecciones.

Se añadieron:

```text
test/test_reglas_logs.py
test/test_analizador_logs_reglas.py
```

y se amplió:

```text
test/test_organizador_logs.py
```

## Validación técnica

La batería completa de FileOrganizer alcanza:

```text
182 passed
```

frente a los:

```text
165 passed
```

con los que se cerró v3.5.

El análisis estático finaliza con:

```text
All checks passed!
```

También se validan:

```bash
python3 -m py_compile core/*.py ui/*.py organizador.py
git diff --check
```

## Commit principal

La implementación funcional de v3.6 quedó registrada en:

```text
c33e65d  v3.6: añade motor de reglas para analisis defensivo de logs
```

## Resultado

La arquitectura resultante puede resumirse como:

```text
                FILEORGANIZER v3.6
                         │
                         ▼
                       LOG
                         │
                         ▼
               analizador_logs.py
                         │
                         ▼
                  reglas_logs.py
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
     SQL Injection   Path Traversal   Command Injection
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                 evento enriquecido
                         │
                regla + descripción
                         │
                         ▼
                     ui/logs.py
```

v3.6 convierte el analizador de logs en una base más próxima conceptualmente a un pequeño sistema de detección defensiva, manteniendo el proyecto comprensible y extensible.
---

# v3.7 — Normalización de eventos de seguridad

La versión **v3.7** introduce una capa específica para construir y normalizar eventos de seguridad.

Después de v3.6, el analizador de logs ya disponía de un motor declarativo de reglas. Sin embargo, `core/analizador_logs.py` seguía construyendo directamente los diccionarios de eventos.

v3.7 separa también esa responsabilidad mediante el nuevo módulo:

```text
core/eventos.py
```

## Objetivo

El objetivo principal es centralizar la creación de eventos de seguridad y definir un contrato común para todos ellos.

Antes de v3.7:

```text
analizador_logs.py
        │
        ▼
construcción manual del diccionario
```

Después de v3.7:

```text
analizador_logs.py
        │
        ▼
crear_evento_seguridad()
        │
        ▼
evento normalizado
```

## Nuevo módulo core/eventos.py

v3.7 incorpora:

```text
core/eventos.py
```

con la función:

```python
crear_evento_seguridad()
```

El evento normalizado contiene:

```text
linea
ip
tipo
severidad
regla
descripcion
contenido
fecha
```

## Validación del contrato

El constructor valida distintos aspectos del evento.

La regla debe contener:

```text
id
tipo
severidad
descripcion
```

Una regla incompleta produce:

```text
ValueError
```

El número de línea debe ser un entero positivo.

Se diferencia entre:

```text
tipo incorrecto de línea  → TypeError
valor incorrecto de línea → ValueError
```

El contenido debe ser una cadena de texto.

Un tipo inválido produce:

```text
TypeError
```

La dirección IP puede ser:

```text
IPv4 válida
None
```

porque no todas las líneas de log contienen una IP.

## Normalización temporal

v3.7 amplía el evento con:

```text
fecha
```

Cuando la línea contiene una fecha Apache compatible:

```text
[16/Aug/2026:09:01:16]
```

`analizar_linea()` reutiliza las funciones existentes:

```text
extraer_fecha_log()
convertir_fecha_log()
```

y almacena el resultado como un objeto `datetime`.

Cuando no existe fecha:

```text
fecha = None
```

## Integración con analizar_linea()

`core/analizador_logs.py` deja de construir manualmente cada evento.

Ahora utiliza:

```python
crear_evento_seguridad()
```

La responsabilidad queda separada así:

```text
reglas_logs.py
└── qué detectar

analizador_logs.py
└── analizar y correlacionar

eventos.py
└── construir y validar eventos
```

## Correlación temporal

La correlación de fuerza bruta también fue adaptada para aprovechar los eventos normalizados.

Cuando un evento ya contiene:

```text
evento["fecha"]
```

la correlación utiliza directamente ese valor.

Para conservar compatibilidad con los eventos históricos y los tests anteriores, se mantiene un fallback:

```text
si fecha existe
    usar evento["fecha"]

si fecha no existe
    extraerla de evento["contenido"]
```

Esto permite evolucionar el contrato sin romper el comportamiento previo.

## Desarrollo mediante TDD

v3.7 se desarrolló mediante ciclos RED/GREEN.

Se caracterizaron:

- estructura normalizada del evento;
- IP ausente;
- regla incompleta;
- línea inválida;
- tipo de línea inválido;
- contenido inválido;
- fecha opcional;
- integración del constructor con `analizar_linea()`;
- extracción de fecha desde el log;
- utilización de la fecha normalizada por la correlación temporal;
- compatibilidad con eventos históricos.

Se añadieron:

```text
test/test_eventos.py
test/test_analizador_logs_eventos.py
```

y se amplió:

```text
test/test_analizador_logs_correlacion.py
```

## Validación técnica

La batería completa alcanza:

```text
192 passed
```

frente a:

```text
182 passed
```

en v3.6.

El análisis estático finaliza con:

```text
All checks passed!
```

También se validaron:

```bash
python3 -m py_compile organizador.py core/*.py ui/*.py
git diff --check
```

## Commit principal

La implementación funcional quedó registrada en:

```text
6902aa3  v3.7: normaliza eventos de seguridad
```

## Resultado

La arquitectura específica del análisis defensivo queda:

```text
                 FILEORGANIZER v3.7
                          │
                          ▼
                        LOG
                          │
                          ▼
                 analizador_logs.py
                          │
             ┌────────────┴────────────┐
             ▼                         ▼
       reglas_logs.py              eventos.py
             │                         │
       qué detectar             cómo representar
             │                         │
             └────────────┬────────────┘
                          ▼
                   evento normalizado
                          │
                          ▼
              correlación / interfaz
```

v3.7 consolida la separación entre detección, análisis y representación de eventos, acercando FileOrganizer a una arquitectura más parecida a la utilizada por sistemas defensivos de monitorización y correlación.
---

# v3.8 — Normalización de alertas de seguridad

La versión **v3.8** cierra la fase defensiva principal de FileOrganizer mediante la normalización de las alertas generadas por la correlación temporal.

Después de v3.7, el sistema ya disponía de un motor declarativo de reglas y de eventos de seguridad normalizados. Sin embargo, la correlación temporal todavía construía directamente los diccionarios de alerta.

v3.8 separa esta responsabilidad mediante el nuevo módulo:

```text
core/alertas.py
Objetivo

Centralizar la creación de alertas de seguridad y establecer un contrato común para su representación.

El flujo evoluciona de:

correlación
    │
    ▼
diccionario construido directamente

a:

correlación
    │
    ▼
crear_alerta_seguridad()
    │
    ▼
alerta normalizada
Nuevo módulo core/alertas.py

Se incorpora la función:

crear_alerta_seguridad()

La alerta normalizada contiene:

ip
tipo
severidad
intentos
ventana_segundos
lineas
fecha

Las alertas actuales de correlación utilizan:

tipo = POSIBLE_FUERZA_BRUTA
severidad = ALTA
Integración con la correlación temporal

detectar_fuerza_bruta_temporal() deja de construir manualmente los diccionarios de alerta y delega esa responsabilidad en:

crear_alerta_seguridad()

La correlación continúa determinando:

IP implicada;
número de intentos;
ventana temporal;
líneas relacionadas.

El constructor se encarga de representar esos datos mediante el contrato normalizado.

Validación del contrato

El número de intentos debe ser un entero válido y mayor que cero.

Un tipo incorrecto produce:

TypeError

Un valor inferior a 1 produce:

ValueError

Esto mantiene la misma filosofía de contrato explícito utilizada para los eventos normalizados de v3.7.

Desarrollo mediante TDD

Se añadieron:

test/test_alertas.py
test/test_analizador_logs_alertas.py

Los ciclos RED/GREEN comprobaron:

creación de la estructura normalizada;
incorporación de fecha opcional;
integración del constructor con la correlación temporal;
rechazo de valores inválidos para intentos;
rechazo de tipos inválidos para intentos;
conservación del comportamiento anterior de la correlación.
Validación técnica

La batería completa alcanza:

197 passed

frente a:

192 passed

en v3.7.

El análisis estático mediante Ruff finaliza con:

All checks passed!

También se validaron:

python3 -m py_compile organizador.py core/*.py ui/*.py
git diff --check
Commit funcional

La implementación funcional de v3.8 quedó registrada en:

e094932  v3.8: normaliza alertas de seguridad
Arquitectura defensiva final

La evolución realizada entre v3.6 y v3.8 puede resumirse como:

                  FILEORGANIZER v3.8
                           │
                           ▼
                          LOG
                           │
                           ▼
                    reglas_logs.py
                           │
                      qué detectar
                           │
                           ▼
                      eventos.py
                           │
                 evento normalizado
                           │
                           ▼
                  analizador_logs.py
                           │
                      correlación
                           │
                           ▼
                      alertas.py
                           │
                           ▼
                  alerta normalizada

La separación de responsabilidades queda conceptualmente definida así:

reglas_logs.py
└── qué detectar

eventos.py
└── cómo representar una detección

analizador_logs.py
└── analizar y correlacionar

alertas.py
└── cómo representar una correlación
Resultado

v3.8 cierra deliberadamente esta fase de evolución Blue Team.

FileOrganizer queda como proyecto defensivo de portfolio con capacidades de:

organización y clasificación de archivos;
configuración externa;
simulación y deshacer;
estadísticas;
detección de duplicados;
hashes SHA-256;
verificación mediante magic numbers;
cuarentena;
monitor de integridad;
auditoría de seguridad;
análisis defensivo de logs;
motor declarativo de reglas;
eventos de seguridad normalizados;
correlación temporal;
alertas de seguridad normalizadas;
testing automatizado;
control de calidad mediante Ruff.

Con v3.8 queda completada la evolución defensiva planificada para esta etapa del proyecto.
