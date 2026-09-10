# Cómo usar Continuum

Continuum conserva contexto útil entre sesiones, personas y asistentes de IA.
No sustituye Git, las pruebas ni las decisiones humanas.

Para la conducta de un asistente consulta la [guía para agentes](guia-para-agentes.md).

## Las piezas principales

| Pieza | Propósito | Cuándo verla |
| --- | --- | --- |
| `AI_COLLABORATION.md` | Reglas operativas compartidas | Al trabajar con un agente |
| `.ai/HANDOFF.md` | Qué dejó la sesión anterior | Al retomar |
| `.ai/state/estado-dev.md` | Índice corto del proyecto | Al retomar |
| `.ai/state/topics/` | Detalle por tema | Solo si hace falta |

El repositorio es la memoria compartida; la conversación es el canal de ejecución.

## Primer uso

Después de instalar Continuum, completa la configuración propia del proyecto y ejecuta:

```bash
tools/continuum install-hooks
tools/continuum doctor
```

`doctor` revisa protocolo, entrypoints, memoria y tareas. Resuelve problemas críticos antes de depender del sistema para cambios importantes.

## Flujo diario

### Retomar el trabajo

```bash
tools/continuum session start
tools/continuum status
```

Si retomas una tarea registrada:

```bash
tools/continuum context --task mi-tarea --why
```

No leas toda `.ai/` por defecto. El índice y `context` indican qué información es pertinente.

### Elegir el nivel de estructura

| Alcance | Qué hacer |
| --- | --- |
| Cambio pequeño y claro | Trabaja directo y deja un handoff. |
| Un módulo o varios archivos | Crea una tarea `medium`. |
| Varios dominios, riesgo o ambigüedad | Crea una tarea `large` y usa su plan. |

```bash
tools/continuum task start mi-tarea --size medium
tools/continuum task claim mi-tarea ana
```

El `claim` da visibilidad; no bloquea archivos ni sustituye la coordinación humana.

### Trabajar, validar y cerrar

Usa las herramientas habituales del proyecto para editar y probar. Antes de terminar, ejecuta las validaciones relevantes y deja continuidad:

```bash
tools/continuum handoff --message "qué se hizo y qué sigue"
tools/continuum task close mi-tarea
```

El segundo comando aplica a tareas formales. Revisa cualquier handoff generado automáticamente y completa decisiones, validaciones, riesgos y siguiente paso.

## Comandos frecuentes

| Comando | Uso |
| --- | --- |
| `status` | Estado y siguiente acción sugerida. |
| `doctor` | Estructura, frescura y contexto. |
| `context --why` | Qué leer y por qué. |
| `tokens` | Costo estimado del contexto. |
| `task current` | Retomar trabajo abierto. |
| `metrics report` | Señales locales, no evidencia científica. |

Ejecuta `tools/continuum --help` para el catálogo completo. Revisa siempre la salida de comandos que escriben, sincronizan, publican o cambian configuración.

## Adopción gradual

1. Empieza con `HANDOFF.md` e `estado-dev.md`.
2. Añade tareas cuando el alcance o la colaboración lo ameriten.
3. Activa roles solo si una tarea necesita una perspectiva especializada.
4. Mide solo ante una pregunta concreta; las métricas no evalúan personas ni prueban eficacia por sí solas.

## Equipo de desarrollo: casos de uso y prompts

Continuum sirve para que el contexto sobreviva al cambio de persona, sesión o
asistente. No sustituye la conversación del equipo ni la revisión de código:
deja visible qué se acordó, qué cambió y qué falta validar.

| Situación | Uso recomendado |
| --- | --- |
| Una persona inicia una función y un agente la implementa | Crea una tarea si el alcance es `medium` o `large`, declara el objetivo y pide al agente que lea el contexto pertinente antes de editar. |
| Otro agente o desarrollador retoma trabajo parcial | Consulta `session start`, el handoff y la tarea; el nuevo responsable confirma qué entiende antes de continuar. |
| Dos cambios avanzan a la vez | Separa ramas o worktrees y tareas por `slug`; un `claim` informa ownership, pero el equipo sigue coordinando los límites. |
| Un agente revisa una contribución | Pídele revisar el diff, las pruebas y los riesgos de su alcance; no le des por aprobada una publicación o un merge. |
| Se termina una sesión o una tarea | Registra decisiones, validación y siguiente paso en el handoff; cierra la tarea formal cuando esté lista. |

### Cómo escribir prompts útiles

Un prompt no necesita repetir el protocolo. Indica el resultado esperado, los
límites y la autorización; pide al agente consultar el repositorio para los
detalles. Sustituye lo que está entre `<…>` y elimina lo que no aplique.

**Iniciar una tarea de desarrollo**

```text
Trabaja en <objetivo>. Antes de editar, lee el protocolo, el handoff y el
contexto pertinente del repositorio. Confirma si el alcance requiere una tarea
formal. Mantente dentro de <límites>. Ejecuta las validaciones relevantes y
deja un handoff claro. No hagas commit, merge ni publicación sin mi aprobación.
```

**Retomar después de una interrupción o con otro asistente**

```text
Retoma la tarea <slug>. Lee primero el handoff, task.md y el contexto que
indiquen. Resume el estado, las decisiones y lo pendiente antes de modificar
archivos. Conserva el alcance; si falta una decisión o autorización, detente y
pregunta. Al terminar, actualiza el handoff con pruebas y siguiente paso.
```

**Trabajo paralelo en un equipo**

```text
Eres responsable de <slug> dentro de <objetivo mayor>. Revisa ownership,
límites y cambios existentes antes de editar. Trabaja solo en <áreas o
archivos>; no sobrescribas el trabajo de otras tareas. Usa una rama o worktree
aislado si corresponde. Reporta dependencias, validación y riesgos en el
handoff.
```

**Revisión o pruebas por un agente**

```text
Revisa <cambio o tarea> sin modificarlo salvo que lo autorice después. Lee el
protocolo y el handoff relevantes; inspecciona el diff y ejecuta las pruebas
proporcionales. Devuelve hallazgos concretos, riesgos y pruebas faltantes. No
apruebes ni publiques cambios por mí.
```

Los prompts funcionan mejor cuando nombran una tarea o resultado verificable.
Evita pegar historiales completos de chat, secretos, datos personales o
instrucciones contradictorias: el repositorio y sus handoffs son la fuente de
continuidad.

## Seguridad y equipo

Usa ramas y worktrees para trabajo simultáneo. No escribas secretos, datos personales, rutas locales, prompts sensibles ni información de terceros en handoffs, tareas o métricas versionadas. Si el proceso se vuelve ceremonioso, reduce la estructura de la tarea, pero conserva una nota útil para quien la retome.
