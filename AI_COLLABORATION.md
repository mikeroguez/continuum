# Protocolo de colaboración con IA (Continuum)

Fuente única de verdad del flujo de trabajo con asistentes de IA en este
repositorio, parte del sistema Continuum. `AGENTS.md`,
`CLAUDE.md` y `GEMINI.md` son entrypoints delgados
que remiten aquí — **si cambia una regla común, edita primero este archivo y
después los tres entrypoints.** No dupliques reglas: un entrypoint con reglas
propias divergentes de este documento es un bug de proceso.

Este archivo contiene el mínimo operativo que una sesión debe aplicar. La
explicación, ejemplos y rutas para personas viven en
[`template/docs/guia-para-agentes.md`](template/docs/guia-para-agentes.md) y
[`template/docs/como-usar-continuum.md`](template/docs/como-usar-continuum.md).
No conviertas este protocolo en una enciclopedia: mueve el detalle estable a
documentación indexada y léelo bajo demanda.

> Principio rector: **el repositorio es la memoria; la conversación es solo
> el canal de ejecución.** Cualquier decisión, hallazgo o estado que importe
> mañana se escribe en un archivo versionado — nunca queda solo en el chat.

## 0. Lo primero que debe leer cualquier sesión nueva

En este orden, y nada más hasta no tener claro el alcance de la tarea:

1. `.ai/HANDOFF.md` — qué dejó pendiente la sesión anterior (de cualquier proveedor o persona).
2. `.ai/state/estado-dev.md` — **índice corto**, no el detalle (§5).
3. Solo los temas de `.ai/state/topics/` que el índice señale como relevantes a la tarea.
4. Si hay una tarea abierta relevante: `.ai/tasks/<slug>/task.md`.

No leas más que eso para empezar. El resto se explora bajo demanda (§3).

## 1. Compatibilidad multi-proveedor

| Proveedor | Entrypoint  | Config propia                    |
|-----------|-------------|-----------------------------------|
| Claude Code | `CLAUDE.md` | `.claude/settings.json` (permisos, hooks) |
| Codex / genérico | `AGENTS.md` | — (Codex usa `AGENTS.md` de forma nativa) |
| Gemini CLI  | `GEMINI.md` | `.gemini/settings.json` si aplica |
| GitHub Copilot | `.github/copilot-instructions.md` + `AGENTS.md` | Configuración de instrucciones y agentes de GitHub |

`continuum doctor` valida que cada entrypoint exista, esté trackeado en git y
referencie este archivo. Un directorio de proveedor vacío o sin trackear es
soporte simbólico, no real — no lo dejes así.

## 2. Ciclo de vida de una tarea

No toda tarea necesita una carpeta propia — la ceremonia excesiva es la razón
por la que estos sistemas se abandonan. Usa el tamaño para decidir:

| Tamaño   | Cuándo aplica                          | Qué se exige |
|----------|------------------------------------------|--------------|
| small    | 1-3 archivos, sin ambigüedad de alcance | Solo actualizar `.ai/HANDOFF.md` al terminar (puede ser un párrafo) |
| medium   | 1 módulo/dominio, o >3 archivos         | `continuum task start <slug> --size medium`; cerrar con `continuum task close <slug>` |
| large    | Cruza dominios, o es ambigua/riesgosa    | Igual que medium + `execution-plan.md` como cola de pasos + considerar dividir en subtareas |

```bash
tools/continuum task start pagos-recurrentes --size medium --owner ana
tools/continuum task claim pagos-recurrentes ana       # visibilidad si trabaja más de una persona
tools/continuum task close pagos-recurrentes           # exige handoff.md completo, archiva la carpeta
```

Nunca renumerar ni reutilizar identificadores de requisitos/tareas ya usados
(RF-###, PA-##, slugs de tarea) aunque se hayan cerrado o descartado.

## 3. Contexto mínimo suficiente (eficiencia de tokens)

- Localiza antes de leer: `rg`/`grep` para encontrar, no explorar carpetas completas "por si acaso".
- Lee índices/encabezados antes que archivos completos cuando el archivo lo permita.
- Usa primero las herramientas nativas de lectura por rango/`grep` de tu
  cliente para archivos grandes. `tools/continuum packetize` (chunking estático
  a Markdown) es **último recurso** — solo para pasarle contenido a un
  sub-proceso o modelo sin acceso a herramientas de archivo. Si tu cliente ya
  puede leer por offset/límite y grepear, trocear a mano no aporta nada y es
  trabajo de más.
- Solo abre un archivo de `.ai/state/topics/` si la tarea lo necesita — el
  índice (`estado-dev.md`) existe justamente para decidir eso sin tener que
  abrirlos todos.
- Si tu cliente soporta prompt caching (Claude vía API/Claude Code lo aplica
  solo si el prefijo del contexto es idéntico entre turnos): **no edites**
  este archivo, los entrypoints ni el índice a media tarea si lo puedes
  evitar — cualquier cambio en ese bloque invalida el caché para el resto de
  la sesión. Todo lo estable va primero, lo variable (diffs, resultados de
  comandos) al final.
- `tools/continuum doctor` reporta el costo estimado en tokens del "paquete de
  arranque" (entrypoints + índice + handoff — los temas NO cuentan porque se
  cargan bajo demanda). Si supera ~8k tokens con el índice acotado, el
  problema casi siempre es contenido inferible en un entrypoint (§3.1), no
  que "haga falta compactar".

### 3.1 Contenido inferible: fuera del arranque

La evidencia sobre archivos de contexto no es concluyente y depende de la
tarea. Sí coincide en un riesgo: repetir README, configuración o código ocupa
contexto que el agente puede localizar por sí mismo. En el arranque conserva
solo información **no inferible** —comandos no obvios, versiones mínimas,
decisiones con alternativa rechazada o riesgos— y mueve el resto a fuentes
indexadas bajo demanda. Si dudas, prioriza localizar antes de cargar.

## 4. Handoff — continuidad entre sesiones, proveedores y personas

`.ai/HANDOFF.md` es el buzón único y siempre vigente. Reglas:

- **Actualízalo antes de cortar la sesión**, no solo al terminar limpio — si
  notas que el contexto/tokens se están agotando a medio camino, escribe el
  handoff YA con lo que tengas, aunque esté incompleto. Un handoff parcial
  vale más que ninguno.
- Si el cliente lo soporta, automatiza esto con un hook (ver
  `.claude/settings.json` de ejemplo) que llame `tools/continuum handoff --auto`
  al recibir la señal de fin de sesión o de compactación de contexto — no
  dependas solo de que la IA se acuerde.
- Formato: objetivo, archivos revisados/modificados, decisión(es) tomada(s),
  suposiciones vigentes, validación ejecutada/pendiente, riesgos, siguiente
  paso recomendado (plantilla en `.ai/templates/HANDOFF.md`).
- Al cerrar una tarea formal, su `handoff.md` es más detallado que el buzón
  general; el buzón general puede resumir "ver `.ai/tasks/_closed/<slug>/handoff.md`".

## 5. Memoria viva: índice + temas, no un snapshot que crece

`estado-dev.md` es un **índice corto** (≤80 líneas) — lista qué temas
existen en `.ai/state/topics/*.md` y una línea de cuándo abrir cada uno. El
detalle vive en los temas, no en el índice. Este es el mismo patrón que usa
nativamente Claude Code (`MEMORY.md` + archivos por tema, ver
`docs/investigacion-2026.md` §1) — no es una convención nuestra aislada.

- Actualiza el tema que corresponda (`arquitectura.md`, `decisiones.md`,
  `pendientes.md`, etc.), no el índice, salvo que estés agregando o quitando
  un tema completo.
- Si un tema acumula entradas fechadas (bitácora de cambios), archívalas con
  `tools/continuum compact --topic <nombre>` — quedan en `.ai/state/archive/`.
- Si un proyecto todavía tiene el `estado-dev.md` monolítico del formato
  anterior (todo en un solo archivo), migra una vez con
  `tools/continuum memory-split-legacy` y revisa el resultado a mano.
- Decisiones de arquitectura con peso propio van a un ADR en
  `docs/architecture/ADR-XXXX-*.md` (plantilla en `.ai/templates/ADR.md`),
  no a un tema.

## 6. Trabajo en equipo (múltiples personas)

- **Aislamiento por tarea**: Cada desarrollador o sesión trabaja en su subcarpeta `.ai/tasks/<slug>/`. Al estar aisladas por slug, los merges entre ramas de Git no producen conflictos en los archivos de tarea.
- **Visibilidad y ownership**: `continuum task claim <slug> <owner>` marca quién está trabajando en una tarea para dar visibilidad al resto del equipo en `continuum status` o `continuum task list`.
- **Manejo de `HANDOFF.md` en merges**: `.ai/HANDOFF.md` representa la continuidad de la rama actual. En Pull Requests o merges a `main`, si ocurre un conflicto en `HANDOFF.md`, la regla es aceptar la versión de la rama principal o regenerarla inmediatamente ejecutando `tools/continuum handoff --auto`.
- **Cierre de tarea en PR**: Antes de hacer merge, la tarea se cierra con `continuum task close <slug>`, lo que traslada la carpeta a `.ai/tasks/_closed/<slug>/` para preservar la evidencia de pruebas en el historial de Git sin colisionar con las tareas activas de otros.
- **Prefijo de commit**: Usar el slug de la tarea cuando exista: `[pagos-recurrentes] feat: agrega validación de monto mínimo` para facilitar búsquedas con `git log --grep`.
- **Concurrencia local (`git worktree`)**: Si dos personas o agentes trabajan localmente al mismo tiempo en el mismo repo, usar `git worktree add ../repo-<slug> <branch>` para aislar los directorios de trabajo en disco.

## 7. Convención de commits

Conventional Commits en inglés para el tipo (`feat|fix|docs|refactor|test|chore|perf|ci`),
mensaje en el idioma del equipo. Ejemplo: `feat: add recurring payment validation`.

## 8. Verificación automática

`tools/continuum doctor` corre como git hook de pre-commit (instalado con
`tools/continuum install-hooks`) y valida: archivo canónico presente, entrypoints
consistentes, sin duplicados divergentes, tamaño y frescura del índice y de
cada tema, tareas abandonadas, y costo en tokens del arranque. Es una
advertencia, no un bloqueo duro — usa `git commit --no-verify` conscientemente
si el caso lo amerita.

## 9. Roles: catálogo de expertos

Un rol es una lente de trabajo, no un agente concurrente. Los roles viven en
`.ai/roles/<pack>/`, se activan por packs en `.ai/config.json` y se consultan
bajo demanda; ver la guía para agentes para la explicación completa.

```bash
tools/continuum roles list                    # roles disponibles en los packs activos
tools/continuum task start <slug> --role backend
tools/continuum handoff --role backend --provider claude
tools/continuum roles sync                    # genera subagentes de Claude Code (.claude/agents/)
```
