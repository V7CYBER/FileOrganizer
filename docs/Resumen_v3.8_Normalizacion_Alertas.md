# FileOrganizer v3.8 — Normalización de alertas de seguridad

## 1. Objetivo de la versión

La versión v3.8 de FileOrganizer completa la evolución defensiva iniciada en las versiones anteriores mediante la introducción de una capa específica para representar alertas de seguridad.

v3.6 separó las reglas de detección del analizador de logs mediante:

```text
core/reglas_logs.py
v3.7 continuó esa separación introduciendo eventos de seguridad normalizados mediante:

core/eventos.py

Sin embargo, después de v3.7 todavía quedaba una responsabilidad integrada directamente dentro de:

core/analizador_logs.py

La correlación temporal de fuerza bruta construía manualmente los diccionarios utilizados para representar una alerta.

v3.8 elimina esa responsabilidad del correlador mediante un nuevo módulo:

core/alertas.py

y una función específica:

crear_alerta_seguridad()

El objetivo arquitectónico es completar el flujo defensivo:

LOG
 │
 ▼
REGLAS
 │
 ▼
EVENTOS
 │
 ▼
CORRELACIÓN
 │
 ▼
ALERTAS

Cada nivel pasa a disponer de una responsabilidad más claramente definida.

2. Punto de partida desde v3.7

FileOrganizer v3.7 terminó con una arquitectura de análisis defensivo basada en tres componentes principales:

reglas_logs.py
eventos.py
analizador_logs.py

Las responsabilidades estaban distribuidas de la siguiente forma:

reglas_logs.py
└── define qué detectar

eventos.py
└── define cómo representar una detección

analizador_logs.py
└── analiza logs y correlaciona eventos

El flujo de una detección individual era:

línea de log
     │
     ▼
evaluación de reglas
     │
     ▼
regla coincidente
     │
     ▼
crear_evento_seguridad()
     │
     ▼
evento normalizado

Los eventos generados podían contener:

linea
ip
tipo
severidad
regla
descripcion
contenido
fecha

Además, v3.7 normalizó el campo:

fecha

como un objeto datetime cuando la fecha podía extraerse correctamente del log.

Esto permitió que la correlación temporal utilizara directamente:

evento["fecha"]

manteniendo al mismo tiempo compatibilidad con eventos históricos que todavía almacenaban la fecha únicamente dentro de:

contenido

La batería completa al cierre de v3.7 era:

192 passed

y la versión quedó publicada mediante:

6902aa3  v3.7: normaliza eventos de seguridad
49b2875  docs: documenta FileOrganizer v3.7

con el tag:

v3.7
3. Problema pendiente después de v3.7

Aunque los eventos ya estaban normalizados, las alertas todavía no disponían de una abstracción equivalente.

La función:

detectar_fuerza_bruta_temporal()

contenida en:

core/analizador_logs.py

realizaba correctamente la correlación de eventos.

Su responsabilidad lógica consistía en:

agrupar eventos por IP
        │
        ▼
seleccionar eventos FUERZA_BRUTA
        │
        ▼
obtener sus fechas
        │
        ▼
ordenarlos temporalmente
        │
        ▼
construir ventanas
        │
        ▼
calcular diferencia temporal
        │
        ▼
decidir si existe una correlación

Pero una vez detectada la correlación, la misma función construía directamente:

{
    "ip": ip,
    "tipo": "POSIBLE_FUERZA_BRUTA",
    "severidad": "ALTA",
    "intentos": umbral,
    "ventana_segundos": diferencia,
    "lineas": [...],
}

Esto significaba que analizador_logs.py tenía dos responsabilidades diferentes:

1. decidir cuándo existe una alerta

2. decidir cómo se representa esa alerta

El problema era conceptualmente similar al resuelto en v3.7 con los eventos.

La correlación debe conocer:

cuándo existe una relación significativa entre eventos

pero no necesita ser responsable de:

cómo construir la estructura final de una alerta

v3.8 separa ambas responsabilidades.

4. Diseño de v3.8

La solución elegida consiste en introducir:

core/alertas.py

Este módulo contiene el constructor:

crear_alerta_seguridad()

El flujo anterior:

detectar_fuerza_bruta_temporal()
        │
        ▼
correlación
        │
        ▼
construcción manual del diccionario
        │
        ▼
alerta

se transforma en:

detectar_fuerza_bruta_temporal()
        │
        ▼
correlación
        │
        ▼
crear_alerta_seguridad()
        │
        ▼
alerta normalizada

La separación final queda:

analizador_logs.py
└── decide cuándo generar una alerta

alertas.py
└── decide cómo representar la alerta

Este cambio es pequeño en cantidad de código, pero importante desde el punto de vista arquitectónico.

No se pretende introducir un nuevo sistema complejo de correlación.

v3.8 tiene un alcance deliberadamente limitado:

normalizar alertas
integrarlas con la correlación existente
validar su contrato
mantener compatibilidad
cerrar la fase Blue Team
5. Nuevo módulo core/alertas.py

El nuevo módulo:

core/alertas.py

incorpora:

crear_alerta_seguridad(
    ip,
    intentos,
    ventana_segundos,
    lineas,
    fecha=None,
)

Su responsabilidad es recibir los datos obtenidos por la correlación y construir una estructura normalizada.

El resultado contiene:

ip
tipo
severidad
intentos
ventana_segundos
lineas
fecha

Para la correlación implementada actualmente se utilizan los valores:

tipo = POSIBLE_FUERZA_BRUTA
severidad = ALTA

Por tanto, el constructor centraliza información que anteriormente estaba definida directamente dentro de la función de correlación.

6. Contrato de una alerta de seguridad

La alerta generada por v3.8 puede representarse conceptualmente como:

{
    "ip": "192.168.1.20",
    "tipo": "POSIBLE_FUERZA_BRUTA",
    "severidad": "ALTA",
    "intentos": 3,
    "ventana_segundos": 20.0,
    "lineas": [1, 2, 3],
    "fecha": None,
}

Cada campo tiene una responsabilidad concreta.

ip

identifica la dirección asociada a los eventos correlacionados.

tipo

identifica el tipo de alerta generada.

severidad

representa la importancia asignada a la correlación.

intentos

indica el número de eventos utilizados para alcanzar el umbral.

ventana_segundos

indica la diferencia temporal entre el primer y último evento de la ventana correlacionada.

lineas

conserva las líneas del log relacionadas con la alerta.

fecha

permite asociar información temporal normalizada a la alerta y se mantiene como campo opcional.

7. Diferencia entre evento y alerta

v3.8 permite establecer de forma más clara una distinción importante en análisis defensivo.

Un:

EVENTO

representa una detección individual.

Por ejemplo:

un intento fallido de autenticación

Una:

ALERTA

puede representar una conclusión obtenida a partir de varios eventos relacionados.

Por ejemplo:

evento 1 ─┐
evento 2 ─┼── correlación temporal ──► POSIBLE_FUERZA_BRUTA
evento 3 ─┘

Por tanto:

evento != alerta

El evento describe algo observado.

La alerta representa una condición considerada suficientemente significativa para ser destacada.

Esta separación es una de las razones principales para disponer de:

eventos.py

y:

alertas.py

como componentes independientes.
---

## 8. Integración con detectar_fuerza_bruta_temporal()

La integración principal de v3.8 se realiza en:

```text
core/analizador_logs.py
La función:

detectar_fuerza_bruta_temporal()

mantiene la lógica de correlación desarrollada anteriormente.

El algoritmo continúa:

eventos
   │
   ▼
agrupar por IP
   │
   ▼
filtrar FUERZA_BRUTA
   │
   ▼
obtener fechas
   │
   ▼
ordenar temporalmente
   │
   ▼
crear ventanas según umbral
   │
   ▼
calcular diferencia temporal
   │
   ▼
comparar con ventana_segundos

El cambio aparece únicamente cuando una ventana cumple las condiciones necesarias para generar una alerta.

Antes de v3.8, detectar_fuerza_bruta_temporal() realizaba directamente:

alertas.append(
    {
        "ip": ip,
        "tipo": "POSIBLE_FUERZA_BRUTA",
        "severidad": "ALTA",
        "intentos": umbral,
        "ventana_segundos": diferencia,
        "lineas": [
            intento["linea"]
            for intento in ventana
        ],
    }
)

En v3.8 esta construcción se sustituye por:

alertas.append(
    crear_alerta_seguridad(
        ip=ip,
        intentos=umbral,
        ventana_segundos=diferencia,
        lineas=[
            intento["linea"]
            for intento in ventana
        ],
    )
)

De esta forma, la correlación conserva su responsabilidad principal:

DETECTAR LA RELACIÓN ENTRE EVENTOS

mientras que:

core/alertas.py

asume:

CONSTRUIR LA REPRESENTACIÓN DE LA ALERTA
9. Importación del constructor

Para realizar la integración, core/analizador_logs.py incorpora:

from core.alertas import crear_alerta_seguridad

Esto establece una dependencia explícita:

analizador_logs.py
        │
        ▼
    alertas.py

La dependencia tiene un propósito concreto.

analizador_logs.py conoce:

cuándo debe existir una alerta

pero delega:

cómo debe construirse

Esta misma filosofía ya se había aplicado en v3.7 mediante:

from core.eventos import crear_evento_seguridad

Por tanto, después de v3.8 el analizador utiliza dos constructores especializados:

crear_evento_seguridad()
crear_alerta_seguridad()

El primero representa detecciones individuales.

El segundo representa resultados de correlación.

10. Conservación del algoritmo de correlación

Uno de los objetivos de v3.8 era evitar cambios innecesarios en una funcionalidad que ya estaba cubierta por tests.

La correlación temporal continúa utilizando:

agrupar_eventos_por_ip()

para separar los eventos según su dirección IP.

Después filtra únicamente:

FUERZA_BRUTA

y obtiene la fecha mediante:

fecha = evento.get("fecha")

Cuando el evento no contiene una fecha normalizada, se conserva el fallback introducido durante v3.7:

if fecha is None:
    fecha_texto = extraer_fecha_log(
        evento["contenido"]
    )

    fecha = convertir_fecha_log(
        fecha_texto
    )

Si tampoco puede obtenerse una fecha desde el contenido:

if fecha is None:
    continue

Por tanto, v3.8 no elimina compatibilidad con los eventos anteriores.

La evolución sigue siendo:

evento moderno
    │
    ├── fecha normalizada disponible
    │       │
    │       └── usar directamente
    │
    └── fecha ausente
            │
            └── intentar extraer del contenido

Esta compatibilidad es importante porque permite evolucionar el contrato de datos sin reescribir de golpe toda la lógica anterior.

11. Ordenación temporal de eventos

Los intentos válidos continúan almacenándose temporalmente con:

fecha
linea

y se ordenan mediante:

intentos.sort(
    key=lambda intento: intento["fecha"]
)

Esta ordenación garantiza que la correlación trabaje cronológicamente aunque los eventos recibidos originalmente no estén ordenados.

El flujo es:

eventos recibidos
      │
      ▼
eventos FUERZA_BRUTA válidos
      │
      ▼
extracción de fecha
      │
      ▼
ordenación cronológica
      │
      ▼
análisis de ventanas

La normalización de alertas introducida en v3.8 no modifica este comportamiento.

12. Ventana temporal y umbral

La correlación utiliza dos parámetros fundamentales:

umbral
ventana_segundos

El valor:

umbral

indica cuántos intentos deben encontrarse dentro de una ventana para considerar que existe una posible fuerza bruta.

El valor:

ventana_segundos

define el intervalo máximo permitido.

La función recorre ventanas mediante:

for indice in range(
    len(intentos) - umbral + 1
):

y selecciona:

ventana = intentos[
    indice : indice + umbral
]

Después calcula:

diferencia = (
    ventana[-1]["fecha"]
    - ventana[0]["fecha"]
).total_seconds()

Si:

diferencia <= ventana_segundos

la correlación considera alcanzada la condición de alerta.

En ese momento se utiliza:

crear_alerta_seguridad()
13. Una alerta por IP correlacionada

Después de generar una alerta se mantiene:

break

Esto evita continuar generando alertas equivalentes para ventanas posteriores de la misma IP una vez encontrada una correlación válida.

Por ejemplo, ante:

09:00:00
09:00:10
09:00:20

con:

umbral = 3
ventana_segundos = 60

se genera una única alerta.

Esta propiedad fue especialmente importante durante la integración del nuevo constructor.

Un error durante el ciclo GREEN produjo temporalmente:

2 alertas

donde los tests esperaban:

1 alerta

El problema no estaba en el constructor.

La causa era una integración incorrecta que provocaba una duplicación de la alerta.

La regresión de correlación permitió detectarlo inmediatamente.

El resultado correcto conserva:

correlación válida
        │
        ▼
crear una alerta
        │
        ▼
break
14. Campo intentos

El campo:

intentos

representa el número de eventos que han provocado la alerta.

En la correlación actual se proporciona mediante:

intentos=umbral

Por ejemplo:

umbral = 3

produce:

intentos = 3

v3.8 añade validación explícita sobre este campo porque forma parte del contrato de la alerta.

15. Validación del tipo de intentos

El constructor comprueba:

if not isinstance(intentos, int):
    raise TypeError("Intentos inválidos")

Esto evita estructuras como:

intentos="3"

Aunque visualmente:

"3"

y:

3

puedan parecer equivalentes, representan tipos diferentes.

El contrato exige:

int

y no:

str

Esta distinción permite que las capas posteriores puedan utilizar el campo sin tener que comprobar continuamente su tipo.

16. Validación del valor de intentos

Además del tipo, se valida el valor:

if intentos < 1:
    raise ValueError("Intentos inválidos")

Por tanto:

intentos = 0

no representa una alerta válida.

Tampoco:

intentos = -1

La diferencia conceptual es:

"3"
 │
 └── tipo incorrecto
     └── TypeError

0
│
└── tipo correcto
    pero valor inválido
    └── ValueError

Esta separación continúa la filosofía utilizada en otros módulos del proyecto.

17. TypeError frente a ValueError

v3.8 vuelve a trabajar una diferencia importante de Python.

Se utiliza:

TypeError

cuando el dato pertenece a un tipo que el contrato no admite.

Ejemplo:

intentos="tres"

Se utiliza:

ValueError

cuando el tipo es correcto pero su valor no pertenece al dominio permitido.

Ejemplo:

intentos=0

Conceptualmente:

DATO
 │
 ▼
¿tipo correcto?
 │
 ├── NO ──► TypeError
 │
 └── SÍ
      │
      ▼
 ¿valor permitido?
      │
      ├── NO ──► ValueError
      └── SÍ ──► continuar

Esta diferenciación hace que los errores sean más precisos y facilita los tests del contrato.

18. Campo fecha

El constructor acepta:

fecha=None

como argumento opcional.

La alerta contiene siempre la clave:

fecha

aunque su valor pueda ser:

None

Esto permite mantener una estructura estable.

Una alerta puede representarse como:

{
    "ip": "192.168.1.20",
    "tipo": "POSIBLE_FUERZA_BRUTA",
    "severidad": "ALTA",
    "intentos": 3,
    "ventana_segundos": 20.0,
    "lineas": [1, 2, 3],
    "fecha": None,
}

o, cuando se proporcione información temporal:

{
    "ip": "192.168.1.20",
    "tipo": "POSIBLE_FUERZA_BRUTA",
    "severidad": "ALTA",
    "intentos": 3,
    "ventana_segundos": 20.0,
    "lineas": [1, 2, 3],
    "fecha": fecha,
}

El objetivo en v3.8 no es desarrollar lógica adicional alrededor de este campo, sino incorporarlo al contrato para que la estructura pueda evolucionar posteriormente sin tener que rediseñarse.

19. RED 1 — Constructor de alertas

El desarrollo de v3.8 comenzó siguiendo TDD.

El primer objetivo fue definir el comportamiento esperado antes de implementar:

core/alertas.py

Se creó:

test/test_alertas.py

con un test que intentaba importar:

from core.alertas import crear_alerta_seguridad

En RED, pytest produjo:

ModuleNotFoundError:
No module named 'core.alertas'

Este fallo era el esperado.

Demostraba que el test estaba caracterizando una funcionalidad que todavía no existía.

El primer contrato exigía que el constructor produjera una alerta con:

ip
tipo
severidad
intentos
ventana_segundos
lineas
20. GREEN 1 — Primer constructor funcional

Para superar el primer RED se creó:

core/alertas.py

con:

crear_alerta_seguridad()

La primera implementación se mantuvo deliberadamente pequeña.

El objetivo del ciclo GREEN no era anticipar todas las validaciones futuras, sino implementar únicamente lo necesario para satisfacer el comportamiento caracterizado.

El resultado fue:

1 passed

junto con:

All checks passed!

en Ruff.

Este ciclo estableció la base de v3.8.

21. RED 2 — Incorporación de fecha

El siguiente ciclo añadió al contrato el campo:

fecha

El nuevo test llamó al constructor mediante:

crear_alerta_seguridad(
    ip="192.168.1.20",
    intentos=3,
    ventana_segundos=20,
    lineas=[1, 2, 3],
    fecha=fecha,
)

La implementación todavía no aceptaba ese argumento.

El resultado RED fue:

TypeError:
crear_alerta_seguridad()
got an unexpected keyword argument 'fecha'

El fallo demostraba exactamente qué parte del contrato faltaba.

22. GREEN 2 — Fecha opcional y regresión del contrato

Se añadió:

fecha=None

al constructor.

El test específico pasó correctamente.

Sin embargo, al ejecutar todos los tests de alertas apareció una regresión.

El test original esperaba una estructura sin:

fecha

mientras que el constructor actualizado devolvía:

fecha = None

Pytest mostró que el diccionario contenía una clave adicional.

Este resultado obligó a decidir cuál debía ser realmente el contrato.

La decisión fue mantener:

fecha

como parte estable de la estructura, incluso cuando no exista un valor temporal.

Por tanto, el test inicial se actualizó para representar el nuevo contrato.

El resultado final del ciclo fue:

2 passed

Este punto es importante porque muestra que TDD no consiste únicamente en conseguir tests verdes.

También obliga a decidir explícitamente cuál es el comportamiento que debe considerarse correcto.

23. RED 3 — Integración con la correlación

Después de construir el nuevo módulo era necesario demostrar que:

detectar_fuerza_bruta_temporal()

realmente lo utilizaba.

Para ello se añadió:

test/test_analizador_logs_alertas.py

El test utilizó:

monkeypatch

para sustituir temporalmente:

crear_alerta_seguridad

por un constructor controlado.

En el primer RED apareció:

AttributeError

porque:

core.analizador_logs

todavía no disponía de:

crear_alerta_seguridad

Esto demostraba que el nuevo constructor todavía no estaba integrado.

24. GREEN 3 — Integración y detección de duplicados

Se incorporó:

from core.alertas import crear_alerta_seguridad

en:

core/analizador_logs.py

y se sustituyó la construcción manual de la alerta.

El primer intento de integración no quedó correctamente cerrado.

El test devolvió:

2 alertas

cuando debía existir:

1 alerta

La regresión también fue detectada por los tests históricos:

test_analizador_logs_correlacion.py

Esto fue especialmente útil porque demostró que los tests anteriores seguían protegiendo el comportamiento del algoritmo durante el refactor.

Después de corregir la integración:

test integración
1 passed

correlación
5 passed

alertas
3 passed

La normalización quedó integrada sin alterar el comportamiento esperado.

25. RED 4 — Valor inválido de intentos

El siguiente ciclo TDD añadió una restricción al contrato.

Se caracterizó:

intentos=0

como inválido.

El test esperaba:

ValueError

con:

Intentos inválidos

La implementación inicial no realizaba esta validación.

Por tanto, pytest indicó:

Failed: DID NOT RAISE ValueError

El RED demostraba que el constructor todavía aceptaba estados que no tenían sentido dentro del dominio de una alerta.

26. GREEN 4 — Validación del valor

La implementación añadió:

if intentos < 1:
    raise ValueError("Intentos inválidos")

El test específico pasó.

La ejecución conjunta produjo:

4 passed

en los tests de alertas y:

5 passed

en correlación.

Durante esta fase Ruff detectó además un problema independiente:

Import block is un-sorted or un-formatted

en:

test/test_alertas.py

El orden de imports fue corregido antes de continuar.

Después:

All checks passed!
27. RED 5 — Tipo inválido de intentos

El último ciclo funcional caracterizó:

intentos="3"

como inválido.

El test esperaba:

TypeError

con el mensaje:

Intentos inválidos

La implementación existente realizaba directamente:

if intentos < 1:

Por tanto, Python intentó comparar:

str < int

y produjo:

'<' not supported between instances
of 'str' and 'int'

Aunque técnicamente era un TypeError, no procedía del contrato definido por FileOrganizer.

Era una excepción accidental causada por la operación de comparación.

El RED permitió distinguir ambos casos.

28. GREEN 5 — Validación explícita del tipo

La solución consistió en validar primero:

if not isinstance(intentos, int):
    raise TypeError("Intentos inválidos")

y después:

if intentos < 1:
    raise ValueError("Intentos inválidos")

El orden es importante.

Primero:

TIPO

y después:

VALOR

El test específico terminó:

1 passed

Los tests de alertas:

5 passed

y los de correlación:

5 passed

Ruff y compilación también finalizaron correctamente.

29. Regresión global después de GREEN 5

Una vez completados los cinco ciclos principales se ejecutó la batería completa de FileOrganizer.

El resultado fue:

197 passed

en:

0.22s

La evolución respecto a v3.7 fue:

v3.7 → 192 tests
v3.8 → 197 tests

Por tanto, v3.8 incorpora:

5 tests adicionales

al total del proyecto.

La regresión global confirmó que la introducción de:

core/alertas.py

no rompía las funcionalidades desarrolladas en las versiones anteriores.

---

## 30. Tests específicos añadidos en v3.8

v3.8 incorpora dos nuevos archivos de tests:

```text
test/test_alertas.py
test/test_analizador_logs_alertas.py
El primero se concentra en el contrato del nuevo constructor:

crear_alerta_seguridad()

El segundo verifica su integración real con:

detectar_fuerza_bruta_temporal()

Esta separación mantiene la misma estrategia utilizada durante las versiones anteriores.

Conceptualmente:

test_alertas.py
│
└── prueba el componente de forma aislada

test_analizador_logs_alertas.py
│
└── prueba la colaboración entre componentes

Esto permite distinguir dos preguntas diferentes:

¿funciona alertas.py?

y:

¿analizador_logs.py utiliza realmente alertas.py?

Una implementación podría superar la primera pregunta y fallar en la segunda.

Por eso ambos niveles de testing son necesarios.

31. Uso de monkeypatch en la integración

El test de integración utiliza la fixture:

monkeypatch

de pytest.

El objetivo es sustituir temporalmente:

core.analizador_logs.crear_alerta_seguridad

por una función controlada durante el test.

Conceptualmente:

detectar_fuerza_bruta_temporal()
            │
            ▼
crear_alerta_seguridad() real

se transforma temporalmente en:

detectar_fuerza_bruta_temporal()
            │
            ▼
constructor controlado por el test

Si el resultado devuelto por el correlador contiene exactamente el objeto proporcionado por el constructor simulado, se demuestra que existe colaboración entre ambos componentes.

Esta técnica evita depender únicamente de que dos implementaciones produzcan casualmente diccionarios iguales.

El test verifica directamente la interacción arquitectónica.

32. Por qué probar la integración

Un test exclusivo sobre:

crear_alerta_seguridad()

demostraría que el constructor funciona.

Pero no demostraría que:

detectar_fuerza_bruta_temporal()

lo utiliza.

El analizador podría continuar construyendo manualmente:

{
    ...
}

y los tests del constructor seguirían pasando.

Por eso v3.8 incorpora un test específico de integración.

La propiedad que se quiere proteger es:

CORRELACIÓN
     │
     ▼
DEBE DELEGAR
     │
     ▼
CONSTRUCTOR DE ALERTAS

Este tipo de test protege una decisión de arquitectura y no solamente un resultado final.

33. Protección mediante tests históricos

Los tests existentes de correlación fueron especialmente importantes durante v3.8.

El archivo:

test/test_analizador_logs_correlacion.py

ya verificaba propiedades como:

detección dentro de una ventana temporal
ausencia de alerta fuera de la ventana
separación entre diferentes IP
ausencia de alerta por debajo del umbral
uso de la fecha normalizada

Cuando la primera integración del constructor produjo dos alertas en lugar de una, estos tests fallaron inmediatamente.

Esto demuestra una ventaja fundamental de una batería acumulativa.

Los tests de versiones anteriores se convierten en una red de seguridad para los refactors posteriores.

La evolución puede representarse como:

v3.6 tests
   │
   ▼
protegen v3.7
   │
   ▼
tests v3.7
   │
   ▼
protegen v3.8

El proyecto no depende únicamente de probar la funcionalidad nueva.

También comprueba que la funcionalidad histórica continúa siendo válida.

34. Regresión específica de correlación

Después de corregir la integración se ejecutó:

test/test_analizador_logs_correlacion.py

El resultado fue:

5 passed

Esto confirmó que se conservaban las cinco propiedades principales caracterizadas para la correlación temporal.

Entre ellas se encuentra una especialmente importante heredada de v3.7:

la correlación utiliza evento["fecha"]
cuando la fecha normalizada está disponible

Por tanto, v3.8 no revierte la normalización temporal realizada anteriormente.

El flujo sigue siendo:

evento normalizado
       │
       ▼
fecha datetime
       │
       ▼
correlación
       │
       ▼
alerta normalizada
35. Regresión específica de alertas

Después de los ciclos RED/GREEN se ejecutaron conjuntamente los tests relacionados con alertas.

El resultado observado antes de la regresión global confirmó:

10 passed

para el conjunto utilizado en la validación de alertas e integración.

Esto permitió validar conjuntamente:

constructor
validaciones
fecha opcional
integración
correlación

antes de ejecutar toda la batería del proyecto.

La estrategia utilizada durante v3.8 fue:

test específico
      │
      ▼
tests del módulo
      │
      ▼
tests relacionados
      │
      ▼
regresión global

Esta progresión reduce el ruido durante el desarrollo.

36. Ruff y calidad de código

Además de pytest, v3.8 mantiene Ruff como herramienta de análisis estático.

Durante el desarrollo se detectó:

I001
Import block is un-sorted or un-formatted

en:

test/test_alertas.py

El problema se encontraba en el orden de:

from datetime import datetime

import pytest

from core.alertas import crear_alerta_seguridad

Después de corregir el bloque de imports, Ruff finalizó con:

All checks passed!

La ejecución final sobre el proyecto completo también terminó sin avisos.

Esto mantiene el criterio de calidad aplicado desde v3.2.

37. Compilación

Además de los tests y Ruff se comprobó la compilación de los módulos Python mediante:

python3 -m py_compile organizador.py core/*.py ui/*.py

La ejecución no produjo errores.

Esta comprobación permite detectar problemas sintácticos o de importación básicos independientemente de las rutas concretas ejecutadas por los tests.

La validación final combina:

pytest
   +
Ruff
   +
py_compile
   +
git diff --check
38. git diff --check

Durante el pre-commit apareció un detalle de formato en:

core/alertas.py

Git detectó:

trailing whitespace

en una línea en blanco.

El aviso apareció mediante:

git diff --cached --check

La línea fue corregida antes del commit.

Después:

CHECK STAGED

no mostró ningún problema.

Este control evita introducir espacios finales innecesarios y otros errores de whitespace en el historial del repositorio.

39. Inspección pre-staging

Antes de preparar el commit se revisó el estado real del proyecto.

Los cambios funcionales eran:

M  core/analizador_logs.py
?? core/alertas.py
?? test/test_alertas.py
?? test/test_analizador_logs_alertas.py

Los nuevos archivos tenían aproximadamente:

 21  core/alertas.py
 84  test/test_alertas.py
 68  test/test_analizador_logs_alertas.py

El cambio se mantuvo deliberadamente pequeño.

El nuevo módulo productivo contiene únicamente la responsabilidad necesaria para normalizar alertas.

No se introdujo lógica adicional de correlación ni nuevas familias de detección.

40. Actualización de versión visible

Antes del commit funcional se detectó que:

organizador.py

todavía mostraba:

FILE ORGANIZER v3.7

Se actualizó a:

FILE ORGANIZER v3.8

El cambio fue:

v3.7
  │
  ▼
v3.8

Esta modificación se incorporó al mismo commit funcional porque representa la versión real del código que se estaba cerrando.

41. Pre-commit final

Después de añadir también:

organizador.py

el staging quedó compuesto por:

A  core/alertas.py
M  core/analizador_logs.py
M  organizador.py
A  test/test_alertas.py
A  test/test_analizador_logs_alertas.py

El resumen fue:

5 files changed
181 insertions
9 deletions

No existían cambios fuera del staging.

Tampoco aparecieron problemas mediante:

git diff --cached --check

Esto permitió realizar el commit funcional sobre un estado controlado.

42. Commit funcional de v3.8

La implementación funcional quedó registrada mediante:

e094932  v3.8: normaliza alertas de seguridad

El commit contiene:

core/alertas.py
core/analizador_logs.py
organizador.py
test/test_alertas.py
test/test_analizador_logs_alertas.py

Después del commit:

git status --short

quedó limpio.

La relación con el remoto era:

main...origin/main [adelante 1]

Esto significa que el código funcional estaba registrado localmente pero todavía pendiente de publicación junto con la documentación final.

43. Evolución de responsabilidades

La evolución de las últimas versiones puede observarse mediante las responsabilidades extraídas del analizador.

Antes:

analizador_logs.py
│
├── definiciones de detección
├── evaluación
├── construcción de eventos
├── análisis
├── correlación
└── construcción de alertas

Después de v3.6:

reglas_logs.py
└── detecciones

analizador_logs.py
├── análisis
├── construcción de eventos
├── correlación
└── construcción de alertas

Después de v3.7:

reglas_logs.py
└── detecciones

eventos.py
└── construcción de eventos

analizador_logs.py
├── análisis
├── correlación
└── construcción de alertas

Después de v3.8:

reglas_logs.py
└── detecciones

eventos.py
└── construcción de eventos

analizador_logs.py
├── análisis
└── correlación

alertas.py
└── construcción de alertas

La evolución no consiste simplemente en crear más archivos.

Cada extracción elimina una responsabilidad concreta de un módulo que estaba acumulando demasiadas funciones conceptuales.

44. Arquitectura defensiva final

La arquitectura específica del análisis de logs queda:

                       LOG
                        │
                        ▼
                 analizador_logs.py
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
                 correlación temporal
                        │
                        ▼
                    alertas.py
                        │
                        ▼
                alerta normalizada

Otra forma de representarlo es:

REGLA
  │
  ▼
DETECCIÓN
  │
  ▼
EVENTO
  │
  ▼
CORRELACIÓN
  │
  ▼
ALERTA

Esta secuencia resume la evolución realizada durante v3.6, v3.7 y v3.8.

45. Flujo completo de una detección

Una línea de log entra en:

analizar_linea()

El motor:

reglas_logs.py

evalúa las reglas configuradas.

Si existe una coincidencia:

línea
  │
  ▼
regla coincidente

se llama a:

crear_evento_seguridad()

El resultado es:

evento normalizado

Los eventos pueden posteriormente entrar en:

detectar_fuerza_bruta_temporal()

La función agrupa, filtra, ordena y correlaciona.

Cuando encuentra una ventana válida llama a:

crear_alerta_seguridad()

y obtiene:

alerta normalizada

El flujo completo es:

línea de log
     │
     ▼
evaluar reglas
     │
     ▼
detección
     │
     ▼
crear evento
     │
     ▼
evento normalizado
     │
     ▼
correlacionar
     │
     ▼
crear alerta
     │
     ▼
alerta normalizada
46. Relación conceptual con sistemas defensivos

FileOrganizer no pretende convertirse en un SIEM real.

Sin embargo, las últimas versiones permiten practicar conceptos que aparecen en sistemas defensivos de mayor escala.

Conceptualmente pueden distinguirse:

detección
normalización
correlación
alertado

En FileOrganizer:

reglas_logs.py
      │
      └── detección

eventos.py
      │
      └── normalización de eventos

analizador_logs.py
      │
      └── correlación

alertas.py
      │
      └── normalización de alertas

Esta arquitectura permite comprender por qué en herramientas defensivas reales resulta útil separar los datos observados de las conclusiones obtenidas a partir de ellos.

47. Evento frente a correlación

Un evento puede existir sin producir una alerta.

Por ejemplo:

1 intento fallido

puede generar:

EVENTO FUERZA_BRUTA

según la nomenclatura utilizada actualmente por las reglas del proyecto.

Pero el correlador puede exigir:

3 intentos

dentro de:

60 segundos

antes de producir:

POSIBLE_FUERZA_BRUTA

Por tanto:

evento
   │
   └── observación individual

alerta
   │
   └── resultado de aplicar una condición
       sobre uno o varios eventos

Esta diferencia evita tratar todas las detecciones individuales como si tuvieran automáticamente el mismo significado operativo.

48. Correlación como capa independiente

Aunque actualmente la función de correlación permanece en:

core/analizador_logs.py

v3.8 deja conceptualmente delimitada su responsabilidad.

La correlación recibe:

EVENTOS

y produce:

ALERTAS

Por tanto:

eventos
   │
   ▼
correlación
   │
   ▼
alertas

La versión no extrae esta lógica a otro módulo porque el objetivo de v3.8 es pequeño y acotado.

Crear nuevas capas únicamente por simetría habría ampliado innecesariamente el alcance.

La decisión fue detener el refactor cuando la responsabilidad de representación de alertas quedó separada.

49. Por qué v3.8 es deliberadamente pequeña

Después de varias versiones centradas en Blue Team existía el riesgo de continuar ampliando indefinidamente el mismo subsistema.

v3.8 se definió desde el principio como:

pequeña
acotada
orientada a alertas
última evolución defensiva de esta fase

El objetivo no era añadir:

más reglas
más correladores
más formatos de logs
más dashboards
más almacenamiento

sino cerrar una inconsistencia arquitectónica concreta:

eventos normalizados
pero alertas construidas manualmente

Una vez resuelta:

eventos normalizados
+
alertas normalizadas

la fase puede considerarse cerrada para los objetivos actuales del proyecto.

50. Evitar sobreingeniería

Una parte importante del aprendizaje de arquitectura consiste también en saber cuándo detener una evolución.

Sería posible continuar con:

core/correladores.py
core/severidades.py
core/tipos_eventos.py
core/tipos_alertas.py
core/persistencia_eventos.py
core/persistencia_alertas.py

Pero cada abstracción adicional necesita justificar su existencia.

Para el alcance actual de FileOrganizer, v3.8 busca un equilibrio:

separación suficiente
        +
código comprensible
        +
tests sólidos
        +
alcance controlado

Esto evita convertir un proyecto de aprendizaje en una arquitectura artificialmente compleja.

51. Conocimientos de Python trabajados

v3.8 refuerza varios conceptos de Python ya utilizados anteriormente.

Entre ellos:

funciones
parámetros opcionales
diccionarios
listas
isinstance()
excepciones
imports entre módulos
comparaciones
break
lambda
ordenación con sort()

También se trabaja de nuevo la diferencia entre:

TypeError

y:

ValueError

y la importancia de validar los datos antes de realizar operaciones sobre ellos.

52. Parámetros opcionales

La firma:

def crear_alerta_seguridad(
    ip,
    intentos,
    ventana_segundos,
    lineas,
    fecha=None,
):

utiliza:

fecha=None

como parámetro opcional.

Esto permite:

crear_alerta_seguridad(
    ip=ip,
    intentos=3,
    ventana_segundos=20,
    lineas=[1, 2, 3],
)

y también:

crear_alerta_seguridad(
    ip=ip,
    intentos=3,
    ventana_segundos=20,
    lineas=[1, 2, 3],
    fecha=fecha,
)

El contrato conserva en ambos casos:

fecha

como clave del resultado.

53. Validación antes de operar

El RED 5 mostró un ejemplo práctico de por qué conviene validar tipos antes de realizar operaciones.

La versión problemática hacía:

if intentos < 1:

sin comprobar previamente el tipo.

Con:

intentos="3"

Python intentaba realizar:

str < int

La versión final realiza:

validar tipo
     │
     ▼
validar valor
     │
     ▼
construir alerta

Esto produce errores controlados por el propio módulo en lugar de errores accidentales derivados de una operación incompatible.

54. Conocimientos de testing trabajados

v3.8 vuelve a aplicar:

TDD
RED
GREEN
regresión
tests unitarios
tests de integración
monkeypatch
pytest.raises
comparación de estructuras

Especialmente importante fue:

monkeypatch

porque permitió comprobar una colaboración entre módulos.

La versión demuestra que los tests pueden proteger:

resultado funcional

pero también:

decisiones de diseño
55. Ciclo de desarrollo utilizado

La secuencia seguida durante v3.8 fue:

RED 1
constructor inexistente
     │
     ▼
GREEN 1
constructor mínimo
     │
     ▼
RED 2
fecha
     │
     ▼
GREEN 2
contrato con fecha
     │
     ▼
RED 3
integración
     │
     ▼
GREEN 3
correlador usa constructor
     │
     ▼
RED 4
valor intentos
     │
     ▼
GREEN 4
ValueError
     │
     ▼
RED 5
tipo intentos
     │
     ▼
GREEN 5
TypeError
     │
     ▼
REGRESIÓN GLOBAL

Este desarrollo incremental permitió introducir cada requisito de forma aislada.

56. Métricas finales

El cierre funcional de v3.8 alcanza:

197 tests

frente a:

192 tests

en v3.7.

La evolución reciente queda:

v3.2 → 101 tests
v3.3 → 131 tests
v3.4 → 151 tests
v3.5 → 165 tests
v3.6 → 182 tests
v3.7 → 192 tests
v3.8 → 197 tests

Desde v3.2 hasta v3.8 la batería ha aumentado en:

96 tests

manteniendo la regresión completa en verde al cierre funcional de cada versión.

57. Archivos añadidos

v3.8 incorpora:

core/alertas.py
test/test_alertas.py
test/test_analizador_logs_alertas.py

El módulo productivo introduce el constructor de alertas.

Los tests se dividen entre:

contrato

e:

integración

Esta estructura mantiene los nuevos cambios localizados y fáciles de identificar.

58. Archivos modificados

La versión modifica:

core/analizador_logs.py
organizador.py

core/analizador_logs.py cambia para delegar la construcción de alertas.

organizador.py cambia únicamente la versión visible:

v3.7 → v3.8

La documentación modifica además:

README.md

e incorpora:

docs/Resumen_v3.8_Normalizacion_Alertas.md

durante el cierre documental.

59. Evolución respecto a v3.7

v3.7 dejó:

REGLAS
   │
   ▼
EVENTOS NORMALIZADOS
   │
   ▼
CORRELACIÓN
   │
   ▼
DICCIONARIO DE ALERTA

v3.8 transforma el último nivel:

REGLAS
   │
   ▼
EVENTOS NORMALIZADOS
   │
   ▼
CORRELACIÓN
   │
   ▼
ALERTAS NORMALIZADAS

El cambio concreto es:

construcción manual
        │
        ▼
constructor especializado

Por tanto, v3.8 completa la simetría conceptual entre:

evento

y:

alerta

sin ampliar innecesariamente el motor defensivo.

60. Evolución v3.6 → v3.8

Las tres últimas versiones forman una secuencia arquitectónica clara.

v3.6
MOTOR DE REGLAS

Pregunta principal:

¿qué detectar?

Componente:

reglas_logs.py
v3.7
NORMALIZACIÓN DE EVENTOS

Pregunta principal:

¿cómo representar una detección?

Componente:

eventos.py
v3.8
NORMALIZACIÓN DE ALERTAS

Pregunta principal:

¿cómo representar una correlación?

Componente:

alertas.py

La evolución completa puede resumirse:

v3.6
REGLAS
   │
   ▼
v3.7
EVENTOS
   │
   ▼
v3.8
ALERTAS
61. Estado de calidad

Al finalizar el código de v3.8 se verificó:

pytest
197 passed
Ruff
All checks passed!
py_compile
sin errores
git diff --check
sin errores

También se revisó el staging antes del commit y se eliminó el trailing whitespace detectado.

El commit funcional quedó con el árbol limpio.

62. README de v3.8

El README se actualiza para reflejar:

FILE ORGANIZER v3.8

y la estructura incorpora:

core/alertas.py

junto con:

test/test_alertas.py
test/test_analizador_logs_alertas.py

También se añade un bloque específico:

v3.8 — Normalización de alertas de seguridad

que resume:

objetivo
nuevo módulo
contrato
integración
validaciones
TDD
tests
arquitectura
resultado

El historial anterior del README se conserva.

63. Commit principal

La implementación funcional de v3.8 está registrada en:

e094932  v3.8: normaliza alertas de seguridad

Este commit representa el cierre del código de la versión.

La documentación se registra posteriormente en un commit independiente, siguiendo el procedimiento utilizado en las versiones anteriores.

64. Resultado de v3.8

v3.8 consigue separar la última responsabilidad de representación que permanecía integrada dentro de la correlación temporal.

Antes:

analizador_logs.py
        │
        ├── analiza
        ├── correlaciona
        └── construye alerta

Después:

analizador_logs.py
        │
        ├── analiza
        └── correlaciona
                 │
                 ▼
             alertas.py
                 │
                 └── construye alerta

La arquitectura queda más explícita sin modificar el comportamiento funcional de la correlación.

65. Cierre de la fase Blue Team

v3.8 se definió como la última evolución defensiva de esta etapa.

FileOrganizer ya ha servido para trabajar progresivamente:

organización de archivos
configuración
historial
deshacer
estadísticas
duplicados
SHA-256
magic numbers
verificación de tipos
cuarentena
robustez
testing
monitor de integridad
auditoría
análisis de logs
reglas de detección
eventos normalizados
correlación temporal
alertas normalizadas

Continuar añadiendo funcionalidades defensivas sería posible, pero dejaría de responder al objetivo actual de aprendizaje.

El proyecto dispone ya de suficiente profundidad para mostrar una evolución técnica real y documentada.

66. FileOrganizer como proyecto de portfolio

FileOrganizer comenzó como un organizador de archivos.

Su evolución ha permitido incorporar progresivamente conceptos de:

Python
arquitectura modular
testing
Git
seguridad de archivos
integridad
auditoría
análisis defensivo

Esto permite mostrar no solamente un resultado final, sino un proceso de evolución.

El historial de versiones refleja:

problema
   │
   ▼
diseño
   │
   ▼
implementación
   │
   ▼
tests
   │
   ▼
refactor
   │
   ▼
documentación

Ese proceso constituye una parte importante del valor del proyecto como portfolio.

67. Transición hacia Red Team

Después del cierre de v3.8, el siguiente objetivo de aprendizaje deja de ser ampliar FileOrganizer por inercia.

La siguiente fase se orienta a:

RED TEAM

en entornos propios, controlados o expresamente autorizados.

La progresión prevista comienza por:

fundamentos de redes ofensivas
        │
        ▼
reconocimiento
        │
        ▼
Nmap
        │
        ▼
enumeración de servicios
        │
        ▼
HTTP y aplicaciones web
        │
        ▼
Burp Suite
        │
        ▼
análisis de vulnerabilidades
        │
        ▼
explotación en laboratorio

La transición no elimina el conocimiento Blue Team adquirido.

Al contrario, comprender:

logs
eventos
reglas
correlación
alertas
integridad

ayuda a entender qué huella producen posteriormente las acciones realizadas durante ejercicios ofensivos.

68. Relación entre Blue Team y Red Team

El trabajo realizado en FileOrganizer permite entrar en la fase ofensiva con una perspectiva defensiva previa.

Por ejemplo, durante Red Team se podrá relacionar:

acción ofensiva
      │
      ▼
tráfico / petición / intento
      │
      ▼
registro en logs
      │
      ▼
evento
      │
      ▼
correlación
      │
      ▼
alerta

Esto ayuda a evitar estudiar las herramientas ofensivas únicamente como una colección de comandos.

El objetivo será comprender también:

qué hace la técnica
por qué funciona
qué información utiliza
qué deja registrado
cómo podría detectarse
69. Próximos pasos

Después de cerrar y publicar v3.8:

FileOrganizer

queda congelado como proyecto principal de esta fase defensiva.

Las mejoras futuras no desaparecen, pero dejan de ser prioritarias.

El siguiente bloque de aprendizaje será:

RED TEAM — FUNDAMENTOS

con una progresión práctica y controlada.

El primer objetivo será consolidar redes desde una perspectiva ofensiva antes de comenzar con enumeración avanzada o explotación.

70. Checklist de cierre de v3.8
Código
[x] crear core/alertas.py
[x] crear crear_alerta_seguridad()
[x] integrar constructor con correlación
[x] mantener compatibilidad temporal
[x] actualizar versión visible a v3.8
Testing
[x] RED/GREEN constructor
[x] RED/GREEN fecha
[x] RED/GREEN integración
[x] RED/GREEN intentos inválidos
[x] RED/GREEN tipo de intentos
[x] regresión de correlación
[x] regresión global
[x] 197 tests
Calidad
[x] Ruff limpio
[x] compilación correcta
[x] git diff --check
[x] staging inspeccionado
[x] trailing whitespace corregido
Git
[x] commit funcional
[x] e094932
[ ] commit documentación
[ ] push main
[ ] crear tag v3.8
[ ] publicar tag v3.8
Documentación
[x] actualizar README
[x] documentar arquitectura v3.8
[x] crear Resumen_v3.8_Normalizacion_Alertas.md
[ ] validar documentación
[ ] registrar commit documental
71. Conclusión

FileOrganizer v3.8 completa la normalización del flujo defensivo desarrollado durante las últimas versiones.

La arquitectura final puede resumirse como:

                   FILEORGANIZER v3.8
                            │
                            ▼
                           LOG
                            │
                            ▼
                      reglas_logs.py
                            │
                            ▼
                     DETECCIONES
                            │
                            ▼
                        eventos.py
                            │
                            ▼
                 EVENTOS NORMALIZADOS
                            │
                            ▼
                  analizador_logs.py
                            │
                            ▼
                      CORRELACIÓN
                            │
                            ▼
                        alertas.py
                            │
                            ▼
                 ALERTAS NORMALIZADAS

v3.6 respondió:

¿qué detectar?

v3.7 respondió:

¿cómo representar los eventos?

v3.8 responde:

¿cómo representar las alertas?

Con esta versión se cierra de forma deliberada la fase Blue Team principal de FileOrganizer.

El proyecto queda con:

197 tests
Ruff limpio
compilación correcta
arquitectura modular
historial Git
documentación por versiones
