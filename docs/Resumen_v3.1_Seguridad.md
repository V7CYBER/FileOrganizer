# FileOrganizer v3.1 — Seguridad y análisis de logs

## 1. Objetivo de la versión

La versión 3.1 introduce una nueva capa de seguridad en FileOrganizer.

El proyecto deja de limitarse a organizar y analizar archivos y comienza a incorporar funcionalidades orientadas a ciberseguridad:

- identificación del tipo real de archivos mediante firmas binarias;
- detección de archivos potencialmente disfrazados;
- aislamiento mediante cuarentena;
- análisis básico de logs;
- detección de patrones relacionados con SQL Injection;
- detección de fallos de autenticación;
- correlación de eventos por dirección IP y tiempo.

---

## 2. Identificación mediante Magic Numbers

Se añadió:

`core/magic_numbers.py`

Este módulo analiza los primeros bytes de un archivo para intentar determinar su tipo real independientemente de su extensión.

Firmas soportadas inicialmente:

- JPEG
- PNG
- GIF
- PDF
- ZIP
- GZIP
- ELF
- PE / Windows executable

Los archivos cuya firma no se reconoce se clasifican como:

`Desconocido`

---

## 3. Verificación de extensión y contenido

Se añadió:

`core/verificador.py`

El verificador compara:

`extensión declarada ↔ tipo real detectado`

Los posibles estados son:

- `OK`
- `SOSPECHOSO`
- `NO_VERIFICADO`

Ejemplo validado durante las pruebas:

Un archivo llamado:

`programa.jpg`

con cabecera:

`MZ`

fue identificado realmente como:

`PE/Windows executable`

y marcado como:

`SOSPECHOSO`

---

## 4. Capa de seguridad

Se añadió:

`core/seguridad.py`

Este módulo centraliza la verificación de los archivos de una carpeta.

Incluye funciones para:

- verificar archivos;
- obtener archivos sospechosos;
- obtener archivos no verificados;
- obtener archivos correctos;
- generar un resumen de seguridad.

También se añadieron validaciones para comprobar que la ruta analizada existe y corresponde a una carpeta.

---

## 5. Sistema de cuarentena

Se añadió:

`core/cuarentena.py`

Los archivos detectados como sospechosos pueden trasladarse a:

`quarantine/`

El sistema:

- crea automáticamente la carpeta de cuarentena;
- evita sobrescribir archivos con el mismo nombre;
- mueve el archivo sospechoso;
- registra la operación;
- conserva información sobre origen, destino, extensión y tipo real.

El registro se almacena en:

`quarantine/alertas.log`

La carpeta completa:

`quarantine/`

se añadió a `.gitignore` para impedir que muestras potencialmente peligrosas o archivos de laboratorio sean incorporados al repositorio.

---

## 6. Confirmación antes de la cuarentena

La seguridad se integró en el flujo principal de organización.

El programa:

1. analiza la carpeta;
2. verifica los archivos;
3. muestra las alertas detectadas;
4. presenta la clasificación prevista;
5. solicita confirmación al usuario;
6. solo después de confirmar aplica la cuarentena y organiza los archivos.

Se validó que cancelar la operación no modifica los archivos.

En modo simulación tampoco se envían archivos a cuarentena.

---

## 7. Analizador de logs

Se añadió:

`core/analizador_logs.py`

Este módulo permite analizar archivos de log línea por línea utilizando expresiones regulares.

Se incorporaron inicialmente dos familias de eventos:

### SQL Injection

Patrones contemplados:

- `UNION SELECT`
- `OR 1=1`
- `AND 1=1`
- comparaciones sospechosas con OR
- `SLEEP()`
- `BENCHMARK()`
- `DROP TABLE`
- `information_schema`

Se asigna severidad:

`ALTA`

### Fallos de autenticación

Patrones contemplados:

- `Failed password`
- `Failed login`
- `Authentication failure`
- `Invalid user`
- `Maximum authentication attempts`
- `Too many authentication failures`

Se asigna inicialmente severidad:

`MEDIA`

---

## 8. Extracción de direcciones IPv4

El analizador incorpora extracción de direcciones IPv4 mediante expresiones regulares.

La validación contempla valores entre:

`0` y `255`

para cada octeto.

Ejemplos validados:

- `192.168.1.20`
- `10.0.0.15`
- `255.255.255.255`

Una dirección inválida como:

`999.999.999.999`

no es aceptada.

---

## 9. Correlación por dirección IP

Los eventos detectados pueden agruparse por IP.

Esto permite distinguir entre eventos individuales y comportamientos repetitivos procedentes del mismo origen.

Durante el laboratorio se detectaron tres fallos consecutivos de autenticación procedentes de:

`192.168.1.20`

El sistema generó una alerta:

`POSIBLE_FUERZA_BRUTA`

con severidad:

`ALTA`

---

## 10. Correlación temporal

La detección de fuerza bruta se mejoró incorporando el factor tiempo.

El analizador extrae fechas con formato tipo Apache y permite comprobar si varios intentos procedentes de una misma IP se producen dentro de una ventana determinada.

Configuración utilizada durante la integración:

- umbral: 3 intentos;
- ventana: 60 segundos.

Caso positivo validado:

- IP: `192.168.1.20`
- intentos: `3`
- ventana real observada: `2.0 segundos`
- líneas: `[3, 4, 5]`

Resultado:

`POSIBLE_FUERZA_BRUTA`

También se realizó una prueba negativa con tres intentos suficientemente separados en el tiempo.

Resultado:

`0 alertas`

Esto evita considerar automáticamente como fuerza bruta cualquier conjunto de fallos de autenticación de una misma IP.

---

## 11. Integración en el menú

El analizador de logs se incorporó como funcionalidad independiente del organizador de archivos.

Menú de v3.1:

1. Organizar carpeta
2. Modo simulación
3. Deshacer última organización
4. Ver estadísticas
5. Buscar archivos duplicados por nombre
6. Buscar archivos duplicados por contenido (SHA-256)
7. Ver historial de organizaciones
8. Analizar archivo de logs
9. Salir

La opción 8 permite seleccionar directamente un archivo de log para analizarlo.

---

## 12. Laboratorio de validación

El laboratorio utilizado contenía:

- tráfico normal;
- tres fallos de autenticación;
- cinco patrones de SQL Injection.

Resultado:

- eventos detectados: 8
- SQL Injection: 5
- eventos de fuerza bruta: 3
- severidad ALTA: 5
- severidad MEDIA: 3

La correlación temporal detectó además:

- IP: `192.168.1.20`
- tipo: `POSIBLE_FUERZA_BRUTA`
- severidad: `ALTA`
- intentos: 3
- ventana: 2.0 segundos
- líneas: `[3, 4, 5]`

---

## 13. Validaciones técnicas

Durante el desarrollo se realizaron pruebas específicas de:

- Magic Numbers;
- detección de archivos disfrazados;
- cuarentena;
- colisiones de nombres;
- cancelación de operaciones;
- organización posterior a la cuarentena;
- SQL Injection;
- fallos de autenticación;
- extracción de IPv4;
- agrupación por IP;
- correlación por número de intentos;
- extracción temporal;
- correlación temporal positiva;
- correlación temporal negativa;
- integración del analizador desde el menú principal.

También se verificó el código mediante:

`python3 -m py_compile core/*.py organizador.py`

y:

`git diff --check`

sin errores.

---

## 14. Nuevos módulos de v3.1

La versión incorpora:

- `core/magic_numbers.py`
- `core/verificador.py`
- `core/seguridad.py`
- `core/cuarentena.py`
- `core/analizador_logs.py`

Además se modificaron:

- `organizador.py`
- `.gitignore`

---

## 15. Resultado de v3.1

FileOrganizer v3.1 supone el inicio de la evolución del proyecto hacia herramientas relacionadas con ciberseguridad.

El programa combina ahora dos áreas:

### Gestión de archivos

- clasificación;
- organización;
- simulación;
- historial;
- estadísticas;
- duplicados;
- hashes SHA-256.

### Seguridad

- análisis de firmas binarias;
- detección de discrepancias entre extensión y contenido;
- cuarentena;
- análisis de logs;
- expresiones regulares;
- detección de eventos;
- extracción de IP;
- correlación por origen;
- correlación temporal;
- detección básica de posibles ataques de fuerza bruta.

La versión v3.1 queda funcionalmente preparada para su cierre y documentación final.
