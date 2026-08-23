# FileOrganizer v3.3 — Monitor de Integridad de Archivos (FIM)

## 1. Introducción

La versión v3.3 representa una nueva evolución de FileOrganizer hacia funcionalidades relacionadas con ciberseguridad defensiva.

En v3.1 el proyecto incorporó una primera capa de seguridad:

- identificación mediante magic numbers;
- comparación entre extensión y contenido real;
- detección de archivos sospechosos;
- cuarentena;
- análisis defensivo de logs;
- detección de patrones relacionados con SQL Injection;
- análisis de fallos de autenticación;
- correlación de posibles ataques de fuerza bruta.

Posteriormente, v3.2 reforzó la forma de desarrollar el proyecto mediante:

- pytest;
- tests de robustez;
- tests de regresión;
- Ruff;
- análisis estático;
- refactorización controlada;
- revisión del tratamiento de excepciones;
- validación continua.

La versión v3.3 utiliza esa infraestructura para desarrollar una nueva funcionalidad defensiva:

```text
File Integrity Monitoring
```

o:

```text
FIM
```

El objetivo consiste en poder registrar el estado conocido de una carpeta y detectar posteriormente si sus archivos han cambiado.

El flujo fundamental es:

```text
CARPETA
   │
   ▼
generar snapshot
   │
   ▼
calcular SHA-256
   │
   ▼
guardar baseline
   │
   │
   │ pasa el tiempo
   ▼
nuevo snapshot
   │
   ▼
comparar estados
   │
   ├── sin cambios
   ├── modificados
   ├── nuevos
   └── eliminados
```

Esta funcionalidad introduce en FileOrganizer un concepto utilizado en seguridad defensiva: comprobar si determinados archivos han sufrido modificaciones respecto a un estado considerado conocido.

---

## 2. Punto de partida de v3.3

v3.3 comienza sobre la base estable dejada por v3.2.

El estado inicial era:

```text
101 tests
Ruff limpio
compilación correcta
git diff --check limpio
main sincronizada
working tree limpio
```

Esto permitió desarrollar el nuevo monitor de integridad utilizando desde el principio la metodología aprendida anteriormente.

La estrategia adoptada fue:

```text
definir comportamiento
        │
        ▼
escribir test
        │
        ▼
ejecutar
        │
        ▼
       RED
        │
        ▼
implementar mínimo necesario
        │
        ▼
ejecutar
        │
        ▼
      GREEN
        │
        ▼
batería completa
```

Por tanto, v3.3 no solo incorpora una nueva funcionalidad.

También constituye la primera versión importante desarrollada aprovechando desde el comienzo la infraestructura de testing creada en v3.2.

---

## 3. Qué es File Integrity Monitoring

File Integrity Monitoring consiste en observar el estado de determinados archivos para detectar cambios posteriores.

Un archivo puede cambiar de diferentes formas.

Por ejemplo:

```text
archivo original
      │
      ├── contenido modificado
      ├── archivo eliminado
      └── permanece igual
```

Además, dentro de la carpeta vigilada pueden aparecer:

```text
archivos nuevos
```

Un FIM necesita disponer de algún estado anterior con el que comparar.

Ese estado se denomina habitualmente:

```text
baseline
```

La idea básica es:

```text
ESTADO CONOCIDO
      │
      ▼
   BASELINE
      │
      │ pasa el tiempo
      ▼
ESTADO ACTUAL
      │
      ▼
 COMPARACIÓN
```

Sin una referencia anterior no podemos saber si un archivo ha cambiado.

---

## 4. Qué es una baseline

Una baseline es una representación de un estado considerado conocido.

En FileOrganizer v3.3 contiene:

```text
ruta base
+
archivos
+
hash SHA-256 de cada archivo
```

Ejemplo conceptual:

```json
{
    "ruta_base": "/home/usuario/documentos",
    "archivos": {
        "informe.pdf": "hash...",
        "datos.txt": "hash...",
        "subcarpeta/config.json": "hash..."
    }
}
```

La baseline no contiene una copia completa de cada archivo.

Contiene una huella criptográfica de su contenido.

Esto permite posteriormente responder:

```text
¿el contenido actual sigue produciendo
el mismo SHA-256?
```

---

## 5. SHA-256 como huella del contenido

Para identificar el estado del contenido utilizamos:

```text
SHA-256
```

Un hash transforma datos de longitud variable en un valor de longitud fija.

Conceptualmente:

```text
contenido archivo
       │
       ▼
    SHA-256
       │
       ▼
64 caracteres hexadecimales
```

Ejemplo:

```text
80bd5123ef75b69c97fb748bf7c1cf2d5d760ecb975785768bdd3a897be68949
```

Si cambia el contenido:

```text
contenido A
   │
   ▼
hash A

contenido B
   │
   ▼
hash B
```

normalmente obtendremos valores diferentes.

Por eso podemos utilizar el hash para detectar modificaciones de contenido.

---

## 6. Hash no significa cifrado

Es importante distinguir:

```text
HASH
```

de:

```text
CIFRADO
```

Un hash no está pensado para recuperar el contenido original.

Conceptualmente:

```text
ARCHIVO
   │
   ▼
SHA-256
   │
   ▼
HUELLA
```

No utilizamos SHA-256 para ocultar el archivo.

Lo utilizamos para obtener una representación que permita comparar su contenido.

En FileOrganizer:

```text
mismo hash
    │
    ▼
contenido considerado sin cambios

hash diferente
    │
    ▼
contenido modificado
```

---

## 7. Nuevo módulo `core/integridad.py`

La lógica principal del FIM se concentra en:

```text
core/integridad.py
```

El módulo separa las operaciones de integridad de la presentación realizada por `organizador.py`.

Entre las responsabilidades desarrolladas se encuentran:

```text
calcular hash
generar snapshot
guardar baseline
cargar baseline
validar baseline
comparar integridad
```

Conceptualmente:

```text
core/integridad.py
       │
       ├── filesystem
       ├── SHA-256
       ├── JSON
       ├── validación
       └── comparación
```

Esta separación mantiene la arquitectura modular que FileOrganizer ha ido desarrollando en versiones anteriores.

---

## 8. Generación del snapshot

Una de las primeras funciones desarrolladas fue:

```python
generar_snapshot(carpeta)
```

Su responsabilidad consiste en recorrer una carpeta y construir una representación del estado actual de sus archivos.

El proceso puede representarse así:

```text
CARPETA
   │
   ▼
validar ruta
   │
   ▼
rglob("*")
   │
   ▼
localizar archivos
   │
   ▼
calcular SHA-256
   │
   ▼
guardar ruta relativa + hash
   │
   ▼
SNAPSHOT
```

El snapshot se representa mediante un diccionario.

Conceptualmente:

```python
{
    "ruta_base": "...",
    "archivos": {
        "archivo.txt": "sha256...",
        "subcarpeta/datos.bin": "sha256..."
    }
}
```

---

## 9. Recorrido recursivo con `rglob()`

El FIM necesita detectar archivos situados también dentro de subdirectorios.

Para ello se utiliza:

```python
Path.rglob("*")
```

Ejemplo:

```text
carpeta/
├── uno.txt
├── dos.txt
└── subcarpeta/
    └── interno.txt
```

El recorrido debe detectar:

```text
uno.txt
dos.txt
subcarpeta/interno.txt
```

Esto permite vigilar una estructura completa y no únicamente los archivos situados en el primer nivel.

---

## 10. Por qué almacenamos rutas relativas

Dentro de:

```text
archivos
```

no almacenamos necesariamente la ruta absoluta completa de cada archivo.

Utilizamos rutas relativas respecto a:

```text
ruta_base
```

Ejemplo:

```text
ruta_base:
/tmp/fileorganizer_fim_final
```

Archivo real:

```text
/tmp/fileorganizer_fim_final/subcarpeta/interno.txt
```

Ruta almacenada:

```text
subcarpeta/interno.txt
```

Esto produce una estructura más clara:

```text
BASE
 │
 ├── eliminado.txt
 ├── modificado.txt
 └── subcarpeta/interno.txt
```

en lugar de repetir:

```text
/tmp/fileorganizer_fim_final/
```

en cada entrada.

---

## 11. La importancia de `ruta_base`

Aunque los archivos se almacenan mediante rutas relativas, la baseline necesita conocer a qué carpeta pertenecen.

Por eso contiene:

```text
ruta_base
```

Ejemplo:

```json
{
    "ruta_base": "/tmp/fileorganizer_fim_final"
}
```

Esto permite comprobar posteriormente que:

```text
baseline
```

y:

```text
snapshot actual
```

corresponden a la misma carpeta.

Sin esta comprobación podríamos comparar accidentalmente dos árboles de archivos completamente diferentes.

---

## 12. `ruta_base` debe ser absoluta

Durante el desarrollo mediante TDD se detectó que no bastaba con comprobar que:

```text
ruta_base
```

fuera una cadena no vacía.

Una baseline como:

```json
{
    "ruta_base": "documentos"
}
```

es ambigua.

Su significado depende del directorio desde el que se ejecute el programa.

En cambio:

```json
{
    "ruta_base": "/home/usuario/documentos"
}
```

identifica una ubicación de forma explícita.

Por eso `cargar_baseline()` valida:

```python
Path(baseline["ruta_base"]).is_absolute()
```

Si no lo es:

```text
ValueError
```

Este comportamiento quedó protegido mediante tests.

---

## 13. Guardar una baseline

Una vez generado un snapshot necesitamos persistirlo.

Para ello se desarrolló:

```python
guardar_baseline(snapshot, ruta)
```

El flujo es:

```text
SNAPSHOT
   │
   ▼
validar destino
   │
   ▼
crear directorios necesarios
   │
   ▼
serializar JSON
   │
   ▼
baseline.json
```

La baseline permite conservar el estado incluso después de cerrar FileOrganizer.

Posteriormente podrá cargarse y compararse con un nuevo snapshot.

---

## 14. JSON como formato de persistencia

La baseline se almacena utilizando JSON.

Ejemplo real utilizado durante la prueba final:

```json
{
    "ruta_base": "/tmp/fileorganizer_fim_final",
    "archivos": {
        "eliminado.txt": "b2de01607389a694c96198a311137823fdc12649f25462ca2f36ff1e94455769",
        "sin_cambios.txt": "80bd5123ef75b69c97fb748bf7c1cf2d5d760ecb975785768bdd3a897be68949",
        "modificado.txt": "9660b3303631e95817f72c7536939f0eca9e20c0d7b86382a39e4a98a1b26151",
        "subcarpeta/interno.txt": "c06752892c2feacd9c38b2edc6febd90b1b1445c37f386ddf61ff3461bd7dd9c"
    }
}
```

JSON resulta apropiado para esta fase porque:

- es legible;
- puede inspeccionarse manualmente;
- Python dispone de soporte mediante la biblioteca estándar;
- permite representar diccionarios;
- facilita testing;
- no introduce dependencias externas.

---

## 15. Prevención de sobrescritura de baselines

Una baseline representa un estado de referencia.

Sobrescribirla accidentalmente podría destruir precisamente el estado que queríamos conservar.

Por eso se añadió protección frente a destinos ya existentes.

Conceptualmente:

```text
baseline.json existe
        │
        ▼
¿guardar encima?
        │
        ▼
       NO
        │
        ▼
FileExistsError
```

Este comportamiento obliga a tomar una decisión explícita antes de sustituir una referencia anterior.

La prevención de sobrescrituras es especialmente importante en una herramienta de integridad.

---

## 16. Carpeta `baselines/`

Para separar los estados generados del código fuente se utiliza:

```text
baselines/
```

La carpeta se añadió a:

```text
.gitignore
```

La razón es similar a otras carpetas generadas por FileOrganizer.

Las baselines pueden contener:

```text
rutas reales del sistema
nombres de archivos
estructura de directorios
información específica de una máquina
```

Por tanto, no deben incorporarse automáticamente al repositorio público.

Conceptualmente:

```text
CÓDIGO
  │
  └── Git

DATOS GENERADOS
  │
  └── baselines/
          │
          └── fuera de Git
```

---

## 17. Cargar una baseline

Para reutilizar una baseline se desarrolló:

```python
cargar_baseline(ruta)
```

La función no se limita a ejecutar:

```python
json.load()
```

También valida la estructura obtenida.

Esto es importante porque un archivo JSON puede ser sintácticamente correcto y, aun así, no representar una baseline válida.

Por ejemplo:

```json
{
    "nombre": "prueba"
}
```

es JSON válido.

Pero no es una baseline válida para FileOrganizer.

---

## 18. Validación de la estructura externa

Una baseline se encuentra almacenada fuera del flujo interno del programa.

Puede haber sido:

- modificada manualmente;
- truncada;
- generada por otra versión;
- manipulada;
- creada incorrectamente.

Por eso no debemos confiar automáticamente en su contenido.

`cargar_baseline()` comprueba inicialmente la existencia de:

```text
ruta_base
archivos
```

Si falta:

```text
ruta_base
```

se genera:

```text
ValueError
```

Si falta:

```text
archivos
```

también se genera:

```text
ValueError
```

Esto introduce un principio defensivo importante:

> Los datos externos deben validarse antes de utilizarlos.

---

## 19. Validación de tipos

No basta con comprobar que las claves existen.

También necesitamos comprobar sus tipos.

`ruta_base` debe ser:

```python
str
```

y:

```text
archivos
```

debe ser:

```python
dict
```

Por ejemplo:

```json
{
    "ruta_base": 1234,
    "archivos": {}
}
```

contiene las claves correctas.

Pero:

```text
ruta_base
```

tiene un tipo incorrecto.

La función genera:

```text
TypeError
```

Esta distinción permitió trabajar de forma práctica la diferencia entre:

```text
TypeError
```

y:

```text
ValueError
```

---

## 20. `TypeError` frente a `ValueError`

Durante v3.3 esta diferencia aparece de forma clara.

Ejemplo de tipo incorrecto:

```python
"ruta_base": 123
```

El dato debería ser texto.

Por tanto:

```text
TypeError
```

Ejemplo de tipo correcto pero valor inválido:

```python
"ruta_base": ""
```

Es una cadena.

Pero no representa una ruta válida.

Por tanto:

```text
ValueError
```

Podemos resumirlo:

```text
TIPO INCORRECTO
      │
      ▼
  TypeError

TIPO CORRECTO
pero contenido inválido
      │
      ▼
  ValueError
```

---

## 21. Validación de `ruta_base` vacía

Una baseline como:

```json
{
    "ruta_base": "   ",
    "archivos": {}
}
```

no debe aceptarse.

Aunque:

```text
"   "
```

es técnicamente una cadena, no identifica una carpeta válida.

Por eso se utiliza:

```python
baseline["ruta_base"].strip()
```

para comprobar que contiene información real.

Si queda vacía:

```text
ValueError
```

---

## 22. Validación de hashes

Los valores almacenados dentro de:

```text
archivos
```

deben representar hashes SHA-256.

No basta con que sean cadenas.

Por ejemplo:

```json
{
    "archivo.txt": "hola"
}
```

es una estructura JSON perfectamente válida.

Pero:

```text
hola
```

no representa un SHA-256.

Por eso se comprueba:

```text
longitud = 64
```

y que todos los caracteres pertenezcan a:

```text
0123456789abcdef
```

También se acepta la comprobación de caracteres independientemente de mayúsculas/minúsculas mediante normalización.

---

## 23. Por qué SHA-256 tiene 64 caracteres hexadecimales

SHA-256 produce:

```text
256 bits
```

Cada carácter hexadecimal representa:

```text
4 bits
```

Por tanto:

```text
256 / 4 = 64
```

De ahí que una representación hexadecimal SHA-256 tenga:

```text
64 caracteres
```

Ejemplo:

```text
b2de01607389a694c96198a311137823fdc12649f25462ca2f36ff1e94455769
```

Esta validación no demuestra por sí sola que el hash haya sido calculado realmente mediante SHA-256.

Pero sí permite rechazar estructuras evidentemente incompatibles con el formato esperado.

---

## 24. Validar antes de comparar

La comparación de integridad asume que trabaja con estructuras coherentes.

Por eso el flujo correcto es:

```text
archivo baseline
      │
      ▼
cargar JSON
      │
      ▼
validar estructura
      │
      ▼
baseline aceptada
      │
      ▼
comparar
```

y no:

```text
archivo externo
      │
      ▼
confiar directamente
      │
      ▼
comparar
```

Esta separación reduce la posibilidad de que datos mal formados provoquen resultados incorrectos o errores difíciles de interpretar posteriormente.

---

## 25. Comparación de integridad

La función principal para comparar estados es:

```python
comparar_integridad(baseline, actual)
```

El resultado se divide en cuatro categorías:

```python
{
    "sin_cambios": [],
    "modificados": [],
    "nuevos": [],
    "eliminados": [],
}
```

Cada categoría responde a una relación diferente entre:

```text
BASELINE
```

y:

```text
SNAPSHOT ACTUAL
```

---

## 26. Archivos sin cambios

Un archivo pertenece a:

```text
sin_cambios
```

cuando:

```text
existe en baseline
+
existe actualmente
+
hash anterior == hash actual
```

Conceptualmente:

```text
BASELINE
archivo.txt → AAA
        │
        ▼
ACTUAL
archivo.txt → AAA
        │
        ▼
SIN CAMBIOS
```

El nombre por sí solo no determina este estado.

La comparación se realiza mediante el hash del contenido.

---

## 27. Archivos modificados

Un archivo pertenece a:

```text
modificados
```

cuando:

```text
existe en baseline
+
existe actualmente
+
hash anterior != hash actual
```

Ejemplo:

```text
BASELINE
config.txt → AAA
        │
        ▼
ACTUAL
config.txt → BBB
        │
        ▼
MODIFICADO
```

La ruta continúa existiendo.

Lo que ha cambiado es el contenido representado por su hash.

---

## 28. Archivos eliminados

Un archivo pertenece a:

```text
eliminados
```

cuando:

```text
existe en baseline
```

pero:

```text
no existe en snapshot actual
```

Ejemplo:

```text
BASELINE
archivo.txt
     │
     ▼
ACTUAL
no aparece
     │
     ▼
ELIMINADO
```

La detección no necesita observar directamente el momento de la eliminación.

Se deduce comparando dos estados.

---

## 29. Archivos nuevos

Un archivo pertenece a:

```text
nuevos
```

cuando:

```text
no estaba en baseline
```

pero:

```text
aparece en snapshot actual
```

Ejemplo:

```text
BASELINE
(no existe nuevo.txt)

ACTUAL
nuevo.txt
     │
     ▼
NUEVO
```

Para detectar este caso necesitamos recorrer también los archivos del snapshot actual y comprobar cuáles no estaban presentes anteriormente.

---

## 30. La comparación necesita dos recorridos

La lógica de comparación utiliza conceptualmente dos perspectivas.

Primera:

```text
recorrer baseline
      │
      ├── mismo hash → sin cambios
      ├── hash distinto → modificado
      └── no existe → eliminado
```

Segunda:

```text
recorrer actual
      │
      └── no estaba en baseline → nuevo
```

Esto es importante porque un archivo nuevo no puede descubrirse recorriendo únicamente los archivos antiguos.

La baseline no sabe todavía que ese archivo existe.

---

## 31. Bug detectado: `return` dentro del bucle

Durante el desarrollo apareció un error especialmente útil desde el punto de vista didáctico.

Un:

```python
return resultado
```

quedó colocado accidentalmente dentro de un bucle.

Conceptualmente:

```text
for archivo in archivos:
    procesar archivo
    return resultado
```

Esto provoca que la función termine después de procesar únicamente el primer elemento.

El flujo incorrecto es:

```text
archivo 1
   │
   ▼
procesar
   │
   ▼
RETURN
   │
   X
archivo 2 nunca procesado
archivo 3 nunca procesado
```

Los tests permitieron detectar el comportamiento.

La corrección consistió en situar:

```python
return resultado
```

fuera del bucle.

Este caso demuestra nuevamente que una indentación aparentemente pequeña puede modificar completamente la lógica de una función.

---

## 32. Comparar únicamente baselines de la misma carpeta

Antes de comparar hashes debemos comprobar que ambos estados corresponden a la misma ubicación.

Por eso:

```python
comparar_integridad()
```

verifica:

```python
baseline["ruta_base"] == actual["ruta_base"]
```

Si no coinciden:

```text
ValueError
```

Conceptualmente:

```text
baseline
/home/user/A
       │
       X
actual
/home/user/B
       │
       ▼
NO COMPARAR
```

Comparar dos carpetas diferentes produciría resultados técnicamente calculables pero semánticamente incorrectos.

---

## 33. Enlaces simbólicos

Los enlaces simbólicos introducen consideraciones especiales.

Un symlink situado dentro de una carpeta puede apuntar a:

```text
otro archivo de la carpeta
```

o incluso:

```text
fuera de la carpeta vigilada
```

Ejemplo:

```text
carpeta_vigilada/
└── enlace
      │
      └────────► /etc/otro_archivo
```

Seguir automáticamente estos enlaces podría ampliar el ámbito del análisis más allá de la carpeta que el usuario pretendía vigilar.

Por eso v3.3 adopta una decisión deliberada:

```text
ignorar enlaces simbólicos
```

durante la generación del snapshot.

---

## 34. Por qué ignoramos symlinks

La decisión tiene una motivación de seguridad y previsibilidad.

Si siguiéramos enlaces automáticamente:

```text
carpeta seleccionada
      │
      ▼
symlink
      │
      ▼
otra ubicación
      │
      ▼
archivo externo
```

el usuario podría terminar monitorizando archivos que no esperaba incluir.

También podrían aparecer:

- enlaces rotos;
- bucles;
- rutas fuera del árbol;
- comportamientos diferentes según el entorno.

Por tanto, para esta versión:

```text
archivo regular → analizar
directorio → recorrer
symlink → ignorar
```

La política puede evolucionar en versiones futuras si se desea añadir una configuración explícita.

---

## 35. Condiciones de carrera en el filesystem

El sistema de archivos puede cambiar mientras lo estamos recorriendo.

Por ejemplo:

```text
rglob detecta archivo
        │
        ▼
archivo existe
        │
        ▼
otro proceso lo elimina
        │
        ▼
intentamos calcular hash
```

Entre:

```text
detectar archivo
```

y:

```text
abrir archivo
```

puede transcurrir tiempo.

Aunque sean milisegundos, otro proceso puede modificar el estado.

Este tipo de situación se relaciona con una condición de carrera.

---

## 36. Archivo que desaparece durante el hashing

Durante v3.3 se añadió un test específico para simular que un archivo desaparece durante el cálculo de SHA-256.

El comportamiento deseado fue:

```text
archivo desaparece
        │
        ▼
FileNotFoundError
        │
        ▼
omitir archivo
        │
        ▼
continuar snapshot
```

No queremos que la desaparición puntual de un archivo impida analizar todos los demás.

Por eso se captura específicamente:

```python
FileNotFoundError
```

---

## 37. No utilizamos `except Exception`

La experiencia de v3.2 con Ruff y:

```text
BLE001
```

se aplica directamente en v3.3.

Para el archivo que desaparece durante el hashing no utilizamos:

```python
except Exception:
```

Utilizamos una excepción concreta:

```python
except FileNotFoundError:
```

La diferencia es importante:

```text
ERROR ESPERADO
archivo desaparece
      │
      ▼
FileNotFoundError
      │
      ▼
sabemos qué hacer
```

frente a:

```text
ERROR INESPERADO
bug interno
TypeError
RuntimeError
...
      │
      ▼
NO ocultarlo automáticamente
```

La regla aprendida sigue siendo:

> Capturar una excepción tiene sentido cuando conocemos el escenario y sabemos cómo responder.

---

## 38. TDD en v3.3

Una de las diferencias importantes respecto a versiones antiguas es que gran parte del FIM se desarrolló mediante:

```text
Test Driven Development
```

simplificado en ciclos:

```text
RED
 │
 ▼
GREEN
```

El procedimiento fue aproximadamente:

```text
1. definir comportamiento
2. escribir test
3. ejecutar test
4. comprobar fallo
5. implementar
6. ejecutar de nuevo
7. comprobar que pasa
8. ejecutar batería completa
```

Esto permitió desarrollar progresivamente la funcionalidad sin esperar hasta el final para comprobarla.

---

## 39. Qué significa RED

RED representa el momento en el que escribimos un test para un comportamiento todavía no implementado o incorrecto.

Por ejemplo:

```text
queremos detectar archivos modificados
        │
        ▼
escribimos test
        │
        ▼
función todavía no lo hace
        │
        ▼
FAILED
```

Ese fallo no representa necesariamente un problema.

En TDD puede ser precisamente la evidencia de que el test es capaz de detectar la ausencia del comportamiento que queremos implementar.

---

## 40. Qué significa GREEN

Después implementamos el código mínimo necesario para satisfacer el comportamiento.

Conceptualmente:

```text
RED
 │
 ▼
implementar
 │
 ▼
ejecutar
 │
 ▼
GREEN
```

Pero no terminamos ahí.

Después ejecutamos:

```text
batería completa
```

para comprobar que la nueva modificación no ha producido regresiones en otras partes del proyecto.

---

## 41. TDD no consiste en hacer pasar tests a cualquier precio

Un riesgo al aprender TDD sería pensar:

```text
objetivo = conseguir verde
```

Pero el objetivo real es:

```text
comportamiento correcto
+
diseño comprensible
+
tests útiles
```

Un test podría hacerse pasar modificándolo incorrectamente.

Por eso debemos preguntarnos:

```text
¿el test expresa realmente el comportamiento deseado?

¿la implementación satisface ese comportamiento?

¿la solución mantiene coherencia con el diseño?

¿la batería completa continúa funcionando?
```

El test es una herramienta.

No sustituye al razonamiento.

---

## 42. Tests específicos del FIM

La lógica del monitor se prueba principalmente en:

```text
test/test_integridad.py
```

Durante v3.3 esta batería fue creciendo progresivamente.

Entre los comportamientos comprobados se encuentran:

- generación de snapshots;
- rutas relativas;
- hashing;
- carpetas vacías;
- subdirectorios;
- rutas inválidas;
- guardado de baseline;
- prevención de sobrescritura;
- carga de baseline;
- validación de estructura;
- validación de tipos;
- validación de hashes;
- rutas base vacías;
- rutas base relativas;
- archivos sin cambios;
- archivos modificados;
- archivos nuevos;
- archivos eliminados;
- comparación de rutas diferentes;
- symlinks;
- archivos que desaparecen durante el hashing.

---

## 43. Tests de integración con `organizador.py`

Además de probar el núcleo se creó:

```text
test/test_organizador_integridad.py
```

Su objetivo es comprobar la integración entre:

```text
core/integridad.py
```

y:

```text
organizador.py
```

Esto permite separar dos niveles:

```text
TEST UNITARIO / LÓGICA
        │
        ▼
core/integridad.py

TEST DE INTEGRACIÓN
        │
        ▼
organizador.py + integridad
```

La existencia de una función correcta en `core/` no garantiza por sí sola que la interfaz la utilice correctamente.

Por eso ambos niveles necesitan validación.

---

## 44. `monkeypatch` aplicado al FIM

Durante las pruebas de integración se reutilizó:

```python
monkeypatch
```

aprendido en v3.2.

Permite sustituir temporalmente funciones para controlar el entorno del test.

Conceptualmente:

```text
organizador.py
      │
      ▼
función real
      │
      X
      │
      ▼
función controlada por test
```

Esto permite comprobar:

- qué función se llama;
- qué argumentos recibe;
- qué resultado presenta la interfaz;
- cómo responde el flujo sin depender de archivos permanentes.

Así, una técnica aprendida en v3.2 se aplica directamente a la nueva funcionalidad de v3.3.

---

## 45. `capsys` aplicado al FIM

La interfaz de FileOrganizer muestra los resultados mediante:

```python
print()
```

Por eso los tests de integración utilizan:

```python
capsys
```

para comprobar la salida.

Ejemplo conceptual:

```text
comparación
     │
     ▼
resultado
     │
     ▼
print()
     │
     ▼
capsys
     │
     ▼
assert
```

Esto permite verificar automáticamente textos como:

```text
Sin cambios
Modificados
Nuevos
Eliminados
```

La presentación de consola pasa así a formar parte de la batería automatizada.

---

## 46. Integración en el menú principal

El FIM se incorporó al menú principal de FileOrganizer.

La versión v3.3 incluye:

```text
9) Crear baseline de integridad
10) Verificar integridad
11) Salir
```

Esto convierte el monitor en una funcionalidad accesible desde la interfaz normal del programa.

No es necesario utilizar directamente:

```python
core.integridad
```

desde una consola Python.

---

## 47. Crear baseline desde el menú

La opción:

```text
9) Crear baseline de integridad
```

realiza conceptualmente:

```text
usuario introduce carpeta
        │
        ▼
generar_snapshot()
        │
        ▼
guardar_baseline()
        │
        ▼
mostrar resultado
```

La interfaz informa de:

```text
ruta de la baseline
número de archivos registrados
```

De esta forma la lógica permanece en:

```text
core/integridad.py
```

mientras:

```text
organizador.py
```

coordina la interacción con el usuario.

---

## 48. Verificar integridad desde el menú

La opción:

```text
10) Verificar integridad
```

realiza:

```text
usuario indica baseline
        │
        ▼
cargar_baseline()
        │
        ▼
obtener ruta_base
        │
        ▼
generar snapshot actual
        │
        ▼
comparar_integridad()
        │
        ▼
mostrar resultado
```

El usuario no necesita volver a introducir la carpeta vigilada.

La baseline ya contiene:

```text
ruta_base
```

y el programa utiliza esa información para generar el estado actual.

---

## 49. Presentación del resultado

La interfaz resume las cuatro categorías.

Ejemplo validado:

```text
===== RESULTADO DE INTEGRIDAD =====
Sin cambios : 2
Modificados : 1
Nuevos      : 1
Eliminados  : 1
```

Este resumen permite interpretar rápidamente el estado.

Conceptualmente:

```text
RESULTADO
   │
   ├── sin cambios
   ├── modificados
   ├── nuevos
   └── eliminados
```

En versiones futuras podría ampliarse para mostrar:

- detalle de cada ruta;
- severidad;
- informes;
- timestamps;
- exportación;
- alertas.

---

## 50. Prueba manual end-to-end

Aunque v3.3 dispone de tests automatizados, también se realizó una prueba manual completa.

Se creó:

```text
/tmp/fileorganizer_fim_final
```

con:

```text
/tmp/fileorganizer_fim_final/eliminado.txt
/tmp/fileorganizer_fim_final/modificado.txt
/tmp/fileorganizer_fim_final/sin_cambios.txt
/tmp/fileorganizer_fim_final/subcarpeta/interno.txt
```

Después se creó una baseline real.

Esta prueba permite validar el flujo desde la perspectiva del usuario, complementando la batería automatizada.

---

## 51. Baseline real de la prueba final

La baseline generada fue:

```json
{
    "ruta_base": "/tmp/fileorganizer_fim_final",
    "archivos": {
        "eliminado.txt": "b2de01607389a694c96198a311137823fdc12649f25462ca2f36ff1e94455769",
        "sin_cambios.txt": "80bd5123ef75b69c97fb748bf7c1cf2d5d760ecb975785768bdd3a897be68949",
        "modificado.txt": "9660b3303631e95817f72c7536939f0eca9e20c0d7b86382a39e4a98a1b26151",
        "subcarpeta/interno.txt": "c06752892c2feacd9c38b2edc6febd90b1b1445c37f386ddf61ff3461bd7dd9c"
    }
}
```

Esto confirmó también que:

```text
ruta_base
```

se almacenaba como ruta absoluta y los archivos como rutas relativas.

---

## 52. Preparación de los cuatro estados

Después de crear la baseline se modificó deliberadamente el laboratorio para producir los cuatro tipos de resultado.

El objetivo fue conseguir:

```text
SIN CAMBIOS
MODIFICADO
NUEVO
ELIMINADO
```

Conceptualmente:

```text
sin_cambios.txt
      │
      └── no tocar

modificado.txt
      │
      └── cambiar contenido

nuevo.txt
      │
      └── crear después de baseline

eliminado.txt
      │
      └── borrar después de baseline
```

Además:

```text
subcarpeta/interno.txt
```

permaneció sin cambios.

---

## 53. Resultado real de la prueba end-to-end

La opción:

```text
10) Verificar integridad
```

produjo:

```text
===== RESULTADO DE INTEGRIDAD =====
Sin cambios : 2
Modificados : 1
Nuevos      : 1
Eliminados  : 1
```

El estado esperado era:

```text
2 sin cambios
1 modificado
1 nuevo
1 eliminado
```

El estado obtenido coincidió exactamente.

Por tanto:

```text
ESTADO REAL
     │
     ▼
FIM
     │
     ▼
RESULTADO
     │
     ▼
COINCIDENCIA
```

Esta prueba complementa los tests automatizados con una validación completa del flujo real.

---

## 54. Test unitario frente a prueba end-to-end

Ambos tipos de prueba tienen objetivos diferentes.

Un test específico puede comprobar:

```text
comparar_integridad()
```

de forma aislada.

Una prueba end-to-end comprueba:

```text
filesystem real
      │
      ▼
baseline
      │
      ▼
interfaz
      │
      ▼
snapshot actual
      │
      ▼
comparación
      │
      ▼
resultado visible
```

Los tests unitarios permiten localizar errores con precisión.

La prueba end-to-end proporciona confianza adicional sobre la integración del sistema completo.

No se sustituyen.

Se complementan.

---

## 55. Errores encontrados gracias a TDD

Durante v3.3 los tests no se limitaron a confirmar código terminado.

Ayudaron a descubrir o definir diferentes problemas.

Entre ellos:

```text
funciones todavía inexistentes
rutas relativas donde se esperaban absolutas
clasificación incompleta de modificados
detección incompleta de nuevos
detección incompleta de eliminados
return dentro de un bucle
estructura de baseline inválida
tipos incorrectos
hashes inválidos
ruta_base vacía
ruta_base relativa
symlinks
archivo desaparecido durante hashing
```

Esto demuestra que el testing participó directamente en el diseño de la funcionalidad.

---

## 56. Evolución de la batería

v3.3 comenzó desde:

```text
101 tests
```

heredados de v3.2.

Durante el desarrollo del FIM se añadieron nuevos escenarios.

La batería específica final de integridad alcanzó:

```text
30 passed
```

y la batería completa del proyecto alcanzó:

```text
131 passed
```

Conceptualmente:

```text
v3.2
101 tests
   │
   ▼
v3.3 añade FIM
   │
   ▼
+30 tests
   │
   ▼
131 tests
```

Esto significa que la nueva funcionalidad se incorpora sin abandonar las comprobaciones de las versiones anteriores.

---

## 57. Regresión y compatibilidad

Cada vez que añadimos una función de integridad también debemos preguntarnos:

```text
¿sigue funcionando cuarentena?

¿siguen funcionando magic numbers?

¿sigue funcionando el analizador de logs?

¿siguen funcionando estadísticas?

¿siguen funcionando movimientos?

¿siguen funcionando duplicados?
```

No comprobamos todo manualmente.

La batería completa permite verificar automáticamente los escenarios cubiertos anteriormente.

Por eso después de los cambios del FIM se ejecutó:

```bash
python -m pytest test/ -q
```

Resultado:

```text
131 passed
```

Esto es precisamente el valor de una batería de regresión.

---

## 58. Auditoría técnica específica del FIM

Antes de documentar el cierre se realizó una auditoría específica mediante:

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

Esto permite comprobar de forma aislada la nueva funcionalidad.

Después se ejecuta la batería completa para comprobar compatibilidad con el resto del proyecto.

---

## 59. Ruff después de añadir el FIM

La nueva funcionalidad también se sometió al análisis estático utilizado desde v3.2.

Comando:

```bash
python -m ruff check .
```

Resultado:

```text
All checks passed!
```

Esto significa que, según las reglas activas de Ruff, el nuevo código no deja avisos detectados.

Como aprendimos en v3.2:

```text
Ruff limpio
≠
código perfecto
```

Pero constituye una comprobación adicional dentro del proceso de calidad.

---

## 60. Compilación

También se ejecutó:

```bash
python3 -m py_compile core/*.py organizador.py
```

Resultado:

```text
sin errores
```

Esta comprobación verifica que los módulos analizados pueden compilarse sintácticamente.

No sustituye a pytest.

Un programa puede compilar correctamente y comportarse mal.

Por eso mantenemos ambas comprobaciones.

---

## 61. `git diff --check`

La revisión técnica también incluyó:

```bash
git diff --check
```

Resultado:

```text
sin errores
```

Esta comprobación permite detectar determinados problemas de whitespace en los cambios pendientes.

Git continúa formando parte del proceso de calidad, no únicamente del almacenamiento de versiones.

---

## 62. Flujo de validación utilizado en v3.3

El flujo consolidado durante esta versión puede representarse como:

```text
NUEVO COMPORTAMIENTO
       │
       ▼
TEST
       │
       ▼
RED
       │
       ▼
IMPLEMENTACIÓN
       │
       ▼
GREEN
       │
       ▼
TESTS ESPECÍFICOS
       │
       ▼
BATERÍA COMPLETA
       │
       ▼
RUFF
       │
       ▼
PY_COMPILE
       │
       ▼
GIT DIFF --CHECK
       │
       ▼
PRUEBA MANUAL
       │
       ▼
DOCUMENTACIÓN
       │
       ▼
COMMIT
```

Esta metodología es una evolución directa del proceso aprendido en v3.2.

---

## 63. Checkpoints de Git durante v3.3

El desarrollo no se realizó como un único bloque gigantesco.

Se utilizaron checkpoints estables.

Entre ellos:

```text
3e14daf
v3.3: inicia monitor de integridad con snapshots
```

Posteriormente:

```text
9bea36a
v3.3: integra monitor de integridad en el menú
```

Y más adelante:

```text
10c7c5e
v3.3: valida rutas absolutas en baselines
```

Los checkpoints permiten conservar estados funcionales durante el desarrollo.

Conceptualmente:

```text
checkpoint A
     │
     ▼
nuevos cambios
     │
     ▼
checkpoint B
     │
     ▼
nuevos cambios
     │
     ▼
checkpoint C
```

Esto proporciona trazabilidad y puntos de recuperación.

---

## 64. Estado del último checkpoint técnico

Antes de documentar el cierre, el último checkpoint confirmado era:

```text
10c7c5e
```

con:

```text
HEAD -> main
origin/main
```

sincronizados.

El árbol de trabajo estaba limpio antes de comenzar la actualización documental.

Esto permite distinguir claramente:

```text
código FIM validado
```

de:

```text
cambios documentales de cierre
```

---

## 65. Seguridad de la propia baseline

Una baseline es una referencia de confianza.

Esto introduce una cuestión importante:

```text
¿qué ocurre si alguien modifica la baseline?
```

La versión actual valida su estructura y formato.

Pero todavía no proporciona autenticidad criptográfica de la baseline.

Por ejemplo, un atacante con capacidad para modificar:

```text
baseline.json
```

podría potencialmente sustituir:

```text
hash antiguo
```

por:

```text
hash del archivo manipulado
```

y hacer que una comparación posterior pareciera correcta.

Este problema no invalida el FIM educativo desarrollado.

Pero muestra una limitación importante que debe comprenderse.

---

## 66. Integridad del archivo frente a integridad de la baseline

Tenemos dos problemas diferentes:

```text
¿ha cambiado el archivo vigilado?
```

y:

```text
¿ha sido manipulada la baseline?
```

La versión v3.3 aborda principalmente el primero.

Conceptualmente:

```text
ARCHIVOS
   │
   ▼
SHA-256
   │
   ▼
BASELINE
```

Pero para confiar completamente en el resultado también debemos poder confiar en:

```text
BASELINE
```

Esto abre futuras posibilidades:

- permisos restrictivos;
- almacenamiento separado;
- firma digital;
- HMAC;
- baseline de solo lectura;
- registro externo;
- control de acceso.

Estas mejoras quedan fuera del alcance actual de v3.3.

---

## 67. Qué detecta el FIM y qué no detecta

El FIM actual puede detectar diferencias entre dos estados observados.

Puede identificar:

```text
contenido modificado
archivo nuevo
archivo eliminado
archivo sin cambios
```

Pero no observa continuamente el filesystem.

Por ejemplo:

```text
09:00 baseline
09:10 archivo modificado
09:15 archivo restaurado exactamente
09:30 verificación
```

Si el contenido final vuelve a producir el mismo hash que la baseline, la comprobación de las 09:30 no demuestra que nunca hubiera existido una modificación intermedia.

Por tanto:

```text
FIM por snapshots
```

no equivale a:

```text
monitorización continua de eventos
```

Esta distinción es importante.

---

## 68. Snapshot frente a monitorización en tiempo real

El diseño actual funciona mediante comparaciones puntuales:

```text
SNAPSHOT A
     │
     │ tiempo
     ▼
SNAPSHOT B
     │
     ▼
COMPARACIÓN
```

Un sistema en tiempo real podría utilizar mecanismos del sistema operativo para recibir eventos cuando cambia un archivo.

Conceptualmente:

```text
archivo cambia
     │
     ▼
evento inmediato
     │
     ▼
monitor
```

v3.3 no implementa ese segundo modelo.

Su objetivo es construir y comprender primero los fundamentos:

```text
baseline
hash
comparación
validación
```

---

## 69. El FIM no determina por qué cambió un archivo

Si el hash cambia sabemos:

```text
el contenido observado ya no coincide
```

Pero no sabemos automáticamente:

```text
quién lo modificó
por qué
qué proceso lo hizo
si fue legítimo
si fue malicioso
```

El FIM proporciona una señal.

La interpretación de esa señal requiere contexto adicional.

Esto es común en seguridad defensiva:

```text
DETECCIÓN
≠
ATRIBUCIÓN
```

Detectar una modificación no implica conocer su causa.

---

## 70. Falsos positivos desde la perspectiva operativa

Técnicamente, si un archivo cambia y el FIM lo marca como modificado, la detección puede ser correcta.

Pero desde una perspectiva operativa el cambio podría ser completamente legítimo.

Ejemplo:

```text
actualización del sistema
       │
       ▼
archivo cambia
       │
       ▼
FIM alerta
```

El FIM ha detectado correctamente el cambio.

Pero el cambio no representa necesariamente un incidente.

Por tanto, una futura evolución podría necesitar:

- listas de exclusión;
- ventanas de mantenimiento;
- clasificación de rutas;
- severidades;
- aprobación de cambios;
- renovación controlada de baselines.

---

## 71. Coste del hashing

Para calcular SHA-256 debemos leer el contenido de cada archivo.

Conceptualmente:

```text
archivo 1 ──► leer ──► hash
archivo 2 ──► leer ──► hash
archivo 3 ──► leer ──► hash
...
```

En una carpeta pequeña el coste es reducido.

Pero en:

```text
miles de archivos
+
archivos muy grandes
```

el tiempo y las operaciones de entrada/salida pueden aumentar significativamente.

v3.3 prioriza:

```text
claridad
corrección
aprendizaje
robustez
```

sobre optimizaciones prematuras.

El rendimiento podrá estudiarse posteriormente con mediciones reales.

---

## 72. No optimizar antes de medir

Una lección importante para futuras versiones es evitar modificar el diseño únicamente porque imaginamos que puede ser lento.

El proceso correcto sería:

```text
medir
  │
  ▼
identificar cuello de botella
  │
  ▼
diseñar optimización
  │
  ▼
probar
  │
  ▼
medir de nuevo
```

No:

```text
suponer
  │
  ▼
complicar código
```

El FIM actual proporciona una implementación suficientemente clara para poder medirla en futuras versiones.

---

## 73. Metadatos frente a contenido

Un archivo posee diferentes atributos:

```text
nombre
ruta
tamaño
mtime
permisos
propietario
contenido
```

v3.3 utiliza principalmente:

```text
ruta
+
SHA-256 del contenido
```

para determinar las categorías de integridad.

Esto significa que el foco actual está en:

```text
integridad del contenido
```

Una futura versión podría incorporar cambios de:

- permisos;
- propietario;
- tamaño;
- timestamps;
- otros metadatos.

Pero añadir más señales también requiere definir cuidadosamente qué significa cada cambio.

---

## 74. Por qué el hash del contenido es una buena base inicial

Utilizar SHA-256 permite comenzar con una pregunta clara:

```text
¿los bytes del archivo siguen siendo los mismos?
```

Esto evita mezclar inicialmente demasiadas dimensiones.

Por ejemplo, un archivo podría conservar exactamente el mismo contenido pero cambiar:

```text
mtime
```

Si nuestro objetivo es detectar modificaciones de contenido, el hash seguiría siendo igual.

Esto muestra la importancia de definir qué significa:

```text
integridad
```

para cada herramienta.

En v3.3 significa principalmente:

```text
presencia
+
ruta
+
contenido
```

---

## 75. Separación entre lógica y presentación

El FIM mantiene una separación importante:

```text
core/integridad.py
        │
        ▼
lógica

organizador.py
        │
        ▼
interfaz
```

Por ejemplo:

```text
comparar_integridad()
```

no necesita imprimir el resultado.

Devuelve una estructura de datos.

Después:

```text
organizador.py
```

decide cómo mostrarla.

Esto facilita:

- tests;
- reutilización;
- futuras interfaces;
- generación de informes;
- mantenimiento.

---

## 76. Por qué devolver estructuras es mejor que imprimir desde el núcleo

Supongamos que:

```python
comparar_integridad()
```

imprimiera directamente:

```text
Modificados: 3
```

La función quedaría acoplada a una interfaz de consola.

En cambio, devolviendo:

```python
{
    "modificados": [...]
}
```

podemos reutilizar el resultado para:

```text
consola
informe TXT
JSON
GUI
API
alerta
```

La lógica permanece independiente de la forma de presentación.

Este principio ya apareció en versiones anteriores y vuelve a reforzarse en v3.3.

---

## 77. Datos externos como frontera de confianza

La baseline almacenada en disco debe considerarse una entrada externa cuando vuelve a cargarse.

Aunque haya sido creada originalmente por nuestro propio programa, entre dos ejecuciones puede haber sido modificada.

Conceptualmente:

```text
PROGRAMA
   │
   ▼
guardar JSON
   │
   ▼
DISCO
   │
   │ tiempo
   │ modificación posible
   ▼
cargar JSON
   │
   ▼
VALIDAR
```

Por eso:

```text
lo escribí yo
```

no significa:

```text
puedo confiar para siempre en ello
```

Este principio es muy importante en desarrollo seguro.

---

## 78. Validación defensiva

La validación de baseline sigue varias capas:

```text
¿existe archivo?
       │
       ▼
¿JSON puede cargarse?
       │
       ▼
¿existe ruta_base?
       │
       ▼
¿existe archivos?
       │
       ▼
¿tipos correctos?
       │
       ▼
¿ruta no vacía?
       │
       ▼
¿ruta absoluta?
       │
       ▼
¿hashes son strings?
       │
       ▼
¿hashes tienen formato esperado?
       │
       ▼
BASELINE ACEPTADA
```

Cada capa reduce la confianza implícita en datos externos.

---

## 79. Qué no garantiza la validación del hash

Comprobar:

```text
64 caracteres
+
hexadecimal
```

permite verificar el formato.

Pero no demuestra que:

```text
ese hash corresponda realmente al archivo indicado
```

ni que:

```text
haya sido generado honestamente
```

Una cadena inventada de 64 caracteres hexadecimales superaría la validación de formato.

Esto distingue:

```text
VALIDACIÓN SINTÁCTICA
```

de:

```text
AUTENTICIDAD
```

La versión actual valida estructura y formato.

No proporciona autenticidad criptográfica de la baseline.

---

## 80. Defensa en profundidad

v3.3 permite relacionar el proyecto con el concepto de:

```text
defensa en profundidad
```

FileOrganizer empieza a disponer de varias capas diferentes:

```text
magic numbers
      │
      ▼
verificación de archivos

cuarentena
      │
      ▼
aislamiento

analizador de logs
      │
      ▼
detección de eventos

correlación
      │
      ▼
detección de comportamiento repetido

FIM
      │
      ▼
detección de cambios en archivos
```

Ninguna capa resuelve por sí sola toda la seguridad.

Cada una observa un aspecto diferente.

---

## 81. Relación con Blue Team

El FIM se relaciona directamente con tareas defensivas.

En un contexto de Blue Team interesa detectar:

```text
archivos críticos modificados
configuraciones alteradas
binarios reemplazados
archivos inesperados
eliminaciones
```

FileOrganizer implementa una versión educativa y simplificada del concepto.

No pretende sustituir herramientas profesionales.

Su valor está en comprender:

```text
qué problema resuelven
qué datos necesitan
cómo comparan estados
qué limitaciones tienen
qué errores deben gestionar
```

---

## 82. Relación entre v3.1, v3.2 y v3.3

Las tres versiones forman una evolución coherente.

```text
v3.1
SEGURIDAD
   │
   ▼
magic numbers
cuarentena
logs
correlación

v3.2
CALIDAD
   │
   ▼
pytest
Ruff
robustez
regresión

v3.3
INTEGRIDAD
   │
   ▼
baseline
SHA-256
FIM
TDD
```

v3.3 no abandona lo aprendido anteriormente.

Utiliza:

```text
seguridad de v3.1
+
testing de v3.2
```

para construir una nueva funcionalidad defensiva.

---

## 83. Reutilización del conocimiento de v3.2

Durante v3.3 se reutilizaron directamente conceptos aprendidos anteriormente:

```text
tmp_path
monkeypatch
capsys
pytest.raises
tests negativos
casos límite
tests de regresión
excepciones específicas
Ruff
Git checkpoints
```

Esto demuestra que el aprendizaje no se encuentra aislado por versiones.

Cada etapa se convierte en herramienta para la siguiente.

---

## 84. Cambio de mentalidad con TDD

En versiones antiguas el flujo habitual podía ser:

```text
pensar función
    │
    ▼
escribir función
    │
    ▼
ejecutar manualmente
    │
    ▼
parece funcionar
```

v3.3 introduce con más claridad:

```text
definir comportamiento
       │
       ▼
escribir test
       │
       ▼
verlo fallar
       │
       ▼
implementar
       │
       ▼
verlo pasar
       │
       ▼
regresión completa
```

El cambio importante consiste en pensar primero:

```text
¿qué comportamiento espero?
```

antes de centrarse únicamente en:

```text
¿qué código escribo?
```

---

## 85. El test como especificación ejecutable

Un test puede funcionar como una pequeña especificación.

Por ejemplo:

```text
si ruta_base es relativa
        │
        ▼
debe producir ValueError
```

Ese comportamiento queda escrito en código.

Dentro de meses podemos ejecutar el test y comprobar si sigue cumpliéndose.

Por tanto:

```text
documentación
```

explica el comportamiento.

Mientras:

```text
test
```

puede verificar automáticamente parte de ese comportamiento.

Ambos se complementan.

---

## 86. Lo que significa tener 131 tests

El resultado final:

```text
131 passed
```

no significa:

```text
FileOrganizer no contiene ningún bug
```

Tampoco significa:

```text
todos los escenarios posibles están cubiertos
```

Significa:

```text
131 escenarios automatizados
producen actualmente
el resultado esperado
```

Todavía pueden existir:

- casos no contemplados;
- condiciones de carrera adicionales;
- diferencias entre sistemas operativos;
- problemas de rendimiento;
- errores de diseño;
- entradas inesperadas;
- limitaciones de seguridad.

La batería aumenta la confianza.

No elimina la necesidad de análisis crítico.

---

## 87. Lo que significa Ruff limpio

El resultado:

```text
All checks passed!
```

significa que Ruff no detecta avisos según la configuración activa.

No significa:

```text
código perfecto
```

ni:

```text
seguridad garantizada
```

Por eso seguimos utilizando:

```text
pytest
+
Ruff
+
py_compile
+
Git
+
pruebas manuales
+
revisión humana
```

Cada mecanismo observa aspectos diferentes.

---

## 88. Estado técnico final de v3.3

La auditoría final de la nueva funcionalidad produjo:

```text
Tests FIM:
30 passed
```

La batería completa produjo:

```text
131 passed
```

Ruff:

```text
All checks passed!
```

Compilación:

```text
sin errores
```

`git diff --check`:

```text
sin errores
```

La prueba manual end-to-end produjo:

```text
Sin cambios : 2
Modificados : 1
Nuevos      : 1
Eliminados  : 1
```

coincidiendo exactamente con el estado preparado.

---

## 89. Competencias técnicas adquiridas

Durante v3.3 se trabajaron de forma práctica nuevas competencias.

### Python

- `pathlib`;
- `Path.resolve()`;
- `Path.is_absolute()`;
- `Path.rglob()`;
- rutas relativas;
- diccionarios;
- JSON;
- lectura de archivos binarios;
- hashing;
- excepciones;
- validación de tipos;
- validación de valores;
- manejo del filesystem.

### Testing

- TDD;
- ciclos RED/GREEN;
- tests de regresión;
- `tmp_path`;
- `monkeypatch`;
- `capsys`;
- `pytest.raises`;
- tests de integración;
- pruebas end-to-end;
- simulación de condiciones de carrera;
- diseño de casos negativos;
- validación de datos externos.

### Ciberseguridad

- File Integrity Monitoring;
- baselines;
- SHA-256;
- detección de cambios;
- integridad de archivos;
- fronteras de confianza;
- validación defensiva;
- symlinks;
- condiciones de carrera;
- limitaciones de un FIM;
- diferencia entre detección y atribución;
- defensa en profundidad.

### Linux

- rutas absolutas;
- rutas relativas;
- estructura de directorios;
- enlaces simbólicos;
- `/tmp`;
- filesystem;
- archivos que cambian durante un recorrido.

### Git

- checkpoints;
- revisión de estado;
- `git diff --check`;
- commits incrementales;
- sincronización con remoto;
- separación entre código y documentación;
- `.gitignore`.

---

## 90. Valor de v3.3 para el portfolio

v3.3 amplía el proyecto en una dirección especialmente relacionada con ciberseguridad defensiva.

El repositorio empieza a demostrar no solo:

```text
sé organizar archivos
```

sino también:

```text
sé calcular hashes
sé construir baselines
sé comparar estados
sé detectar modificaciones
sé detectar archivos nuevos
sé detectar eliminaciones
sé validar datos externos
sé trabajar con symlinks
sé pensar en condiciones de carrera
sé desarrollar mediante TDD
sé probar integración
sé realizar una prueba end-to-end
```

Además, la funcionalidad se construye sobre una batería de regresión existente.

Esto aporta al portfolio una combinación de:

```text
Python
+
Linux
+
testing
+
Git
+
ciberseguridad defensiva
```

---

## 91. Limitaciones conocidas

La versión actual tiene deliberadamente un alcance limitado.

Entre las limitaciones se encuentran:

- no existe monitorización en tiempo real;
- las comprobaciones se realizan mediante snapshots;
- no se registra quién modificó un archivo;
- no se determina si un cambio es legítimo o malicioso;
- no se protege criptográficamente la autenticidad de la baseline;
- no se monitorizan todavía permisos o propietarios;
- los symlinks se ignoran;
- no existen exclusiones configurables específicas del FIM;
- no se generan alertas automáticas externas;
- no existe todavía un informe persistente de cambios;
- no se ha realizado optimización para árboles masivos.

Estas limitaciones no son necesariamente defectos.

Definen el alcance actual de una implementación educativa que puede evolucionar progresivamente.

---

## 92. Posibles evoluciones futuras del FIM

El monitor podría ampliarse posteriormente con funcionalidades como:

```text
metadatos
    │
    ├── permisos
    ├── propietario
    ├── tamaño
    └── timestamps

alertas
    │
    ├── logs
    ├── informes
    └── severidades

configuración
    │
    ├── exclusiones
    ├── rutas críticas
    └── perfiles

protección baseline
    │
    ├── HMAC
    ├── firma
    └── almacenamiento protegido
```

También podría estudiarse monitorización basada en eventos del sistema operativo.

Pero estas mejoras deben añadirse de forma incremental y respaldadas por tests.

---

## 93. No convertir FileOrganizer en demasiadas cosas a la vez

El proyecto ha evolucionado desde un organizador de archivos hacia un laboratorio de aprendizaje.

Eso permite experimentar con:

```text
automatización
testing
seguridad
filesystem
logs
integridad
```

Pero existe un riesgo:

```text
añadir funcionalidades sin límite
        │
        ▼
perder coherencia
```

Por eso cada nueva versión debe preguntarse:

```text
¿qué objetivo técnico tiene?

¿qué aprendizaje aporta?

¿encaja con la arquitectura?

¿puede probarse?

¿mejora el portfolio?

¿está suficientemente delimitada?
```

v3.3 tiene un objetivo claro:

```text
comprender e implementar
un monitor de integridad basado en baselines
```

---

## 94. De organizador a laboratorio defensivo

La evolución general puede representarse así:

```text
FILEORGANIZER
     │
     ▼
organización de archivos
     │
     ▼
estadísticas
     │
     ▼
duplicados
     │
     ▼
hashes
     │
     ▼
magic numbers
     │
     ▼
cuarentena
     │
     ▼
análisis de logs
     │
     ▼
correlación
     │
     ▼
testing y robustez
     │
     ▼
File Integrity Monitoring
```

El proyecto continúa teniendo como base Python y el filesystem.

Pero esas bases se utilizan progresivamente para estudiar problemas relacionados con seguridad defensiva.

---

## 95. Resultado conceptual de v3.3

La funcionalidad puede resumirse mediante:

```text
             CARPETA VIGILADA
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
                    │
              pasa el tiempo
                    │
                    ▼
            generar_snapshot()
                    │
                    ▼
          comparar_integridad()
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
   modificados    nuevos    eliminados
        │
        └───────────┬───────────┘
                    │
                    ▼
             RESULTADO FIM
```

A esto se añade:

```text
validación de baseline
+
tests automatizados
+
Ruff
+
manejo de errores
+
integración de menú
```

---

## 96. Resultado metodológico de v3.3

El resultado más importante no es únicamente:

```text
tenemos un FIM
```

También es:

```text
hemos construido una funcionalidad nueva
utilizando la infraestructura de calidad
creada en la versión anterior
```

La evolución metodológica es:

```text
v3.1
crear seguridad

v3.2
crear red de seguridad para el código

v3.3
usar esa red para desarrollar nueva seguridad
```

Esto demuestra que pytest y Ruff no fueron añadidos únicamente como elementos decorativos del repositorio.

Se convirtieron en herramientas reales del proceso de desarrollo.

---

## 97. Conclusión de v3.3

FileOrganizer v3.3 incorpora un monitor de integridad funcional basado en:

```text
SHA-256
+
baselines
+
comparación de snapshots
```

El sistema puede detectar:

```text
archivos sin cambios
archivos modificados
archivos nuevos
archivos eliminados
```

También incorpora validaciones destinadas a evitar trabajar silenciosamente con baselines mal formadas.

Se han estudiado y probado situaciones relacionadas con:

```text
rutas absolutas
rutas relativas
hashes inválidos
tipos incorrectos
symlinks
archivos desaparecidos
sobrescrituras
estructuras JSON incorrectas
```

La funcionalidad se encuentra integrada en el menú principal y ha sido validada mediante una prueba manual end-to-end.

---

## 98. Estado final

La versión v3.3 termina técnicamente con:

```text
FIM funcional
baseline persistente
validación defensiva
comparación de integridad
integración en menú
TDD aplicado
30 tests específicos de integridad
131 tests totales
Ruff limpio
compilación correcta
git diff --check limpio
prueba end-to-end correcta
```

El resultado final de la prueba real fue:

```text
Sin cambios : 2
Modificados : 1
Nuevos      : 1
Eliminados  : 1
```

El estado observado coincidió exactamente con el esperado.

---

## 99. Lección principal de v3.3

La principal lección técnica puede resumirse así:

> Para detectar un cambio necesitamos primero definir qué consideramos un estado conocido y conservar una referencia fiable de ese estado.

Y la principal lección metodológica es:

> Una nueva funcionalidad puede desarrollarse de forma mucho más controlada cuando los comportamientos se definen mediante tests y cada modificación se valida frente a una batería de regresión.

El ciclo consolidado queda:

```text
ENTENDER
   │
   ▼
DISEÑAR
   │
   ▼
TEST
   │
   ▼
RED
   │
   ▼
IMPLEMENTAR
   │
   ▼
GREEN
   │
   ▼
REGRESIÓN
   │
   ▼
ANÁLISIS ESTÁTICO
   │
   ▼
PRUEBA REAL
   │
   ▼
DOCUMENTAR
   │
   ▼
VERSIONAR
```

Este ciclo constituye la base sobre la que pueden construirse las siguientes versiones de FileOrganizer.

---

## 100. Punto de partida para la siguiente versión

Después de cerrar v3.3, FileOrganizer dispone de tres pilares especialmente importantes:

```text
                 FILEORGANIZER
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
    SEGURIDAD        CALIDAD       INTEGRIDAD
        │              │              │
        ▼              ▼              ▼
 magic numbers       pytest          FIM
 cuarentena           Ruff         SHA-256
 logs                 Git          baselines
 correlación        regresión      snapshots
```

La siguiente versión no debería comenzar simplemente preguntando:

```text
¿Qué función nueva podemos añadir?
```

La pregunta debería ser:

```text
¿Qué problema técnico queremos resolver ahora?

¿Qué aprendizaje aporta?

¿Qué diseño necesita?

¿Qué riesgos introduce?

¿Qué tests deberían escribirse?

¿Cómo sabremos que funciona?

¿Cómo evitaremos romper lo anterior?
```

Ese cambio de enfoque es uno de los resultados más importantes de la evolución de FileOrganizer hasta v3.3.
