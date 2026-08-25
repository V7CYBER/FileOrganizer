# FileOrganizer v3.4 — Auditoría de Seguridad

## 1. Introducción

La versión **v3.4** de FileOrganizer introduce un sistema unificado de auditoría de seguridad.

Hasta v3.3, el proyecto disponía de distintos mecanismos defensivos desarrollados progresivamente:

- verificación de archivos;
- detección de archivos sospechosos;
- análisis mediante magic numbers;
- clasificación de archivos no verificados;
- cuarentena;
- análisis defensivo de logs;
- File Integrity Monitoring (FIM);
- snapshots;
- baselines;
- detección de modificaciones, archivos nuevos y eliminados.

Estas funcionalidades existían como componentes independientes.

El objetivo principal de v3.4 ha sido comenzar a **correlacionar información procedente de distintos mecanismos de seguridad** para obtener una visión conjunta del estado de una carpeta.

---

# 2. Objetivo de v3.4

El objetivo principal puede representarse como:

```text
Seguridad de archivos
        +
Integridad de archivos
        │
        ▼
Auditoría unificada
        │
        ▼
Nivel de seguridad
        │
        ▼
Informe
```

La versión debía ser capaz de:

1. analizar los archivos de una carpeta;
2. obtener su estado de seguridad;
3. cargar una baseline de integridad;
4. generar un snapshot actual;
5. comparar ambos estados;
6. resumir los resultados;
7. determinar un nivel de auditoría;
8. generar un informe;
9. guardar el informe sin sobrescribir otros existentes;
10. ejecutar todo el proceso desde el menú principal.

---

# 3. Nuevo módulo `core/auditoria.py`

Para mantener la separación de responsabilidades se creó:

```text
core/auditoria.py
```

Este módulo actúa como capa de coordinación entre funcionalidades que ya existían en otros módulos.

La auditoría reutiliza principalmente componentes procedentes de:

```text
core/seguridad.py
core/integridad.py
```

La idea arquitectónica es importante:

```text
auditoria.py
```

no debe volver a implementar el sistema de magic numbers ni el FIM.

Su responsabilidad consiste en **coordinar sus resultados**.

Esto reduce duplicación de código y permite reutilizar componentes previamente probados.

---

# 4. Arquitectura de la auditoría

El flujo final desarrollado en v3.4 puede representarse así:

```text
             ejecutar_auditoria()
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
                     │
                     ▼
                 resultado
```

Posteriormente la interfaz puede guardar el informe mediante:

```text
guardar_informe_auditoria()
```

---

# 5. Resumen de seguridad

El primer componente de la auditoría procede del sistema de seguridad de archivos.

Los resultados se resumen mediante tres estados:

```text
ok
sospechosos
no_verificados
```

Conceptualmente:

```python
{
    "ok": ...,
    "sospechosos": ...,
    "no_verificados": ...,
}
```

Estos valores permiten conocer cuántos archivos han sido reconocidos correctamente, cuántos presentan discrepancias de seguridad y cuántos no pueden verificarse mediante los mecanismos disponibles.

---

# 6. Resumen de integridad

El segundo componente procede del File Integrity Monitoring desarrollado en v3.3.

La comparación de integridad proporciona cuatro estados:

```text
sin_cambios
modificados
nuevos
eliminados
```

La auditoría transforma los resultados del FIM en cantidades que pueden combinarse con el resumen de seguridad.

Conceptualmente:

```python
{
    "sin_cambios": ...,
    "modificados": ...,
    "nuevos": ...,
    "eliminados": ...,
}
```

---

# 7. `generar_resumen_auditoria()`

Esta función combina los dos bloques anteriores.

El resultado tiene una estructura similar a:

```python
{
    "seguridad": {
        "ok": 8,
        "sospechosos": 0,
        "no_verificados": 0,
    },
    "integridad": {
        "sin_cambios": 8,
        "modificados": 0,
        "nuevos": 0,
        "eliminados": 0,
    },
}
```

Esta estructura separa claramente:

```text
seguridad
integridad
```

pero permite que ambos componentes sean evaluados conjuntamente.

---

# 8. Niveles de auditoría

v3.4 introduce tres niveles:

```text
OK
ADVERTENCIA
ALERTA
```

La función responsable es:

```text
determinar_nivel_auditoria()
```

---

# 9. Nivel `OK`

El nivel:

```text
OK
```

representa el escenario sin incidencias relevantes detectadas por las reglas actuales.

Durante el desarrollo se creó primero un test específico para establecer este contrato.

Esto permitió comenzar la función con el comportamiento mínimo necesario antes de introducir niveles adicionales.

---

# 10. Nivel `ADVERTENCIA`

El nivel:

```text
ADVERTENCIA
```

se utiliza cuando existe una situación que requiere revisión pero no se ha detectado un archivo clasificado como sospechoso.

Entre los casos desarrollados se encuentran:

```text
archivos modificados
archivos nuevos
archivos eliminados
archivos no verificados
```

Por ejemplo:

```text
Modificados: 1
```

provoca:

```text
ADVERTENCIA
```

También:

```text
No verificados: 1
```

provoca:

```text
ADVERTENCIA
```

---

# 11. Nivel `ALERTA`

El nivel:

```text
ALERTA
```

representa la situación de mayor severidad implementada en v3.4.

Se utiliza cuando existen archivos clasificados como:

```text
sospechosos
```

Ejemplo:

```python
"seguridad": {
    "ok": 7,
    "sospechosos": 1,
    "no_verificados": 0,
}
```

produce:

```text
ALERTA
```

---

# 12. Prioridad de `ALERTA`

Durante el desarrollo se añadió un test específico para comprobar la prioridad de niveles.

La regla es:

```text
ALERTA > ADVERTENCIA > OK
```

Por tanto, si una auditoría presenta simultáneamente:

```text
archivo sospechoso
+
archivo modificado
```

el resultado no debe ser:

```text
ADVERTENCIA
```

sino:

```text
ALERTA
```

Este test protege una regla de negocio importante y evita que una condición menos severa oculte una incidencia de mayor prioridad.

---

# 13. Generación del informe

Se implementó:

```text
generar_informe_auditoria()
```

Su responsabilidad consiste en convertir el resultado estructurado de la auditoría en información legible.

El informe incluye:

```text
Nivel
OK
Sospechosos
No verificados
Sin cambios
Modificados
Nuevos
Eliminados
```

Ejemplo:

```text
===== AUDITORÍA DE SEGURIDAD =====
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

---

# 14. Persistencia de informes

Se implementó:

```text
guardar_informe_auditoria()
```

La función recibe:

```text
contenido del informe
ruta de destino
```

y crea el archivo correspondiente.

Además, crea automáticamente el directorio necesario cuando todavía no existe.

---

# 15. Prevención de sobrescrituras

Un informe de seguridad constituye información histórica.

Sobrescribir automáticamente un informe anterior provocaría pérdida de información.

Por este motivo se desarrolló mediante TDD un mecanismo de prevención de sobrescrituras.

Si existe:

```text
auditoria.txt
```

la siguiente ejecución puede generar:

```text
auditoria_1.txt
```

Después:

```text
auditoria_2.txt
```

y así sucesivamente.

Se añadió además una prueba específica para múltiples colisiones, evitando que la solución funcionara únicamente para una segunda ejecución.

---

# 16. `ejecutar_auditoria()`

La función:

```text
ejecutar_auditoria()
```

constituye el orquestador principal del nuevo sistema.

Su responsabilidad consiste en conectar los distintos componentes.

Conceptualmente:

```text
cargar baseline
      │
      ▼
validar rutas
      │
      ▼
analizar seguridad
      │
      ▼
generar snapshot actual
      │
      ▼
comparar integridad
      │
      ▼
crear resumen
      │
      ▼
determinar nivel
      │
      ▼
crear informe
      │
      ▼
devolver resultado
```

El resultado incluye:

```text
resumen
nivel
informe
```

Esto permite mantener separada la lógica del núcleo de la presentación utilizada por `organizador.py`.

---

# 17. Reutilización de la ruta de la baseline

Una baseline FIM almacena:

```text
ruta_base
```

Esta ruta identifica la carpeta cuyo estado fue registrado.

La generación del nuevo snapshot utiliza esta información para saber qué ubicación debe compararse con el estado de referencia.

Durante v3.4 se creó un test específico para comprobar este comportamiento.

---

# 18. Problema detectado durante la prueba manual

Durante la prueba end-to-end apareció una situación importante.

Se creó una nueva baseline y el sistema evitó sobrescribir otra existente:

```text
baselines/baseline_1.json
```

Sin embargo, al introducir accidentalmente:

```text
baselines/baseline.json
```

se cargó una baseline anterior cuya `ruta_base` apuntaba a:

```text
/tmp/fileorganizer_fim_final
```

La auditoría respondió:

```text
No existe la ruta: /tmp/fileorganizer_fim_final
```

El comportamiento era técnicamente correcto, pero permitió identificar una posible inconsistencia arquitectónica.

---

# 19. Coherencia entre carpeta y baseline

`ejecutar_auditoria()` recibe una carpeta para realizar el análisis de seguridad.

Al mismo tiempo, la baseline contiene su propia:

```text
ruta_base
```

Sin una validación adicional era técnicamente posible utilizar:

```text
Seguridad → carpeta A
Integridad → carpeta B
```

Esto produciría una auditoría conceptualmente incoherente.

---

# 20. Nuevo contrato de rutas

Se añadió una regla explícita:

```text
carpeta solicitada == baseline["ruta_base"]
```

Si ambas rutas no coinciden:

```text
ValueError
```

El flujo pasa a ser:

```text
cargar baseline
      │
      ▼
normalizar rutas
      │
      ▼
¿coinciden?
 ├── NO ──► ValueError
 │
 └── SÍ
      │
      ▼
continuar auditoría
```

---

# 21. Normalización mediante `Path.resolve()`

La comparación no se realiza únicamente mediante strings.

Se utilizan objetos `Path` y:

```python
Path(...).resolve()
```

Esto permite comparar rutas normalizadas.

La decisión refuerza la coherencia del sistema y reutiliza conocimientos de `pathlib` empleados en versiones anteriores.

---

# 22. Evolución de un contrato antiguo

La introducción de la validación de rutas provocó el fallo de un test anterior:

```text
test_ejecutar_auditoria_usa_ruta_base_de_baseline
```

El test antiguo utilizaba deliberadamente:

```text
carpeta de seguridad != ruta_base de baseline
```

porque su único objetivo original era comprobar qué ruta recibía `generar_snapshot()`.

Con el nuevo contrato, esa situación ya no era válida.

En lugar de eliminar la nueva protección para mantener artificialmente el test antiguo, se actualizó el test para utilizar rutas coherentes.

Finalmente quedaron protegidos dos comportamientos complementarios:

```text
rutas iguales
→ continuar
→ utilizar ruta_base de baseline

rutas distintas
→ ValueError
```

Este caso muestra que una batería de tests también debe evolucionar cuando cambia de forma deliberada el contrato del software.

---

# 23. Integración en `organizador.py`

Se añadió una nueva función de interfaz:

```text
mostrar_auditoria_seguridad()
```

Su responsabilidad consiste en conectar al usuario con el motor de auditoría.

El flujo es:

```text
usuario
   │
   ▼
carpeta a auditar
   │
   ▼
ruta baseline
   │
   ▼
ejecutar_auditoria()
   │
   ▼
mostrar informe
   │
   ▼
guardar informe
```

---

# 24. Manejo de errores en la interfaz

Durante el ciclo TDD se comprobó que un:

```text
FileNotFoundError
```

procedente del motor podía propagarse hasta terminar la ejecución.

Se añadió manejo controlado de errores en la capa de interfaz.

Durante esta modificación apareció también un:

```text
IndentationError
```

al introducir el bloque `try`.

El error fue detectado inmediatamente durante la colección de pytest.

Antes de repetir los tests se utilizó:

```bash
python3 -m py_compile organizador.py
```

para validar la sintaxis.

Este incidente reforzó el uso de compilación explícita como comprobación rápida después de cambios estructurales.

---

# 25. Integración en el menú principal

La versión mostrada por el programa pasó a ser:

```text
FILE ORGANIZER v3.4
```

y se añadió:

```text
11) Ejecutar auditoría de seguridad
12) Salir
```

El menú final queda:

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

---

# 26. Tests de integración de la interfaz

Se creó:

```text
test/test_organizador_auditoria.py
```

Los tests verifican:

- presentación del resultado;
- manejo de errores;
- almacenamiento del informe;
- existencia de la nueva opción del menú;
- ejecución de la auditoría desde el menú.

Se utilizaron técnicas ya introducidas anteriormente:

```text
monkeypatch
capsys
```

Esto permite probar una interfaz basada en `input()` y `print()` sin intervención manual.

---

# 27. Desarrollo mediante TDD

v3.4 continuó la metodología introducida y consolidada en versiones anteriores:

```text
RED
 ↓
GREEN
 ↓
validación
 ↓
nuevo requisito
```

Entre los ciclos desarrollados estuvieron:

```text
generar resumen
nivel OK
nivel ADVERTENCIA
nivel ALERTA
prioridad ALERTA
archivos no verificados
generar informe
informe completo
guardar informe
evitar sobrescritura
múltiples colisiones
ejecutar auditoría real
usar ruta base
incluir informe
integración con interfaz
manejo de errores
guardar informe desde UI
opción de menú
ejecución desde menú
coherencia de rutas
```

---

# 28. Importancia del RED

Los fallos iniciales no se consideraron errores accidentales del proceso.

Cada RED demostraba que el test era capaz de detectar la ausencia del comportamiento requerido.

Ejemplos observados durante v3.4:

```text
ImportError
AssertionError
FileNotFoundError
IndentationError
```

Cada uno permitió avanzar hacia un contrato más preciso.

---

# 29. Prueba manual end-to-end

Una vez superados los tests automatizados se realizó una prueba con archivos reales.

Se creó:

```text
/tmp/fileorganizer_v34/vigilada
```

con dos archivos:

```text
documento.txt
notas.txt
```

Después se creó una baseline desde el menú.

La baseline registró:

```text
Archivos registrados: 2
```

---

# 30. Primera auditoría real

Sin modificar los archivos se ejecutó la auditoría.

Resultado:

```text
===== AUDITORÍA DE SEGURIDAD =====
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

El nivel fue:

```text
ADVERTENCIA
```

porque los dos archivos `.txt` quedaron clasificados como no verificados por los mecanismos de seguridad disponibles.

El FIM confirmó correctamente:

```text
Sin cambios: 2
```

---

# 31. Segunda auditoría real

Se modificó deliberadamente:

```text
documento.txt
```

sin actualizar la baseline.

La nueva auditoría produjo:

```text
===== AUDITORÍA DE SEGURIDAD =====
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

El sistema detectó correctamente la modificación.

Esto confirmó el funcionamiento conjunto de:

```text
interfaz
seguridad
baseline
snapshot
SHA-256
comparación
resumen
nivel
informe
persistencia
```

---

# 32. Informes reales generados

Durante la prueba manual también se confirmó la prevención de sobrescrituras.

Se generaron, entre otros:

```text
reports/auditoria_6.txt
reports/auditoria_7.txt
```

Esto demostró que el comportamiento probado mediante tests funcionaba también en una ejecución real.

---

# 33. Testing final

Los tests específicos del motor de auditoría finalizaron con:

```text
15 passed
```

Los tests específicos de integración de la interfaz finalizaron con:

```text
5 passed
```

La batería completa del proyecto alcanzó:

```text
151 passed
```

---

# 34. Ruff

El análisis estático completo se ejecutó mediante:

```bash
python -m ruff check .
```

Resultado:

```text
All checks passed!
```

Durante el desarrollo Ruff detectó, entre otras cosas, bloques de imports que necesitaban reorganización.

Esto permitió mantener consistencia en el código antes de crear los checkpoints.

---

# 35. Compilación

También se comprobó:

```bash
python3 -m py_compile core/*.py organizador.py
```

sin errores.

La compilación explícita fue especialmente útil después del `IndentationError` detectado durante la integración de la interfaz.

---

# 36. Validación Git

Antes de los commits se utilizó:

```bash
git diff --check
```

y posteriormente:

```bash
git diff --cached --check
```

para detectar posibles problemas formales antes de registrar los cambios.

---

# 37. Commits principales de v3.4

Durante el desarrollo se crearon checkpoints independientes.

Entre los principales commits se encuentran:

```text
a7dc0ba  v3.4: inicia auditoria de seguridad
801cdd1  v3.4: añade informes de auditoria de seguridad
9611ca7  v3.4: integra auditoria real de seguridad e integridad
9bf880d  v3.4: integra auditoria de seguridad en el menu
af899f5  v3.4: valida coherencia de rutas en auditoria
```

Esta estrategia permite disponer de puntos de recuperación pequeños y comprensibles.

---

# 38. Competencias trabajadas

v3.4 permitió trabajar de forma práctica:

- diseño modular;
- reutilización de componentes;
- separación entre lógica y presentación;
- orquestación de módulos;
- correlación de información de seguridad;
- diseño de niveles de severidad;
- prioridad de reglas;
- estructuras de datos anidadas;
- generación de informes;
- persistencia segura;
- prevención de sobrescrituras;
- manejo de colisiones de nombres;
- `pathlib`;
- `Path.resolve()`;
- validación de contratos;
- `ValueError`;
- `FileNotFoundError`;
- manejo de errores en interfaces;
- TDD;
- ciclos RED/GREEN;
- evolución de tests ante cambios de contrato;
- mocks mediante `monkeypatch`;
- captura de salida mediante `capsys`;
- pruebas de integración;
- pruebas end-to-end;
- análisis estático con Ruff;
- validación mediante `py_compile`;
- control de versiones con Git.

---

# 39. Evolución del proyecto

La evolución reciente de FileOrganizer puede representarse como:

```text
v3.1
Seguridad de archivos
+ análisis defensivo de logs
        │
        ▼
v3.2
Testing + robustez + calidad
        │
        ▼
v3.3
File Integrity Monitoring
        │
        ▼
v3.4
Auditoría unificada
```

Cada versión reutiliza infraestructura creada anteriormente.

Esto evita desarrollar funcionalidades aisladas y permite que el proyecto evolucione progresivamente hacia una arquitectura defensiva más completa.

---

# 40. Resultado final

Con v3.4, FileOrganizer incorpora una capa de auditoría capaz de combinar:

```text
estado de seguridad
+
estado de integridad
```

para producir:

```text
resumen
+
nivel
+
informe
```

El flujo final puede resumirse como:

```text
                   CARPETA
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
   verificar_archivos()      BASELINE
          │                       │
          ▼                       ▼
 resumen_seguridad        snapshot_actual
          │                       │
          │                       ▼
          │              comparar_integridad()
          │                       │
          └───────────┬───────────┘
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

La versión finaliza con:

```text
15 tests de auditoría
5 tests de interfaz de auditoría
151 tests totales
Ruff limpio
Compilación correcta
git diff --check limpio
Prueba end-to-end correcta
```

v3.4 representa un nuevo paso en la transformación de FileOrganizer desde un organizador de archivos hacia un proyecto práctico de **Python aplicado a ciberseguridad defensiva**.
