# FileOrganizer v3.2 — Testing, robustez y calidad de código

## 1. Introducción

La versión v3.2 representa un cambio importante en la evolución de FileOrganizer.

En versiones anteriores el proyecto fue creciendo principalmente mediante nuevas funcionalidades:

- organización y clasificación de archivos;
- configuración mediante JSON;
- modo simulación;
- historial y estadísticas;
- detección de duplicados;
- generación de informes;
- centralización de rutas y configuración;
- identificación mediante magic numbers;
- verificación de archivos;
- cuarentena;
- análisis defensivo de logs;
- detección de patrones relacionados con SQL Injection;
- análisis de fallos de autenticación;
- extracción de IPv4;
- correlación de posibles ataques de fuerza bruta.

Sin embargo, cuanto más crece un programa, mayor es el riesgo de que una modificación aparentemente pequeña rompa una funcionalidad que anteriormente funcionaba correctamente.

v3.2 nace precisamente para afrontar ese problema.

El objetivo principal de esta versión no consiste en añadir una gran funcionalidad visible para el usuario, sino en mejorar la forma en la que desarrollamos y validamos FileOrganizer.

Para ello se incorporan dos herramientas fundamentales:

```text
pytest
Ruff
```

`pytest` permite comprobar automáticamente el comportamiento del programa.

`Ruff` permite analizar estáticamente el código y detectar determinados problemas de calidad, estilo, mantenibilidad o robustez.

Ambas herramientas cumplen funciones diferentes y complementarias.

```text
                    FILEORGANIZER v3.2
                           │
             ┌─────────────┴─────────────┐
             │                           │
          pytest                       Ruff
             │                           │
             ▼                           ▼
      ¿El programa hace          ¿El código presenta
      lo que esperamos?          problemas detectables
                                 estáticamente?
```

Esta distinción es uno de los conceptos fundamentales aprendidos durante v3.2.

Un programa puede superar todos sus tests y contener código mejorable.

Del mismo modo, un programa puede superar un análisis estático y comportarse incorrectamente.

Por eso utilizamos ambas herramientas conjuntamente.

---

## 2. Situación inicial de v3.2

La versión comenzó sobre la base estable dejada por v3.1.

El proyecto ya disponía de una capa inicial de ciberseguridad defensiva, pero todavía no existía una batería automatizada suficientemente amplia que protegiera esas funcionalidades frente a futuras modificaciones.

El trabajo de v3.2 comenzó introduciendo tests progresivamente.

No se intentó probar todo el proyecto de una sola vez.

La estrategia utilizada fue:

```text
seleccionar módulo
      │
      ▼
comprender su comportamiento
      │
      ▼
diseñar casos de prueba
      │
      ▼
ejecutar pytest
      │
      ▼
analizar fallos
      │
      ▼
corregir código o test
      │
      ▼
volver a ejecutar
```

Este procedimiento permitió utilizar el testing no solo como mecanismo de validación, sino también como herramienta para comprender mejor el propio código.

Durante esta fase la batería terminó alcanzando inicialmente:

```text
100 tests
19 archivos de test
```

Posteriormente, durante la revisión con Ruff, se añadió un nuevo test de regresión relacionado con el tratamiento de excepciones en `core/movimientos.py`.

El resultado final pasó a ser:

```text
101 tests
20 archivos de test
```

---

## 3. Qué es un test automatizado

Un test automatizado es código cuyo propósito consiste en comprobar otro código.

En lugar de ejecutar manualmente FileOrganizer, seleccionar opciones, preparar archivos y observar visualmente el resultado cada vez que modificamos una función, podemos describir mediante código cuál debería ser su comportamiento.

Ejemplo conceptual:

```python
resultado = identificar_tipo_real(archivo)

assert resultado == "JPEG"
```

El test prepara una situación determinada, ejecuta el código que queremos comprobar y compara el resultado obtenido con el resultado esperado.

Si coinciden:

```text
PASSED
```

Si no coinciden:

```text
FAILED
```

La ventaja fundamental es la repetibilidad.

Podemos ejecutar los mismos tests:

- después de modificar una función;
- después de refactorizar;
- después de corregir un error;
- después de actualizar otra parte del proyecto;
- antes de realizar un commit;
- antes de publicar una nueva versión.

De esta forma, una batería de tests funciona como una red de seguridad frente a regresiones.

---

## 4. Qué es una regresión

Una regresión ocurre cuando una modificación provoca que algo que anteriormente funcionaba correctamente deje de hacerlo.

Imaginemos que modificamos el sistema de cuarentena para mejorar el tratamiento de nombres duplicados.

La nueva funcionalidad podría funcionar perfectamente, pero accidentalmente podríamos romper el registro de alertas.

Sin tests sería necesario recordar manualmente todas las funcionalidades relacionadas y volver a comprobarlas una por una.

Con tests podemos ejecutar:

```bash
python -m pytest test/
```

y comprobar automáticamente muchas condiciones del proyecto.

Esto no significa que los tests garanticen que el programa no contiene errores.

Significa que garantizan que los comportamientos cubiertos por esos tests continúan cumpliendo las condiciones que hemos definido.

Esta diferencia es importante:

```text
101 tests superados
        ≠
software matemáticamente libre de errores
```

Lo que realmente significa es:

```text
101 comportamientos o escenarios automatizados
han producido el resultado esperado.
```

Cuanto mejor diseñados estén los tests y mayor sea la cobertura de escenarios relevantes, mayor será la confianza que proporcionan.

---

## 5. Estructura Arrange — Act — Assert

Durante v3.2 utilizamos de forma habitual la estructura:

```text
ARRANGE
ACT
ASSERT
```

Esta estructura divide conceptualmente un test en tres partes.

### 5.1 Arrange — Preparar

En esta fase se construye el escenario necesario para realizar la prueba.

Por ejemplo:

```python
archivo = tmp_path / "foto.jpg"
archivo.write_bytes(b"\xFF\xD8\xFF")
```

Estamos preparando un archivo temporal que comienza con una firma compatible con JPEG.

### 5.2 Act — Actuar

Ejecutamos la función que queremos comprobar.

Por ejemplo:

```python
resultado = identificar_tipo_real(archivo)
```

### 5.3 Assert — Comprobar

Verificamos el resultado.

Por ejemplo:

```python
assert resultado == "JPEG"
```

El flujo completo puede representarse como:

```text
ARRANGE
crear archivo JPEG de prueba
        │
        ▼
ACT
identificar_tipo_real()
        │
        ▼
ASSERT
¿resultado == "JPEG"?
        │
   ┌────┴────┐
   │         │
  sí         no
   │         │
PASSED     FAILED
```

Esta estructura facilita la lectura de los tests porque permite identificar rápidamente:

1. qué escenario estamos construyendo;
2. qué función estamos ejecutando;
3. qué comportamiento esperamos.

---

## 6. Por qué empezamos por magic numbers

`core/magic_numbers.py` fue un buen punto de partida para introducir testing automático porque contiene una responsabilidad relativamente concreta:

```text
leer los primeros bytes de un archivo
            │
            ▼
compararlos con firmas conocidas
            │
            ▼
identificar su posible tipo real
```

Esto permite construir entradas controladas fácilmente.

Por ejemplo, una firma JPEG comienza con determinados bytes característicos.

Podemos crear un archivo temporal con esos bytes y comprobar automáticamente la respuesta del programa.

Durante v3.2 se probaron formatos como:

- JPEG;
- PNG;
- GIF;
- PDF;
- ZIP;
- GZIP;
- ELF;
- PE/Windows.

Pero también se probaron situaciones menos ideales:

- archivo vacío;
- archivo inexistente;
- firma desconocida;
- firma incompleta;
- archivo de un solo byte;
- nombres Unicode;
- nombres con espacios;
- directorios utilizados como si fueran archivos.

Esto introduce otra idea importante:

> Probar únicamente el camino correcto no es suficiente.

Un programa robusto también debe tener un comportamiento definido cuando recibe entradas anómalas o cuando el entorno no se encuentra en las condiciones ideales.

---

## 7. Tests positivos, negativos y casos límite

Durante v3.2 no todos los tests preguntan:

```text
¿funciona correctamente con una entrada válida?
```

También preguntamos:

```text
¿Qué ocurre si el archivo no existe?

¿Qué ocurre si está vacío?

¿Qué ocurre si no tiene extensión?

¿Qué ocurre si el nombre contiene Unicode?

¿Qué ocurre si la extensión está en mayúsculas?

¿Qué ocurre si aparecen varias extensiones?

¿Qué ocurre si un enlace simbólico está roto?

¿Qué ocurre si faltan permisos?

¿Qué ocurre si el log contiene bytes no válidos?

¿Qué ocurre si una fecha tiene un formato incorrecto?
```

Podemos dividir estos escenarios de forma simplificada:

```text
TESTS
 │
 ├── positivos
 │     └── entradas y comportamiento esperado normal
 │
 ├── negativos
 │     └── entradas incorrectas o situaciones de error
 │
 └── casos límite
       └── condiciones poco habituales o fronterizas
```

Esta forma de pensar es especialmente importante en ciberseguridad.

El software no debe diseñarse suponiendo que todas las entradas serán correctas, completas o bien formadas.

Los datos pueden ser:

- inesperados;
- corruptos;
- incompletos;
- manipulados;
- maliciosos.

Por eso el testing de robustez encaja directamente con el enfoque defensivo que FileOrganizer comenzó a desarrollar en v3.1.
---

## 8. `tmp_path`: pruebas aisladas del sistema de archivos

Muchas funcionalidades de FileOrganizer trabajan directamente con archivos y directorios.

Esto plantea una dificultad evidente para los tests:

```text
¿Dónde crear los archivos de prueba?

¿Dónde moverlos?

¿Cómo evitar ensuciar el proyecto?

¿Cómo evitar sobrescribir datos reales?
```

Para resolver este problema utilizamos la fixture:

```python
tmp_path
```

`pytest` crea automáticamente un directorio temporal independiente para cada test.

Ejemplo:

```python
def test_archivo_jpeg_correcto(tmp_path):
    archivo = tmp_path / "foto.jpg"

    archivo.write_bytes(
        b"\xFF\xD8\xFF\xE0\x00\x10\x4A\x46"
    )

    resultado = verificar_archivo(archivo)

    assert resultado["estado"] == "OK"
```

Durante el test, `tmp_path` puede apuntar a una ruta similar a:

```text
/tmp/pytest-of-wakan/pytest-4/test_archivo_jpeg_correcto0/
```

El test puede crear, modificar y eliminar archivos dentro de ese espacio sin afectar al proyecto real.

Esto permite probar de forma segura:

- creación de archivos;
- lectura;
- eliminación;
- cuarentena;
- permisos;
- enlaces simbólicos;
- logs;
- extensiones;
- archivos corruptos;
- archivos sospechosos.

Antes de utilizar `tmp_path`, uno de los primeros tests utilizaba manualmente una ruta como:

```text
/tmp/test_log_vacio.log
```

y posteriormente eliminaba el archivo mediante:

```python
archivo.unlink()
```

El test fue refactorizado para utilizar `tmp_path`.

La mejora conceptual fue:

```text
ANTES
ruta temporal global
+
limpieza manual

DESPUÉS
tmp_path
+
aislamiento automático por test
```

Esto reduce interferencias entre tests y hace la batería más reproducible.

---

## 9. `pytest.raises()`: comprobar excepciones esperadas

No todos los comportamientos correctos terminan devolviendo un valor.

En algunas situaciones, el comportamiento esperado consiste precisamente en lanzar una excepción.

Por ejemplo:

```text
archivo inexistente
        │
        ▼
identificar_tipo_real()
        │
        ▼
FileNotFoundError
```

Para comprobar este comportamiento utilizamos:

```python
pytest.raises()
```

Ejemplo conceptual:

```python
with pytest.raises(FileNotFoundError):
    identificar_tipo_real(archivo)
```

El test pasa únicamente si dentro del bloque se produce la excepción esperada.

Si no aparece:

```text
FAILED
```

También podemos comprobar parte del mensaje:

```python
with pytest.raises(
    RuntimeError,
    match="Fallo inesperado simulado",
):
    ...
```

Durante v3.2 se utilizó este mecanismo para validar distintos escenarios de error.

Entre ellos:

- archivos inexistentes;
- rutas que no son directorios;
- rutas que no son archivos;
- permisos insuficientes;
- errores inesperados simulados.

Esto es especialmente importante porque:

> Una excepción también forma parte del contrato de comportamiento de una función.

No solo importa qué devuelve una función cuando todo funciona.

También importa cómo falla.

---

## 10. `@pytest.mark.parametrize`: un test, muchas entradas

Algunas funciones deben responder correctamente ante muchas entradas diferentes.

Por ejemplo, `identificar_tipo_real()` debe reconocer múltiples firmas.

Podríamos escribir:

```text
test_jpeg()
test_png()
test_gif()
test_pdf()
test_zip()
...
```

Pero muchas de esas pruebas compartirían exactamente la misma estructura.

Para evitar duplicación utilizamos:

```python
@pytest.mark.parametrize(...)
```

Ejemplo simplificado:

```python
@pytest.mark.parametrize(
    "nombre, contenido, esperado",
    [
        ("foto.jpg", b"\xFF\xD8\xFF", "JPEG"),
        ("imagen.png", b"\x89PNG", "PNG"),
        ("documento.pdf", b"%PDF", "PDF"),
    ],
)
def test_identificar_tipo_real(
    tmp_path,
    nombre,
    contenido,
    esperado,
):
    archivo = tmp_path / nombre
    archivo.write_bytes(contenido)

    resultado = identificar_tipo_real(archivo)

    assert resultado == esperado
```

La estructura del test se escribe una sola vez.

Pytest ejecuta automáticamente una instancia distinta para cada conjunto de datos.

Podemos visualizarlo como:

```text
MISMO TEST
   │
   ├── JPEG ──► PASS
   ├── PNG  ──► PASS
   ├── PDF  ──► PASS
   ├── ZIP  ──► PASS
   └── ELF  ──► PASS
```

Esta técnica se utilizó especialmente en:

- magic numbers;
- patrones SQL;
- fallos de autenticación;
- IPv4;
- diferentes tipos de archivos.

La parametrización mejora:

- legibilidad;
- mantenimiento;
- reducción de código repetido;
- facilidad para añadir nuevos casos.

---

## 11. `capsys`: comprobar la salida de `print()`

FileOrganizer es actualmente una aplicación de consola.

Muchas funciones comunican información al usuario mediante:

```python
print()
```

Durante el refactor de `organizador.py` empezamos a extraer funciones cuyo comportamiento consiste principalmente en mostrar información.

Por ejemplo:

```python
mostrar_alertas_seguridad()
mostrar_analisis_carpeta()
mostrar_clasificacion()
```

Para probar este tipo de funciones utilizamos:

```python
capsys
```

`capsys` captura temporalmente la salida estándar producida durante el test.

Ejemplo:

```python
def test_alertas_vacias_no_imprimen(capsys):
    mostrar_alertas_seguridad([])

    salida = capsys.readouterr().out

    assert salida == ""
```

Otro ejemplo:

```python
salida = capsys.readouterr().out

assert "ALERTA DE SEGURIDAD" in salida
assert "programa.jpg" in salida
```

Esto convierte algo que anteriormente se comprobaba visualmente en un comportamiento verificable automáticamente.

Antes:

```text
ejecuto función
      │
      ▼
miro la pantalla
      │
      ▼
parece correcto
```

Después:

```text
ejecuto función
      │
      ▼
capsys captura stdout
      │
      ▼
assert
      │
      ▼
PASS / FAIL
```

Este cambio es importante porque la interfaz de consola también forma parte del comportamiento del programa.

---

## 12. `monkeypatch`: sustituir dependencias durante un test

Algunas funciones dependen de otras funciones o módulos externos.

Por ejemplo:

```text
enviar_sospechosos_cuarentena()
             │
             ▼
poner_en_cuarentena()
             │
             ▼
mueve archivos reales
```

No queremos que cada test de la función superior modifique realmente la cuarentena del proyecto.

Para resolver este problema utilizamos:

```python
monkeypatch
```

`monkeypatch` permite sustituir temporalmente un atributo, función o dependencia.

Ejemplo conceptual:

```python
def cuarentena_falsa(
    ruta_archivo,
    tipo_real,
    extension,
):
    return Path("/tmp/quarantine") / ruta_archivo.name
```

Después:

```python
monkeypatch.setattr(
    organizador,
    "poner_en_cuarentena",
    cuarentena_falsa,
)
```

Durante ese test:

```text
poner_en_cuarentena()
```

ya no representa la función real.

Representa nuestra función controlada.

Esto permite comprobar:

- cuántas veces se llama una dependencia;
- con qué argumentos;
- qué hace la función superior con el resultado;
- cómo reacciona ante errores simulados.

Al terminar el test, pytest restaura automáticamente el valor original.

Esta técnica también fue utilizada para redirigir:

```text
CUARENTENA
REGISTRO_CUARENTENA
```

hacia rutas temporales.

De esta forma pudimos probar el sistema de cuarentena sin tocar:

```text
FileOrganizer/quarantine/
```

---

## 13. Simulación controlada de errores

Una de las aplicaciones más importantes de `monkeypatch` durante v3.2 fue provocar errores de forma deliberada.

Esto permite responder preguntas como:

```text
¿Qué ocurre si shutil.move() falla?

¿Qué ocurre si aparece una excepción inesperada?

¿La función la oculta?

¿La propaga?

¿La registra?
```

Para analizar el aviso `BLE001` de Ruff se sustituyó temporalmente:

```python
shutil.move()
```

por una función falsa:

```python
def mover_falso(*args, **kwargs):
    raise RuntimeError(
        "Fallo inesperado simulado"
    )
```

El objetivo del test era comprobar que:

```python
RuntimeError
```

se propagara.

Inicialmente el test produjo:

```text
FAILED: DID NOT RAISE RuntimeError
```

¿Por qué?

Porque `core/movimientos.py` contenía:

```python
except Exception as error:
```

Ese bloque capturaba también el `RuntimeError` simulado.

El programa mostraba:

```text
Error inesperado: Fallo inesperado simulado
```

y continuaba.

Desde el punto de vista del usuario esto podía parecer robusto.

Pero desde el punto de vista del desarrollo existía un problema:

```text
un error inesperado de programación
podía quedar oculto.
```

Después de eliminar:

```python
except Exception
```

el mismo test produjo:

```text
PASSED
```

y la batería completa terminó en:

```text
101 passed
```

Este caso muestra una idea fundamental:

> Un test no solo comprueba el código que tenemos. También puede definir el comportamiento que queremos tener.

---

## 14. Mock, stub y dependencia falsa: idea práctica

Durante v3.2 no profundizamos todavía en frameworks especializados de mocking.

Sin embargo, conceptualmente ya hemos utilizado dependencias falsas.

Por ejemplo:

```python
def cuarentena_falsa(...):
    ...
```

o:

```python
def mover_falso(...):
    raise RuntimeError(...)
```

Estas funciones sustituyen temporalmente una dependencia real.

De forma simplificada:

```text
FUNCIÓN REAL
shutil.move()
   │
   ▼
modifica filesystem

FUNCIÓN FALSA
mover_falso()
   │
   ▼
produce comportamiento controlado
```

Esto nos permite aislar la unidad que queremos probar.

El principio importante es:

> Un buen test intenta controlar las dependencias que pueden hacer que el resultado sea impredecible o peligroso.

Por eso aislamos:

- filesystem;
- cuarentena;
- errores;
- funciones auxiliares.

---

## 15. Qué hemos aprendido sobre fixtures

Durante v3.2 utilizamos varias fixtures proporcionadas automáticamente por pytest.

Entre ellas:

```text
tmp_path
capsys
monkeypatch
```

Una fixture proporciona al test un recurso o entorno preparado.

Por ejemplo:

```python
def test_algo(tmp_path):
```

no significa que nosotros hayamos definido `tmp_path`.

Pytest reconoce el nombre y proporciona automáticamente el recurso.

Podemos visualizarlo así:

```text
pytest
  │
  ├── tmp_path ──► directorio temporal
  │
  ├── capsys ────► captura stdout/stderr
  │
  └── monkeypatch ► modificación temporal controlada
```

Las fixtures reducen la cantidad de código de preparación que tenemos que repetir.

También facilitan que los tests permanezcan aislados entre sí.

Ese aislamiento es fundamental.

Un test no debería depender de que otro test se haya ejecutado antes.

Idealmente:

```text
Test A
Test B
Test C
```

deben poder ejecutarse:

```text
A → B → C
C → A → B
solo B
solo C
```

sin cambiar su resultado.

Las fixtures ayudan a conseguir ese comportamiento.
---

## 16. Testing aplicado a la capa de seguridad

Una parte especialmente importante de v3.2 fue aplicar testing automático a las funcionalidades de seguridad introducidas en v3.1.

Hasta ese momento habíamos comprobado manualmente aspectos como:

```text
archivo
   │
   ▼
magic number
   │
   ▼
tipo real
   │
   ▼
comparación con extensión
   │
   ├── coincide ─────► OK
   │
   └── no coincide ──► SOSPECHOSO
```

En v3.2 este comportamiento pasó a estar protegido mediante tests automatizados.

Esto es especialmente importante en código relacionado con seguridad.

Un error en una función de presentación puede producir una salida incorrecta.

Un error en una función de seguridad puede provocar:

- falsos positivos;
- falsos negativos;
- archivos sospechosos no detectados;
- archivos legítimos tratados incorrectamente;
- pérdida de información;
- comportamiento inesperado ante entradas manipuladas.

Por eso no basta con probar únicamente el caso correcto.

También debemos probar:

```text
entradas válidas
entradas inválidas
casos límite
errores del filesystem
contenido inesperado
nombres extraños
rutas incorrectas
```

---

## 17. Tests de magic numbers

Los magic numbers son firmas binarias situadas normalmente al principio de determinados tipos de archivo.

Por ejemplo:

```text
JPEG
FF D8 FF

PNG
89 50 4E 47

PDF
25 50 44 46

ELF
7F 45 4C 46
```

La extensión de un archivo:

```text
foto.jpg
```

es solamente parte de su nombre.

No garantiza que su contenido sea realmente JPEG.

Por ejemplo:

```text
programa.jpg
```

podría comenzar internamente con:

```text
4D 5A
```

que corresponde a la firma utilizada por ejecutables PE/Windows.

Por esta razón, v3.1 incorporó:

```text
core/magic_numbers.py
```

y v3.2 añadió tests automáticos para proteger este comportamiento.

La batería verifica firmas correspondientes a:

- JPEG;
- PNG;
- GIF;
- PDF;
- ZIP;
- GZIP;
- ELF;
- PE/Windows.

Pero también se probaron entradas menos evidentes:

```text
archivo vacío
archivo desconocido
firma incompleta
archivo de un byte
archivo inexistente
directorio en lugar de archivo
nombre Unicode
nombre con espacios
```

Esto introduce una idea importante de seguridad:

> No debemos confiar únicamente en la extensión declarada por un archivo.

La extensión puede ser modificada fácilmente.

El contenido proporciona información adicional que podemos utilizar para verificarlo.

---

## 18. Tests del verificador de archivos

El siguiente nivel de la cadena es:

```text
core/verificador.py
```

Su responsabilidad consiste en relacionar:

```text
EXTENSIÓN DECLARADA
        +
TIPO REAL DETECTADO
        │
        ▼
      ESTADO
```

Los tests comprobaron diferentes combinaciones.

Caso normal:

```text
foto.jpg
   │
   ├── extensión: .jpg
   └── tipo real: JPEG
            │
            ▼
            OK
```

Caso sospechoso:

```text
programa.jpg
   │
   ├── extensión: .jpg
   └── tipo real: PE
            │
            ▼
       SOSPECHOSO
```

También se comprobaron situaciones como:

- PDF disfrazado de ejecutable;
- extensiones no verificadas;
- extensiones escritas en mayúsculas;
- archivos sin extensión;
- archivos vacíos;
- nombres Unicode;
- múltiples extensiones.

Un nombre como:

```text
documento.pdf.exe
```

es especialmente interesante desde el punto de vista de seguridad.

La parte visual del nombre puede intentar inducir al usuario a interpretar el archivo como un documento cuando realmente su extensión final es otra.

Los tests ayudan a garantizar que el programa analiza el archivo según las reglas implementadas y no según una interpretación visual del nombre.

---

## 19. Tests de `core/seguridad.py`

Una vez verificado individualmente cada archivo, necesitamos comprobar la capa encargada de analizar un conjunto de archivos.

Para ello se añadieron tests sobre:

```text
core/seguridad.py
```

La lógica general puede representarse así:

```text
CARPETA
   │
   ▼
recorrer archivos
   │
   ▼
verificar cada archivo
   │
   ├── OK
   ├── SOSPECHOSO
   └── NO_VERIFICADO
   │
   ▼
generar resumen
```

Los tests comprobaron:

- análisis de archivos;
- exclusión de subdirectorios;
- rutas inexistentes;
- rutas que no son directorios;
- filtrado por estado;
- generación del resumen de seguridad.

Esta separación es importante porque evita mezclar responsabilidades.

```text
magic_numbers.py
      │
      ▼
identifica contenido

verificador.py
      │
      ▼
compara contenido/extensión

seguridad.py
      │
      ▼
coordina el análisis
```

Cada capa puede probarse independientemente.

Eso facilita localizar un fallo.

Si un test de `seguridad.py` falla, podemos comprobar si el problema está realmente en:

```text
seguridad.py
verificador.py
magic_numbers.py
```

en lugar de revisar todo el programa sin una dirección clara.

---

## 20. Testing del sistema de cuarentena

El sistema de cuarentena es una funcionalidad delicada porque modifica físicamente el sistema de archivos.

Su operación principal es:

```text
archivo sospechoso
       │
       ▼
quarantine/
       │
       ▼
registro de alerta
```

Los tests de:

```text
core/cuarentena.py
```

validaron situaciones como:

- movimiento correcto del archivo;
- creación del registro;
- archivo inexistente;
- archivo sin extensión;
- nombres Unicode;
- nombres con espacios;
- colisiones de nombres;
- múltiples colisiones consecutivas;
- múltiples entradas en el log;
- prevención de sobrescrituras.

El problema de las colisiones merece especial atención.

Supongamos que ya existe:

```text
quarantine/programa.exe
```

y queremos poner en cuarentena otro archivo llamado:

```text
programa.exe
```

El sistema no debe sobrescribir silenciosamente el archivo anterior.

Debe generar un destino alternativo.

Conceptualmente:

```text
programa.exe
programa_1.exe
programa_2.exe
programa_3.exe
...
```

Los tests verifican precisamente que este mecanismo continúe funcionando aunque aparezcan varias colisiones consecutivas.

---

## 21. Por qué la cuarentena debe probarse en un entorno temporal

Probar una función que mueve archivos reales directamente sobre:

```text
FileOrganizer/quarantine/
```

sería una mala práctica.

Los tests podrían:

- dejar residuos;
- alterar logs reales;
- sobrescribir datos;
- depender del estado anterior de la carpeta;
- producir resultados diferentes entre ejecuciones.

Por eso utilizamos:

```text
tmp_path
+
monkeypatch
```

La idea es:

```text
CUARENTENA REAL
FileOrganizer/quarantine/
        X
        │
        │ no tocar
        ▼

CUARENTENA DEL TEST
/tmp/.../quarantine/
        │
        ▼
entorno controlado
```

Durante el test podemos redirigir temporalmente variables como:

```python
CUARENTENA
REGISTRO_CUARENTENA
```

hacia el directorio temporal.

Al terminar:

```text
pytest elimina el entorno temporal
```

y el proyecto permanece limpio.

Este principio es aplicable a muchas herramientas de ciberseguridad:

> Las pruebas deben realizarse en entornos controlados y aislados siempre que puedan modificar datos o producir efectos secundarios.

---

## 22. Robustez frente al sistema de archivos

Los sistemas de archivos no siempre se comportan como el escenario ideal que imaginamos al programar.

Un archivo puede:

```text
existir al comenzar una operación
```

y desaparecer antes de que termine.

También puede:

```text
existir
pero no ser legible
```

o incluso ser:

```text
un enlace simbólico roto
```

Por eso v3.2 incorporó tests específicos de robustez.

Se probaron situaciones relacionadas con:

- enlaces simbólicos válidos;
- enlaces simbólicos rotos;
- archivos eliminados antes de procesarse;
- archivos sin permisos suficientes;
- directorios sin permisos adecuados.

Esto nos acerca a una idea muy importante:

```text
CASO IDEAL
≠
MUNDO REAL
```

El código robusto debe considerar que el entorno puede cambiar o contener estados inesperados.

---

## 23. Tests de permisos

Los permisos son especialmente importantes en Linux.

Un archivo puede existir pero el proceso puede no tener permiso para leerlo.

Un directorio puede existir pero impedir determinadas operaciones.

Conceptualmente:

```text
archivo.exists()
      │
      ▼
     True
      │
      ▼
¿puedo leerlo?
      │
   ┌──┴──┐
   │     │
  Sí     No
   │     │
   ▼     ▼
leer   PermissionError
```

Esto demuestra que:

```python
archivo.exists()
```

no garantiza que todas las operaciones posteriores vayan a funcionar.

Los tests de robustez permiten comprobar cómo responde FileOrganizer ante este tipo de situaciones.

En seguridad esto es importante porque los permisos forman parte de los controles básicos del sistema operativo.

Un programa no debería asumir que dispone de acceso ilimitado a todos los recursos.

---

## 24. Testing del analizador defensivo de logs

Otra parte importante de v3.2 fue ampliar la cobertura automática de:

```text
core/analizador_logs.py
```

El analizador introducido en v3.1 busca patrones potencialmente relacionados con eventos de seguridad.

El flujo simplificado es:

```text
ARCHIVO LOG
    │
    ▼
leer línea
    │
    ▼
aplicar patrones
    │
    ├── SQL Injection
    │
    └── fallo autenticación
    │
    ▼
extraer información
    │
    ├── IP
    ├── fecha
    ├── línea
    └── severidad
    │
    ▼
correlacionar eventos
```

La nueva batería permitió verificar cada una de estas piezas por separado.

Esto es mejor que depender exclusivamente de una prueba completa del analizador.

Si únicamente probáramos:

```text
archivo log completo
        │
        ▼
resultado final
```

un fallo podría proceder de muchas partes diferentes.

Al probar funciones individuales podemos localizar mejor la causa.

---

## 25. Tests de patrones SQL Injection

Los patrones de SQL Injection se implementaron mediante expresiones regulares.

Entre los casos comprobados se encuentran:

```text
UNION SELECT
OR 1=1
AND 1=1
OR 'a' = 'a'
SLEEP()
BENCHMARK()
DROP TABLE
information_schema
```

Con `pytest.mark.parametrize` podemos utilizar una estructura conceptual como:

```python
@pytest.mark.parametrize(
    "linea",
    [
        "UNION SELECT ...",
        "OR 1=1",
        "AND 1=1",
        "SLEEP(5)",
        "DROP TABLE usuarios",
    ],
)
def test_detecta_sql_injection(linea):
    ...
```

Así podemos añadir nuevos patrones de ataque sin duplicar toda la estructura del test.

Pero durante estas pruebas ocurrió algo especialmente valioso.

Uno de los tests falló.

---

## 26. Un test descubre un bug real

La expresión:

```text
OR 'a' = 'a'
```

debía ser identificada como posible SQL Injection.

Sin embargo, el test indicó que no estaba siendo detectada correctamente.

Esto es exactamente lo que queremos que ocurra durante el desarrollo:

```text
escribimos comportamiento esperado
          │
          ▼
ejecutamos test
          │
          ▼
        FAIL
          │
          ▼
investigamos
          │
          ▼
encontramos bug
```

El problema estaba relacionado con una frontera de palabra:

```regex
\b
```

situada al final de la expresión regular.

Una frontera de palabra representa una transición entre:

```text
carácter de palabra
y
carácter que no es de palabra
```

El patrón concreto terminaba en una comilla.

La utilización de `\b` en esa posición impedía que determinados casos válidos para nuestra detección coincidieran como esperábamos.

Después de corregir la expresión regular:

```text
test específico
      │
      ▼
PASS
```

y posteriormente:

```text
batería completa
      │
      ▼
PASS
```

Este fue uno de los ejemplos más claros de toda v3.2 sobre el valor práctico del testing.

Sin ese test, el programa podía parecer correcto durante una revisión superficial.

El test convirtió una suposición en una comprobación reproducible.

---

## 27. Tests positivos y negativos en detección de seguridad

Cuando desarrollamos detectores de seguridad no basta con comprobar que detectan ataques.

También debemos comprobar que no clasifican tráfico legítimo como ataque.

Tenemos dos problemas diferentes:

```text
ATAQUE REAL
   │
   ▼
no detectado
   │
   ▼
FALSO NEGATIVO
```

y:

```text
TRÁFICO LEGÍTIMO
   │
   ▼
detectado como ataque
   │
   ▼
FALSO POSITIVO
```

Por eso los tests incluyeron tanto patrones sospechosos como líneas normales.

Ejemplos legítimos:

```text
GET /index.html HTTP/1.1
GET /contacto HTTP/1.1
POST /formulario HTTP/1.1
```

El objetivo es que:

```text
patrón sospechoso ──► evento

tráfico normal ─────► ningún evento
```

Esta distinción es fundamental en herramientas defensivas.

Un detector que alerta por todo resulta poco útil.

Y un detector que nunca alerta tampoco cumple su función.

---

## 28. Testing de direcciones IPv4

La extracción de direcciones IPv4 también recibió una batería específica.

Una IPv4 contiene cuatro octetos:

```text
A.B.C.D
```

Cada octeto debe estar entre:

```text
0 y 255
```

Se probaron casos como:

```text
192.168.1.10
0.0.0.0
255.255.255.255
```

y valores inválidos como:

```text
999.999.999.999
256.1.1.1
```

También se comprobaron:

- líneas sin IP;
- múltiples direcciones en una misma línea.

Cuando aparecen varias direcciones, la implementación actual devuelve la primera IPv4 válida encontrada.

Esto significa que el test no debe comprobar lo que imaginamos que la función debería hacer.

Debe comprobar el contrato real que hemos definido para esa función.

---

## 29. Testing de fechas de logs

Los logs utilizados durante esta fase contienen fechas con un formato similar a:

```text
16/Aug/2026:09:01:16
```

La función:

```python
convertir_fecha_log()
```

transforma ese texto en un objeto:

```python
datetime
```

Los tests comprobaron:

- fecha válida;
- ausencia de fecha;
- entrada `None`;
- formato incorrecto.

Durante el análisis con Ruff apareció además:

```text
DTZ007
```

porque:

```python
datetime.strptime()
```

creaba un `datetime` sin información de zona horaria.

En este caso concreto decidimos conservar deliberadamente ese comportamiento.

¿Por qué?

Porque el formato de log procesado actualmente:

```text
%d/%b/%Y:%H:%M:%S
```

no contiene información de zona horaria.

Asignar arbitrariamente:

```text
UTC
```

o cualquier otra zona habría significado inventar información que el log no proporciona.

Por eso se documentó explícitamente la decisión mediante:

```python
# noqa: DTZ007
```

Esta es una lección importante:

> Una advertencia de una herramienta estática debe analizarse, no obedecerse automáticamente.

---

## 30. Correlación temporal de eventos

Detectar una línea individual de autenticación fallida aporta información.

Pero varios eventos relacionados pueden aportar mucha más.

Por ejemplo:

```text
09:01:16  Failed login  192.168.1.20
09:01:17  Failed login  192.168.1.20
09:01:18  Failed login  192.168.1.20
```

Individualmente tenemos:

```text
3 fallos de autenticación
```

Correlacionados tenemos:

```text
misma IP
+
3 intentos
+
2 segundos
        │
        ▼
POSIBLE_FUERZA_BRUTA
```

Los tests validaron una configuración de:

```text
umbral = 3
ventana = 60 segundos
```

y comprobaron varios escenarios.

Caso positivo:

```text
misma IP
3 intentos
2 segundos
      │
      ▼
ALERTA
```

Caso negativo por tiempo:

```text
misma IP
3 intentos
varios minutos
      │
      ▼
SIN ALERTA
```

Caso negativo por IP:

```text
IP A
IP B
IP C
      │
      ▼
SIN ALERTA CORRELACIONADA
```

Caso negativo por umbral:

```text
misma IP
2 intentos
      │
      ▼
SIN ALERTA
```

También se comprobó el comportamiento ante eventos sin fecha.

---

## 31. De detección a correlación

Este cambio representa una evolución conceptual importante del proyecto.

En una primera fase:

```text
LÍNEA
  │
  ▼
¿contiene patrón sospechoso?
```

Después:

```text
EVENTO
  │
  ▼
¿de qué IP procede?
```

Y finalmente:

```text
EVENTOS
   │
   ├── misma IP
   ├── mismo tipo
   ├── proximidad temporal
   └── número de ocurrencias
          │
          ▼
       CORRELACIÓN
```

Esta idea está relacionada con el funcionamiento general de sistemas defensivos que no analizan únicamente eventos aislados, sino relaciones entre múltiples eventos.

FileOrganizer todavía implementa una versión sencilla y educativa de este concepto.

Pero el salto conceptual es importante:

```text
detectar
   ↓
clasificar
   ↓
agrupar
   ↓
correlacionar
```

El testing permite asegurar que cada etapa mantenga el comportamiento esperado mientras seguimos evolucionando el proyecto.

---

## 32. Logs con bytes UTF-8 inválidos

Un archivo de logs real no siempre contiene texto perfectamente formado.

Puede contener bytes que no sean válidos según UTF-8.

Si abrimos un archivo esperando exclusivamente texto UTF-8 válido, una secuencia incorrecta puede provocar:

```text
UnicodeDecodeError
```

El analizador utiliza:

```python
errors="replace"
```

durante la lectura.

Esto permite sustituir determinados bytes inválidos y continuar procesando el resto del archivo.

Se añadió un test específico para verificar este comportamiento.

Conceptualmente:

```text
LOG
 │
 ├── línea válida
 ├── bytes inválidos
 └── línea sospechosa
        │
        ▼
el analizador continúa
```

Esta decisión mejora la robustez.

En análisis defensivo, descartar un archivo completo por una pequeña anomalía de codificación podría impedir analizar información útil situada posteriormente.

---

## 33. Lo que nos enseñó este bloque de seguridad

Las pruebas de seguridad de v3.2 no consistieron simplemente en aumentar un contador de tests.

Permitieron estudiar varias ideas importantes:

```text
No confiar en extensiones
        │
        ▼
verificar contenido

No probar solo casos válidos
        │
        ▼
probar entradas anómalas

No probar solo detecciones
        │
        ▼
probar también falsos positivos

No analizar solo eventos aislados
        │
        ▼
correlacionar eventos

No asumir filesystem perfecto
        │
        ▼
probar errores y permisos
```

También comprobamos algo especialmente importante:

> Los tests son una herramienta defensiva para el propio software.

Nos protegen frente a cambios que accidentalmente rompan comportamientos que ya habíamos validado.

Podemos representarlo así:

```text
SEGURIDAD DEL PROGRAMA
        │
        ├── validación de archivos
        ├── cuarentena
        ├── análisis de logs
        └── correlación

SEGURIDAD DEL DESARROLLO
        │
        ├── pytest
        ├── tests de robustez
        ├── regresiones
        └── análisis estático
```

Ambas capas son diferentes, pero se complementan.
---

## 34. Introducción al análisis estático con Ruff

Después de construir una batería sólida de tests, el siguiente objetivo de v3.2 fue analizar la calidad del código sin necesidad de ejecutarlo.

Para ello incorporamos:

```text
Ruff 0.16.3
```

Ruff es una herramienta de análisis estático y linting para Python.

La diferencia fundamental respecto a pytest es:

```text
pytest
   │
   ▼
ejecuta el código
   │
   ▼
comprueba comportamiento
```

mientras que:

```text
Ruff
   │
   ▼
analiza el código fuente
   │
   ▼
detecta determinados problemas
```

Por tanto, ambas herramientas cumplen funciones diferentes.

Pytest puede responder:

```text
¿La función devuelve el resultado esperado?
```

Ruff puede responder:

```text
¿Hay imports sin utilizar?

¿Los imports están desordenados?

¿Existe una captura demasiado genérica de excepciones?

¿Se están utilizando datetimes sin zona horaria?

¿Hay construcciones innecesarias?
```

Una herramienta no sustituye a la otra.

Se complementan.

---

## 35. Primer análisis con Ruff

Ruff se instaló dentro del entorno virtual del proyecto:

```text
.venv
```

La versión utilizada durante v3.2 fue:

```text
ruff 0.16.3
```

El primer análisis completo encontró:

```text
37 avisos
```

Esto no significaba:

```text
37 bugs
```

Un aviso de linting puede representar:

- código innecesario;
- una inconsistencia de estilo;
- una construcción mejorable;
- una posible fuente de errores;
- una decisión que necesita revisión;
- un comportamiento perfectamente válido que debe justificarse.

Por eso decidimos no ejecutar una corrección automática masiva.

La estrategia utilizada fue:

```text
Ruff detecta
     │
     ▼
seleccionar una regla
     │
     ▼
entender el aviso
     │
     ▼
revisar el código
     │
     ▼
corregir manualmente
     │
     ▼
pytest
     │
     ▼
Ruff
     │
     ▼
git diff --check
```

Este procedimiento permitió aprender qué significaba cada regla y reducir el riesgo de introducir cambios no comprendidos.

---

## 36. Por qué no utilizamos `--fix` masivamente

Ruff puede corregir automáticamente muchos avisos mediante:

```bash
ruff check --fix
```

Sin embargo, durante v3.2 evitamos utilizarlo de forma indiscriminada sobre todo el proyecto.

La razón fue pedagógica y técnica.

Si hubiéramos ejecutado:

```text
37 avisos
     │
     ▼
--fix
     │
     ▼
muchos cambios automáticos
```

habríamos obtenido posiblemente un código más limpio, pero habríamos perdido gran parte del aprendizaje.

Nuestro procedimiento fue:

```text
1 aviso
   │
   ▼
¿qué significa?
   │
   ▼
¿dónde aparece?
   │
   ▼
¿por qué aparece?
   │
   ▼
¿la recomendación tiene sentido?
   │
   ▼
corregir
   │
   ▼
volver a probar
```

Además, una herramienta automática no conoce completamente la intención del programa.

Por eso la regla utilizada durante esta fase fue:

> Ruff propone; nosotros analizamos y decidimos.

---

## 37. F401 — imports no utilizados

El primer grupo revisado fue:

```text
F401
```

Ruff encontró cuatro imports que no se utilizaban.

Entre ellos aparecía:

```python
from core.mensajes import mostrar_error, mostrar_error_ruta
```

pero:

```python
mostrar_error
```

ya no era utilizado en `organizador.py`.

También aparecieron imports innecesarios en tests, como:

```python
from pathlib import Path
```

o:

```python
import pytest
```

cuando el archivo correspondiente ya no utilizaba esos nombres.

El problema puede representarse así:

```text
IMPORT
  │
  ▼
nombre disponible
  │
  ▼
nunca utilizado
```

Aunque normalmente no rompe el programa, genera:

- ruido;
- dependencias aparentes innecesarias;
- confusión para quien lee el código;
- mantenimiento más difícil.

Se eliminaron únicamente los imports confirmados como innecesarios.

Resultado:

```text
All checks passed!
```

Después:

```text
100 passed
```

Esto confirmó que la limpieza no había modificado el comportamiento esperado.

---

## 38. F541 — f-strings sin interpolación

La siguiente regla revisada fue:

```text
F541
```

Ruff encontró construcciones como:

```python
print(f"\nArchivo:")
```

Una f-string tiene sentido cuando necesitamos insertar valores:

```python
print(f"Archivo: {nombre}")
```

Pero en:

```python
f"\nArchivo:"
```

no existe ningún:

```text
{valor}
```

Por tanto, el prefijo:

```python
f
```

es innecesario.

Se cambió:

```python
print(f"\nArchivo:")
```

por:

```python
print("\nArchivo:")
```

y:

```python
print(f"\nMotivo:")
```

por:

```python
print("\nMotivo:")
```

No cambió el resultado mostrado al usuario.

Fue una limpieza de código.

Después:

```text
F541
All checks passed!
```

y:

```text
100 passed
```

---

## 39. I001 — normalización de imports

La regla:

```text
I001
```

detectó bloques de imports desordenados o con formato no normalizado.

Inicialmente se localizaron:

```text
17 errores
```

La revisión afectó a diferentes módulos de:

```text
core/
```

a:

```text
organizador.py
```

y a varios tests.

Por ejemplo, teníamos situaciones conceptualmente similares a:

```python
from pathlib import Path
import shutil
```

Ruff propuso el orden:

```python
import shutil
from pathlib import Path
```

También normalizó la separación entre:

```text
biblioteca estándar

imports internos del proyecto
```

Por ejemplo:

```python
from datetime import datetime
from pathlib import Path

from core.analizador import analizar_carpeta
```

La corrección se realizó en dos tandas:

```text
TANDA A
core/
+
organizador.py
```

y posteriormente:

```text
TANDA B
tests
```

Después de cada tanda ejecutamos la batería completa.

Resultado final:

```text
I001
All checks passed!
```

sin regresiones.

---

## 40. PLR0402 — imports mediante alias innecesarios

Ruff detectó construcciones como:

```python
import core.cuarentena as cuarentena
```

mediante:

```text
PLR0402
```

La forma recomendada fue:

```python
from core import cuarentena
```

La misma revisión se aplicó al módulo de movimientos utilizado por los tests.

La diferencia puede parecer pequeña:

```text
import core.cuarentena as cuarentena
```

frente a:

```text
from core import cuarentena
```

pero Ruff busca una forma más directa de expresar la dependencia.

Después de modificar estos imports:

```text
PLR0402
All checks passed!
```

y la batería continuó en:

```text
101 passed
```

---

## 41. FLY002 — construcción de cadenas

Ruff detectó también:

```text
FLY002
```

en algunos tests del analizador de logs.

El código utilizaba:

```python
"\n".join(
    [
        "línea 1",
        "línea 2",
        "línea 3",
    ]
)
```

para construir contenido fijo.

En esos casos concretos, Ruff propuso una construcción más directa.

La revisión se realizó únicamente sobre los tests afectados.

Lo importante no fue sustituir automáticamente cualquier uso de:

```python
join()
```

porque `join()` es una herramienta perfectamente válida.

La cuestión era analizar el contexto.

Si tenemos una colección dinámica:

```python
lineas = obtener_lineas()

texto = "\n".join(lineas)
```

`join()` tiene pleno sentido.

Pero si todo el contenido es fijo y conocido al escribir el código, puede existir una representación más sencilla.

Después de revisar ambos casos:

```text
FLY002
All checks passed!
```

y los tests específicos del analizador mostraron:

```text
10 passed
```

mientras la batería completa permaneció en:

```text
101 passed
```

---

## 42. BLE001 — captura demasiado amplia de excepciones

Uno de los avisos más importantes de Ruff fue:

```text
BLE001
```

en:

```text
core/movimientos.py
```

El código contenía:

```python
except Exception as error:
```

Antes de este bloque ya existían excepciones específicas:

```python
except PermissionError:
```

```python
except FileNotFoundError:
```

```python
except OSError as error:
```

y finalmente:

```python
except Exception as error:
```

El último bloque capturaba prácticamente cualquier excepción derivada de `Exception`.

A primera vista podía parecer una medida de robustez:

```text
ocurre cualquier error
        │
        ▼
lo capturo
        │
        ▼
el programa continúa
```

Pero existe un riesgo importante:

```text
BUG DE PROGRAMACIÓN
        │
        ▼
except Exception
        │
        ▼
bug ocultado
        │
        ▼
el programa continúa
```

Un error inesperado no siempre debe convertirse silenciosamente en un mensaje para el usuario.

A veces necesitamos que se propague para poder detectarlo durante el desarrollo.

---

## 43. No eliminamos `except Exception` solo porque Ruff lo dijo

En lugar de borrar inmediatamente:

```python
except Exception
```

primero creamos un test.

El objetivo fue definir el comportamiento deseado:

```text
si aparece un RuntimeError inesperado
        │
        ▼
NO debe quedar oculto
```

Mediante `monkeypatch` sustituimos:

```python
shutil.move()
```

por una función que generaba deliberadamente:

```python
RuntimeError(
    "Fallo inesperado simulado"
)
```

El test esperaba:

```python
with pytest.raises(RuntimeError):
```

La primera ejecución produjo:

```text
FAILED
DID NOT RAISE RuntimeError
```

El motivo quedó demostrado:

```text
RuntimeError
     │
     ▼
except Exception
     │
     ▼
capturado
```

Solo después de tener esta evidencia eliminamos el bloque genérico.

Al repetir el test:

```text
PASSED
```

Después:

```text
BLE001
All checks passed!
```

y finalmente:

```text
101 passed
```

Este procedimiento fue especialmente importante porque convirtió una recomendación del linter en una decisión respaldada por un test.

---

## 44. Excepciones específicas frente a excepciones genéricas

Después de la revisión, `core/movimientos.py` mantiene tratamiento específico para errores que sí conocemos y sabemos gestionar.

Conceptualmente:

```text
PermissionError
      │
      ▼
permiso denegado
      │
      ▼
mensaje controlado
```

```text
FileNotFoundError
      │
      ▼
archivo desaparecido/no encontrado
      │
      ▼
mensaje controlado
```

```text
OSError
      │
      ▼
error del sistema operativo
      │
      ▼
mensaje controlado
```

Pero un error inesperado diferente:

```text
RuntimeError
TypeError
bug interno
...
```

ya no queda absorbido automáticamente por:

```python
except Exception
```

La idea aprendida es:

> Capturar una excepción tiene sentido cuando sabemos qué hacer con ella.

Capturar todo simplemente para que el programa no termine puede ocultar defectos importantes.

---

## 45. EXE001 — shebang y permiso de ejecución

Ruff encontró:

```text
EXE001
```

en:

```text
organizador.py
```

El archivo comenzaba con:

```python
#!/usr/bin/env python3
```

Este shebang indica que el script está pensado para poder ejecutarse directamente en sistemas Unix/Linux.

Por ejemplo:

```bash
./organizador.py
```

Pero el archivo no tenía activado el permiso de ejecución.

Existía una inconsistencia:

```text
SHEBANG
   │
   ▼
"puedo ejecutarme directamente"

PERMISOS
   │
   ▼
"no soy ejecutable"
```

Se corrigió mediante:

```bash
chmod +x organizador.py
```

Los permisos pasaron a incluir:

```text
x
```

y Git registró:

```text
mode change 100644 => 100755
```

Después:

```text
EXE001
All checks passed!
```

Esto también muestra que Git no controla únicamente el contenido textual.

En sistemas compatibles puede registrar el bit de ejecutable del archivo.

---

## 46. La familia DTZ — fechas y zonas horarias

Ruff detectó varios avisos relacionados con fechas:

```text
DTZ001
DTZ005
DTZ006
DTZ007
```

Estos avisos señalan usos de `datetime` sin información explícita de zona horaria.

Por ejemplo:

```python
datetime.now()
```

crea un `datetime` naive.

También:

```python
datetime.fromtimestamp(...)
```

sin indicar zona horaria puede depender del entorno local.

Esto puede producir problemas cuando:

- el programa se ejecuta en máquinas diferentes;
- existen cambios de horario;
- se comparan eventos de distintas zonas;
- los datos se almacenan y posteriormente se interpretan en otro sistema.

---

## 47. Datetime naive y timezone-aware

Un `datetime` naive no contiene información de zona horaria.

Ejemplo conceptual:

```text
2026-08-18 11:30:00
```

Sabemos la hora.

Pero no sabemos explícitamente:

```text
¿UTC?
¿Europa/Madrid?
¿otra zona?
```

Un `datetime` aware contiene información adicional sobre su relación temporal.

Conceptualmente:

```text
2026-08-18 11:30:00 +02:00
```

La diferencia es importante cuando necesitamos representar instantes reales de forma inequívoca.

Durante v3.2 revisamos cada aparición individualmente en lugar de aplicar una sustitución automática global.

---

## 48. Corrección de `datetime.now()`

En módulos como:

```text
core/cuarentena.py
core/logger.py
core/estadisticas.py
core/informes.py
```

existían llamadas como:

```python
datetime.now()
```

Se modificaron para partir de una referencia explícita:

```python
datetime.now(timezone.utc)
```

y, cuando se necesitaba representación local:

```python
datetime.now(timezone.utc).astimezone()
```

La idea es:

```text
UTC explícito
     │
     ▼
instante inequívoco
     │
     ▼
conversión local cuando sea necesaria
```

Después de cada grupo de cambios se ejecutaron los tests y Ruff.

No se realizó una sustitución masiva sin comprobar el contexto.

---

## 49. Corrección de `datetime.fromtimestamp()`

También aparecieron avisos:

```text
DTZ006
```

sobre construcciones como:

```python
datetime.fromtimestamp(
    archivo["fecha"]
)
```

El timestamp Unix representa un instante temporal.

Por eso es preferible interpretarlo con una zona explícita.

Las apariciones revisadas estaban en:

```text
core/informes.py
organizador.py
```

La corrección permitió evitar que la interpretación dependiera implícitamente de la configuración temporal del entorno.

Esto mejora la previsibilidad del código.

---

## 50. DTZ007 — una advertencia que decidimos no corregir

El caso de:

```text
core/analizador_logs.py
```

fue diferente.

Ruff señaló:

```text
DTZ007
```

sobre:

```python
datetime.strptime(
    fecha_texto,
    "%d/%b/%Y:%H:%M:%S",
)
```

Podríamos haber añadido artificialmente:

```text
UTC
```

pero el texto analizado:

```text
16/Aug/2026:09:01:16
```

no contiene zona horaria.

Por tanto:

```text
dato original
      │
      ▼
no especifica timezone
```

Asignarle una zona arbitraria significaría:

```text
inventar información
```

Decidimos conservar deliberadamente un `datetime` naive para la correlación temporal interna.

La decisión quedó documentada:

```python
# El formato de log analizado no incluye
# información de zona horaria.
# Se conserva un datetime naive deliberadamente
# para la correlación temporal interna.
```

y la línea se marcó mediante:

```python
# noqa: DTZ007
```

Esto indica a Ruff:

```text
conozco este aviso
lo he revisado
esta excepción es deliberada
```

---

## 51. `# noqa` no significa ignorar los problemas

Es importante comprender correctamente:

```python
# noqa
```

No debería utilizarse como:

```text
Ruff molesta
     │
     ▼
silenciar aviso
```

Su uso correcto es más parecido a:

```text
Ruff detecta algo
       │
       ▼
analizamos el contexto
       │
       ▼
la construcción es deliberada
       │
       ▼
documentamos el motivo
       │
       ▼
silenciamos solo esa regla
```

Por eso utilizamos:

```python
# noqa: DTZ007
```

en lugar de un:

```python
# noqa
```

genérico.

Así especificamos exactamente qué regla estamos exceptuando.

Este enfoque mantiene el análisis estático útil.

---

## 52. DTZ001 en el test de tiempo

Ruff también detectó:

```text
DTZ001
```

en un test que construía directamente:

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

El test estaba comprobando precisamente el resultado naive producido por:

```python
convertir_fecha_log()
```

Por tanto, cambiar únicamente el valor esperado a un datetime aware habría roto la coherencia del test.

La decisión fue la misma:

```text
producción devuelve naive deliberadamente
              │
              ▼
test debe esperar naive
```

El aviso se documentó de forma específica.

Después:

```text
DTZ
All checks passed!
```

y los tests temporales mostraron:

```text
9 passed
```

mientras la batería completa permaneció en:

```text
101 passed
```

---

## 53. Ruff no es un juez automático

La experiencia con DTZ dejó una de las enseñanzas más importantes de esta versión.

Una herramienta estática puede decir:

```text
esto merece revisión
```

pero no siempre puede determinar:

```text
qué intención tenía el programador
```

Por tanto, nuestro flujo debe ser:

```text
AVISO
  │
  ▼
ENTENDER
  │
  ▼
REVISAR CONTEXTO
  │
  ├── problema real ─────► corregir
  │
  └── decisión válida ───► documentar
```

Esto es muy diferente de:

```text
AVISO
  │
  ▼
CORREGIR AUTOMÁTICAMENTE TODO
```

Las herramientas ayudan al desarrollador.

No sustituyen su criterio.

---

## 54. Validación continua después de cada grupo

Durante toda la limpieza con Ruff mantuvimos una regla:

```text
CAMBIO
  │
  ▼
RUFF específico
  │
  ▼
PYTEST
  │
  ▼
COMPILACIÓN
  │
  ▼
GIT DIFF --CHECK
```

Por ejemplo:

```text
F401
  │
  ▼
All checks passed
  │
  ▼
100 passed
```

Después:

```text
F541
  │
  ▼
All checks passed
  │
  ▼
100 passed
```

Después:

```text
I001
  │
  ▼
All checks passed
  │
  ▼
100 passed
```

Y tras incorporar el nuevo test de movimientos:

```text
BLE001
  │
  ▼
All checks passed
  │
  ▼
101 passed
```

Esta forma de trabajar limita el tamaño de cada cambio.

Si aparece una regresión sabemos aproximadamente qué modificación la produjo.

---

## 55. Resultado final de Ruff

Después de revisar progresivamente todos los avisos seleccionados, ejecutamos Ruff sobre el proyecto completo.

Resultado:

```text
All checks passed!
```

Simultáneamente:

```text
pytest
101 passed
```

y:

```text
python3 -m py_compile core/*.py organizador.py
```

no produjo errores.

También:

```text
git diff --check
```

permaneció limpio.

El resultado puede representarse así:

```text
              CÓDIGO v3.2
                   │
        ┌──────────┼──────────┐
        │          │          │
        ▼          ▼          ▼
     pytest       Ruff    py_compile
        │          │          │
        ▼          ▼          ▼
  comportamiento calidad    sintaxis
        │          │          │
        └──────────┼──────────┘
                   │
                   ▼
             validación final
```

Ruff no hizo que el programa fuera correcto por sí solo.

Pytest tampoco garantiza que no exista ningún bug.

Pero juntos proporcionan controles diferentes y complementarios.

---

## 56. Qué aprendimos realmente utilizando Ruff

Durante esta fase aprendimos a interpretar distintas categorías de problemas:

```text
F401
imports sin utilizar

F541
f-strings innecesarias

I001
orden y formato de imports

PLR0402
forma de importar módulos

FLY002
construcción simplificable de cadenas

BLE001
captura demasiado amplia de excepciones

EXE001
incoherencia entre shebang y permisos

DTZ
manejo explícito de fechas y zonas horarias
```

Pero el aprendizaje principal fue metodológico:

```text
herramienta detecta
       │
       ▼
programador comprende
       │
       ▼
test protege
       │
       ▼
cambio controlado
       │
       ▼
validación completa
```

Este procedimiento es mucho más valioso que conseguir simplemente:

```text
0 avisos
```

El objetivo no es satisfacer a Ruff.

El objetivo es utilizar Ruff para escribir y mantener mejor software.
---

## 57. Refactorización de `organizador.py`

Durante v3.2 no solo se añadieron tests.

También se utilizó esa nueva red de seguridad para empezar a mejorar la estructura de:

```text
organizador.py
```

Antes del refactor, la función:

```python
seleccionar_carpeta()
```

concentraba demasiadas responsabilidades.

Entre otras tareas:

```text
pedir ruta
validar ruta
analizar carpeta
verificar seguridad
mostrar alertas
mostrar estadísticas
mostrar clasificación
pedir confirmación
gestionar cuarentena
gestionar simulación
mover archivos
mostrar resumen final
```

Una función que concentra demasiadas responsabilidades:

- cuesta más de leer;
- cuesta más de probar;
- cuesta más de modificar;
- aumenta el riesgo de romper comportamientos no relacionados.

Por eso comenzamos una separación progresiva.

---

## 58. Funciones extraídas del flujo principal

Durante v3.2 se extrajeron varias responsabilidades concretas:

```python
mostrar_alertas_seguridad()
mostrar_analisis_carpeta()
mostrar_clasificacion()
enviar_sospechosos_cuarentena()
```

El objetivo no fue reescribir todo el archivo.

La estrategia fue:

```text
seleccionar bloque pequeño
        │
        ▼
extraer función
        │
        ▼
ejecutar tests
        │
        ▼
crear test específico
        │
        ▼
volver a ejecutar batería completa
```

Esto reduce el riesgo frente a un refactor grande.

---

## 59. Separar lógica y presentación

Una de las mejoras conceptuales del refactor fue distinguir mejor entre:

```text
lógica
```

y:

```text
presentación
```

Por ejemplo:

```python
mostrar_analisis_carpeta(datos)
```

tiene una responsabilidad clara:

```text
recibir datos
      │
      ▼
presentarlos al usuario
```

Del mismo modo:

```python
mostrar_clasificacion(clasificacion)
```

se encarga únicamente de presentar la clasificación prevista y devolver un valor que permita al flujo principal decidir si debe continuar.

Separar estas tareas facilita:

- lectura;
- testing;
- mantenimiento;
- futura reutilización.

---

## 60. La recursión accidental durante el refactor

Durante la extracción de:

```python
mostrar_analisis_carpeta()
```

se introdujo accidentalmente una llamada a sí misma.

Conceptualmente:

```python
def mostrar_analisis_carpeta(datos):
    mostrar_analisis_carpeta(datos)
```

Esto provoca:

```text
función
  │
  ▼
se llama a sí misma
  │
  ▼
se vuelve a llamar
  │
  ▼
se vuelve a llamar
  │
  ▼
...
```

hasta alcanzar:

```text
RecursionError
```

Los tests específicos detectaron inmediatamente:

```text
maximum recursion depth exceeded
```

La función fue corregida y posteriormente:

```text
3 passed
```

en los tests afectados.

Después:

```text
96 passed
```

en la batería completa de ese momento.

Este caso fue una demostración muy clara de:

> Refactorizar con tests es mucho más seguro que refactorizar únicamente observando el resultado manualmente.

---

## 61. Por qué el número de líneas no es la única métrica

Durante el refactor observamos que `organizador.py` tenía más de quinientas líneas.

Podría parecer lógico pensar:

```text
menos líneas = mejor código
```

pero no siempre es así.

El objetivo real era:

```text
responsabilidades más claras
```

No se buscó reducir líneas a cualquier precio.

Una función más pequeña puede ser mejor si:

- tiene una responsabilidad concreta;
- tiene un nombre descriptivo;
- puede probarse de forma aislada;
- reduce duplicación;
- facilita entender el flujo.

Por tanto:

```text
CALIDAD
≠
mínimo número de líneas
```

La calidad depende de cómo se estructura el comportamiento.

---

## 62. Testing como red de seguridad para refactorizar

Antes de disponer de pytest, modificar una función grande podía generar dudas:

```text
¿habré roto la simulación?

¿seguirá funcionando la cuarentena?

¿la clasificación se mostrará igual?

¿seguirán funcionando los logs?
```

Con una batería automatizada, después de cada refactor podemos ejecutar:

```bash
python -m pytest test/ -q
```

y comprobar si los comportamientos cubiertos continúan funcionando.

El flujo pasa de:

```text
modifico
   │
   ▼
espero no haber roto nada
```

a:

```text
modifico
   │
   ▼
ejecuto tests
   │
   ▼
evidencia automática
```

Esto aumenta la confianza durante cambios estructurales.

---

## 63. Limpieza del entorno de desarrollo

La revisión final de v3.2 también incluyó elementos que no forman parte directamente de la lógica del programa.

Se revisaron:

```text
.gitignore
requirements.txt
requirements-dev.txt
cachés
entorno virtual
permisos
```

Esto forma parte de mantener un repositorio limpio y reproducible.

---

## 64. Corrección de `requirements.txt`

El proyecto contenía:

```text
requeriments.txt
```

El nombre correcto según la convención habitual es:

```text
requirements.txt
```

Se renombró el archivo.

Actualmente permanece vacío porque FileOrganizer utiliza la biblioteca estándar de Python para su funcionalidad principal.

No necesita instalar paquetes externos para ejecutarse.

---

## 65. Separación de dependencias de desarrollo

Aunque FileOrganizer no necesita paquetes externos en producción, v3.2 sí utiliza herramientas externas durante el desarrollo.

Por eso se creó:

```text
requirements-dev.txt
```

con:

```text
pytest==9.1.1
ruff==0.16.3
```

La separación conceptual queda así:

```text
requirements.txt
        │
        ▼
dependencias necesarias
para ejecutar el programa

requirements-dev.txt
        │
        ▼
herramientas necesarias
para desarrollar y validar
```

Esto permite preparar un entorno de desarrollo equivalente mediante:

```bash
python -m pip install -r requirements-dev.txt
```

---

## 66. Por qué fijamos versiones

En:

```text
requirements-dev.txt
```

utilizamos:

```text
pytest==9.1.1
ruff==0.16.3
```

El operador:

```text
==
```

indica una versión exacta.

Esto mejora la reproducibilidad.

Si en el futuro una nueva versión de Ruff cambia reglas o comportamiento, podemos reconstruir el entorno utilizado durante v3.2 con las versiones conocidas.

Conceptualmente:

```text
MISMO CÓDIGO
+
MISMAS HERRAMIENTAS
+
MISMAS VERSIONES
        │
        ▼
entorno más reproducible
```

---

## 67. Mejora de `.gitignore`

Durante las ejecuciones de pytest y Ruff aparecieron directorios automáticos:

```text
.pytest_cache/
.ruff_cache/
```

No forman parte del código fuente.

Por eso se añadieron a:

```text
.gitignore
```

El archivo ya excluía elementos como:

```text
.venv/
__pycache__/
*.pyc
.vscode/
logs/
reports/*.txt
stats/estadisticas.json
quarantine/
```

y ahora también:

```text
.pytest_cache/
.ruff_cache/
```

Esto evita subir al repositorio archivos generados localmente sin valor como código fuente.

---

## 68. Por qué no subimos `.venv`

El entorno:

```text
.venv/
```

contiene:

- ejecutables;
- paquetes instalados;
- metadatos;
- archivos específicos del entorno.

Puede ocupar bastante espacio y no es necesario versionarlo.

En lugar de subirlo:

```text
.venv/
```

guardamos:

```text
requirements-dev.txt
```

De este modo cualquier máquina puede recrear el entorno.

La idea es:

```text
NO versionar entorno construido

SÍ versionar instrucciones para reconstruirlo
```

---

## 69. Repositorio público y archivos sensibles

FileOrganizer incluye funciones de cuarentena y análisis de archivos potencialmente sospechosos.

Por eso fue importante mantener:

```text
quarantine/
```

fuera del control de versiones.

También:

```text
logs/
```

y determinados archivos generados no deben publicarse automáticamente.

Un repositorio público debe contener:

- código;
- documentación;
- configuración segura;
- tests;
- ejemplos controlados.

No debe contener accidentalmente:

- muestras potencialmente maliciosas;
- datos personales;
- logs reales sensibles;
- secretos;
- credenciales;
- entornos locales completos.

Esta revisión forma parte también de la calidad del proyecto.

---

## 70. Flujo de validación profesional adoptado

Durante v3.2 se consolidó un flujo de trabajo repetible.

Antes de considerar un cambio estable:

```text
1. modificar
2. ejecutar test específico
3. ejecutar batería completa
4. ejecutar Ruff
5. compilar
6. revisar Git
```

Conceptualmente:

```text
CÓDIGO
  │
  ▼
TEST ESPECÍFICO
  │
  ▼
PYTEST COMPLETO
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
REVISIÓN DIFF
  │
  ▼
COMMIT
```

Este flujo reduce el riesgo de publicar cambios no revisados.

---

## 71. Git como parte del proceso de calidad

Git no se utilizó únicamente para guardar versiones.

También se utilizó para inspeccionar los cambios.

Comandos como:

```bash
git status
```

permiten comprobar qué archivos han cambiado.

```bash
git diff
```

permite estudiar las modificaciones antes de confirmarlas.

```bash
git diff --check
```

detecta determinados problemas de whitespace.

```bash
git diff --cached
```

permite revisar exactamente qué contenido entrará en el siguiente commit.

Por tanto:

```text
Git
```

también forma parte del proceso de control de calidad.

---

## 72. Checkpoints durante el desarrollo

v3.2 utilizó un checkpoint importante:

```text
9ce9422
```

correspondiente a:

```text
v3.2: añade batería de tests y refactoriza flujo principal
```

En ese punto:

```text
100 tests
19 archivos
main sincronizada
working tree limpio
```

El checkpoint permitió continuar la revisión con Ruff sabiendo que existía una base estable a la que volver si algo salía mal.

Esto muestra otra utilidad de Git:

```text
COMMIT ESTABLE
      │
      ▼
punto de recuperación
```

No es necesario esperar a terminar una versión completa para crear un commit útil.

---

## 73. De 100 a 101 tests

La batería alcanzó inicialmente:

```text
100 tests
```

Ese número coincidió con el final del primer gran bloque de testing.

Sin embargo, durante Ruff apareció:

```text
BLE001
```

y decidimos crear:

```text
test/test_movimientos_robustez.py
```

El test comprobó que un:

```text
RuntimeError
```

inesperado no quedara oculto.

La batería pasó entonces a:

```text
101 tests
```

Este crecimiento es especialmente significativo.

El test número 101 no fue añadido simplemente para aumentar cobertura.

Nació de:

```text
análisis estático
      │
      ▼
pregunta sobre comportamiento
      │
      ▼
nuevo test
      │
      ▼
mejora de diseño
```

Esto representa muy bien el espíritu de v3.2.

---

## 74. Estado técnico final de v3.2

La versión termina con:

```text
20 archivos de tests
101 tests
Ruff limpio
compilación correcta
git diff --check limpio
```

La validación principal utiliza:

```bash
python -m pytest test/ -q
```

Resultado:

```text
101 passed
```

Ruff:

```bash
python -m ruff check core organizador.py test
```

Resultado:

```text
All checks passed!
```

Compilación:

```bash
python3 -m py_compile core/*.py organizador.py
```

Resultado:

```text
sin errores
```

Git:

```bash
git diff --check
```

Resultado:

```text
sin errores
```

---

## 75. Competencias técnicas adquiridas

Durante v3.2 se trabajaron de forma práctica competencias relacionadas con:

### Python

- funciones;
- módulos;
- excepciones;
- `pathlib`;
- expresiones regulares;
- `datetime`;
- zonas horarias;
- manejo del filesystem.

### Testing

- pytest;
- Arrange / Act / Assert;
- `assert`;
- `pytest.raises`;
- `pytest.mark.parametrize`;
- `tmp_path`;
- `capsys`;
- `monkeypatch`;
- tests positivos;
- tests negativos;
- casos límite;
- tests de regresión;
- pruebas de robustez.

### Calidad de código

- Ruff;
- imports no utilizados;
- normalización de imports;
- f-strings innecesarias;
- tratamiento de excepciones;
- linting;
- análisis estático;
- decisiones documentadas mediante `noqa`.

### Linux

- permisos;
- chmod;
- shebang;
- enlaces simbólicos;
- filesystem;
- entorno virtual.

### Git

- status;
- diff;
- diff --check;
- staging;
- commits;
- checkpoints;
- sincronización con remoto.

### Seguridad

- magic numbers;
- extensión frente a tipo real;
- cuarentena;
- robustez ante entradas anómalas;
- SQL Injection;
- fallos de autenticación;
- IPv4;
- correlación;
- ventanas temporales;
- posibles ataques de fuerza bruta.

---

## 76. Cambio de mentalidad durante v3.2

Uno de los resultados más importantes no es una función concreta.

Es un cambio en la forma de desarrollar.

Al principio de FileOrganizer el flujo podía parecerse a:

```text
escribir código
      │
      ▼
ejecutarlo
      │
      ▼
parece funcionar
```

v3.2 introduce un flujo más cercano a:

```text
entender comportamiento
      │
      ▼
escribir/modificar código
      │
      ▼
test automático
      │
      ▼
análisis estático
      │
      ▼
revisión
      │
      ▼
evidencia
```

La diferencia está en pasar de:

```text
"creo que funciona"
```

a:

```text
"tengo varias comprobaciones automáticas
que respaldan que estos escenarios funcionan"
```

Ese cambio es fundamental para proyectos que empiezan a crecer.

---

## 77. Qué no significa tener 101 tests

Es importante no interpretar incorrectamente el resultado:

```text
101 passed
```

No significa:

```text
FileOrganizer no tiene ningún bug
```

Tampoco significa:

```text
todo el código está cubierto
```

Ni:

```text
todos los casos posibles han sido considerados
```

Significa:

```text
101 escenarios automatizados
producen actualmente
el resultado esperado
```

Todavía pueden existir:

- escenarios no cubiertos;
- errores de diseño;
- problemas de rendimiento;
- condiciones de carrera;
- casos específicos de otros sistemas operativos;
- entradas que aún no hemos considerado.

El testing aumenta confianza.

No elimina la necesidad de seguir pensando críticamente.

---

## 78. Qué no significa tener Ruff limpio

Del mismo modo:

```text
All checks passed!
```

no significa:

```text
código perfecto
```

Solo significa que:

```text
según las reglas activas de Ruff
no quedan avisos detectados
```

Ruff no conoce toda la intención del proyecto.

No puede determinar por sí solo:

- si la arquitectura es correcta;
- si una regla de negocio está bien diseñada;
- si un algoritmo produce siempre la decisión adecuada;
- si una detección de seguridad tiene suficientes patrones;
- si el programa es seguro en todos los contextos.

Por eso:

```text
RUFF
+
PYTEST
+
REVISIÓN HUMANA
```

es mucho más útil que cualquiera de esas herramientas por separado.

---

## 79. Valor de v3.2 para el portfolio

v3.2 aporta algo importante al proyecto como portfolio.

Ya no muestra únicamente:

```text
sé escribir funciones Python
```

También empieza a demostrar:

```text
sé probar código

sé detectar regresiones

sé trabajar con filesystem temporal

sé simular dependencias

sé interpretar excepciones

sé utilizar análisis estático

sé revisar warnings

sé documentar decisiones

sé refactorizar con una red de seguridad

sé mantener Git limpio
```

En un repositorio profesional, estos aspectos tienen mucho valor porque muestran preocupación por:

- mantenibilidad;
- reproducibilidad;
- calidad;
- robustez;
- trazabilidad.

---

## 80. Conclusión de v3.2

FileOrganizer v3.2 no es principalmente una versión de nuevas funciones visibles.

Es una versión de:

```text
madurez técnica
```

Durante esta etapa el proyecto incorpora una base formada por:

```text
                  FileOrganizer
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
       pytest         Ruff         Git
          │            │            │
          ▼            ▼            ▼
   comportamiento   calidad     trazabilidad
          │            │            │
          └────────────┼────────────┘
                       │
                       ▼
                  desarrollo
                 más controlado
```

Los principales resultados son:

```text
101 tests automatizados
20 archivos de test
0 avisos Ruff
refactor parcial de organizador.py
mejor manejo de excepciones
fechas revisadas
entorno de desarrollo reproducible
.gitignore reforzado
documentación ampliada
```

Pero el resultado más importante es metodológico:

> Las siguientes versiones de FileOrganizer ya no parten únicamente de código funcional.

Parten de:

```text
código
+
tests
+
análisis estático
+
Git
+
documentación
```

Esto hace posible continuar ampliando el proyecto con una base mucho más sólida frente a regresiones.

---

## 81. Punto de partida para la siguiente etapa

Después de cerrar v3.2, FileOrganizer queda preparado para continuar creciendo sobre una base validada.

Las próximas funcionalidades podrán desarrollarse siguiendo el ciclo aprendido:

```text
DISEÑAR
   │
   ▼
IMPLEMENTAR
   │
   ▼
PROBAR
   │
   ▼
ANALIZAR
   │
   ▼
REFACTORIZAR
   │
   ▼
DOCUMENTAR
   │
   ▼
VERSIONAR
```

A partir de este momento, añadir una nueva funcionalidad debería implicar también preguntarse:

```text
¿Qué tests necesita?

¿Qué casos negativos existen?

¿Qué casos límite existen?

¿Qué errores pueden aparecer?

¿Cómo sabré dentro de seis meses
que esta función sigue funcionando?
```

Esa pregunta resume una de las principales enseñanzas de FileOrganizer v3.2.