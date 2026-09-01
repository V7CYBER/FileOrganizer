# FileOrganizer v3.6 — Motor de reglas para análisis defensivo de logs

## 1. Objetivo de la versión

La versión v3.6 de FileOrganizer tiene como objetivo evolucionar el sistema de análisis defensivo de logs introducido en versiones anteriores.

Hasta este momento, `core/analizador_logs.py` contenía tanto la lógica encargada de analizar las líneas de un log como las definiciones concretas de los patrones de seguridad.

v3.6 separa ambas responsabilidades mediante la creación de un nuevo módulo:

```text
core/reglas_logs.py
```

Este módulo contiene las reglas de detección y el motor encargado de evaluarlas.

El objetivo arquitectónico es pasar de un analizador con patrones embebidos a un sistema extensible basado en reglas.

---

## 2. Punto de partida desde v3.5

v3.5 dejó FileOrganizer con una arquitectura más modular después de separar la interfaz de usuario de la lógica funcional.

La estructura general pasó a distinguir principalmente:

```text
organizador.py
│
├── ui/
│   └── interacción y presentación
│
└── core/
    └── lógica funcional
```

Esta separación permitió que v3.6 pudiera concentrarse en evolucionar una funcionalidad concreta de ciberseguridad sin volver a aumentar las responsabilidades de `organizador.py`.

El componente elegido fue:

```text
core/analizador_logs.py
```

El analizador ya disponía de funcionalidades como:

- extracción de direcciones IPv4;
- detección de SQL Injection;
- detección de fallos de autenticación;
- generación de eventos;
- agrupación de eventos por IP;
- generación de resúmenes;
- extracción de fechas;
- conversión de fechas;
- correlación básica de fuerza bruta;
- correlación temporal de eventos.

v3.6 conserva estas capacidades y modifica la arquitectura utilizada para realizar las detecciones.

---

## 3. Problema del analizador anterior

Antes de v3.6, `core/analizador_logs.py` contenía estructuras como:

```text
PATRONES_SEGURIDAD
SEVERIDADES
```

Estas estructuras relacionaban directamente los patrones de detección con el propio analizador.

Aunque el sistema era funcional, existía un problema de diseño.

El mismo módulo tenía que conocer:

```text
qué amenazas existen
qué patrones identifican cada amenaza
qué severidad tienen
cómo analizar una línea
cómo construir un evento
cómo procesar un archivo de log
cómo correlacionar eventos
```

Esto incrementaba el acoplamiento.

Añadir nuevos tipos de detección implicaba seguir aumentando el contenido del analizador.

v3.6 busca separar:

```text
DEFINICIÓN DE DETECCIONES
```

de:

```text
PROCESAMIENTO DE LOGS
```

---

## 4. Diseño de v3.6

La arquitectura propuesta para v3.6 introduce un nuevo componente:

```text
core/reglas_logs.py
```

El flujo general pasa a ser:

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
reglas coincidentes
     │
     ▼
eventos de seguridad
```

De esta manera, el analizador deja de decidir directamente qué patrones representan cada amenaza.

Su responsabilidad consiste en solicitar al motor de reglas que evalúe la línea.

---

## 5. Separación entre analizador y reglas

Después del refactor, las responsabilidades principales quedan divididas.

### core/analizador_logs.py

Responsable de:

```text
extraer información del log
analizar líneas
analizar archivos
generar eventos
generar resúmenes
agrupar eventos
correlacionar eventos
procesar fechas
```

### core/reglas_logs.py

Responsable de:

```text
definir reglas
almacenar patrones
identificar amenazas
definir severidades
describir detecciones
evaluar reglas
evaluar líneas contra varias reglas
```

La separación reduce el acoplamiento entre la lógica del analizador y las firmas concretas de detección.

---

## 6. Nuevo módulo core/reglas_logs.py

v3.6 incorpora:

```text
core/reglas_logs.py
```

Este archivo contiene dos elementos fundamentales:

```text
REGLAS_DETECCION
```

y las funciones:

```python
evaluar_regla()
evaluar_linea_con_reglas()
```

`REGLAS_DETECCION` contiene las definiciones declarativas.

Las funciones constituyen el pequeño motor encargado de evaluarlas.

---

## 7. Estructura declarativa de una regla

Cada regla se representa mediante un diccionario Python.

Su contrato básico contiene:

```text
id
tipo
severidad
descripcion
patrones
```

Conceptualmente:

```python
{
    "id": "...",
    "tipo": "...",
    "severidad": "...",
    "descripcion": "...",
    "patrones": [...],
}
```

Cada campo tiene una responsabilidad.

### id

Identificador único de la regla.

Ejemplo:

```text
WEB_PATH_001
```

### tipo

Categoría del evento detectado.

Ejemplo:

```text
PATH_TRAVERSAL
```

### severidad

Nivel asignado al evento.

Ejemplo:

```text
ALTA
```

### descripcion

Texto explicativo sobre la detección.

### patrones

Lista de expresiones regulares compiladas utilizadas para identificar la amenaza.

---

## 8. REGLAS_DETECCION

Las reglas se almacenan en:

```python
REGLAS_DETECCION
```

La estructura permite recorrer todas las reglas mediante un único mecanismo.

El analizador ya no necesita implementar una condición específica para cada amenaza.

El motor puede hacer conceptualmente:

```text
para cada regla
    evaluar sus patrones

si coincide
    devolver la regla
```

Esto hace que la arquitectura sea extensible.

---

## 9. Identificadores de reglas

v3.6 utiliza identificadores explícitos para las detecciones.

Las reglas definidas al cierre de la versión son:

```text
WEB_SQL_001
AUTH_FAIL_001
WEB_PATH_001
WEB_CMD_001
```

Los identificadores aportan información adicional respecto al uso exclusivo del campo `tipo`.

Por ejemplo:

```text
tipo  = PATH_TRAVERSAL
regla = WEB_PATH_001
```

El tipo describe la familia del evento.

El identificador señala qué regla concreta produjo la detección.

Esto permitirá que en el futuro puedan existir varias reglas pertenecientes al mismo tipo.

---

## 10. Regla WEB_SQL_001

La detección existente de SQL Injection se migra al nuevo motor.

La regla utiliza:

```text
id.......... WEB_SQL_001
tipo........ SQL_INJECTION
severidad... ALTA
```

Su descripción identifica el evento como un posible intento de SQL Injection.

Entre los patrones caracterizados durante el desarrollo se encuentran expresiones relacionadas con técnicas como:

```text
UNION SELECT
OR 1=1
AND 1=1
SLEEP()
BENCHMARK()
DROP TABLE
information_schema
```

La finalidad de v3.6 no es crear un IDS completo, sino disponer de una arquitectura donde este conjunto pueda evolucionar sin modificar el analizador principal.

---

## 11. Regla AUTH_FAIL_001

La segunda regla base corresponde a eventos de autenticación fallida.

Utiliza:

```text
id.......... AUTH_FAIL_001
tipo........ FUERZA_BRUTA
severidad... MEDIA
```

La regla reconoce patrones asociados a fallos de autenticación, entre ellos variantes relacionadas con:

```text
Failed password
Failed login
Authentication failure
Invalid user
Maximum authentication attempts
Too many authentication failures
```

Estos eventos pueden ser posteriormente utilizados por las funciones de correlación ya existentes en `core/analizador_logs.py`.

Por tanto, v3.6 separa la detección individual de la correlación.

---

## 12. Regla WEB_PATH_001

Una de las nuevas capacidades incorporadas en v3.6 es la detección básica de Path Traversal.

La regla utiliza:

```text
id.......... WEB_PATH_001
tipo........ PATH_TRAVERSAL
severidad... ALTA
```

y una descripción:

```text
Posible intento de Path Traversal
```

La incorporación de esta regla demostró una de las ventajas del nuevo diseño: añadir una nueva familia de detección sin introducir lógica específica dentro de `analizar_linea()`.

---

## 13. Path Traversal

Path Traversal es una técnica mediante la cual una entrada intenta acceder a rutas situadas fuera del directorio previsto.

Una representación típica utiliza secuencias como:

```text
../
```

Por ejemplo, una línea de log podría contener una petición similar a:

```text
GET /../../etc/passwd HTTP/1.1
```

En v3.6 se incorporan patrones destinados a reconocer formas básicas de este comportamiento.

El objetivo dentro de FileOrganizer es educativo y defensivo: analizar registros e identificar indicadores que merecen revisión.

---

## 14. Path Traversal codificado

Durante el desarrollo TDD se comprobó que detectar únicamente:

```text
../
```

era insuficiente.

Las rutas HTTP pueden contener caracteres codificados.

Se introdujeron pruebas para variantes como:

```text
/%2e%2e%2f%2e%2e%2fetc/passwd
/%2e%2e/etc/passwd
/..%2fetc/passwd
```

El primer test de estas variantes produjo RED.

El motor no detectaba todavía todas las representaciones.

Los patrones fueron ampliados hasta conseguir GREEN.

Esto demuestra un aspecto importante del testing de seguridad:

```text
una misma intención
puede representarse
mediante entradas diferentes
```

La detección debe caracterizar las variantes que se quieran soportar explícitamente.

---

## 15. Regla WEB_CMD_001

La segunda nueva familia de amenazas incorporada en v3.6 es Command Injection.

La regla utiliza:

```text
id.......... WEB_CMD_001
tipo........ COMMAND_INJECTION
severidad... ALTA
```

y la descripción:

```text
Posible intento de Command Injection
```

Esta regla amplía el motor más allá de las detecciones disponibles anteriormente.

---

## 16. Command Injection

Para caracterizar inicialmente esta regla se introdujeron ejemplos que representan intentos de encadenar comandos.

Entre los casos probados durante v3.6 aparecen:

```text
;whoami
&&id
```

Por ejemplo:

```text
GET /?cmd=&&id HTTP/1.1
```

El primer test de la variante `&&id` produjo RED.

Después se amplió la regla para reconocerla y el test pasó a GREEN.

Este proceso evita añadir patrones sin una prueba que demuestre el comportamiento esperado.

---

## 17. Función evaluar_regla()

El motor incorpora:

```python
def evaluar_regla(regla, linea):
```

Su responsabilidad es evaluar una regla concreta contra una línea.

El funcionamiento es:

```text
recibir regla
     │
     ▼
recorrer patrones
     │
     ▼
patron.search(linea)
     │
 ┌───┴───┐
 ▼       ▼
sí       no
│        │
True   continuar
```

Si alguno de los patrones coincide:

```python
return True
```

Si ninguno coincide:

```python
return False
```

La función tiene una responsabilidad pequeña y claramente definida.

---

## 18. Función evaluar_linea_con_reglas()

La segunda función del motor es:

```python
def evaluar_linea_con_reglas(linea, reglas):
```

Esta función recibe:

```text
una línea
una colección de reglas
```

y devuelve las reglas que coinciden.

El algoritmo puede representarse como:

```text
coincidencias = []

para cada regla:
    si evaluar_regla(regla, linea):
        añadir regla

devolver coincidencias
```

Una característica importante es que el resultado es una lista.

Esto permite que una misma línea produzca más de una coincidencia.

Durante los tests se verificó un caso que contenía simultáneamente indicadores de:

```text
SQL_INJECTION
FUERZA_BRUTA
```

El motor devolvió ambas reglas.

---

## 19. Integración con analizar_linea()

Una vez construido el motor, `core/analizador_logs.py` fue conectado con él.

El analizador importa:

```text
REGLAS_DETECCION
evaluar_linea_con_reglas
```

y `analizar_linea()` delega la detección en el nuevo componente.

Conceptualmente:

```text
analizar_linea()
       │
       ▼
evaluar_linea_con_reglas(
    linea,
    REGLAS_DETECCION
)
       │
       ▼
reglas coincidentes
       │
       ▼
crear eventos
```

Esto constituye el cambio arquitectónico principal de v3.6.

---

## 20. Eliminación del sistema legacy

Después de integrar el motor se inspeccionaron las referencias a:

```text
PATRONES_SEGURIDAD
SEVERIDADES
```

Se comprobó que las antiguas estructuras ya no eran necesarias.

La lógica legacy fue eliminada.

La definición de amenazas queda centralizada en:

```text
core/reglas_logs.py
```

mientras que:

```text
core/analizador_logs.py
```

mantiene las responsabilidades de análisis y correlación.

La limpieza fue validada buscando referencias residuales antes de continuar.

---

## 21. Enriquecimiento de eventos

La nueva arquitectura permite que los eventos contengan información procedente directamente de la regla.

Antes, un evento utilizaba principalmente campos como:

```text
linea
ip
tipo
severidad
contenido
```

v3.6 añade:

```text
regla
descripcion
```

Esto convierte el evento en una estructura más informativa.

---

## 22. Metadatos regla y descripción

Un evento puede ahora identificar explícitamente:

```text
Regla........ WEB_SQL_001
Tipo......... SQL_INJECTION
Severidad.... ALTA
Descripción.. Posible intento de SQL Injection
```

Los nuevos campos permiten diferenciar:

```text
qué categoría de amenaza se detectó
```

de:

```text
qué regla concreta generó la detección
```

Esta separación prepara el proyecto para futuras ampliaciones del catálogo.

---

## 23. Integración con ui/logs.py

La incorporación de nuevos metadatos no debía quedarse únicamente en el core.

La interfaz de análisis de logs fue actualizada para mostrar:

```text
regla
descripcion
```

junto con la información ya existente.

El flujo completo pasa a ser:

```text
reglas_logs.py
      │
      ▼
analizador_logs.py
      │
      ▼
evento enriquecido
      │
      ▼
ui/logs.py
      │
      ▼
terminal
```

La integración fue cubierta mediante tests de interfaz.

---

## 24. Conservación de la correlación temporal

v3.6 no reemplaza las capacidades de correlación construidas anteriormente.

El analizador continúa disponiendo de funciones como:

```python
agrupar_eventos_por_ip()
detectar_fuerza_bruta_por_ip()
extraer_fecha_log()
convertir_fecha_log()
detectar_fuerza_bruta_temporal()
```

El nuevo motor trabaja en la fase de detección.

La correlación trabaja posteriormente sobre los eventos.

Esto permite distinguir dos conceptos:

```text
DETECCIÓN
una línea coincide con una regla

CORRELACIÓN
varios eventos relacionados forman un comportamiento relevante
```

Esta distinción es importante en análisis defensivo.

---

## 25. Desarrollo mediante TDD

v3.6 se desarrolló incrementalmente mediante Test-Driven Development.

El ciclo utilizado fue:

```text
RED
 ↓
implementar mínimo necesario
 ↓
GREEN
 ↓
validar regresión
 ↓
limpiar/refactorizar
```

Los nuevos comportamientos se introdujeron primero mediante tests.

Esto permitió construir el motor paso a paso sin reemplazar de golpe el analizador existente.

---

## 26. RED/GREEN del contrato de reglas

El primer objetivo fue definir el contrato de `REGLAS_DETECCION`.

El primer RED apareció porque:

```text
core.reglas_logs
```

todavía no existía.

Se creó el módulo y posteriormente se validó que cada regla dispusiera de los campos necesarios.

El contrato establecido fue:

```text
id
tipo
severidad
descripcion
patrones
```

Después se caracterizaron las reglas base.

---

## 27. RED/GREEN del motor

El siguiente paso fue crear:

```python
evaluar_regla()
```

El RED inicial apareció porque la función todavía no existía.

Una vez implementada se verificaron dos situaciones fundamentales:

```text
coincidencia
sin coincidencia
```

Después se añadió:

```python
evaluar_linea_con_reglas()
```

y se comprobaron:

```text
una coincidencia
ninguna coincidencia
varias coincidencias
```

Con ello quedó construido el núcleo del motor.

---

## 28. RED/GREEN de integración

El siguiente ciclo TDD conectó el nuevo motor con:

```text
core/analizador_logs.py
```

La prueba utilizó `monkeypatch` para sustituir temporalmente:

```text
evaluar_linea_con_reglas
```

El primer RED demostró que el analizador todavía no conocía la nueva función.

Tras la integración, el test pasó a GREEN.

Después se añadió una prueba específica para comprobar que los eventos incluían:

```text
regla
descripcion
```

El RED produjo inicialmente:

```text
KeyError: 'regla'
```

Después del enriquecimiento del evento, el test pasó a GREEN.

---

## 29. RED/GREEN de Path Traversal

La incorporación de:

```text
WEB_PATH_001
```

también comenzó mediante RED.

Inicialmente la regla no existía y se produjo:

```text
KeyError: 'WEB_PATH_001'
```

Tras crear la regla se validó una detección real.

Posteriormente se añadieron variantes codificadas.

Una primera versión no detectó:

```text
/%2e%2e%2f%2e%2e%2fetc/passwd
```

lo que generó un nuevo RED.

Después se añadieron patrones adecuados.

También se caracterizaron variantes como:

```text
/%2e%2e/etc/passwd
/..%2fetc/passwd
```

hasta conseguir GREEN.

---

## 30. RED/GREEN de Command Injection

La regla:

```text
WEB_CMD_001
```

también se introdujo mediante TDD.

El primer test produjo:

```text
KeyError: 'WEB_CMD_001'
```

porque todavía no existía.

Después de crear la regla, el test pasó a GREEN.

Posteriormente se añadió una detección real y una variante:

```text
&&id
```

Esta variante produjo RED inicialmente:

```text
assert 0 == 1
```

El patrón fue ampliado y finalmente pasó a GREEN.

---

## 31. Tests añadidos

v3.6 incorpora dos archivos específicos:

```text
test/test_reglas_logs.py
test/test_analizador_logs_reglas.py
```

Al cierre previo de la versión sus tamaños eran:

```text
169 líneas  test/test_reglas_logs.py
196 líneas  test/test_analizador_logs_reglas.py
365 líneas  total
```

También se amplió:

```text
test/test_organizador_logs.py
```

para verificar la presentación de los metadatos del motor en la interfaz.

---

## 32. Regresión

Una condición fundamental durante el desarrollo fue mantener el comportamiento histórico.

Se ejecutaron repetidamente:

```text
tests del motor
tests de integración
tests históricos de logs
tests de interfaz
```

Antes del cierre documental se ejecutó la batería completa del proyecto.

Resultado:

```text
182 passed
```

Esto confirma que la incorporación del motor no rompe las funcionalidades cubiertas por los tests existentes.

---

## 33. Ruff y calidad de código

Ruff se utilizó durante todo el desarrollo.

Entre los problemas detectados durante los ciclos aparecieron:

```text
imports desordenados
import duplicado de re
función duplicada
```

Estos errores fueron corregidos antes de continuar.

El resultado final fue:

```text
All checks passed!
```

El proceso muestra que los tests funcionales y el análisis estático cubren problemas diferentes.

Un programa puede superar sus tests y seguir conteniendo problemas estructurales detectables por Ruff.

---

## 34. Compilación

Además de pytest y Ruff se utilizó compilación explícita de los módulos.

Esto resultó especialmente útil después de una edición accidental que produjo:

```text
"patrones":"patrones":
```

Python detectó inmediatamente:

```text
SyntaxError
```

Después de corregir el archivo se volvió a validar la compilación.

También se utilizó:

```bash
git diff --check
```

para comprobar problemas de formato en los cambios.

---

## 35. Arquitectura final

La arquitectura específica del análisis de logs queda:

```text
                   FileOrganizer
                        │
                        ▼
                    ui/logs.py
                        │
                        ▼
              core/analizador_logs.py
                        │
                        ▼
                core/reglas_logs.py
                        │
       ┌────────────────┼────────────────┐
       ▼                ▼                ▼
 SQL Injection     Path Traversal   Command Injection
       │                │                │
       └────────────────┼────────────────┘
                        ▼
                reglas coincidentes
                        │
                        ▼
                eventos enriquecidos
```

Los fallos de autenticación también forman parte del catálogo mediante:

```text
AUTH_FAIL_001
```

y continúan alimentando la lógica de correlación de fuerza bruta.

---

## 36. Flujo de detección

El flujo completo puede expresarse así:

```text
archivo de log
      │
      ▼
analizar_log()
      │
      ▼
leer línea
      │
      ▼
analizar_linea()
      │
      ▼
evaluar_linea_con_reglas()
      │
      ▼
evaluar_regla()
      │
      ▼
patron.search()
      │
      ▼
regla coincidente
      │
      ▼
evento
      │
      ├── línea
      ├── IP
      ├── tipo
      ├── severidad
      ├── regla
      ├── descripción
      └── contenido
```

Posteriormente esos eventos pueden ser resumidos, agrupados o correlacionados.

---

## 37. Extensibilidad

Uno de los principales resultados de v3.6 es la mejora de extensibilidad.

Antes, una nueva detección podía requerir modificar directamente el analizador.

Ahora el diseño permite incorporar una nueva regla dentro de:

```text
REGLAS_DETECCION
```

manteniendo estable la lógica general del motor.

Conceptualmente:

```python
{
    "id": "NUEVA_REGLA",
    "tipo": "NUEVO_EVENTO",
    "severidad": "...",
    "descripcion": "...",
    "patrones": [...],
}
```

El mismo:

```python
evaluar_linea_con_reglas()
```

puede procesarla.

---

## 38. Aplicación a ciberseguridad defensiva

El motor desarrollado no pretende sustituir herramientas profesionales como un SIEM o un IDS.

Su valor dentro de FileOrganizer es educativo y arquitectónico.

Permite practicar conceptos utilizados en sistemas defensivos:

```text
eventos
reglas
firmas
severidades
indicadores
normalización
metadatos
correlación
falsos positivos
extensibilidad
```

El proyecto comienza así a combinar programación Python con conceptos directamente relacionados con análisis defensivo.

---

## 39. Conocimientos de Python trabajados

v3.6 refuerza varios conceptos de Python.

### Diccionarios

Cada regla se representa mediante un diccionario.

### Listas

Las reglas y las coincidencias utilizan colecciones ordenadas.

### Funciones

El motor divide responsabilidades mediante funciones pequeñas.

### Módulos

La separación entre:

```text
analizador_logs.py
reglas_logs.py
```

refuerza el diseño modular.

### Expresiones regulares

Los patrones utilizan `re.compile()` y `search()`.

### Iteración

El motor recorre reglas y patrones.

### Valores booleanos

`evaluar_regla()` expresa directamente si una regla coincide.

### Importaciones

El analizador consume la API proporcionada por el módulo de reglas.

---

## 40. Conocimientos de testing trabajados

Durante v3.6 se practicaron:

```text
TDD
Arrange / Act / Assert
tests unitarios
tests de integración
monkeypatch
regresión
caracterización
casos positivos
casos negativos
variantes de entrada
múltiples coincidencias
```

También se reforzó una idea importante:

```text
un RED esperado demuestra
que el test puede detectar
la ausencia del comportamiento
```

Los ciclos RED/GREEN se conservaron deliberadamente durante el desarrollo.

---

## 41. Evolución respecto a v3.5

v3.5 se centró principalmente en arquitectura de interfaz.

Su objetivo fue separar:

```text
UI
```

de:

```text
CORE
```

v3.6 continúa esa evolución dentro del propio core.

Ahora se separa:

```text
ANÁLISIS
```

de:

```text
REGLAS DE DETECCIÓN
```

La evolución puede representarse como:

```text
v3.5
organizador.py
   │
   ├── ui/
   └── core/

v3.6
core/
   │
   ├── analizador_logs.py
   └── reglas_logs.py
```

La modularización se aplica progresivamente a distintos niveles del proyecto.

---

## 42. Métricas finales

Al cierre funcional previo a la documentación:

```text
Tests totales.............. 182
Resultado.................. 182 passed
Tests v3.5................. 165
Incremento................. 17 tests
```

Los dos nuevos archivos específicos suman:

```text
365 líneas de tests
```

El motor queda contenido en:

```text
core/reglas_logs.py
```

con cuatro reglas definidas:

```text
WEB_SQL_001
AUTH_FAIL_001
WEB_PATH_001
WEB_CMD_001
```

Las funciones públicas principales del motor son:

```text
evaluar_regla()
evaluar_linea_con_reglas()
```

---

## 43. Commit principal

La implementación funcional del motor quedó registrada en:

```text
c33e65d
```

con el mensaje:

```text
v3.6: añade motor de reglas para analisis defensivo de logs
```

En ese checkpoint:

```text
HEAD -> main
```

se encontraba un commit por delante de:

```text
origin/main
```

y el árbol de trabajo estaba limpio.

Posteriormente comenzó el cierre documental de v3.6.

---

## 44. Resultado de v3.6

v3.6 transforma el analizador de logs desde una implementación con patrones internos hacia un pequeño motor declarativo.

Antes:

```text
analizador_logs.py
├── patrones
├── severidades
├── análisis
└── correlación
```

Después:

```text
reglas_logs.py
├── reglas
├── patrones
└── evaluación

analizador_logs.py
├── análisis
├── eventos
├── resumen
└── correlación
```

Esto reduce responsabilidades y mejora la capacidad de ampliación.

---

## 45. Próximos pasos

El siguiente paso no debe consistir simplemente en añadir reglas indefinidamente.

Antes de iniciar v3.7 conviene evaluar qué evolución aporta más valor al aprendizaje y al portfolio.

Posibles líneas futuras incluyen:

```text
normalización de eventos
configuración externa de reglas
nuevos tipos de detección
mejor control de falsos positivos
estadísticas de reglas
informes de seguridad
correlación más avanzada
niveles de severidad más estructurados
```

El alcance concreto de v3.7 deberá decidirse después de cerrar oficialmente v3.6.

---

## 46. Conclusión

FileOrganizer v3.6 supone un nuevo paso en la evolución del proyecto hacia ciberseguridad defensiva.

La versión no se limita a añadir dos nuevas detecciones.

El cambio principal es arquitectónico:

```text
las amenazas dejan de estar
embebidas en el analizador
```

y pasan a formar parte de:

```text
un catálogo declarativo de reglas
```

El proyecto dispone ahora de:

```text
reglas identificables
patrones independientes
severidades
descripciones
eventos enriquecidos
detección múltiple
correlación existente
tests específicos
integración con la UI
```

Todo ello se ha construido incrementalmente mediante TDD y manteniendo la regresión del proyecto bajo control.

El resultado final de v3.6 es una base más modular y extensible para continuar estudiando Python, testing, arquitectura de software y análisis defensivo de seguridad.