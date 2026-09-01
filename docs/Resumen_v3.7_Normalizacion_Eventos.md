# FileOrganizer v3.7 — Normalización de eventos de seguridad

## 1. Objetivo de la versión

La versión v3.7 de FileOrganizer continúa la evolución del sistema de análisis defensivo de logs iniciada en versiones anteriores.

v3.6 introdujo un motor declarativo de reglas mediante:

```text
core/reglas_logs.py
```

Con ese cambio se consiguió separar la definición de las amenazas de la lógica encargada de analizar los archivos de log.

Sin embargo, después de cerrar v3.6 todavía quedaba una responsabilidad dentro de:

```text
core/analizador_logs.py
```

El propio analizador seguía construyendo directamente los diccionarios que representaban los eventos de seguridad.

La estructura era conceptualmente:

```text
línea de log
     │
     ▼
analizador_logs.py
     │
     ├── evalúa reglas
     ├── extrae IP
     ├── extrae información
     │
     └── construye manualmente el evento
```

v3.7 tiene como objetivo separar también esta última responsabilidad.

Para ello se introduce un nuevo módulo:

```text
core/eventos.py
```

encargado de construir y validar una representación normalizada de los eventos de seguridad.

El nuevo flujo pasa a ser:

```text
línea de log
     │
     ▼
analizador_logs.py
     │
     ├── reglas_logs.py
     │       │
     │       └── determina qué se ha detectado
     │
     └── eventos.py
             │
             └── determina cómo se representa
```

El objetivo de v3.7 no es añadir simplemente otro tipo de ataque.

El cambio principal es arquitectónico:

```text
DETECCIÓN
    +
NORMALIZACIÓN DE EVENTOS
```

De esta forma FileOrganizer continúa evolucionando hacia un sistema defensivo más modular, donde cada componente tiene una responsabilidad más claramente definida.

---

## 2. Punto de partida desde v3.6

v3.6 dejó el sistema de análisis de logs con una arquitectura basada en reglas.

El nuevo módulo:

```text
core/reglas_logs.py
```

pasó a contener las definiciones de detección.

Entre las reglas existentes se encuentran detecciones relacionadas con:

```text
SQL Injection
fallos de autenticación
Path Traversal
Command Injection
```

Cada regla dispone de información estructurada como:

```text
id
tipo
severidad
descripcion
patrones
```

El analizador puede evaluar una línea contra todas las reglas disponibles y obtener aquellas que coinciden.

Conceptualmente:

```text
                 línea
                   │
                   ▼
        evaluar_linea_con_reglas()
                   │
                   ▼
           reglas coincidentes
                   │
                   ▼
             analizar_linea()
```

Además, el analizador ya disponía de otras capacidades desarrolladas anteriormente:

- extracción de direcciones IPv4;
- lectura de archivos de log;
- análisis línea por línea;
- extracción de fechas Apache;
- conversión de fechas a `datetime`;
- agrupación de eventos por IP;
- correlación de intentos de autenticación;
- correlación temporal de fuerza bruta;
- generación de resúmenes;
- integración con la interfaz de usuario.

Por tanto, v3.7 parte de un sistema funcional.

El problema no estaba en que FileOrganizer no pudiera detectar eventos.

El problema estaba en cómo se representaban esos eventos después de ser detectados.

---

## 3. Problema de la construcción manual de eventos

Después de v3.6, `analizar_linea()` obtenía las reglas coincidentes y construía directamente un diccionario por cada detección.

La lógica tenía una estructura equivalente a:

```python
eventos.append(
    {
        "linea": numero_linea,
        "ip": extraer_ip(linea),
        "tipo": regla["tipo"],
        "severidad": regla["severidad"],
        "regla": regla["id"],
        "descripcion": regla["descripcion"],
        "contenido": linea.rstrip("\n"),
    }
)
```

Este código funcionaba.

Sin embargo, introducía un problema de diseño.

`analizador_logs.py` tenía que conocer simultáneamente:

```text
cómo analizar una línea
cómo evaluar reglas
cómo extraer una IP
cómo procesar fechas
cómo correlacionar eventos
qué campos debe tener un evento
cómo construir ese evento
```

La representación de un evento estaba implícita dentro del propio analizador.

No existía un punto central que definiera:

```text
¿Qué campos debe tener un evento de seguridad?
```

Tampoco existía un componente responsable de validar que esos campos fueran coherentes.

Esto podía convertirse en un problema a medida que FileOrganizer evolucionara.

Por ejemplo, distintos componentes podrían terminar generando estructuras como:

```text
evento A
├── ip
├── tipo
└── contenido
```

mientras otro componente podría generar:

```text
evento B
├── linea
├── ip
├── severidad
├── regla
└── contenido
```

Aunque ambos fueran considerados "eventos", no compartirían necesariamente el mismo contrato.

v3.7 busca evitar esa situación.

La solución consiste en centralizar la construcción de eventos.

---

## 4. Diseño de v3.7

La arquitectura propuesta introduce:

```text
core/eventos.py
```

Este módulo contiene el constructor:

```python
crear_evento_seguridad()
```

A partir de v3.7, `analizar_linea()` deja de construir directamente el diccionario.

En su lugar proporciona al constructor los datos necesarios:

```text
numero de línea
IP
regla detectada
contenido original
fecha normalizada
```

El constructor se encarga de producir la estructura definitiva.

El flujo queda:

```text
             línea de log
                  │
                  ▼
          analizar_linea()
                  │
          ┌───────┴────────┐
          │                │
          ▼                ▼
   extraer datos      evaluar reglas
                           │
                           ▼
                    regla coincidente
                           │
          ┌────────────────┘
          │
          ▼
 crear_evento_seguridad()
          │
          ▼
   evento normalizado
```

Esta separación permite establecer una frontera clara.

`analizador_logs.py` responde principalmente a:

```text
¿Qué ocurre en esta línea?
```

`reglas_logs.py` responde a:

```text
¿Qué condiciones representan una detección?
```

`eventos.py` responde a:

```text
¿Cómo debe representarse una detección?
```

Esta división será una de las ideas arquitectónicas centrales de v3.7.

---

## 5. Separación de responsabilidades

Uno de los objetivos de las últimas versiones de FileOrganizer ha sido reducir progresivamente la cantidad de responsabilidades concentradas en un mismo módulo.

La evolución puede verse desde varias versiones.

v3.5 trabajó principalmente la separación entre:

```text
interfaz
    │
    └── ui/

lógica
    │
    └── core/
```

v3.6 separó:

```text
procesamiento de logs
        │
        └── analizador_logs.py

definición de detecciones
        │
        └── reglas_logs.py
```

v3.7 añade una nueva separación:

```text
representación de eventos
        │
        └── eventos.py
```

El resultado conceptual es:

```text
core/
│
├── analizador_logs.py
│   └── analiza y correlaciona
│
├── reglas_logs.py
│   └── define y evalúa reglas
│
└── eventos.py
    └── construye y valida eventos
```

Esto aplica el principio de separación de responsabilidades.

En lugar de tener un gran módulo encargado de todas las operaciones relacionadas con seguridad, se crean componentes especializados.

Una ventaja importante es que cada componente puede probarse de forma independiente.

Por ejemplo:

```text
test_reglas_logs.py
        │
        └── prueba el motor de reglas

test_eventos.py
        │
        └── prueba el contrato de eventos

test_analizador_logs_eventos.py
        │
        └── prueba la integración
```

Esta separación también facilita localizar errores.

Si una regla no detecta correctamente:

```text
reglas_logs.py
```

es el primer componente a revisar.

Si una detección existe pero el evento está mal construido:

```text
eventos.py
```

es el componente responsable.

Si ambos funcionan individualmente pero no trabajan correctamente juntos:

```text
analizador_logs.py
```

o sus tests de integración permiten investigar la conexión.

---

## 6. Nuevo módulo core/eventos.py

v3.7 incorpora un nuevo archivo:

```text
core/eventos.py
```

Su contenido actual está deliberadamente concentrado en una única responsabilidad.

La función principal es:

```python
def crear_evento_seguridad(
    linea,
    ip,
    regla,
    contenido,
    fecha=None,
):
```

El constructor realiza dos operaciones fundamentales:

```text
1. validar datos esenciales
2. construir la representación normalizada
```

Las validaciones actuales comprueban:

```text
regla completa
tipo del número de línea
valor del número de línea
tipo del contenido
```

Después de superar las validaciones, se devuelve un diccionario con la estructura:

```python
{
    "linea": linea,
    "ip": ip,
    "tipo": regla["tipo"],
    "severidad": regla["severidad"],
    "regla": regla["id"],
    "descripcion": regla["descripcion"],
    "contenido": contenido,
    "fecha": fecha,
}
```

Aunque el módulo es pequeño, su importancia arquitectónica es mayor que su número de líneas.

Antes de v3.7 el contrato estaba distribuido implícitamente en el código consumidor.

Ahora existe un lugar concreto donde puede observarse cómo se representa un evento.

Esto permite que futuras modificaciones del contrato tengan un punto de entrada claramente identificado.

---

## 7. Qué es un evento de seguridad

Dentro de FileOrganizer, un evento de seguridad representa una detección producida durante el análisis de una línea de log.

Por ejemplo, una línea podría contener:

```text
192.168.1.30 - - [16/Aug/2026:09:01:16] UNION SELECT username FROM users
```

El sistema puede detectar que la línea coincide con una regla relacionada con SQL Injection.

Sin embargo, la coincidencia de una regla y un evento no son exactamente lo mismo.

La regla describe:

```text
qué buscamos
```

El evento describe:

```text
qué hemos encontrado
```

Esta diferencia es importante.

Una regla puede contener:

```text
id = WEB_SQL_001
tipo = SQL_INJECTION
severidad = ALTA
descripcion = Posible intento de SQL Injection
```

Pero cuando esa regla coincide con una línea real necesitamos añadir contexto.

Por ejemplo:

```text
línea donde ocurrió
IP encontrada
contenido que produjo la detección
fecha del evento
```

Por tanto:

```text
REGLA
  │
  │ se aplica sobre
  ▼
LÍNEA DE LOG
  │
  │ produce
  ▼
EVENTO
```

La regla es una definición.

El evento es una instancia concreta de una detección.

Esta distinción es fundamental en sistemas de monitorización de seguridad.

---

## 8. Contrato del evento normalizado

v3.7 establece una estructura común para los eventos creados mediante `crear_evento_seguridad()`.

Actualmente el contrato contiene ocho campos:

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

Podemos agruparlos conceptualmente.

### Localización

```text
linea
```

Indica en qué línea del archivo analizado se produjo la detección.

### Origen

```text
ip
```

Representa la dirección IPv4 extraída cuando existe.

### Clasificación

```text
tipo
severidad
regla
descripcion
```

Estos campos proceden de la regla que generó la detección.

### Evidencia

```text
contenido
```

Conserva el contenido de la línea analizada.

### Información temporal

```text
fecha
```

Contiene el instante extraído del log y convertido a `datetime` cuando existe una fecha compatible.

La estructura completa puede representarse como:

```text
EVENTO
│
├── localización
│   └── linea
│
├── origen
│   └── ip
│
├── clasificación
│   ├── tipo
│   ├── severidad
│   ├── regla
│   └── descripcion
│
├── evidencia
│   └── contenido
│
└── tiempo
    └── fecha
```

Esta normalización permite que las funciones posteriores trabajen con una estructura conocida.

Por ejemplo, la correlación temporal puede consultar:

```python
evento["fecha"]
```

sin tener que considerar la fecha únicamente como texto incrustado dentro del contenido original.

---

## 9. Función crear_evento_seguridad()

La función central de v3.7 es:

```python
crear_evento_seguridad()
```

Su responsabilidad es recibir los datos obtenidos durante el análisis y devolver un evento con el contrato establecido.

La firma actual es:

```python
def crear_evento_seguridad(
    linea,
    ip,
    regla,
    contenido,
    fecha=None,
):
```

El flujo interno puede resumirse como:

```text
             datos de entrada
                    │
                    ▼
          validar regla completa
                    │
                    ▼
          validar tipo de línea
                    │
                    ▼
         validar valor de línea
                    │
                    ▼
        validar tipo de contenido
                    │
                    ▼
          construir diccionario
                    │
                    ▼
           evento normalizado
```

La función no intenta detectar ataques.

Tampoco analiza archivos.

No evalúa expresiones regulares.

No busca direcciones IP.

No realiza correlación temporal.

Todas esas responsabilidades pertenecen a otros componentes.

Su responsabilidad es mucho más concreta:

```text
construir correctamente un evento
```

Esto hace que la función sea sencilla de probar mediante tests unitarios.

Dado un conjunto determinado de entradas, podemos verificar exactamente:

```text
qué estructura devuelve
```

o:

```text
qué excepción produce
```

---

## 10. Parámetros del constructor

`crear_evento_seguridad()` recibe cinco parámetros.

Cuatro son obligatorios:

```text
linea
ip
regla
contenido
```

y uno dispone de valor por defecto:

```text
fecha=None
```

### linea

Representa el número de línea dentro del archivo de log.

Ejemplo:

```python
linea=10
```

Debe ser un entero positivo.

---

### ip

Contiene la dirección IPv4 asociada a la línea cuando ha podido extraerse.

Ejemplo:

```python
ip="192.168.1.30"
```

También puede ser:

```python
ip=None
```

porque la presencia de una IP no es obligatoria para que exista una detección.

---

### regla

Es el diccionario que representa la regla coincidente.

Debe proporcionar al menos:

```text
id
tipo
severidad
descripcion
```

Por ejemplo:

```python
regla = {
    "id": "WEB_SQL_001",
    "tipo": "SQL_INJECTION",
    "severidad": "ALTA",
    "descripcion": "Posible intento de SQL Injection",
}
```

El constructor utiliza estos datos para enriquecer el evento.

---

### contenido

Representa la evidencia textual que originó la detección.

Por ejemplo:

```python
contenido="UNION SELECT username FROM users"
```

Debe ser una cadena de texto.

Esto permite conservar el contexto que produjo el evento.

---

### fecha

Representa la información temporal normalizada.

Puede contener un objeto:

```python
datetime
```

o:

```python
None
```

Su valor por defecto es:

```python
fecha=None
```

Esta decisión permite que el constructor siga funcionando con líneas que no contienen información temporal.

También facilita la evolución desde los eventos anteriores a v3.7, donde el campo `fecha` todavía no formaba parte explícita de la estructura generada por `analizar_linea()`.

---

Hasta este punto, v3.7 ya establece las dos bases fundamentales de la versión:

```text
core/eventos.py
        +
contrato normalizado
```

Los siguientes apartados profundizan individualmente en cada campo, las validaciones introducidas mediante TDD y la integración de la fecha normalizada con el sistema de correlación temporal.
## 11. Campo linea

El campo:

```text
linea
```

identifica la posición de la línea que produjo el evento dentro del archivo de log analizado.

Por ejemplo:

```python
"linea": 10
```

Este dato permite relacionar posteriormente una detección con su posición exacta dentro de la fuente original.

Cuando `analizar_log()` procesa un archivo utiliza:

```python
enumerate(
    archivo,
    start=1,
)
```

Por tanto, las líneas utilizadas por el sistema comienzan en:

```text
1
```

y no en:

```text
0
```

Esto explica una de las reglas del contrato introducidas en v3.7:

```text
linea >= 1
```

Un evento con:

```python
linea=0
```

no representa una posición válida dentro del modelo utilizado por FileOrganizer.

El número de línea forma parte además de las alertas generadas por la correlación temporal.

Esto permite conservar información sobre qué eventos individuales participaron en una detección correlacionada.

Conceptualmente:

```text
archivo.log
│
├── línea 1
├── línea 2
├── línea 3  ──► evento
├── línea 4  ──► evento
└── línea 5  ──► evento
                     │
                     ▼
                 correlación
                     │
                     ▼
              líneas [3, 4, 5]
```

Por tanto, `linea` no es únicamente información auxiliar.

También permite mantener trazabilidad entre:

```text
evento
    ↕
fuente original
```

---

## 12. Campo ip

El campo:

```text
ip
```

almacena la dirección IPv4 asociada al evento cuando puede extraerse de la línea analizada.

Por ejemplo:

```python
"ip": "192.168.1.30"
```

La extracción sigue siendo responsabilidad de:

```python
extraer_ip()
```

dentro de:

```text
core/analizador_logs.py
```

El constructor de eventos no intenta localizar una dirección IP.

Recibe el resultado ya procesado:

```python
crear_evento_seguridad(
    linea=numero_linea,
    ip=extraer_ip(linea),
    ...
)
```

Esta separación es importante.

`eventos.py` no necesita conocer:

```text
expresiones regulares IPv4
formato de los logs
posición de la IP
```

Solo necesita recibir el valor correspondiente.

Además, v3.7 establece deliberadamente que una IP puede estar ausente.

Por tanto, ambos valores son compatibles con el contrato:

```python
"ip": "192.168.1.30"
```

y:

```python
"ip": None
```

Esto refleja una característica real del análisis de logs:

```text
no todo evento contiene necesariamente una dirección IP
```

Una detección puede seguir siendo válida aunque no pueda atribuirse inmediatamente a una dirección de origen.

---

## 13. Campo tipo

El campo:

```text
tipo
```

representa la categoría de seguridad asociada a la detección.

Su valor procede directamente de:

```python
regla["tipo"]
```

Por ejemplo:

```text
SQL_INJECTION
FUERZA_BRUTA
PATH_TRAVERSAL
COMMAND_INJECTION
```

El constructor no decide qué tipo corresponde al evento.

Esa decisión pertenece a la regla que ha coincidido.

El flujo es:

```text
reglas_logs.py
      │
      │ define
      ▼
    tipo
      │
      ▼
evento normalizado
```

Por ejemplo, si una regla contiene:

```python
{
    "id": "WEB_SQL_001",
    "tipo": "SQL_INJECTION",
    ...
}
```

el evento resultante contiene:

```python
"tipo": "SQL_INJECTION"
```

Esto mantiene una relación directa entre:

```text
clasificación de la regla
          │
          ▼
clasificación del evento
```

El campo `tipo` es utilizado posteriormente por otros componentes.

Un ejemplo especialmente importante es la correlación temporal de fuerza bruta:

```python
if evento["tipo"] != "FUERZA_BRUTA":
    continue
```

Por tanto, la normalización del campo permite que otros componentes procesen eventos según su categoría.

---

## 14. Campo severidad

El campo:

```text
severidad
```

indica la importancia asignada a la detección.

Su valor también procede de la regla:

```python
regla["severidad"]
```

Por ejemplo:

```text
MEDIA
ALTA
```

El constructor copia esta información al evento:

```python
"severidad": regla["severidad"]
```

La separación entre regla y evento vuelve a ser importante.

La regla establece la severidad prevista para una determinada detección.

Cuando esa regla coincide, el evento conserva esa clasificación.

Conceptualmente:

```text
REGLA
│
└── severidad = ALTA
          │
          ▼
      coincidencia
          │
          ▼
EVENTO
│
└── severidad = ALTA
```

De esta manera, los componentes consumidores no necesitan volver a consultar el catálogo de reglas para conocer la severidad del evento.

El propio evento contiene la información necesaria.

---

## 15. Campo regla

El campo:

```text
regla
```

permite conocer exactamente qué regla produjo la detección.

Su valor procede de:

```python
regla["id"]
```

Por ejemplo:

```python
"regla": "WEB_SQL_001"
```

Este campo fue introducido previamente como parte del enriquecimiento de eventos de v3.6 y se conserva dentro del contrato normalizado de v3.7.

La diferencia entre:

```text
tipo
```

y:

```text
regla
```

es importante.

El tipo representa una categoría:

```text
SQL_INJECTION
```

mientras que la regla representa una definición concreta:

```text
WEB_SQL_001
```

Conceptualmente:

```text
tipo
└── familia de detección

regla
└── detector concreto que produjo el evento
```

Esta distinción permite que en el futuro puedan existir varias reglas asociadas al mismo tipo de amenaza.

Por ejemplo, conceptualmente podría existir:

```text
SQL_INJECTION
├── WEB_SQL_001
├── WEB_SQL_002
└── WEB_SQL_003
```

sin necesidad de cambiar la categoría general del evento.

---

## 16. Campo descripcion

El campo:

```text
descripcion
```

proporciona una explicación legible de la detección.

Procede de:

```python
regla["descripcion"]
```

Por ejemplo:

```text
Posible intento de SQL Injection
```

Mientras campos como:

```text
tipo
regla
```

están especialmente orientados al procesamiento estructurado, `descripcion` facilita la interpretación humana del evento.

El evento puede contener simultáneamente:

```text
tipo        = SQL_INJECTION
regla       = WEB_SQL_001
descripcion = Posible intento de SQL Injection
```

Cada campo tiene una función diferente:

```text
tipo
└── clasificación

regla
└── identificación

descripcion
└── explicación
```

Esta combinación resulta útil para interfaces, informes y futuras funcionalidades de auditoría.

---

## 17. Campo contenido

El campo:

```text
contenido
```

conserva la evidencia textual asociada al evento.

Durante la integración con `analizar_linea()` se proporciona mediante:

```python
contenido=linea.rstrip("\n")
```

Esto elimina el salto de línea final procedente de la lectura del archivo, pero conserva el contenido analizado.

Por ejemplo:

```text
192.168.1.20 - - [16/Aug/2026:09:01:16] Failed password
```

El campo es importante porque permite conservar evidencia contextual.

Un evento estructurado puede indicar:

```text
tipo = FUERZA_BRUTA
ip = 192.168.1.20
```

pero `contenido` permite observar también qué línea concreta produjo esa detección.

En v3.7 este campo adquiere además otra importancia relacionada con la compatibilidad.

Los eventos anteriores no disponían necesariamente de:

```text
fecha
```

normalizada.

La correlación temporal histórica extraía la fecha desde:

```python
evento["contenido"]
```

Por este motivo, v3.7 mantiene el contenido original y conserva un mecanismo de fallback para eventos que todavía no contienen fecha normalizada.

---

## 18. Campo fecha

Una de las ampliaciones más importantes del contrato en v3.7 es:

```text
fecha
```

Antes de esta versión, la fecha podía existir dentro del contenido textual:

```text
[16/Aug/2026:09:01:16]
```

pero no formaba parte explícita del evento construido por `analizar_linea()`.

Esto obligaba a determinados consumidores a volver a procesar:

```python
evento["contenido"]
```

para recuperar información temporal.

v3.7 cambia este diseño.

Cuando `analizar_linea()` procesa una línea realiza:

```python
fecha_texto = extraer_fecha_log(linea)
fecha = convertir_fecha_log(fecha_texto)
```

y posteriormente proporciona el resultado al constructor:

```python
crear_evento_seguridad(
    ...
    fecha=fecha,
)
```

El evento puede contener entonces:

```python
"fecha": datetime(...)
```

Si no existe una fecha compatible:

```python
"fecha": None
```

Esto supone una normalización importante.

La información deja de existir únicamente como texto:

```text
"16/Aug/2026:09:01:16"
```

y pasa a disponer también de una representación preparada para operaciones temporales:

```python
datetime(
    2026,
    8,
    16,
    9,
    1,
    16,
)
```

Esto permite realizar posteriormente:

```text
ordenación
comparación
diferencias temporales
correlación
```

sin tener que volver a interpretar el texto cada vez.

---

## 19. Validación de la regla

El constructor necesita determinados campos de la regla para poder generar el evento.

Los campos obligatorios son:

```text
id
tipo
severidad
descripcion
```

En `core/eventos.py` se representan mediante un conjunto:

```python
campos_obligatorios = {
    "id",
    "tipo",
    "severidad",
    "descripcion",
}
```

La comprobación utiliza:

```python
if not campos_obligatorios <= regla.keys():
    raise ValueError("Regla incompleta")
```

Aquí se utiliza una operación de conjuntos.

La expresión:

```python
campos_obligatorios <= regla.keys()
```

comprueba si todos los elementos de `campos_obligatorios` están presentes entre las claves de la regla.

Conceptualmente:

```text
campos requeridos
{id, tipo, severidad, descripcion}

                ⊆

claves disponibles en regla
```

Si falta cualquiera de ellos, el constructor no puede garantizar el contrato.

Por ejemplo:

```python
regla = {
    "id": "WEB_SQL_001",
    "tipo": "SQL_INJECTION",
    "severidad": "ALTA",
}
```

no contiene:

```text
descripcion
```

y por tanto produce:

```text
ValueError: Regla incompleta
```

Esta validación evita esperar a que el código llegue posteriormente a:

```python
regla["descripcion"]
```

y falle indirectamente con un `KeyError`.

En su lugar, el constructor detecta explícitamente que la entrada no cumple su contrato.

---

## 20. Diferencia entre TypeError y ValueError

Durante el desarrollo de v3.7 apareció una distinción importante relacionada con las excepciones.

No todos los datos inválidos representan el mismo tipo de problema.

Python diferencia conceptualmente entre:

```text
tipo incorrecto
```

y:

```text
valor incorrecto
```

Para ello existen dos excepciones especialmente relevantes:

```python
TypeError
ValueError
```

### TypeError

Se utiliza cuando el tipo del objeto recibido no es el esperado.

Por ejemplo, el número de línea debe ser:

```python
int
```

Si se recibe:

```python
linea="10"
```

el valor parece representar un número, pero su tipo real es:

```python
str
```

Por tanto:

```python
raise TypeError("Línea inválida")
```

Otro ejemplo es `contenido`.

Debe ser:

```python
str
```

Si recibe:

```python
contenido=None
```

el problema es el tipo.

Por tanto:

```python
raise TypeError("Contenido inválido")
```

### ValueError

Se utiliza cuando el tipo es correcto pero el valor no cumple las restricciones del contrato.

Por ejemplo:

```python
linea=0
```

es efectivamente un:

```python
int
```

pero no es válido porque FileOrganizer numera las líneas desde 1.

Por tanto:

```python
raise ValueError("Línea inválida")
```

La diferencia puede resumirse así:

```text
linea="10"
     │
     └── tipo incorrecto
             │
             ▼
          TypeError


linea=0
     │
     └── tipo correcto, valor incorrecto
             │
             ▼
          ValueError
```

Esta distinción apareció también durante el ciclo TDD.

Inicialmente, una validación podía hacer conjuntamente:

```python
if not isinstance(linea, int) or linea < 1:
    raise ValueError("Línea inválida")
```

Sin embargo, eso hacía que ambos errores se representaran mediante la misma excepción.

La separación definitiva quedó conceptualmente:

```python
if not isinstance(linea, int):
    raise TypeError("Línea inválida")

if linea < 1:
    raise ValueError("Línea inválida")
```

Ruff también ayudó durante el desarrollo a detectar el uso inadecuado de `ValueError` para un problema de tipo en la validación del contenido.

Esto convierte un detalle aparentemente pequeño en una lección importante de diseño de APIs:

```text
las excepciones también forman parte del contrato de una función
```

Un consumidor puede distinguir entre:

```text
he recibido el tipo de objeto equivocado
```

y:

```text
he recibido el tipo correcto con un valor no permitido
```

v3.7 aplica esta distinción explícitamente dentro del nuevo constructor de eventos.
## 21. Validación del número de línea

El campo:

```text
linea
```

tiene dos condiciones dentro del contrato de eventos:

```text
debe ser un entero
debe ser mayor o igual que 1
```

Estas condiciones se validan independientemente:

```python
if not isinstance(linea, int):
    raise TypeError("Línea inválida")

if linea < 1:
    raise ValueError("Línea inválida")
```

La primera comprobación protege el tipo.

La segunda protege el rango permitido.

Esto permite distinguir situaciones diferentes.

Un valor como:

```python
linea="10"
```

no es válido porque:

```text
type("10") == str
```

mientras que:

```python
linea=0
```

sí tiene el tipo correcto:

```text
int
```

pero está fuera del dominio aceptado.

Los tests de v3.7 caracterizan ambos comportamientos por separado:

```text
test_crear_evento_seguridad_rechaza_linea_invalida
test_crear_evento_seguridad_rechaza_tipo_linea_invalido
```

Esta separación mejora el contrato de la función porque no se limita a comprobar que "algo está mal".

Especifica qué clase de error se ha producido.

El diseño queda:

```text
              linea
                │
                ▼
        ¿es un entero?
          │           │
         NO           SÍ
          │           │
          ▼           ▼
     TypeError    ¿linea >= 1?
                    │      │
                   NO      SÍ
                    │      │
                    ▼      ▼
               ValueError válido
```

---

## 22. Validación del contenido

El parámetro:

```text
contenido
```

representa la evidencia textual que produjo el evento.

Por este motivo, el constructor exige que sea:

```python
str
```

La validación implementada es:

```python
if not isinstance(contenido, str):
    raise TypeError("Contenido inválido")
```

Por ejemplo:

```python
contenido=None
```

produce:

```text
TypeError: Contenido inválido
```

Esta validación fue especialmente útil durante el desarrollo mediante TDD.

El test introducido esperaba inicialmente que el constructor rechazara un contenido inválido.

Después de implementar la comprobación utilizando `ValueError`, Ruff señaló:

```text
TRY004 Prefer `TypeError` exception for invalid type
```

Esto permitió mejorar inmediatamente el diseño.

El problema no era que:

```python
None
```

fuera un valor textual no permitido.

El problema era que:

```python
None
```

no era texto.

Por tanto, la excepción semánticamente correcta era:

```python
TypeError
```

Este ciclo muestra cómo en FileOrganizer se combinan dos herramientas diferentes:

```text
pytest
│
└── verifica comportamiento

Ruff
│
└── detecta problemas de calidad y semántica
```

Ambas contribuyeron a definir el contrato final.

---

## 23. IP opcional y eventos sin dirección origen

Una decisión explícita de v3.7 es permitir:

```python
ip=None
```

El constructor no rechaza un evento simplemente porque no exista una dirección IPv4.

Esto se verifica mediante:

```text
test_crear_evento_seguridad_permite_ip_ausente
```

La razón es que la presencia de una IP y la existencia de un evento son conceptos diferentes.

Puede existir una línea relevante como:

```text
Failed login
```

sin que esa línea incluya necesariamente una dirección IPv4.

Si una regla coincide, la detección sigue existiendo.

La información disponible podría ser:

```text
tipo       = FUERZA_BRUTA
severidad  = MEDIA
regla      = AUTH_FAIL_001
contenido  = Failed login
ip         = None
```

Rechazar ese evento provocaría pérdida de información.

Por tanto, el contrato distingue entre:

```text
campo existente
```

y:

```text
dato disponible
```

El campo `ip` forma parte del evento, pero su valor puede ser `None`.

Conceptualmente:

```text
              EVENTO
                 │
                 ▼
            campo ip
             │      │
             │      └── None
             │
             └── "192.168.1.20"
```

Esta decisión hace el modelo más flexible ante diferentes formatos de logs.

---

## 24. Fecha opcional y compatibilidad

El parámetro temporal se definió como:

```python
fecha=None
```

en la firma:

```python
def crear_evento_seguridad(
    linea,
    ip,
    regla,
    contenido,
    fecha=None,
):
```

El valor por defecto tiene dos consecuencias importantes.

La primera es que una línea sin fecha sigue pudiendo generar un evento.

Por ejemplo:

```text
192.168.1.20 Failed password
```

puede producir:

```python
{
    ...
    "fecha": None,
}
```

La segunda consecuencia es la compatibilidad con llamadas que no proporcionan explícitamente el nuevo argumento.

El constructor puede utilizarse como:

```python
crear_evento_seguridad(
    linea=10,
    ip="192.168.1.30",
    regla=regla,
    contenido="UNION SELECT",
)
```

sin necesidad de escribir:

```python
fecha=None
```

El resultado sigue incluyendo el campo:

```python
"fecha": None
```

Esto permite que el contrato del evento sea estable:

```text
evento con fecha
└── fecha = datetime(...)

evento sin fecha
└── fecha = None
```

En ambos casos existe la misma clave.

La diferencia está únicamente en su valor.

---

## 25. Integración con analizar_linea()

Después de construir y probar `core/eventos.py`, el siguiente paso de v3.7 fue integrarlo con:

```python
analizar_linea()
```

dentro de:

```text
core/analizador_logs.py
```

Para ello se añadió:

```python
from core.eventos import crear_evento_seguridad
```

El analizador sigue obteniendo las reglas coincidentes mediante:

```python
reglas_coincidentes = evaluar_linea_con_reglas(
    linea,
    REGLAS_DETECCION,
)
```

Pero la construcción del evento cambia.

En lugar de crear directamente el diccionario, utiliza:

```python
crear_evento_seguridad(
    linea=numero_linea,
    ip=extraer_ip(linea),
    regla=regla,
    contenido=linea.rstrip("\n"),
    fecha=fecha,
)
```

La función `analizar_linea()` actúa ahora como coordinadora de varios componentes:

```text
                   analizar_linea()
                         │
             ┌───────────┼───────────┐
             │           │           │
             ▼           ▼           ▼
        extraer_ip   reglas_logs   fecha
                         │
                         ▼
                  reglas coincidentes
                         │
                         ▼
                    eventos.py
                         │
                         ▼
                evento normalizado
```

Esto reduce el conocimiento que el analizador necesita tener sobre la estructura interna del evento.

---

## 26. Eliminación de la construcción manual

Antes de v3.7, `analizar_linea()` contenía directamente una estructura equivalente a:

```python
{
    "linea": numero_linea,
    "ip": extraer_ip(linea),
    "tipo": regla["tipo"],
    "severidad": regla["severidad"],
    "regla": regla["id"],
    "descripcion": regla["descripcion"],
    "contenido": linea.rstrip("\n"),
}
```

Después de v3.7 esa responsabilidad desaparece del analizador.

Ahora se utiliza:

```python
crear_evento_seguridad(...)
```

Este cambio evita duplicar conocimiento.

Antes:

```text
analizador_logs.py
│
├── sabe qué campos tiene un evento
├── sabe de dónde obtenerlos
└── construye la estructura
```

Después:

```text
analizador_logs.py
│
└── proporciona los datos

eventos.py
│
└── conoce el contrato
```

Esto es importante porque, si el contrato cambia en el futuro, existe un componente específico responsable de su construcción.

Por ejemplo, v3.7 añadió:

```text
fecha
```

La existencia de `eventos.py` proporciona una ubicación natural para representar ese nuevo campo.

La modificación no consiste únicamente en reducir unas líneas de código.

Consiste en mover una responsabilidad al módulo que conceptualmente debe poseerla.

---

## 27. Extracción de fecha desde el log

FileOrganizer ya disponía antes de v3.7 de una función para extraer fechas de logs con formato similar a Apache:

```python
extraer_fecha_log()
```

El patrón utilizado reconoce estructuras como:

```text
[16/Aug/2026:09:01:16]
```

mediante:

```python
PATRON_FECHA_LOG = re.compile(
    r"\[(\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2})\]"
)
```

La función busca una coincidencia:

```python
coincidencia = PATRON_FECHA_LOG.search(linea)
```

Si existe devuelve el grupo capturado:

```python
return coincidencia.group(1)
```

Por tanto, una línea como:

```text
192.168.1.20 - - [16/Aug/2026:09:01:16] Failed password
```

produce:

```text
16/Aug/2026:09:01:16
```

Si la línea no contiene una fecha compatible:

```python
return None
```

v3.7 no reimplementa esta funcionalidad.

La reutiliza.

Este punto es importante desde el punto de vista arquitectónico:

```text
si una función existente ya tiene una responsabilidad bien definida,
no debe duplicarse su lógica
```

---

## 28. Conversión a datetime

Después de extraer la representación textual, FileOrganizer utiliza:

```python
convertir_fecha_log()
```

La función transforma:

```text
16/Aug/2026:09:01:16
```

en un objeto:

```python
datetime
```

mediante:

```python
datetime.strptime(
    fecha_texto,
    "%d/%b/%Y:%H:%M:%S",
)
```

El formato especifica:

```text
%d  → día
%b  → mes abreviado
%Y  → año
%H  → hora
%M  → minuto
%S  → segundo
```

Por tanto:

```text
16/Aug/2026:09:01:16
```

se convierte conceptualmente en:

```python
datetime(
    2026,
    8,
    16,
    9,
    1,
    16,
)
```

Si se proporciona:

```python
None
```

la función devuelve:

```python
None
```

Si se proporciona un texto con formato inválido:

```text
fecha-invalida
```

`datetime.strptime()` produce:

```python
ValueError
```

Este comportamiento ya estaba caracterizado mediante los tests temporales existentes y v3.7 lo reutiliza para normalizar el evento.

---

## 29. datetime naive y decisión de diseño

Las fechas utilizadas por el formato de log actualmente analizado no contienen información de zona horaria.

El ejemplo:

```text
16/Aug/2026:09:01:16
```

indica:

```text
fecha
hora
minuto
segundo
```

pero no indica algo como:

```text
UTC
+0200
Europe/Madrid
```

Por tanto, `convertir_fecha_log()` genera deliberadamente un:

```text
datetime naive
```

Un `datetime` naive es un objeto que no contiene información de zona horaria.

El código mantiene explícitamente esta decisión:

```python
return datetime.strptime(  # noqa: DTZ007
    fecha_texto,
    "%d/%b/%Y:%H:%M:%S",
)
```

Los tests también reflejan esta característica mediante:

```python
datetime(  # noqa: DTZ001
    2026,
    8,
    16,
    9,
    1,
    16,
)
```

El uso de:

```text
# noqa: DTZ007
# noqa: DTZ001
```

no pretende ocultar accidentalmente un problema.

Documenta una decisión consciente.

El log de origen no proporciona zona horaria.

Inventarla introduciría información que no existe en la fuente.

Para la correlación temporal interna actual es suficiente comparar fechas procedentes del mismo tipo de log y bajo la misma interpretación temporal.

Esto enseña una idea importante:

```text
normalizar datos no significa inventar datos
```

Si la fuente no contiene zona horaria, v3.7 conserva esa limitación explícitamente.

---

## 30. Evento enriquecido con fecha normalizada

La integración de las funciones temporales con el nuevo constructor produce uno de los cambios fundamentales de v3.7.

`analizar_linea()` realiza:

```python
fecha_texto = extraer_fecha_log(linea)
fecha = convertir_fecha_log(fecha_texto)
```

Después proporciona:

```python
fecha=fecha
```

a:

```python
crear_evento_seguridad()
```

Por tanto, una línea como:

```text
192.168.1.20 - - [16/Aug/2026:09:01:16] Failed password
```

puede terminar representada conceptualmente como:

```python
{
    "linea": 10,
    "ip": "192.168.1.20",
    "tipo": "FUERZA_BRUTA",
    "severidad": "MEDIA",
    "regla": "AUTH_FAIL_001",
    "descripcion": "Intento de autenticación fallido",
    "contenido": (
        "192.168.1.20 - - "
        "[16/Aug/2026:09:01:16] "
        "Failed password"
    ),
    "fecha": datetime(
        2026,
        8,
        16,
        9,
        1,
        16,
    ),
}
```

Ahora existen simultáneamente dos representaciones de la información temporal:

```text
contenido
│
└── evidencia original

fecha
│
└── representación normalizada
```

No son redundantes desde el punto de vista funcional.

El contenido conserva la evidencia.

La fecha permite operar con el tiempo.

Por ejemplo:

```text
EVIDENCIA
"16/Aug/2026:09:01:16"

        │ normalización
        ▼

DATETIME
2026-08-16 09:01:16

        │ procesamiento
        ▼

ordenar
comparar
restar
correlacionar
```

Esta transformación es especialmente importante para la siguiente parte de v3.7.

Hasta este momento, la correlación temporal recuperaba la fecha desde el contenido del evento.

Ahora que el evento dispone de una fecha normalizada, la correlación puede consumir directamente:

```python
evento["fecha"]
```

Ese cambio será el siguiente paso de la arquitectura de v3.7.
## 31. Problema de la correlación temporal anterior

Antes de v3.7, FileOrganizer ya disponía de correlación temporal para detectar posibles ataques de fuerza bruta.

La función:

```python
detectar_fuerza_bruta_temporal()
```

recibe una colección de eventos y busca múltiples intentos procedentes de una misma dirección IP dentro de una ventana temporal determinada.

Por ejemplo:

```text
192.168.1.20 → 09:01:16
192.168.1.20 → 09:01:17
192.168.1.20 → 09:01:18
```

Con:

```text
umbral = 3
ventana_segundos = 60
```

los tres eventos deben generar una alerta porque:

```text
09:01:18 - 09:01:16 = 2 segundos
```

y:

```text
2 <= 60
```

La correlación temporal ya funcionaba correctamente antes de v3.7.

Sin embargo, existía una característica arquitectónica que ahora podía mejorarse.

La fecha no formaba parte del contrato normalizado del evento.

Por este motivo, la correlación tenía que recuperar la información temporal desde:

```python
evento["contenido"]
```

El flujo era conceptualmente:

```text
evento
  │
  ▼
contenido completo
  │
  ▼
extraer_fecha_log()
  │
  ▼
texto de fecha
  │
  ▼
convertir_fecha_log()
  │
  ▼
datetime
  │
  ▼
correlación
```

Esto era funcional, pero significaba que una información que ya había estado presente en el log tenía que volver a extraerse cuando llegaba el momento de correlacionar.

Con la introducción de:

```python
evento["fecha"]
```

en v3.7, este comportamiento podía evolucionar.

El nuevo objetivo pasa a ser:

```text
evento normalizado
        │
        ▼
evento["fecha"]
        │
        ▼
correlación
```

La correlación deja así de depender obligatoriamente del formato textual del contenido.

---

## 32. RED 9 — La correlación debe utilizar la fecha normalizada

Para caracterizar el nuevo comportamiento se añadió un test específico:

```text
test_correlacion_temporal_utiliza_fecha_normalizada
```

El objetivo del test era importante.

No bastaba con comprobar que la correlación siguiera funcionando con eventos tradicionales.

Había que demostrar que podía trabajar utilizando exclusivamente:

```python
evento["fecha"]
```

Para ello se construyeron eventos cuyo contenido no tenía ninguna fecha:

```python
{
    "linea": 1,
    "ip": "192.168.1.20",
    "tipo": "FUERZA_BRUTA",
    "severidad": "MEDIA",
    "contenido": "sin fecha en contenido",
    "fecha": datetime(
        2026,
        8,
        16,
        9,
        0,
        0,
    ),
}
```

Los tres eventos del test contienen fechas normalizadas:

```text
09:00:00
09:00:10
09:00:20
```

pero el campo:

```text
contenido
```

contiene deliberadamente:

```text
sin fecha en contenido
```

Esto elimina cualquier posibilidad de que el test pase accidentalmente utilizando el mecanismo antiguo.

La condición esperada es:

```python
alertas = detectar_fuerza_bruta_temporal(
    eventos,
    umbral=3,
    ventana_segundos=60,
)
```

y posteriormente:

```python
assert len(alertas) == 1
assert alertas[0]["ip"] == "192.168.1.20"
assert alertas[0]["intentos"] == 3
```

La primera ejecución produjo:

```text
FAILED
```

con:

```text
assert 0 == 1
```

El resultado era correcto para la fase RED.

Demostraba que la correlación todavía dependía de:

```python
evento["contenido"]
```

para recuperar la fecha.

El nuevo campo:

```python
evento["fecha"]
```

todavía no estaba siendo utilizado.

---

## 33. Primer intento GREEN y error de alcance de variable

La primera adaptación de la correlación comenzó recuperando:

```python
fecha = evento.get("fecha")
```

y utilizando el mecanismo anterior solamente cuando la fecha no existiera.

La intención era:

```text
obtener evento["fecha"]

si existe:
    utilizarla

si no existe:
    extraer fecha desde contenido
```

Sin embargo, durante el primer cambio apareció un error de implementación.

La estructura quedó conceptualmente equivalente a:

```python
fecha = evento.get("fecha")

if fecha is None:
    fecha_texto = extraer_fecha_log(evento["contenido"])

fecha = convertir_fecha_log(fecha_texto)
```

Este código contiene un problema.

Cuando:

```python
fecha is not None
```

no se ejecuta:

```python
fecha_texto = ...
```

pero después se intenta utilizar igualmente:

```python
fecha_texto
```

Python produjo:

```text
UnboundLocalError
```

con un mensaje equivalente a:

```text
cannot access local variable 'fecha_texto'
where it is not associated with a value
```

Este fallo fue útil porque mostró claramente que existían dos caminos diferentes:

```text
CAMINO A
evento ya tiene datetime

CAMINO B
evento no tiene datetime
```

y únicamente el segundo necesita ejecutar:

```text
extraer_fecha_log()
convertir_fecha_log()
```

La estructura correcta no debía ser:

```text
obtener fecha

si falta:
    obtener fecha_texto

convertir fecha_texto siempre
```

sino:

```text
obtener fecha

si falta:
    obtener fecha_texto
    convertir fecha_texto
```

La conversión pertenece al fallback.

No al flujo principal.

---

## 34. GREEN 9 — Uso directo de evento["fecha"]

La implementación corregida quedó basada en:

```python
fecha = evento.get("fecha")

if fecha is None:
    fecha_texto = extraer_fecha_log(
        evento["contenido"]
    )

    fecha = convertir_fecha_log(
        fecha_texto
    )

if fecha is None:
    continue
```

Este bloque establece dos fuentes posibles para la información temporal.

La fuente principal es:

```python
evento.get("fecha")
```

La fuente secundaria es:

```python
evento["contenido"]
```

El flujo puede representarse como:

```text
                    evento
                       │
                       ▼
              evento.get("fecha")
                       │
              ┌────────┴────────┐
              │                 │
           datetime            None
              │                 │
              │                 ▼
              │         evento["contenido"]
              │                 │
              │                 ▼
              │       extraer_fecha_log()
              │                 │
              │                 ▼
              │       convertir_fecha_log()
              │                 │
              └────────┬────────┘
                       ▼
                     fecha
                       │
              ┌────────┴────────┐
              │                 │
           datetime            None
              │                 │
              ▼                 ▼
         correlacionar       ignorar
```

Después de esta corrección:

```text
test_correlacion_temporal_utiliza_fecha_normalizada
```

pasó correctamente.

La correlación ya no necesita que la fecha permanezca incrustada dentro del contenido textual cuando el evento dispone de una representación normalizada.

Esto introduce una mejora importante en el diseño.

Antes:

```text
correlación
    │
    ▼
depende del formato textual del log
```

Ahora:

```text
correlación
    │
    ▼
depende del contrato del evento
```

Esta segunda arquitectura es más flexible.

El sistema podría recibir en el futuro eventos procedentes de otra fuente que ya proporcionara un `datetime`, incluso aunque su contenido textual no utilizara el formato Apache actualmente reconocido.

---

## 35. Compatibilidad con eventos históricos

Modificar la correlación para utilizar exclusivamente:

```python
evento["fecha"]
```

habría introducido una ruptura innecesaria.

Los tests anteriores a v3.7 construían algunos eventos manualmente mediante una función auxiliar equivalente a:

```python
def crear_evento(ip, fecha, linea):
    return {
        "linea": linea,
        "ip": ip,
        "tipo": "FUERZA_BRUTA",
        "severidad": "MEDIA",
        "contenido": (
            f"{ip} - - [{fecha}] "
            '"POST /login HTTP/1.1" 401 Failed password'
        ),
    }
```

Estos eventos no contienen:

```python
"fecha"
```

como campo independiente.

La información temporal solamente existe dentro de:

```python
"contenido"
```

Por tanto, si v3.7 hubiera implementado:

```python
fecha = evento.get("fecha")

if fecha is None:
    continue
```

la nueva prueba habría funcionado, pero las pruebas históricas habrían dejado de hacerlo.

Esto habría supuesto una regresión.

La solución adoptada mantiene ambos formatos:

```python
fecha = evento.get("fecha")

if fecha is None:
    fecha_texto = extraer_fecha_log(
        evento["contenido"]
    )

    fecha = convertir_fecha_log(
        fecha_texto
    )
```

Por tanto, FileOrganizer acepta temporalmente dos generaciones de eventos.

### Evento normalizado v3.7

```python
{
    "linea": 1,
    "ip": "192.168.1.20",
    "tipo": "FUERZA_BRUTA",
    "severidad": "MEDIA",
    "contenido": "sin fecha en contenido",
    "fecha": datetime(...),
}
```

La correlación utiliza:

```text
fecha
```

directamente.

### Evento anterior

```python
{
    "linea": 1,
    "ip": "192.168.1.20",
    "tipo": "FUERZA_BRUTA",
    "severidad": "MEDIA",
    "contenido": (
        "192.168.1.20 - - "
        "[16/Aug/2026:09:01:16] "
        "Failed password"
    ),
}
```

La correlación detecta que:

```python
evento.get("fecha")
```

devuelve:

```python
None
```

y activa el fallback:

```text
contenido
    │
    ▼
extraer_fecha_log()
    │
    ▼
convertir_fecha_log()
    │
    ▼
datetime
```

Este comportamiento permitió conservar todos los tests anteriores de correlación.

Después de corregir GREEN 9:

```text
5 passed
```

en:

```text
test/test_analizador_logs_correlacion.py
```

y Ruff volvió a finalizar con:

```text
All checks passed!
```

La decisión proporciona una transición progresiva:

```text
             EVENTOS ANTIGUOS
                    │
                    │ fallback
                    ▼
            ┌───────────────┐
            │  CORRELACIÓN  │
            └───────────────┘
                    ▲
                    │ directo
                    │
             EVENTOS v3.7
```

Esta compatibilidad es especialmente importante porque v3.7 no pretende reescribir todo el sistema de logs.

Pretende introducir un contrato mejor sin destruir las capacidades existentes.

El principio aplicado puede resumirse como:

```text
nuevo contrato
     +
compatibilidad anterior
     +
regresión completa
     =
evolución controlada
```

La validación posterior confirmó precisamente este objetivo.

La batería global alcanzó:

```text
192 passed
```

sin romper los comportamientos que ya estaban caracterizados en las versiones anteriores.
## 36. Algoritmo de correlación mediante ventana temporal

La función:

```python
detectar_fuerza_bruta_temporal()
```

no se limita a contar eventos de autenticación fallida.

Su objetivo es determinar si un número determinado de eventos procedentes de una misma dirección IP ocurre dentro de una ventana temporal suficientemente pequeña.

Los parámetros principales son:

```python
umbral=3
ventana_segundos=60
```

Esto significa:

```text
umbral
└── número mínimo de intentos necesarios

ventana_segundos
└── intervalo temporal máximo permitido
```

Por ejemplo:

```text
IP: 192.168.1.20

09:00:00 → intento 1
09:00:10 → intento 2
09:00:20 → intento 3
```

La diferencia entre el primer y el último evento es:

```text
20 segundos
```

Como:

```text
20 <= 60
```

se considera que los tres eventos cumplen la condición temporal.

El resultado es una alerta:

```python
{
    "ip": "192.168.1.20",
    "tipo": "POSIBLE_FUERZA_BRUTA",
    "severidad": "ALTA",
    "intentos": 3,
    "ventana_segundos": 20.0,
    "lineas": [1, 2, 3],
}
```

### Agrupación previa por IP

Antes de realizar la correlación temporal se ejecuta:

```python
agrupados = agrupar_eventos_por_ip(eventos)
```

El objetivo es evitar mezclar eventos procedentes de diferentes direcciones.

Por ejemplo:

```text
192.168.1.20 → evento
192.168.1.30 → evento
192.168.1.20 → evento
192.168.1.20 → evento
```

se transforma conceptualmente en:

```text
192.168.1.20
├── evento 1
├── evento 3
└── evento 4

192.168.1.30
└── evento 2
```

Cada IP se analiza independientemente.

### Filtrado por tipo

Dentro de cada grupo solamente interesan los eventos:

```python
if evento["tipo"] != "FUERZA_BRUTA":
    continue
```

Por tanto, una misma IP podría generar diferentes tipos de eventos:

```text
192.168.1.20
├── SQL_INJECTION
├── FUERZA_BRUTA
├── PATH_TRAVERSAL
└── FUERZA_BRUTA
```

pero la correlación específica de fuerza bruta únicamente procesa:

```text
FUERZA_BRUTA
```

### Obtención de la fecha

En v3.7 el siguiente paso es:

```python
fecha = evento.get("fecha")
```

Si existe una fecha normalizada, se utiliza directamente.

Si no existe:

```python
if fecha is None:
```

se activa la compatibilidad con eventos anteriores:

```python
fecha_texto = extraer_fecha_log(
    evento["contenido"]
)

fecha = convertir_fecha_log(
    fecha_texto
)
```

Finalmente:

```python
if fecha is None:
    continue
```

impide utilizar eventos para los que no se dispone de información temporal.

### Construcción de intentos

Los eventos válidos se reducen a la información necesaria para la correlación:

```python
intentos.append(
    {
        "fecha": fecha,
        "linea": evento["linea"],
    }
)
```

Por ejemplo:

```text
[
    {
        fecha: 09:00:20,
        linea: 3
    },
    {
        fecha: 09:00:00,
        linea: 1
    },
    {
        fecha: 09:00:10,
        linea: 2
    }
]
```

### Ordenación temporal

Los intentos se ordenan mediante:

```python
intentos.sort(
    key=lambda intento: intento["fecha"]
)
```

El resultado pasa a ser:

```text
09:00:00 → línea 1
09:00:10 → línea 2
09:00:20 → línea 3
```

Esto permite analizar correctamente los eventos aunque el orden recibido no sea estrictamente cronológico.

### Construcción de ventanas

El algoritmo recorre:

```python
for indice in range(
    len(intentos) - umbral + 1
):
```

y genera ventanas mediante slicing:

```python
ventana = intentos[
    indice : indice + umbral
]
```

Si existen:

```text
E1
E2
E3
E4
E5
```

y:

```text
umbral = 3
```

las ventanas evaluadas conceptualmente son:

```text
E1 E2 E3

E2 E3 E4

E3 E4 E5
```

Para cada una se calcula:

```python
diferencia = (
    ventana[-1]["fecha"]
    - ventana[0]["fecha"]
).total_seconds()
```

Si:

```python
diferencia <= ventana_segundos
```

se genera la alerta.

Después se ejecuta:

```python
break
```

porque para esa IP ya se ha encontrado una ventana que satisface la condición.

Este algoritmo representa una primera forma de correlación temporal dentro de FileOrganizer.

---

## 37. Separación de responsabilidades en v3.7

Con v3.7, el sistema de análisis defensivo queda dividido principalmente entre tres componentes:

```text
core/reglas_logs.py
core/analizador_logs.py
core/eventos.py
```

Cada módulo responde ahora a una pregunta diferente.

### reglas_logs.py — ¿Qué detectar?

El módulo:

```text
core/reglas_logs.py
```

introducido en v3.6 contiene las definiciones declarativas de las detecciones.

Por ejemplo, una regla contiene información equivalente a:

```python
{
    "id": "...",
    "tipo": "...",
    "severidad": "...",
    "descripcion": "...",
    "patrones": [...],
}
```

Por tanto:

```text
reglas_logs.py
```

conoce:

```text
qué amenaza buscar
qué patrones utilizar
qué identificador asignar
qué severidad tiene
qué descripción utilizar
```

Pero no necesita conocer cómo se representa finalmente un evento completo.

### analizador_logs.py — ¿Cómo procesar y correlacionar?

El módulo:

```text
core/analizador_logs.py
```

continúa siendo responsable del procesamiento del log.

Entre sus responsabilidades se encuentran:

```text
leer líneas
extraer IPv4
extraer fechas
convertir fechas
evaluar reglas
procesar archivos
agrupar eventos
generar resúmenes
correlacionar eventos
```

Sin embargo, deja de decidir directamente la estructura exacta del diccionario que representa cada detección.

### eventos.py — ¿Cómo representar el resultado?

El nuevo módulo:

```text
core/eventos.py
```

responde a una tercera pregunta:

```text
¿Cómo debe representarse un evento de seguridad?
```

Para ello introduce:

```python
crear_evento_seguridad()
```

El constructor centraliza el contrato:

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

La arquitectura resultante puede resumirse como:

```text
                   línea de log
                        │
                        ▼
               analizador_logs.py
                        │
             evaluar línea
                        │
                        ▼
                  reglas_logs.py
                        │
                 reglas coincidentes
                        │
                        ▼
               analizador_logs.py
                        │
              extraer IP + fecha
                        │
                        ▼
                    eventos.py
                        │
                        ▼
              evento normalizado
                        │
                        ▼
               analizador_logs.py
                        │
                        ▼
                  correlación
```

Esta separación reduce el número de decisiones concentradas en un único módulo.

La evolución arquitectónica desde v3.5 puede verse así:

```text
v3.5
separación de interfaz y lógica

        ↓

v3.6
separación de reglas y análisis

        ↓

v3.7
separación de representación y análisis
```

Cada versión ha reducido progresivamente el acoplamiento del proyecto.

---

## 38. Tests específicos de integración

La creación de:

```text
core/eventos.py
```

no debía probarse únicamente de forma aislada.

También era necesario comprobar que:

```text
analizador_logs.py
```

utilizaba realmente el nuevo constructor.

Para ello se añadió:

```text
test/test_analizador_logs_eventos.py
```

Este archivo contiene pruebas específicas de integración entre:

```text
analizador_logs.py
```

y:

```text
eventos.py
```

### Comprobación del uso del constructor

Uno de los tests es:

```python
test_analizar_linea_utiliza_constructor_eventos
```

La prueba utiliza:

```python
monkeypatch
```

para sustituir temporalmente:

```python
crear_evento_seguridad
```

por una función controlada.

Se define primero un evento conocido:

```python
evento_creado = {
    "linea": 99,
    "ip": "10.0.0.10",
    "tipo": "EVENTO_PRUEBA",
    "severidad": "ALTA",
    "regla": "TEST_001",
    "descripcion": (
        "Evento construido por el normalizador"
    ),
    "contenido": "contenido",
}
```

Después:

```python
monkeypatch.setattr(
    core.analizador_logs,
    "crear_evento_seguridad",
    lambda **_kwargs: evento_creado,
)
```

Esto sustituye el constructor utilizado por:

```text
core.analizador_logs
```

durante la ejecución del test.

También se sustituye:

```python
evaluar_linea_con_reglas()
```

para garantizar una regla coincidente conocida.

Finalmente:

```python
eventos = core.analizador_logs.analizar_linea(
    "10.0.0.10 contenido",
    5,
)
```

debe devolver:

```python
[evento_creado]
```

La aserción:

```python
assert eventos == [evento_creado]
```

demuestra que:

```text
analizar_linea()
```

está utilizando realmente el constructor normalizado.

Este test es diferente de comprobar solamente el resultado final.

Sin él podría ocurrir que:

```text
analizar_linea()
```

continuara construyendo manualmente un diccionario idéntico.

El resultado externo sería parecido, pero la arquitectura no habría cambiado realmente.

### Integración temporal

El segundo test importante es:

```python
test_analizar_linea_incluye_fecha_normalizada
```

Se utiliza una línea realista:

```text
192.168.1.20 - - [16/Aug/2026:09:01:16] Failed password
```

y se ejecuta:

```python
eventos = core.analizador_logs.analizar_linea(
    linea,
    10,
)
```

Se comprueba primero:

```python
assert len(eventos) == 1
```

y posteriormente:

```python
assert evento["fecha"] == datetime(
    2026,
    8,
    16,
    9,
    1,
    16,
)
```

Por tanto, esta prueba recorre un flujo mucho más amplio:

```text
línea real
   │
   ▼
analizar_linea()
   │
   ├── evaluar regla
   ├── extraer IP
   ├── extraer fecha
   ├── convertir fecha
   │
   ▼
crear_evento_seguridad()
   │
   ▼
evento normalizado
```

Los tests de:

```text
test/test_eventos.py
```

comprueban el constructor.

Los tests de:

```text
test/test_analizador_logs_eventos.py
```

comprueban su integración.

Y:

```text
test/test_analizador_logs_correlacion.py
```

comprueba que los eventos normalizados pueden continuar avanzando por el sistema.

Esto crea tres niveles:

```text
CONTRATO
test_eventos.py

        ↓

INTEGRACIÓN
test_analizador_logs_eventos.py

        ↓

COMPORTAMIENTO
test_analizador_logs_correlacion.py
```

---

## 39. Relación conceptual con un SIEM

FileOrganizer no es un SIEM completo.

Sin embargo, la evolución del analizador de logs empieza a reproducir, a pequeña escala y con objetivos didácticos, algunas ideas utilizadas por sistemas defensivos reales.

Un SIEM procesa información procedente de múltiples fuentes para permitir:

```text
recolección
normalización
detección
enriquecimiento
correlación
generación de alertas
análisis
```

En FileOrganizer ya aparecen varias de estas etapas.

### Entrada

El sistema recibe:

```text
archivo de log
```

que contiene eventos en formato textual.

```text
LOG
 │
 ▼
analizador_logs.py
```

### Detección

El motor desarrollado en v3.6 permite aplicar reglas:

```text
reglas_logs.py
```

para identificar comportamientos relacionados con:

```text
SQL Injection
fallos de autenticación
Path Traversal
Command Injection
```

Conceptualmente:

```text
evento bruto
     │
     ▼
reglas de detección
     │
     ▼
detección
```

### Normalización

v3.7 introduce explícitamente una etapa de normalización.

Distintas detecciones terminan representándose mediante el mismo contrato:

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

Por tanto:

```text
detecciones diferentes
        │
        ▼
crear_evento_seguridad()
        │
        ▼
estructura común
```

Esta idea es especialmente relevante en análisis defensivo.

Los datos originales pueden tener formatos diferentes, pero las capas posteriores del sistema resultan mucho más sencillas si trabajan con una representación consistente.

### Enriquecimiento

Los eventos no contienen únicamente el texto original.

También incorporan información derivada:

```text
ip
tipo
severidad
regla
descripcion
fecha
```

Es decir:

```text
dato original
     +
metadatos derivados
     =
evento enriquecido
```

### Correlación

FileOrganizer ya puede relacionar varios eventos mediante:

```text
IP
tipo
tiempo
```

Por ejemplo:

```text
misma IP
   +
FUERZA_BRUTA
   +
3 intentos
   +
<= 60 segundos
   =
POSIBLE_FUERZA_BRUTA
```

Esto introduce una diferencia importante entre:

```text
DETECCIÓN
```

y:

```text
CORRELACIÓN
```

Una línea individual:

```text
Failed password
```

puede representar un fallo de autenticación.

Pero:

```text
Failed password
Failed password
Failed password
```

desde la misma IP y dentro de pocos segundos puede representar un comportamiento diferente:

```text
POSIBLE_FUERZA_BRUTA
```

El significado aparece al relacionar varios eventos.

### Flujo conceptual actual

Después de v3.7, el subsistema puede representarse como:

```text
                    LOG
                     │
                     ▼
               INGESTA BÁSICA
                     │
                     ▼
             analizador_logs.py
                     │
                     ▼
                 DETECCIÓN
                     │
                     ▼
               reglas_logs.py
                     │
                     ▼
               NORMALIZACIÓN
                     │
                     ▼
                 eventos.py
                     │
                     ▼
             EVENTO ENRIQUECIDO
                     │
                     ▼
                CORRELACIÓN
                     │
                     ▼
                  ALERTA
```

FileOrganizer sigue siendo un proyecto educativo y no pretende sustituir herramientas especializadas.

La importancia de esta evolución está en que permite aprender los principios arquitectónicos mediante código suficientemente pequeño como para poder entender cada pieza.

---

## 40. Diferencia entre evento y alerta

v3.7 también ayuda a distinguir dos conceptos importantes:

```text
EVENTO
```

y:

```text
ALERTA
```

No son exactamente lo mismo.

### Evento

Un evento representa algo que ha sido detectado en una línea concreta.

Por ejemplo:

```text
Failed password
```

puede producir:

```python
{
    "linea": 10,
    "ip": "192.168.1.20",
    "tipo": "FUERZA_BRUTA",
    "severidad": "MEDIA",
    "regla": "AUTH_FAIL_001",
    "descripcion": (
        "Intento de autenticación fallido"
    ),
    "contenido": "...",
    "fecha": datetime(...),
}
```

Este objeto representa una observación individual.

Conceptualmente:

```text
una línea
    │
    ▼
una detección
    │
    ▼
un evento
```

### Alerta correlacionada

La correlación temporal recibe múltiples eventos:

```text
EVENTO 1
EVENTO 2
EVENTO 3
```

y puede producir:

```python
{
    "ip": "192.168.1.20",
    "tipo": "POSIBLE_FUERZA_BRUTA",
    "severidad": "ALTA",
    "intentos": 3,
    "ventana_segundos": 20.0,
    "lineas": [1, 2, 3],
}
```

Esta estructura ya no representa una única línea.

Representa una conclusión obtenida a partir de varias observaciones.

El flujo es:

```text
evento
evento
evento
   │
   ▼
correlación
   │
   ▼
alerta
```

Esto permite entender por qué:

```text
FUERZA_BRUTA
```

y:

```text
POSIBLE_FUERZA_BRUTA
```

cumplen funciones distintas dentro del sistema actual.

El primero identifica eventos individuales compatibles con fallos de autenticación.

El segundo representa una conclusión obtenida después de analizar varios eventos en conjunto.

### Cambio de severidad

También puede observarse una evolución de severidad.

Los eventos individuales utilizan:

```text
severidad = MEDIA
```

mientras que la correlación genera:

```text
severidad = ALTA
```

Conceptualmente:

```text
1 fallo de autenticación
        │
        ▼
     MEDIA

varios fallos correlacionados
desde la misma IP
en una ventana pequeña
        │
        ▼
      ALTA
```

Esto introduce una idea importante:

```text
el contexto modifica el significado
```

Una observación aislada puede no ser especialmente significativa.

La combinación de varias observaciones puede justificar una alerta de mayor prioridad.

### Arquitectura resultante

La distinción puede representarse como:

```text
                   LOG
                    │
                    ▼
              REGLAS v3.6
                    │
                    ▼
             DETECCIÓN SIMPLE
                    │
                    ▼
              EVENTO v3.7
                    │
                    ▼
               NORMALIZADO
                    │
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
       análisis           correlación
                              │
                              ▼
                            ALERTA
```

La normalización introducida en v3.7 crea así una frontera arquitectónica útil:

```text
ENTRADA
  ↓
DETECCIÓN
  ↓
EVENTO NORMALIZADO
  ↓
CORRELACIÓN
  ↓
ALERTA
```

Esta separación prepara FileOrganizer para que futuras versiones puedan evolucionar el subsistema defensivo sin volver a concentrar todas las responsabilidades dentro de `core/analizador_logs.py`.
## 41. Conocimientos de Python trabajados en v3.7

Aunque el objetivo visible de v3.7 es normalizar los eventos de seguridad, durante su desarrollo se han trabajado varios conceptos importantes de Python.

La versión no introduce estructuras especialmente complejas.

La dificultad principal está en utilizar correctamente conceptos ya conocidos para mejorar el diseño del programa.

### Funciones como fronteras de responsabilidad

El nuevo módulo:

```text
core/eventos.py
```

introduce:

```python
crear_evento_seguridad()
```

La función encapsula una responsabilidad concreta:

```text
recibir datos
    │
    ▼
validarlos
    │
    ▼
construir evento
    │
    ▼
devolver estructura normalizada
```

Esto evita repetir dentro del analizador una construcción como:

```python
{
    "linea": numero_linea,
    "ip": extraer_ip(linea),
    "tipo": regla["tipo"],
    "severidad": regla["severidad"],
    "regla": regla["id"],
    "descripcion": regla["descripcion"],
    "contenido": linea.rstrip("\n"),
}
```

Ahora esa responsabilidad pertenece a una función específica.

El concepto trabajado es:

```text
una función
=
una responsabilidad claramente identificable
```

---

### Parámetros obligatorios y opcionales

La función se define como:

```python
def crear_evento_seguridad(
    linea,
    ip,
    regla,
    contenido,
    fecha=None,
):
```

Los parámetros:

```text
linea
ip
regla
contenido
```

forman parte de la llamada normal al constructor.

Mientras que:

```python
fecha=None
```

permite que la información temporal sea opcional.

Esto conserva compatibilidad con llamadas que todavía no proporcionen fecha.

El uso de:

```python
None
```

representa explícitamente:

```text
dato no disponible
```

en lugar de inventar un valor artificial.

---

### Diccionarios

Los eventos continúan representándose mediante:

```python
dict
```

Por ejemplo:

```python
{
    "linea": linea,
    "ip": ip,
    "tipo": regla["tipo"],
    "severidad": regla["severidad"],
    "regla": regla["id"],
    "descripcion": regla["descripcion"],
    "contenido": contenido,
    "fecha": fecha,
}
```

Aquí se trabajan dos usos diferentes de diccionarios.

La regla es un diccionario de entrada:

```python
regla["tipo"]
regla["severidad"]
regla["id"]
regla["descripcion"]
```

y el evento es otro diccionario construido a partir de esos datos.

Conceptualmente:

```text
REGLA
  │
  ├── id
  ├── tipo
  ├── severidad
  └── descripcion
        │
        ▼
crear_evento_seguridad()
        │
        ▼
EVENTO
```

---

### Conjuntos y comprobación de subconjuntos

Para validar las reglas se utiliza:

```python
campos_obligatorios = {
    "id",
    "tipo",
    "severidad",
    "descripcion",
}
```

Esta estructura es un:

```text
set
```

Posteriormente:

```python
if not campos_obligatorios <= regla.keys():
    raise ValueError("Regla incompleta")
```

El operador:

```python
<=
```

comprueba en este contexto si:

```text
campos_obligatorios
```

es subconjunto de:

```text
regla.keys()
```

Por ejemplo:

```text
campos obligatorios

{id, tipo, severidad, descripcion}

              <=

claves disponibles

{id, tipo, severidad, descripcion, patrones}
```

produce:

```text
True
```

Pero:

```text
{id, tipo, severidad, descripcion}

              <=

{id, tipo, severidad}
```

produce:

```text
False
```

Esta solución evita escribir comprobaciones independientes como:

```python
if "id" not in regla:
    ...

if "tipo" not in regla:
    ...

if "severidad" not in regla:
    ...

if "descripcion" not in regla:
    ...
```

---

### isinstance()

Para validar el número de línea se utiliza:

```python
if not isinstance(linea, int):
    raise TypeError("Línea inválida")
```

Y para el contenido:

```python
if not isinstance(contenido, str):
    raise TypeError("Contenido inválido")
```

Esto permite diferenciar entre:

```text
tipo incorrecto
```

y:

```text
valor incorrecto
```

Por ejemplo:

```python
linea="10"
```

tiene un tipo incorrecto.

Por tanto:

```text
TypeError
```

Mientras que:

```python
linea=0
```

sí es un entero, pero no representa una línea válida dentro del contrato establecido.

Por tanto:

```text
ValueError
```

Esta distinción mejora la semántica de las excepciones.

---

### dict.get()

La adaptación de la correlación utiliza:

```python
fecha = evento.get("fecha")
```

en lugar de:

```python
fecha = evento["fecha"]
```

La diferencia es importante para la compatibilidad.

Si el evento antiguo no contiene:

```text
fecha
```

la expresión:

```python
evento["fecha"]
```

produciría:

```text
KeyError
```

Mientras que:

```python
evento.get("fecha")
```

devuelve:

```python
None
```

Esto permite implementar:

```python
if fecha is None:
```

y activar el fallback correspondiente.

---

### datetime

v3.7 incorpora el objeto:

```python
datetime
```

directamente dentro del evento normalizado.

Una fecha textual como:

```text
16/Aug/2026:09:01:16
```

se convierte en:

```python
datetime(
    2026,
    8,
    16,
    9,
    1,
    16,
)
```

La ventaja es que las capas posteriores pueden realizar operaciones temporales directamente:

```python
fecha_final - fecha_inicial
```

y obtener después:

```python
.total_seconds()
```

sin volver a interpretar el texto original.

---

### sorted mediante sort() y lambda

La correlación utiliza:

```python
intentos.sort(
    key=lambda intento: intento["fecha"]
)
```

Aquí se trabaja:

```text
list.sort()
lambda
key
```

La función lambda indica qué campo debe utilizarse para ordenar cada elemento.

Conceptualmente:

```text
intento
   │
   ▼
intento["fecha"]
   │
   ▼
clave de ordenación
```

Esto permite ordenar cronológicamente los eventos antes de construir las ventanas temporales.

---

### Slicing

Las ventanas se generan mediante:

```python
ventana = intentos[
    indice : indice + umbral
]
```

Esto utiliza slicing de listas.

Con:

```text
umbral = 3
```

y:

```text
[A, B, C, D, E]
```

pueden obtenerse:

```text
[A, B, C]
[B, C, D]
[C, D, E]
```

La técnica permite construir una ventana deslizante sencilla sin introducir estructuras adicionales.

---

## 42. Diseño de un contrato de datos

Uno de los conceptos arquitectónicos más importantes de v3.7 es el de:

```text
contrato de datos
```

No se ha introducido una clase específica ni una librería de validación.

Sin embargo, `crear_evento_seguridad()` establece de facto qué estructura debe tener un evento generado por el analizador.

El contrato actual es:

```text
evento
├── linea
├── ip
├── tipo
├── severidad
├── regla
├── descripcion
├── contenido
└── fecha
```

Esto significa que otras partes del programa pueden empezar a asumir una representación común.

### Antes de la normalización

Sin un constructor central, diferentes zonas del programa podrían terminar generando:

```python
{
    "ip": "...",
    "tipo": "...",
}
```

o:

```python
{
    "direccion_ip": "...",
    "evento": "...",
}
```

o:

```python
{
    "ip": "...",
    "tipo": "...",
    "timestamp": "...",
}
```

Aunque representaran conceptos similares, las estructuras serían incompatibles.

Las capas consumidoras tendrían que conocer cada variante.

### Después de la normalización

El constructor establece:

```text
una representación común
```

Por tanto:

```text
productor A ──┐
              │
productor B ──┼──► EVENTO NORMALIZADO ──► consumidor
              │
productor C ──┘
```

En v3.7 solamente existe todavía un flujo principal de generación, pero establecer el contrato ahora permite preparar el sistema para futuras extensiones.

### Contrato y validación

El constructor no se limita a devolver un diccionario.

También valida parte de las precondiciones.

Por ejemplo:

```python
if not campos_obligatorios <= regla.keys():
    raise ValueError("Regla incompleta")
```

Esto impide construir eventos a partir de una regla que no pueda proporcionar los metadatos necesarios.

También:

```python
if not isinstance(linea, int):
    raise TypeError("Línea inválida")

if linea < 1:
    raise ValueError("Línea inválida")
```

protege el campo:

```text
linea
```

Y:

```python
if not isinstance(contenido, str):
    raise TypeError("Contenido inválido")
```

protege:

```text
contenido
```

Por tanto, el constructor actúa como frontera entre:

```text
datos recibidos
```

y:

```text
evento aceptado por el sistema
```

### Por qué no introducir una clase todavía

v3.7 mantiene deliberadamente una estructura basada en diccionarios.

La versión tiene como objetivo:

```text
separar
normalizar
validar
```

sin introducir simultáneamente una transformación mayor del modelo de datos.

El cambio realizado es incremental:

```text
diccionario construido dentro del analizador
                ↓
diccionario construido por función específica
```

Una evolución futura podría estudiar alternativas como:

```text
dataclass
TypedDict
Enum
```

pero no son necesarias para cumplir el objetivo actual de v3.7.

El principio seguido vuelve a ser:

```text
un problema arquitectónico
        ↓
un cambio controlado
        ↓
tests
        ↓
regresión
```

---

## 43. TDD aplicado durante v3.7

v3.7 se desarrolló mediante una secuencia incremental de ciclos:

```text
RED
 ↓
GREEN
 ↓
validación
 ↓
siguiente comportamiento
```

La estrategia permitió construir el nuevo contrato sin realizar una refactorización grande de una sola vez.

### Primer nivel — Constructor de eventos

Los primeros ciclos se centraron en:

```text
core/eventos.py
```

Se caracterizaron progresivamente comportamientos relacionados con:

```text
estructura del evento
IP ausente
regla incompleta
número de línea
contenido
tipo del número de línea
fecha
```

Cada prueba añadía una propiedad concreta al contrato.

Por ejemplo:

```text
RED
crear_evento_seguridad() no admite fecha

        ↓

GREEN
se añade fecha=None

        ↓

TEST
evento["fecha"] contiene datetime
```

### Segundo nivel — Integración

Una vez construido el normalizador, el siguiente problema era demostrar que:

```text
analizador_logs.py
```

lo utilizaba realmente.

Para ello se añadió:

```text
test/test_analizador_logs_eventos.py
```

La prueba mediante:

```python
monkeypatch
```

permitió verificar la colaboración entre componentes.

El ciclo puede resumirse como:

```text
constructor existe
      │
      ▼
¿analizador lo utiliza?
      │
      ▼
test de integración
      │
      ▼
analizar_linea() delegado
```

### Tercer nivel — Fecha normalizada

Después se añadió la fecha al flujo real:

```text
línea Apache
     │
     ▼
extraer_fecha_log()
     │
     ▼
convertir_fecha_log()
     │
     ▼
crear_evento_seguridad()
     │
     ▼
evento["fecha"]
```

El test correspondiente comprobó el resultado como:

```python
datetime
```

y no solamente como texto.

### Cuarto nivel — Correlación

Finalmente se comprobó que la capa consumidora aprovechara realmente la nueva representación.

El RED específico utilizó:

```text
contenido = "sin fecha en contenido"
```

junto con:

```text
fecha = datetime(...)
```

Esto obligó a la correlación a utilizar:

```python
evento["fecha"]
```

para superar el test.

La prueba evitó un falso positivo arquitectónico.

Si el contenido hubiera seguido incluyendo una fecha Apache, el test podría haber pasado utilizando accidentalmente el mecanismo antiguo.

### Importancia de los RED

Durante el desarrollo se observaron fallos reales como:

```text
TypeError
AssertionError
UnboundLocalError
```

Estos fallos no significan que TDD esté fallando.

Forman parte del proceso.

Un RED correcto demuestra que el test es capaz de detectar la ausencia del comportamiento que se pretende introducir.

La secuencia seguida ha sido:

```text
especificar comportamiento
        │
        ▼
observar fallo
        │
        ▼
implementar mínimo cambio
        │
        ▼
observar GREEN
        │
        ▼
ejecutar regresión
```

Esto reduce el riesgo de introducir varios cambios simultáneos sin saber cuál ha provocado una regresión.

---

## 44. Regresión completa

Una vez completada la normalización y adaptada la correlación temporal, se ejecutó la batería completa del proyecto.

El resultado final fue:

```text
192 passed in 0.24s
```

La versión anterior, v3.6, había cerrado con:

```text
182 passed
```

Por tanto, v3.7 incrementa la batería en:

```text
192 - 182 = 10 tests
```

El crecimiento corresponde a la caracterización del nuevo comportamiento relacionado con:

```text
constructor de eventos
validaciones
fecha normalizada
integración
correlación
```

### Importancia de la regresión

Los tests específicos de v3.7 podían demostrar que las nuevas funciones trabajaban correctamente.

Pero eso no era suficiente.

FileOrganizer ya contiene funcionalidades relacionadas con:

```text
organización
clasificación
configuración
duplicados
SHA-256
cuarentena
magic numbers
integridad
auditoría
logs
reglas
correlación
interfaz
robustez del filesystem
```

Modificar:

```text
core/analizador_logs.py
```

podía afectar a pruebas creadas en versiones anteriores.

Por ello se ejecutó:

```bash
pytest
```

sobre la batería completa.

El resultado:

```text
192 passed
```

demuestra que los comportamientos actualmente caracterizados continúan funcionando.

### Regresión específica del analizador

Durante el desarrollo también se ejecutaron baterías más pequeñas.

Por ejemplo:

```text
tests de eventos
tests de integración
tests de correlación
tests de logs
```

Esto permitió trabajar con ciclos rápidos antes de ejecutar la batería global.

El flujo utilizado fue:

```text
test específico
      ↓
módulo relacionado
      ↓
regresión de logs
      ↓
batería completa
```

Esta estrategia resulta más eficiente que ejecutar siempre todos los tests después de cada modificación pequeña.

### Evolución de la batería

La evolución reciente queda:

```text
v3.5
165 tests

   │
   ▼

v3.6
182 tests

   │
   ▼

v3.7
192 tests
```

Por tanto, desde el cierre de v3.5 se han incorporado:

```text
27 tests
```

mientras se evolucionaba el subsistema defensivo.

El objetivo no es aumentar el número por sí mismo.

Cada test debe proteger un comportamiento relevante.

---

## 45. Ruff, compilación y calidad de código

La validación de v3.7 no terminó con:

```text
192 passed
```

También se ejecutaron controles adicionales.

### Ruff

El análisis estático completo finalizó con:

```text
All checks passed!
```

Durante el desarrollo Ruff detectó problemas reales.

Entre ellos aparecieron temporalmente:

```text
F841
```

por una variable asignada pero no utilizada;

```text
F811
```

por redefiniciones;

```text
F821
```

por referencias a nombres no definidos;

y:

```text
I001
```

por organización incorrecta del bloque de imports.

Estos avisos permitieron detectar errores introducidos durante los ciclos de edición.

Por ejemplo, durante GREEN 8 existieron temporalmente dos definiciones de:

```python
analizar_linea()
```

y Ruff señaló la redefinición.

También se detectó un import duplicado de:

```python
datetime
```

en:

```text
test/test_analizador_logs_eventos.py
```

La validación final quedó:

```text
All checks passed!
```

### Compilación

También se ejecutó:

```bash
python3 -m py_compile organizador.py core/*.py ui/*.py
```

sin errores.

Este control permite comprobar que los módulos Python implicados pueden compilarse correctamente.

El resultado final fue limpio:

```text
sin salida
=
sin errores de compilación
```

### git diff --check

Finalmente:

```bash
git diff --check
```

también terminó sin salida.

Este comando permite detectar determinados problemas de formato en los cambios, como espacios en blanco incorrectos.

La ausencia de salida confirma:

```text
check limpio
```

### Validación conjunta

Los controles finales de código pueden resumirse como:

```text
pytest
│
└── 192 passed

ruff
│
└── All checks passed!

py_compile
│
└── correcto

git diff --check
│
└── limpio
```

Cada herramienta comprueba un aspecto diferente.

```text
pytest
└── comportamiento

Ruff
└── calidad estática y estilo

py_compile
└── validez sintáctica/compilación

git diff --check
└── higiene del diff
```

La combinación proporciona una validación más completa que depender únicamente de que el programa aparentemente funcione.

### Estado antes del commit

Después de la validación, los archivos correspondientes a la implementación de v3.7 fueron preparados en staging:

```text
M  core/analizador_logs.py
A  core/eventos.py
M  organizador.py
M  test/test_analizador_logs_correlacion.py
A  test/test_analizador_logs_eventos.py
A  test/test_eventos.py
```

El resumen staged fue:

```text
6 files changed
367 insertions(+)
14 deletions(-)
```

sin cambios adicionales fuera del staging.

Esto permitió realizar el commit funcional sobre un conjunto de cambios previamente inspeccionado y validado.
## 46. Commit principal de v3.7

Una vez completada la implementación funcional, ejecutada la regresión completa y superados los controles de calidad, los cambios de código de v3.7 se registraron en Git.

El commit realizado fue:

```text
6902aa3  v3.7: normaliza eventos de seguridad
```

Este commit contiene exactamente los seis archivos correspondientes al cambio funcional:

```text
M  core/analizador_logs.py
A  core/eventos.py
M  organizador.py
M  test/test_analizador_logs_correlacion.py
A  test/test_analizador_logs_eventos.py
A  test/test_eventos.py
```

El resumen del commit fue:

```text
6 files changed
367 insertions(+)
14 deletions(-)
```

### Nuevo módulo

Se incorpora:

```text
core/eventos.py
```

con:

```python
crear_evento_seguridad()
```

como punto central para construir eventos normalizados.

### Modificación del analizador

Se modifica:

```text
core/analizador_logs.py
```

para:

```text
utilizar crear_evento_seguridad()
normalizar la fecha durante analizar_linea()
utilizar evento["fecha"] en la correlación
mantener fallback para eventos anteriores
```

### Modificación de correlación

Se amplía:

```text
test/test_analizador_logs_correlacion.py
```

para demostrar que la correlación puede trabajar directamente con fechas normalizadas.

### Nuevos tests

Se incorporan:

```text
test/test_eventos.py
test/test_analizador_logs_eventos.py
```

El primero caracteriza el contrato del constructor.

El segundo verifica su integración con:

```python
analizar_linea()
```

### Versión mostrada por la aplicación

También se modifica:

```text
organizador.py
```

actualizando:

```text
FILE ORGANIZER v3.6
```

a:

```text
FILE ORGANIZER v3.7
```

Por tanto, el cambio de versión mostrado por la interfaz forma parte del mismo commit funcional.

### Estado posterior

Después del commit:

```text
HEAD -> main
```

quedó situado en:

```text
6902aa3
```

con:

```text
working tree limpio
```

y la relación con el remoto era:

```text
main...origin/main [adelante 1]
```

Esto significa que el commit funcional estaba registrado localmente, pero todavía no se había publicado en `origin/main` en ese punto del proceso.

La documentación de cierre se realiza posteriormente y de forma separada.

---

## 47. Arquitectura final de v3.7

La evolución realizada entre v3.5, v3.6 y v3.7 ha ido separando responsabilidades progresivamente.

Después de v3.7, el subsistema defensivo relacionado con logs puede representarse como:

```text
                        LOG
                         │
                         ▼
                analizador_logs.py
                         │
            ┌────────────┴────────────┐
            │                         │
            ▼                         ▼
      extracción                  evaluación
      IP / fecha                  de reglas
                                      │
                                      ▼
                              reglas_logs.py
                                      │
                                      ▼
                             reglas coincidentes
                                      │
            ┌─────────────────────────┘
            │
            ▼
       eventos.py
            │
            ▼
crear_evento_seguridad()
            │
            ▼
    EVENTO NORMALIZADO
            │
     ┌──────┴──────┐
     │             │
     ▼             ▼
 resumen       correlación
                   │
                   ▼
                 ALERTA
```

Esta arquitectura contiene ahora tres componentes con responsabilidades claramente diferenciadas.

### reglas_logs.py

Responde principalmente a:

```text
¿QUÉ DETECTAR?
```

Contiene:

```text
reglas
identificadores
tipos
severidades
descripciones
patrones
motor de evaluación
```

### analizador_logs.py

Responde principalmente a:

```text
¿CÓMO PROCESAR LOS LOGS?
```

Mantiene responsabilidades relacionadas con:

```text
lectura
extracción
análisis
agrupación
resúmenes
correlación
```

### eventos.py

Responde principalmente a:

```text
¿CÓMO REPRESENTAR UNA DETECCIÓN?
```

Centraliza:

```text
validación
construcción
normalización
```

mediante:

```python
crear_evento_seguridad()
```

La división conceptual queda:

```text
reglas_logs.py
│
└── qué detectar

analizador_logs.py
│
└── cómo procesar

eventos.py
│
└── cómo representar
```

### Dependencias

El flujo de dependencias también queda más explícito:

```text
analizador_logs.py
       │
       ├────────► reglas_logs.py
       │
       └────────► eventos.py
```

El analizador coordina ambos componentes.

`reglas_logs.py` no necesita conocer la correlación.

`eventos.py` tampoco necesita conocer cómo se leen los archivos de log.

Esto reduce el acoplamiento entre responsabilidades.

### Arquitectura general

Dentro del proyecto completo:

```text
                       organizador.py
                            │
                            ▼
                           ui/
                            │
                            ▼
                          core/
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
 organización           seguridad          análisis logs
                                                │
                                                ▼
                                      analizador_logs.py
                                                │
                              ┌─────────────────┴───────────────┐
                              ▼                                 ▼
                       reglas_logs.py                       eventos.py
```

v3.7 no cambia la arquitectura global de FileOrganizer.

Profundiza en la modularización de uno de sus subsistemas.

---

## 48. Evolución respecto a v3.6

v3.6 introdujo una separación fundamental:

```text
DEFINICIÓN DE DETECCIONES
```

frente a:

```text
PROCESAMIENTO DEL LOG
```

Antes de v3.6:

```text
analizador_logs.py
├── patrones
├── severidades
├── análisis
├── eventos
└── correlación
```

Después de v3.6:

```text
reglas_logs.py
├── reglas
└── evaluación

analizador_logs.py
├── procesamiento
├── eventos
└── correlación
```

Sin embargo, todavía quedaba una responsabilidad dentro del analizador:

```text
construcción de eventos
```

El código construía directamente estructuras equivalentes a:

```python
{
    "linea": numero_linea,
    "ip": extraer_ip(linea),
    "tipo": regla["tipo"],
    "severidad": regla["severidad"],
    "regla": regla["id"],
    "descripcion": regla["descripcion"],
    "contenido": linea.rstrip("\n"),
}
```

v3.7 extrae esta responsabilidad.

La evolución completa es:

```text
v3.6
────────────────────────────────

reglas_logs.py
└── detecciones

analizador_logs.py
├── procesamiento
├── construcción de eventos
└── correlación
```

y pasa a:

```text
v3.7
────────────────────────────────

reglas_logs.py
└── detecciones

eventos.py
└── construcción de eventos

analizador_logs.py
├── procesamiento
└── correlación
```

Por tanto, v3.7 continúa exactamente la dirección arquitectónica iniciada en v3.6.

### Evolución del evento

También cambia la representación.

En v3.6:

```text
linea
ip
tipo
severidad
regla
descripcion
contenido
```

En v3.7:

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

La fecha deja de ser únicamente información incrustada dentro del texto original.

Pasa a convertirse en un dato normalizado.

### Evolución de la correlación

Antes:

```text
evento
  │
  ▼
contenido
  │
  ▼
extraer fecha
  │
  ▼
convertir fecha
  │
  ▼
correlacionar
```

Ahora:

```text
evento
  │
  ▼
fecha
  │
  ▼
correlacionar
```

con compatibilidad:

```text
si evento["fecha"] no existe
          │
          ▼
usar contenido como fallback
```

### Evolución de tests

v3.6 cerró con:

```text
182 passed
```

v3.7 alcanza:

```text
192 passed
```

Se incorporan por tanto:

```text
10 tests
```

adicionales.

Estos nuevos tests protegen principalmente:

```text
normalización
validación
integración
fecha
correlación
compatibilidad
```

La evolución puede resumirse como:

```text
                 v3.6
                   │
                   ▼
          MOTOR DE REGLAS
                   │
                   ▼
             qué detectar
                   │
                   ▼
                 v3.7
                   │
                   ▼
       NORMALIZACIÓN DE EVENTOS
                   │
                   ▼
         cómo representar
```

---

## 49. Métricas finales de v3.7

La versión puede resumirse mediante varias métricas objetivas.

### Tests

Estado anterior:

```text
v3.6
182 passed
```

Estado actual:

```text
v3.7
192 passed
```

Incremento:

```text
+10 tests
```

### Nuevos archivos

Se incorporan:

```text
core/eventos.py
test/test_eventos.py
test/test_analizador_logs_eventos.py
```

Por tanto:

```text
3 archivos nuevos
```

### Archivos modificados en el commit funcional

Se modifican:

```text
core/analizador_logs.py
organizador.py
test/test_analizador_logs_correlacion.py
```

Por tanto:

```text
3 archivos modificados
```

El commit funcional afecta en total a:

```text
6 archivos
```

### Tamaño de los archivos nuevos

Durante la inspección previa al commit:

```text
core/eventos.py
36 líneas

test/test_eventos.py
176 líneas

test/test_analizador_logs_eventos.py
72 líneas
```

Total:

```text
284 líneas
```

en los tres archivos nuevos.

### Diff del commit funcional

El commit registró:

```text
367 insertions(+)
14 deletions(-)
```

### Calidad

La validación final fue:

```text
pytest
192 passed
```

```text
Ruff
All checks passed!
```

```text
py_compile
correcto
```

```text
git diff --check
limpio
```

### Commit

Código funcional:

```text
6902aa3
v3.7: normaliza eventos de seguridad
```

### Comparación reciente

La evolución de tests desde v3.5 queda:

```text
v3.5
165
 │
 │ +17
 ▼
v3.6
182
 │
 │ +10
 ▼
v3.7
192
```

Desde v3.5:

```text
192 - 165 = 27
```

Por tanto:

```text
+27 tests
```

han sido incorporados durante las dos versiones dedicadas principalmente a evolucionar el análisis defensivo de logs.

Estas métricas no determinan por sí solas la calidad del proyecto.

Sirven como registro verificable de su evolución.

---

## 50. Conocimientos de ciberseguridad trabajados

v3.7 tiene un objetivo arquitectónico, pero ese objetivo está directamente relacionado con conceptos utilizados en sistemas de monitorización defensiva.

Los principales conceptos trabajados son:

```text
evento
normalización
enriquecimiento
regla
correlación
ventana temporal
alerta
severidad
compatibilidad de formatos
```

### Evento de seguridad

Una detección individual pasa a representarse mediante una estructura explícita:

```text
EVENTO
```

con:

```text
origen
tipo
regla
severidad
contenido
fecha
```

En FileOrganizer, algunos de estos conceptos se representan mediante:

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

El objetivo es separar:

```text
dato bruto
```

de:

```text
dato interpretado
```

### Dato bruto

Ejemplo:

```text
192.168.1.20 - - [16/Aug/2026:09:01:16] Failed password
```

Es simplemente una línea de texto.

### Dato interpretado

Después del análisis:

```text
IP          → 192.168.1.20
tipo        → FUERZA_BRUTA
severidad   → MEDIA
regla       → AUTH_FAIL_001
fecha       → datetime(...)
```

La información adquiere estructura.

### Normalización

La normalización permite transformar información extraída de un formato concreto en campos utilizables por el resto del sistema.

Por ejemplo:

```text
[16/Aug/2026:09:01:16]
```

se transforma en:

```python
datetime(
    2026,
    8,
    16,
    9,
    1,
    16,
)
```

La correlación ya no necesita conocer cómo estaba escrita originalmente la fecha.

Esto introduce una idea fundamental:

```text
la capa de análisis posterior
no debería depender innecesariamente
del formato original del dato
```

### Enriquecimiento

La línea original no contiene explícitamente:

```text
tipo = FUERZA_BRUTA
severidad = MEDIA
regla = AUTH_FAIL_001
```

Estos datos son añadidos por el sistema después de evaluar las reglas.

Por tanto:

```text
línea original
      +
información derivada
      =
evento enriquecido
```

### Regla de detección

Gracias a v3.6, cada detección puede relacionarse con un identificador.

Por ejemplo:

```text
AUTH_FAIL_001
```

Esto permite conocer:

```text
qué regla produjo el evento
```

en lugar de conservar únicamente una etiqueta genérica.

### Correlación

v3.7 refuerza el concepto de que una detección individual y una conclusión correlacionada son cosas diferentes.

Ejemplo:

```text
09:00:00 Failed password
```

produce un evento.

Pero:

```text
09:00:00 Failed password
09:00:10 Failed password
09:00:20 Failed password
```

desde la misma IP puede generar:

```text
POSIBLE_FUERZA_BRUTA
```

La correlación utiliza contexto adicional:

```text
IP
+
tipo
+
cantidad
+
tiempo
```

### Ventana temporal

La variable:

```python
ventana_segundos
```

establece el intervalo dentro del cual deben producirse los eventos.

Con:

```text
umbral = 3
ventana_segundos = 60
```

se busca:

```text
3 eventos
de la misma IP
del tipo requerido
en <= 60 segundos
```

Esto permite diferenciar:

```text
3 fallos durante varias horas
```

de:

```text
3 fallos en pocos segundos
```

aunque el número total sea idéntico.

El contexto temporal modifica la interpretación.

### Severidad

Los eventos individuales pueden tener:

```text
MEDIA
```

mientras que la alerta correlacionada utiliza:

```text
ALTA
```

El sistema empieza así a representar que:

```text
evento individual
       │
       ▼
evidencia limitada

varios eventos relacionados
       │
       ▼
evidencia contextual mayor
```

### Compatibilidad

La correlación acepta tanto:

```text
eventos normalizados v3.7
```

como eventos anteriores cuya fecha únicamente está presente dentro de:

```text
contenido
```

Esto reproduce otro problema real de los sistemas de procesamiento de datos:

```text
los formatos evolucionan
```

y las capas consumidoras pueden necesitar soportar temporalmente más de una representación.

### Visión defensiva completa

El aprendizaje realizado entre v3.6 y v3.7 puede resumirse así:

```text
                  DATO BRUTO
                      │
                      ▼
                 línea de log
                      │
                      ▼
              MOTOR DE REGLAS
                    v3.6
                      │
                      ▼
                  DETECCIÓN
                      │
                      ▼
               NORMALIZACIÓN
                    v3.7
                      │
                      ▼
             EVENTO ENRIQUECIDO
                      │
                      ▼
                 CORRELACIÓN
                      │
                      ▼
                    ALERTA
```

FileOrganizer no implementa la complejidad de un SIEM profesional.

El valor didáctico está precisamente en construir estos conceptos de forma reducida y comprensible.

Cada fase puede inspeccionarse directamente en Python:

```text
qué entra
qué función lo procesa
qué estructura produce
qué tests lo protegen
qué componente consume el resultado
```

De esta forma, v3.7 no solamente mejora la arquitectura del proyecto.

También conecta conceptos de programación como:

```text
funciones
diccionarios
validaciones
datetime
listas
ordenación
slicing
excepciones
módulos
testing
```

con conceptos de ciberseguridad defensiva como:

```text
detección
normalización
enriquecimiento
eventos
correlación
alertas
ventanas temporales
severidad
```

Ese vínculo entre desarrollo Python y seguridad defensiva continúa siendo uno de los objetivos centrales de FileOrganizer.
## 51. Errores reales encontrados durante el desarrollo

El desarrollo de v3.7 no consistió únicamente en escribir el nuevo módulo y obtener tests verdes.

Durante los ciclos RED/GREEN aparecieron varios errores reales que ayudaron a comprender mejor tanto Python como el proceso de refactorización mediante TDD.

Estos errores forman parte del aprendizaje de la versión.

### Duplicación accidental de analizar_linea()

Durante la integración de la normalización apareció temporalmente una segunda definición de:

```python
def analizar_linea(linea, numero_linea):
```

El archivo llegó a contener:

```text
analizar_linea()  ← primera definición
analizar_linea()  ← segunda definición
```

Ruff detectó correctamente el problema:

```text
F811 Redefinition of unused `analizar_linea`
```

Además, la primera definición había quedado incompleta y contenía:

```python
eventos = []
```

sin utilizar la variable.

Esto produjo también:

```text
F841 Local variable `eventos` is assigned to but never used
```

La solución fue eliminar completamente la definición duplicada y conservar una única implementación funcional.

El control posterior:

```bash
grep -n "^def analizar_linea" core/analizador_logs.py
```

confirmó:

```text
30:def analizar_linea(linea, numero_linea):
```

Es decir:

```text
1 única definición
```

### Import duplicado de datetime

Durante la creación del test de integración apareció también:

```python
from datetime import datetime
```

dos veces dentro de:

```text
test/test_analizador_logs_eventos.py
```

Ruff lo detectó mediante:

```text
F811 Redefinition of unused `datetime`
```

El archivo fue corregido para mantener únicamente el import situado al comienzo.

La comprobación:

```bash
grep -n "^from datetime import datetime" \
    test/test_analizador_logs_eventos.py
```

terminó mostrando únicamente:

```text
1:from datetime import datetime
```

### Eliminación accidental del import de core

Durante la limpieza de los imports se eliminó temporalmente:

```python
import core.analizador_logs
```

aunque los tests continuaban utilizando:

```python
core.analizador_logs
```

Esto provocó:

```text
F821 Undefined name `core`
```

y durante pytest:

```text
NameError: name 'core' is not defined
```

El problema afectó a:

```text
test_analizar_linea_utiliza_constructor_eventos
test_analizar_linea_incluye_fecha_normalizada
```

La solución correcta no era modificar los tests para ocultar el problema, sino restaurar:

```python
import core.analizador_logs
```

La cabecera quedó finalmente:

```python
from datetime import datetime

import core.analizador_logs
```

### Variable fecha_texto sin inicializar

El error más significativo apareció durante la adaptación de la correlación temporal.

Una implementación intermedia contenía una estructura equivalente a:

```python
fecha = evento.get("fecha")

if fecha is None:
    fecha_texto = extraer_fecha_log(evento["contenido"])

fecha = convertir_fecha_log(fecha_texto)
```

El problema está en el flujo de ejecución.

Si:

```text
evento["fecha"]
```

ya contenía un `datetime`, entonces:

```python
if fecha is None:
```

no se ejecutaba.

Por tanto:

```text
fecha_texto
```

nunca era creada.

Después el código intentaba utilizarla igualmente:

```python
convertir_fecha_log(fecha_texto)
```

Python produjo:

```text
UnboundLocalError:
cannot access local variable 'fecha_texto'
where it is not associated with a value
```

Este error permitió identificar con claridad la lógica correcta.

La conversión solamente debe ejecutarse cuando sea necesario utilizar el fallback:

```python
fecha = evento.get("fecha")

if fecha is None:
    fecha_texto = extraer_fecha_log(
        evento["contenido"]
    )
    fecha = convertir_fecha_log(fecha_texto)
```

Así existen dos caminos independientes:

```text
evento normalizado
       │
       ▼
usar fecha directamente
```

o:

```text
evento legacy
       │
       ▼
extraer fecha del contenido
       │
       ▼
convertirla
```

### Regresión temporal

Después de una primera modificación de la correlación aparecieron simultáneamente dos fallos:

```text
test_detectar_fuerza_bruta_en_ventana_temporal
test_correlacion_temporal_utiliza_fecha_normalizada
```

Esto era especialmente importante porque demostraba que una modificación destinada a soportar el nuevo formato había roto el comportamiento anterior.

La solución definitiva debía cumplir simultáneamente:

```text
nuevo evento con fecha
        +
evento histórico sin fecha
```

Después de corregir el flujo:

```text
5 passed
```

en la batería específica de correlación.

Posteriormente:

```text
192 passed
```

en la batería completa.

### Valor de estos errores

Estos fallos no se ocultaron ni se resolvieron modificando arbitrariamente los tests.

Cada uno señaló un problema diferente:

```text
F811
→ duplicación

F841
→ código sin utilizar

F821
→ dependencia/import ausente

NameError
→ símbolo no disponible

UnboundLocalError
→ flujo incorrecto de variables

test de regresión fallido
→ comportamiento anterior roto
```

Por tanto, v3.7 también sirvió para practicar diagnóstico mediante:

```text
tracebacks
pytest
Ruff
grep
git diff
tests específicos
regresión completa
```

---

## 52. Evolución arquitectónica v3.5 → v3.7

Las tres últimas versiones forman una evolución arquitectónica relacionada.

No son funcionalidades completamente independientes.

Cada una prepara el terreno para la siguiente.

### v3.5 — separación de interfaz

v3.5 trabajó principalmente sobre la arquitectura general de FileOrganizer.

La responsabilidad de `organizador.py` fue reducida mediante la extracción de componentes de interfaz.

La separación principal quedó:

```text
organizador.py
      │
      ▼
     ui/
      │
      ▼
    core/
```

Conceptualmente:

```text
organizador.py
→ coordinación

ui/
→ interacción

core/
→ lógica
```

Esto permitió continuar desarrollando funcionalidades sin volver a concentrar toda la lógica en el archivo principal.

### v3.6 — separación de reglas

El siguiente problema arquitectónico se encontraba dentro del analizador de logs.

Antes:

```text
analizador_logs.py
├── patrones
├── severidades
├── análisis
├── eventos
└── correlación
```

v3.6 extrajo:

```text
core/reglas_logs.py
```

La separación pasó a ser:

```text
reglas_logs.py
→ qué detectar

analizador_logs.py
→ procesar el log
```

Esto introdujo un motor declarativo de reglas.

### v3.7 — separación de eventos

Después de extraer las reglas todavía quedaba dentro de:

```text
analizador_logs.py
```

la construcción manual de eventos.

v3.7 extrae esta responsabilidad mediante:

```text
core/eventos.py
```

La separación queda:

```text
reglas_logs.py
→ qué detectar

eventos.py
→ cómo representar

analizador_logs.py
→ cómo procesar y correlacionar
```

### Evolución completa

La secuencia puede representarse como:

```text
v3.5
────────────────────────────

organizador.py
     │
     ▼
separación UI / CORE
     │
     ▼

v3.6
────────────────────────────

analizador_logs.py
     │
     ▼
separación REGLAS / ANÁLISIS
     │
     ▼

v3.7
────────────────────────────

analizador_logs.py
     │
     ▼
separación EVENTOS / ANÁLISIS
```

El resultado acumulado es:

```text
                     organizador.py
                          │
                          ▼
                         ui/
                          │
                          ▼
                         core/
                          │
             ┌────────────┴─────────────┐
             │                          │
             ▼                          ▼
       otras funciones             análisis logs
                                        │
                         ┌──────────────┼──────────────┐
                         ▼              ▼              ▼
                  reglas_logs.py  analizador_logs.py  eventos.py
```

### Principio aprendido

Esta evolución permite observar una idea importante de diseño:

```text
modularizar no significa
crear archivos arbitrariamente
```

Cada extracción realizada responde a una responsabilidad identificable.

```text
UI
→ interacción

reglas
→ detección

eventos
→ representación

analizador
→ procesamiento
```

La modularidad tiene sentido cuando los límites representan responsabilidades reales.

---

## 53. Estado final de archivos de v3.7

La implementación funcional de v3.7 afecta exactamente a seis archivos.

### Archivo nuevo: core/eventos.py

```text
core/eventos.py
```

Responsabilidad:

```text
construcción y validación
de eventos de seguridad
```

Contiene:

```python
crear_evento_seguridad()
```

y establece el contrato:

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

### Archivo modificado: core/analizador_logs.py

```text
core/analizador_logs.py
```

Ahora importa:

```python
from core.eventos import crear_evento_seguridad
```

`analizar_linea()` utiliza el constructor centralizado.

También normaliza:

```text
fecha
```

antes de construir el evento.

La correlación temporal utiliza prioritariamente:

```python
evento.get("fecha")
```

manteniendo extracción desde `contenido` como fallback.

### Archivo modificado: organizador.py

```text
organizador.py
```

El cambio funcional es únicamente la actualización de la versión mostrada:

```text
FILE ORGANIZER v3.6
```

a:

```text
FILE ORGANIZER v3.7
```

No se introducen nuevas responsabilidades en el archivo principal.

### Archivo nuevo: test/test_eventos.py

```text
test/test_eventos.py
```

Contiene los tests específicos del nuevo constructor.

Caracteriza:

```text
estructura normalizada
IP opcional
regla incompleta
línea inválida
tipo de línea inválido
contenido inválido
fecha
```

### Archivo nuevo: test/test_analizador_logs_eventos.py

```text
test/test_analizador_logs_eventos.py
```

Comprueba la integración entre:

```text
analizador_logs.py
```

y:

```text
eventos.py
```

Incluye pruebas sobre:

```text
utilización del constructor
normalización de fecha desde el log
```

### Archivo modificado: test/test_analizador_logs_correlacion.py

```text
test/test_analizador_logs_correlacion.py
```

Se amplía para demostrar que:

```text
detectar_fuerza_bruta_temporal()
```

puede trabajar directamente con:

```python
evento["fecha"]
```

sin depender de que la fecha continúe incrustada dentro de:

```python
evento["contenido"]
```

### Resumen

El cambio funcional queda:

```text
core/
├── analizador_logs.py       MODIFICADO
└── eventos.py               NUEVO

test/
├── test_analizador_logs_correlacion.py  MODIFICADO
├── test_analizador_logs_eventos.py      NUEVO
└── test_eventos.py                      NUEVO

organizador.py               MODIFICADO
```

El commit:

```text
6902aa3
```

registra exactamente estos seis archivos.

---

## 54. Documentación de v3.7

El cierre de una versión de FileOrganizer no termina con el commit funcional.

El procedimiento establecido incluye también documentación.

Para v3.7 se actualiza:

```text
README.md
```

y se prepara este documento:

```text
docs/Resumen_v3.7_Normalizacion_Eventos.md
```

### README

El README incorpora la nueva arquitectura.

La estructura del proyecto añade:

```text
core/eventos.py
```

y los tests:

```text
test/test_eventos.py
test/test_analizador_logs_eventos.py
```

También incorpora un bloque específico:

```text
# v3.7 — Normalización de eventos de seguridad
```

que documenta:

```text
objetivo
nuevo módulo
contrato del evento
validaciones
normalización temporal
integración
correlación
TDD
validación
commit
arquitectura resultante
```

La actualización mantiene el historial anterior.

No se elimina la documentación de:

```text
v3.1
v3.2
v3.3
v3.4
v3.5
v3.6
```

### Resumen didáctico

Este documento conserva un nivel de detalle superior al README.

Su finalidad no es únicamente describir qué hace la versión.

También registra:

```text
por qué se hizo
cómo se diseñó
qué código cambió
qué tests se escribieron
qué errores aparecieron
cómo se resolvieron
qué conceptos de Python se practicaron
qué conceptos de ciberseguridad se trabajaron
```

Esto permite utilizar posteriormente FileOrganizer no solamente como repositorio de código, sino también como registro del aprendizaje.

### Continuidad documental

La secuencia de documentos queda:

```text
docs/
├── Resumen_v3.1_Seguridad.md
├── Resumen_v3.2_Robustez_Testing.md
├── Resumen_v3.3_Monitor_Integridad.md
├── Resumen_v3.4_Auditoria_Seguridad.md
├── Resumen_v3.5_Refactor_Arquitectura.md
├── Resumen_v3.6_Motor_Reglas_Logs.md
└── Resumen_v3.7_Normalizacion_Eventos.md
```

Cada resumen representa un checkpoint técnico de la evolución del proyecto.

### Separación código/documentación

El código funcional ya está registrado en:

```text
6902aa3
v3.7: normaliza eventos de seguridad
```

La documentación se mantiene separada para que el historial Git permita distinguir:

```text
implementación
```

de:

```text
documentación de cierre
```

Este mismo procedimiento ya se ha utilizado en versiones anteriores del proyecto.

---

## 55. Resultado final de v3.7

v3.7 partió de una cuestión arquitectónica concreta.

Después de v3.6 existía:

```text
core/reglas_logs.py
```

para representar:

```text
qué detectar
```

pero:

```text
core/analizador_logs.py
```

todavía era responsable de construir directamente los eventos.

v3.7 elimina esa responsabilidad mediante:

```text
core/eventos.py
```

y:

```python
crear_evento_seguridad()
```

### Antes

```text
regla
  │
  ▼
analizador_logs.py
  │
  ├── procesa
  ├── extrae
  ├── construye evento
  └── correlaciona
```

### Después

```text
                     regla
                       │
                       ▼
                reglas_logs.py
                       │
                       ▼
               analizador_logs.py
                       │
                       ▼
                  eventos.py
                       │
                       ▼
             evento normalizado
                       │
                       ▼
                  correlación
```

### Contrato resultante

Cada nuevo evento generado por `analizar_linea()` puede contener:

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

Esto permite que otras capas consuman información ya estructurada.

### Compatibilidad

La evolución no obliga a eliminar inmediatamente el comportamiento histórico.

La correlación acepta:

```text
evento con fecha normalizada
```

y también:

```text
evento sin fecha normalizada
```

mediante fallback.

Esto permitió mantener verdes los tests anteriores.

### Resultado de testing

La versión termina con:

```text
192 passed
```

sin regresiones conocidas dentro de la batería existente.

### Resultado de calidad

Ruff:

```text
All checks passed!
```

Compilación:

```text
correcta
```

Integridad del diff:

```text
git diff --check
```

sin errores.

### Resultado arquitectónico

La evolución reciente puede resumirse:

```text
v3.5
SEPARAR INTERFAZ
      │
      ▼
v3.6
SEPARAR DETECCIÓN
      │
      ▼
v3.7
SEPARAR REPRESENTACIÓN
```

El subsistema defensivo queda ahora dividido en componentes especializados:

```text
reglas_logs.py
→ detección

eventos.py
→ representación

analizador_logs.py
→ procesamiento y correlación

ui/logs.py
→ presentación
```

### Resultado didáctico

v3.7 ha permitido trabajar de forma conjunta:

```text
PYTHON
────────────────────
módulos
funciones
diccionarios
validaciones
datetime
flujo condicional
listas
ordenación
excepciones
imports

TESTING
────────────────────
TDD
RED
GREEN
monkeypatch
regresión
tests unitarios
tests de integración

CALIDAD
────────────────────
Ruff
py_compile
git diff --check
diagnóstico de errores

GIT
────────────────────
diff
staging
commit
estado local/remoto

CIBERSEGURIDAD
────────────────────
eventos
reglas
normalización
enriquecimiento
correlación
ventanas temporales
alertas
severidades
```

### Estado técnico al finalizar la implementación

El código funcional de v3.7 queda registrado en:

```text
6902aa3
v3.7: normaliza eventos de seguridad
```

con:

```text
192 tests
Ruff limpio
compilación correcta
git diff --check limpio
```

En el checkpoint posterior al commit funcional:

```text
main
```

estaba:

```text
1 commit por delante de origin/main
```

La documentación de cierre se está preparando después del commit funcional.

Por tanto, todavía quedan pendientes las operaciones finales de publicación de la versión antes de considerar v3.7 oficialmente cerrada.

La secuencia correcta continúa siendo:

```text
código v3.7
    ✅

tests
    ✅

Ruff
    ✅

compilación
    ✅

git diff --check
    ✅

commit funcional
    ✅ 6902aa3

README
    🚧

Resumen v3.7
    🚧

validación documental
    ⏳

commit documentación
    ⏳

push
    ⏳

tag v3.7
    ⏳

verificación local/remoto
    ⏳

CIERRE OFICIAL v3.7
    ⏳
```

Hasta completar esos pasos, v3.7 está funcionalmente terminada pero todavía no debe considerarse publicada y cerrada oficialmente.
## 56. Próximos pasos

v3.7 deja consolidada la normalización de eventos de seguridad, pero no determina automáticamente el contenido de la siguiente versión.

Antes de iniciar v3.8 se realizará una revisión específica del estado del proyecto para decidir su objetivo y alcance.

La decisión deberá mantener los principios utilizados hasta ahora:

- evolución incremental;
- orientación a ciberseguridad defensiva;
- aplicación práctica de Python;
- desarrollo mediante TDD;
- arquitectura modular;
- ausencia de regresiones;
- utilidad real para el portfolio.

Por tanto, v3.8 no se inicia todavía.

Primero se cerrará y publicará completamente v3.7.

---

## 57. Checklist de cierre de v3.7

Estado de la versión:

```text
IMPLEMENTACIÓN
[✓] Crear core/eventos.py
[✓] Implementar crear_evento_seguridad()
[✓] Definir contrato normalizado
[✓] Validar reglas
[✓] Validar número de línea
[✓] Validar contenido
[✓] Permitir IP ausente
[✓] Incorporar fecha al evento

INTEGRACIÓN
[✓] Integrar eventos.py con analizador_logs.py
[✓] Normalizar fecha desde el log
[✓] Utilizar fecha normalizada en correlación
[✓] Mantener fallback para eventos anteriores
[✓] Actualizar versión visible a v3.7

TESTING
[✓] Tests unitarios de eventos
[✓] Tests de integración
[✓] Test de fecha normalizada
[✓] Test de correlación normalizada
[✓] Regresión completa
[✓] 192 tests superados

CALIDAD
[✓] Ruff limpio
[✓] Compilación correcta
[✓] git diff --check limpio

GIT
[✓] Revisar cambios
[✓] Staging del código
[✓] Commit funcional
[✓] 6902aa3 — v3.7: normaliza eventos de seguridad

DOCUMENTACIÓN
[✓] Actualizar README
[✓] Documentar arquitectura v3.7
[✓] Preparar Resumen_v3.7_Normalizacion_Eventos.md
[ ] Validar documentación final
[ ] Commit documental
[ ] Push a origin/main
[ ] Crear tag v3.7
[ ] Publicar tag
[ ] Verificar sincronización final
58. Conclusión

FileOrganizer v3.7 representa un nuevo paso en la evolución arquitectónica del subsistema de análisis defensivo de logs.

v3.6 había separado:

qué detectar

mediante:

core/reglas_logs.py

v3.7 separa ahora:

cómo representar lo detectado

mediante:

core/eventos.py

El flujo resultante es:

                    LOG
                     │
                     ▼
             analizador_logs.py
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
   reglas_logs.py           eventos.py
          │                     │
     detección            normalización
          │                     │
          └──────────┬──────────┘
                     ▼
             evento de seguridad
                     │
                     ▼
                correlación
                     │
                     ▼
                  alerta

El analizador deja así de ser responsable de conocer todos los detalles de representación de los eventos.

El contrato común:

linea
ip
tipo
severidad
regla
descripcion
contenido
fecha

establece una base sobre la que podrán construirse futuras capacidades defensivas sin volver a introducir construcción manual de eventos en diferentes puntos del proyecto.

La versión también mejora la correlación temporal.

Los eventos nuevos transportan directamente su fecha normalizada como datetime, mientras que el sistema conserva compatibilidad con eventos anteriores mediante extracción desde el contenido cuando sea necesario.

El desarrollo mediante TDD permitió introducir estos cambios manteniendo el comportamiento existente.

El resultado técnico comprobado es:

192 passed
All checks passed!
compilación correcta
git diff --check limpio

El código funcional queda registrado en:

6902aa3 — v3.7: normaliza eventos de seguridad

La evolución reciente de FileOrganizer queda así:

v3.5
Refactor de arquitectura
        │
        ▼
separación UI / lógica
        │
        ▼
v3.6
Motor de reglas
        │
        ▼
separación detección / análisis
        │
        ▼
v3.7
Normalización de eventos
        │
        ▼
separación representación / análisis

Con v3.7, FileOrganizer dispone de una arquitectura defensiva más claramente dividida entre:

DETECCIÓN
    │
    ▼
REGLAS

PROCESAMIENTO
    │
    ▼
ANALIZADOR

REPRESENTACIÓN
    │
    ▼
EVENTOS

CORRELACIÓN
    │
    ▼
ALERTAS


