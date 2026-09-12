# Tarea: adopcion-ideas-cbm

**Creada:** 2026-09-12 · **Tamaño:** large · **Owner:** mike · **Rol:** (sin asignar)

## Objetivo
Adaptar a Continuum un subconjunto de ideas de ingeniería de contexto y
distribución observadas en el proyecto externo
[`codebase-memory-mcp`](https://github.com/DeusData/codebase-memory-mcp)
(CBM) — un motor de intelligence de código para agentes de IA, de dominio
muy distinto a Continuum (grafo de conocimiento de código vs. memoria de
sesión en Markdown) pero que resuelve el mismo problema de fondo: que un
agente arranque con el contexto correcto sin depender de que decida leerlo.
Cada cambio de protocolo/CLI se acompaña de su actualización de
documentación correspondiente — no se implementa nada "silencioso".

**Nota de proceso (2026-09-12):** antes de tocar código se hizo una
investigación dedicada, con el mismo rigor que `docs/investigacion-2026.md`
y el criterio de admisión de `ARCHITECTURE.md` §2 (no el marketing de CBM),
para decidir por ítem si implementar, ajustar o descartar. Resultado
completo en `docs/investigacion-2026.md` §10 y `docs/decision-log.md`
ADR-012. Las listas de abajo ya reflejan esa investigación, no la propuesta
original sin filtrar.

## Incluido en el alcance
- **[hecho]** Reconciliar el estado de `pendientes.md` sobre el rollout:
  confirmado por el owner que Continuum ya está en uso activo en los 4
  proyectos dependientes (`seguimiento-talleres`, `seguimiento-deportes`,
  `seguimiento-clubes`, `SISETAP`); distinguido de "aplicar
  `docs/rollout-guide.md` formalmente", que sigue pendiente y es un ítem
  aparte.
- **[hecho]** ADR-012 en `docs/decision-log.md` documentando qué se adopta,
  qué se ajusta y qué se descarta de CBM, con el razonamiento completo.
- **[hecho]** Sección 10 en `docs/investigacion-2026.md` analizando cada
  idea de CBM contra los principios de `ARCHITECTURE.md` §2 y el job central
  de Continuum, con la fuente citada explícitamente.
- `continuum context` (hook `SessionStart`): en vez de solo listar los
  archivos OBLIGATORIOS, volcar inline el contenido de los que ya están
  presupuestados en ese nivel (~3.3k tokens hoy), para no depender de que el
  agente decida abrir esos archivos. **(ADR-012, punto 1 — implementar sin
  ajustes.)**
- `continuum doctor`: nueva verificación que detecta marcadores de conflicto
  de git (`<<<<<<<`) sin resolver dentro de `.ai/HANDOFF.md`. **(ADR-012,
  punto 2 — reemplaza la idea original de `.gitattributes merge=ours`,
  descartada por riesgo de pérdida silenciosa de handoffs; ver "fuera de
  alcance".)**
- `continuum doctor`: nueva verificación que detecta números de ADR
  duplicados o con huecos, cubriendo las dos convenciones que admite el
  protocolo (`docs/decision-log.md` y `docs/architecture/ADR-*.md`).
  **(ADR-012, punto 3.)** Extensión implementada a pedido explícito del
  owner tras el cierre inicial: `continuum adr new "<título>"`, que calcula
  el siguiente número libre y escribe en la convención que el proyecto ya
  esté usando.
- **[agregado tras el cierre inicial]** `continuum doctor --fix
  --no-dry-run` corrige solo la huella sha256 de
  `.github/copilot-instructions.md` (ADR-010) cuando queda desactualizada
  respecto de `AI_COLLABORATION.md`, sin tocar su prosa — automatiza el
  efecto colateral que esta misma tarea encontró y corrigió a mano dos veces
  antes de esta extensión.
- `docs/metodologia-medicion.md` (en `template/docs/`, para que llegue a
  todo proyecto que instale Continuum): protocolo de medición antes/después
  inspirado en `docs/MEASURING_SAVINGS.md` de CBM, adaptado a Continuum y
  pensado para poder correrlo sobre uno de los 4 proyectos reales que ya lo
  usan. Documento opt-in, no un paso obligatorio de ningún flujo. **(ADR-012,
  punto 4.)**
- Frase de postura de confianza (100% local, sin dependencias externas, sin
  telemetría) en el README de cara a adopción. **(ADR-012, punto 5.)**

## Explícitamente fuera de alcance
- **Contrato de evidencia por tamaño de tarea** al estilo Scout/Verify/
  Auditor de CBM — descartado en la investigación (ADR-012): sería una
  norma sin ninguna forma de verificación mecánica, el mismo patrón de falla
  ya documentado en el Proyecto B, y no ataca ningún job real de Continuum.
- **`.gitattributes` con `merge=ours` para `.ai/HANDOFF.md`** — descartado
  en la investigación (ADR-012): a diferencia del artefacto derivable de
  CBM, `.ai/HANDOFF.md` es narrativa irremplazable; `merge=ours` la
  descartaría en silencio sin marcador de conflicto. Reemplazado por la
  verificación de marcadores de conflicto sin resolver (ver arriba).
- **`continuum init --detect`** (auto-detección de proveedores instalados)
  — descartado por completo en la investigación (ADR-012), no solo diferido:
  no existe en Continuum el problema que ese mecanismo resuelve en CBM (sus
  entrypoints ya son archivos versionados dentro del repo, sin combinación
  insegura que detectar). No se registra ni como pendiente futuro.
- Cualquier forma de grafo de conocimiento de código, parsing con
  tree-sitter, embeddings o búsqueda semántica de código — cambiaría la
  identidad del producto, no es lo que CBM aporta de útil aquí.
- Daemon de coordinación entre sesiones concurrentes al estilo CBM — ya
  cubierto por decisión explícita en ADR-011 (`--worktree`, no locks); no se
  reabre esa decisión.
- Artefacto binario de estado compartido (equivalente a
  `.codebase-memory/graph.db.zst`) — no aplica, el estado de Continuum ya es
  texto plano versionable nativamente.
- Ejecutar la medición piloto en un proyecto real con
  `docs/metodologia-medicion.md` — se documenta el método en esta tarea, la
  ejecución piloto es trabajo de seguimiento (potencial tarea `medium`
  separada, uno de los 4 proyectos).

## Write-set (archivos que se espera tocar)
No editar fuera de esta lista sin actualizarla primero. Evita refactors oportunistas.

- `.ai/state/topics/pendientes.md` — hecho
- `docs/decision-log.md` (ADR-012) — hecho
- `docs/investigacion-2026.md` (§10) — hecho
- `tools/_continuum/context.py` y `template/tools/_continuum/context.py`
  (volcar contenido de OBLIGATORIOS)
- `tools/_continuum/doctor.py` y `template/tools/_continuum/doctor.py`
  (verificación de marcadores de conflicto en `HANDOFF.md` + verificación de
  numeración de ADRs)
- `tools/_continuum/__main__.py` y `template/tools/_continuum/__main__.py`
  (registro del subcomando `adr new`) — hecho
- `tools/_continuum/adr.py` y `template/tools/_continuum/adr.py` (nuevo) —
  hecho
- `tools/_continuum/common.py` y `template/tools/_continuum/common.py`
  (refactor: `collect_adr_numbers`/`adr_numbering_issues`/`slugify` movidos
  aquí desde `doctor.py` para que `adr.py` los reutilice) — hecho
- `.github/copilot-instructions.md` y `template/.github/copilot-instructions.md`
  (huella sha256 recalculada varias veces durante la tarea; la del `template/`
  sigue siendo manual — ver `pendientes.md`) — hecho
- `AI_COLLABORATION.md` y `template/AI_COLLABORATION.md` (§0/§3 sobre
  `context`; §5 sobre `adr new`; §6 sobre la verificación de `HANDOFF.md`;
  §8 sobre `doctor --fix`) — hecho
- `template/docs/metodologia-medicion.md` (nuevo) y `docs/metodologia-medicion.md`
  en este mismo repositorio por ser autoalojado (ver `ARCHITECTURE.md` doble
  copia raíz/`template/`) — hecho
- `README.md` y `README.en.md` — hecho
- `.ai/state/topics/pendientes.md` — hecho
- `tests/test_context.py`, `tests/test_doctor.py`, `tests/test_adr.py` (nuevo),
  `tests/test_status_fix.py` — hecho

## Fuentes de verdad a leer antes de empezar
- `.ai/state/estado-dev.md`
- `.ai/state/topics/arquitectura.md` (regla de doble copia raíz/`template/`)
- `.ai/state/topics/pendientes.md`
- `AI_COLLABORATION.md` (protocolo completo, §0, §2, §5, §6)
- `docs/decision-log.md` (ADR-011 es el más reciente; ADR-004 y ADR-008 como
  ejemplo de ADRs que citan evidencia externa)
- `docs/investigacion-2026.md` (formato de las secciones existentes)
- `tools/_continuum/context.py` (comportamiento actual de `cmd_context`)
- Fuente externa: https://github.com/DeusData/codebase-memory-mcp — en
  particular `README.md`, `docs/MEASURING_SAVINGS.md` y
  `docs/CONFIGURATION.md` de ese repositorio (ya revisados en la sesión que
  originó esta tarea; no hace falta releer todo desde cero, solo las
  secciones citadas en el execution-plan).

## Contexto mínimo sugerido
Según el tamaño declarado arriba, no cargues más de lo necesario:

| Tamaño  | Techo de lectura inicial orientativo |
|---------|----------------------------------------|
| small   | 1-3 archivos concretos, sin explorar carpetas completas |
| medium  | 1 módulo/dominio, usar `rg`/`grep` para localizar antes de leer |
| large   | fragmentar con `continuum packetize`; considerar dividir en subtareas |

Dado el tamaño `large`, considerar cerrar esta tarea tras los pasos 0-6 del
execution-plan (documentación + quick wins de bajo riesgo) y abrir tareas
`medium` separadas para el paso 7 (subcomando `adr`, toca CLI + tests) si el
contexto se agota antes.
