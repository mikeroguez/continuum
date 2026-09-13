# Metodología de medición: ahorro real de tokens y tool-calls

`continuum doctor`/`continuum tokens` reportan una **estimación estática**
del costo de arranque (tokens de los archivos que toda sesión nueva debería
leer). Eso es visibilidad barata y siempre disponible, pero no es una
medición: no dice cuántos tokens o tool-calls gastó de verdad una sesión de
agente real al reanudar trabajo, ni si la respuesta que produjo fue
correcta. Esta guía describe cómo medir eso — inspirada en la metodología de
[`docs/MEASURING_SAVINGS.md`](https://github.com/DeusData/codebase-memory-mcp/blob/main/docs/MEASURING_SAVINGS.md)
de `codebase-memory-mcp`, adaptada al problema real de Continuum (ver
`docs/decision-log.md` ADR-012): continuidad de sesión, no exploración de
código.

Es un protocolo **opt-in** — no un paso obligatorio de ningún flujo de
Continuum (`ARCHITECTURE.md` §2, principio 2). Úsalo cuando quieras
cuantificar la adopción con datos, no como ceremonia de cada tarea.

No mezcles tres preguntas distintas:

1. ¿La sesión reanuda trabajo con el contexto correcto?
2. ¿Cuánto le cuesta en tokens/tool-calls llegar ahí?
3. ¿Ese costo es menor que sin Continuum?

Un ahorro de tokens no vale nada si la sesión reanuda con contexto
incorrecto — mide calidad y eficiencia por separado.

## El escenario que se mide

El evento que Continuum ataca (`ARCHITECTURE.md` §4) es la reanudación de
trabajo después de una discontinuidad: una sesión nueva, un cambio de
proveedor de IA, un cambio de persona, o una compactación de contexto a
media tarea. La medición tiene sentido en ese punto exacto — no al medir
una sesión completa de principio a fin sin ninguna discontinuidad real.

## Congelar el experimento

Ambas condiciones deben partir del mismo commit exacto y del mismo punto de
discontinuidad real (por ejemplo: el estado del repositorio justo antes de
retomar una tarea concreta que quedó a medias). Antes de medir, registra:

- el repositorio y el commit SHA exactos;
- la tarea concreta a reanudar y su alcance esperado (qué archivos toca, qué
  decisiones previas debe respetar);
- el modelo/proveedor de IA, su versión, y el presupuesto de tokens por
  intento;
- qué condición corre primero, y la política de "calentamiento" si aplica;
- el cliente o arnés de evaluación que va a capturar tokens y tool-calls —
  Continuum no puede medir el consumo real de un agente, solo estimar el
  tamaño de sus propios archivos.

Usa el mismo commit, la misma tarea y el mismo modelo para ambas
condiciones. La sesión de la segunda condición no debe ver las respuestas
ni los resultados de herramientas de la primera.

Define las dos condiciones sobre el mismo checkout limpio:

| Condición | Qué ve la sesión al arrancar |
|---|---|
| Con Continuum | El repositorio tal cual, con `.ai/HANDOFF.md`, `.ai/state/`, entrypoints y hooks activos |
| Baseline (sin Continuum) | El mismo repositorio, pero sin `.ai/`, sin entrypoints, sin hooks — la sesión debe reconstruir contexto con `git log`, lectura de código y, si existe, un sistema de tickets externo |

## 1. Medir calidad de la reanudación

Antes de medir eficiencia, define qué es "reanudar correctamente" para la
tarea elegida: qué decisiones previas no debe contradecir, qué archivos
debe identificar como relevantes, qué pasos pendientes debe reconocer. Usa
una rúbrica simple — CORRECTO / PARCIAL / INCORRECTO — evaluada contra la
evidencia real (el handoff que sí se escribió, los commits reales), no
contra qué tan convincente suena la respuesta. Registra la calidad de cada
condición por separado y consérvala junto con las métricas de eficiencia,
nunca mezclada en un solo número.

## 2. Medir ahorro de tokens y tool-calls

Corre ambas condiciones sobre el mismo punto de reanudación congelado. El
cliente o arnés de evaluación debe capturar el uso — Continuum no conoce el
consumo final de tokens de entrada/salida del modelo ni el total de
tool-calls de la sesión.

Define cada `run_id` como una repetición pareada. Cada `(run_id, condición)`
es una sesión aislada que reanuda la misma tarea. Captura una fila por cada
ventana de uso que el cliente mida directamente:

```text
run_id,condicion,repo_sha,tarea_id,ventana,tokens_entrada,tokens_salida,tokens_total,tool_calls,tiempo_ms,calidad
```

`tool_calls` cuenta toda invocación de herramienta dentro de esa ventana —
lecturas de archivo, `git log`, búsquedas, y cualquier comando de
`continuum` — no solo las relacionadas con Continuum. Ventanas candidatas:

- **Tokens de reanudación**: desde el inicio de la sesión hasta el primer
  punto en que la sesión tiene contexto suficiente para actuar
  correctamente (no hasta que termina la tarea completa).
- **Tokens de sesión completa**: la sesión aislada de principio a fin,
  incluyendo la tarea en sí — representa mejor el costo total real, pero
  mezcla el efecto de Continuum con la dificultad de la tarea.

Compara solo una ventana común entre ambas condiciones a la vez:

```text
reducción de tokens (%)     = 100 * (tokens_baseline - tokens_continuum) / tokens_baseline
reducción de tool-calls (%) = 100 * (calls_baseline  - calls_continuum)  / calls_baseline
```

Si el denominador es cero, la reducción correspondiente es N/A — no
inventes un pseudo-conteo. Publica los conteos pareados crudos junto con los
porcentajes, no solo el porcentaje.

## Checklist de reproducibilidad

- Commit exacto registrado; ambas condiciones parten del mismo checkout
  limpio y del mismo punto de discontinuidad real.
- Modelo, proveedor, presupuesto de tokens y orden de las condiciones
  congelados de antemano.
- La condición Baseline elimina `.ai/`, entrypoints y hooks — no solo los
  ignora de palabra.
- Calidad y eficiencia se reportan por separado, nunca combinadas en un
  solo número.
- Los conteos de tokens/tool-calls vienen directamente del cliente o arnés
  de evaluación, nunca de la estimación estática de `continuum doctor`.
- Se conservan los resultados crudos, incluyendo repeticiones fallidas.
- Ninguna afirmación generaliza más allá del repositorio, la tarea, el
  modelo y el número de repeticiones realmente medidos.

## Dónde correr esto primero

Los proyectos que ya tienen Continuum en uso activo en producción son el
terreno natural para la primera aplicación real de esta metodología — miden
adopción real, no un escenario sintético construido para la ocasión. Para
este repositorio en concreto, hay 4 proyectos dependientes ya en producción
candidatos (nombres omitidos por privacidad — ver el registro interno del
equipo). La aplicación piloto en sí queda fuera del alcance de
`docs/decision-log.md` ADR-012 — es trabajo de seguimiento.
