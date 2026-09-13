# Handoff: afinar-roles-software

**Fecha:** 2026-09-12 · **Rol:** (sin asignar)

## Objetivo
Reforzar los roles de `software` que producen código (`backend`,
`frontend`, `devops-infraestructura`) para que por defecto generen
soluciones eficientes, código corto sin sacrificar claridad, y
documentación mínima — a pedido explícito del owner, que los describió como
"genéricos, deberían funcionar para cualquier desarrollo de producto de
software".

## Archivos revisados
- Los 6 roles del pack `software` y los 9 del pack `comun` (contenido
  completo, para decidir alcance).
- `.ai/roles/comun/accesibilidad.md` como precedente de rol "beefed up" con
  checklist concreto — la vara de especificidad a igualar.
- `docs/investigacion-2026.md` §4 (Gloaguen et al. / McMillan et al.): la
  evidencia ya revisada en este mismo repositorio dice que el contenido
  genérico/inferible en un archivo de contexto *empeora* el resultado, no
  lo mejora — condicionó todo el diseño del contenido nuevo.
- `tools/_continuum/roles.py`: confirma que `sync()` copia `role["text"]`
  completo y literal al subagente generado — nada que no esté en el .md
  fuente llega al agente real.

## Archivos modificados
- `.ai/roles/software/{backend,frontend,devops-infraestructura}.md` +
  espejo en `template/.ai/roles/software/` — sección nueva "Estándares de
  código por defecto" en cada uno, con guías concretas y específicas del
  dominio (no genéricas).
- `.ai/roles/comun/qa.md` + espejo — una frase corta añadida (fuera del
  párrafo de Mandato, para no inflar el `description` del frontmatter
  generado) que hace de estos estándares parte de lo que QA verifica en
  software.

## Decisión(es) tomada(s)
- **Alcance limitado a los tres roles que producen código + QA**, no a todo
  el pack `software` ni a todo `comun` — `ux-ui`/`producto-jtbd`/
  `ux-research` no escriben código, y los roles de `comun` restantes ya
  tienen mandatos específicos que no se solapan con "código eficiente".
  Ampliar sin un problema real sería ceremonia (`ARCHITECTURE.md` §2,
  principio 2). Ver "Explícitamente fuera de alcance" en `task.md`.
- **Contenido concreto y accionable, no platitudes** ("evita N+1", "valida
  en los bordes", checklist de accesibilidad ya existente) en vez de
  "escribe código limpio y eficiente" — directamente por la evidencia de
  `docs/investigacion-2026.md` §4 ya citada arriba. Un consejo genérico que
  cualquier modelo capaz ya sigue por defecto no aporta nada verificable y
  sí cuesta tokens en cada subagente generado.
- El refuerzo a `qa.md` se puso en una oración aparte, no dentro del párrafo
  de `**Mandato:**`, porque ese párrafo alimenta literalmente el campo
  `description` del frontmatter YAML del subagente generado
  (`tools/_continuum/roles.py`) — inflarlo habría sido el mismo error de
  verbosidad que se está corrigiendo en el resto de la tarea.

## Suposiciones vigentes
- No se tocó el mecanismo de `roles.py`/`sync()` — es contenido de
  catálogo, no cambio de arquitectura.
- No se extendió el mismo refuerzo a `ux-ui`/`producto-jtbd`/`ux-research`
  ni al resto de `comun`; queda registrado como posible extensión futura si
  el owner lo pide, con un criterio de concisión distinto al de código (ver
  `pendientes.md`).

## Validación
- Ejecutada: `python3 -m unittest discover -s tests -t .` → 131 tests, 0
  fallos (sin tests nuevos — es contenido de catálogo, no lógica; los tests
  de `test_roles.py` ya cubren que `sync()` propaga el contenido tal cual).
  `tools/continuum doctor` → 0 críticos. `continuum roles sync
  --provider claude` corrido dos veces (antes y después del cambio a
  `qa.md`) para confirmar que el contenido nuevo llega íntegro a
  `.claude/agents/backend.md` y al resto — verificado leyendo el archivo
  generado directamente.
- No ejecutada: no se probó el resultado con un subagente real ejecutando
  una tarea de código (validaría si el contenido nuevo cambia el
  comportamiento observado, no solo que se propaga el texto).

## Riesgos / dudas abiertas
- El valor real de este cambio se mide en comportamiento del agente, no en
  que el texto exista — recomendado usar
  `docs/metodologia-medicion.md` (de la tarea anterior,
  `adopcion-ideas-cbm`) para comparar calidad/concisión del código
  producido por `backend`/`frontend` antes y después de este cambio, en un
  proyecto real.

## Siguiente paso recomendado
Tarea completa, sin trabajo bloqueado. Si el owner confirma que el alcance
está bien acotado, cerrar con `continuum task close afinar-roles-software`.
Si quiere extender el mismo espíritu a los roles de producto/investigación
o al resto de `comun`, es una tarea nueva con un criterio de concisión
distinto (no "código eficiente", sino "documentos cortos y específicos").
