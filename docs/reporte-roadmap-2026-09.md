# Reporte y propuesta de roadmap — septiembre 2026

Documento de discusión, no de decisión. Reúne dos revisiones de evidencia
externa hechas sobre Continuum en septiembre de 2026, una auditoría del
propio código, y una propuesta de hacia dónde llevar el producto. Antes de
tomar cualquiera de estas decisiones como definitiva, este documento debe
leerlo el equipo completo (@mikeroguez, @8Wada) y acordarse en conjunto.

## Resumen ejecutivo

Se revisaron dos fuentes externas — el proyecto `codebase-memory-mcp` (motor
de grafo de código) y un artículo de blog sobre ahorro de tokens — contra la
evidencia que Continuum ya tenía documentada (`docs/investigacion-2026.md`)
y contra lo que el código realmente implementa hoy. Conclusión central: **no
hay evidencia nueva que justifique relajar ninguna restricción arquitectónica
existente** (ADR-003, ADR-006, ADR-008). Lo que sí hay es un patrón que
Continuum ya aplicó dos veces sin nombrarlo como principio — construir una
versión propia y mínima en vez de depender de una herramienta de terceros —
y una brecha real: la metodología de medición de ahorro de tokens
(`docs/metodologia-medicion.md`) existe desde hace días y nunca se corrió
sobre un proyecto real.

## 1. Qué se revisó y por qué

| Fuente | Qué es | Resultado ya aplicado |
|---|---|---|
| [`codebase-memory-mcp`](https://github.com/DeusData/codebase-memory-mcp) | Motor de grafo de conocimiento de código para agentes de IA (dominio distinto: indexa código, Continuum indexa decisiones/estado) | ADR-012 — 5 ideas adoptadas, 2 descartadas. Ya implementado y en producción en la rama `mikeroguez` / PR #6. |
| [Artículo lidr.co — "Cómo ahorrar tokens en desarrollo de software"](https://www.lidr.co/blog/como-ahorrar-tokens-en-desarrollo-de-software/) | Blog de industria, sin metodología citada en sus cifras de ahorro | Analizado en esta sesión — ninguna acción aplicada todavía, ver §3. |
| Auditoría del código propio | Búsqueda exhaustiva de cualquier lógica de orquestación/concurrencia real en `tools/_continuum/` | Confirmó que el código coincide al 100% con lo documentado en ADR-003/009/011 — ver §4. |

## 2. `codebase-memory-mcp` — resumen del resultado (ADR-012)

De 7 ideas candidatas: **5 adoptadas** (2 con ajuste de diseño descubierto
durante la implementación), **2 descartadas por completo**.

**Adoptado:**
1. `continuum context` vuelca el contenido completo de los archivos
   obligatorios en `SessionStart`, no solo su lista.
2. `continuum doctor` detecta marcadores de conflicto sin resolver en
   `HANDOFF.md` (reemplaza una idea peor — `.gitattributes merge=ours` —
   que arriesgaba perder handoffs en silencio).
3. `continuum doctor` detecta números de ADR duplicados o con huecos, en
   las dos convenciones que admite el protocolo. `continuum adr new
   "<título>"` como extensión.
4. `docs/metodologia-medicion.md` — protocolo de medición de ahorro real
   (ver §6, es la prioridad #1 de este reporte).
5. Frase de postura de confianza en el README (100% local, sin
   dependencias, sin telemetría).

**Descartado:**
6. Contrato de evidencia por tamaño de tarea (estilo Scout/Verify/Auditor)
   — no verificable mecánicamente en Continuum, mismo patrón de falla que
   una regla sin verificación (Proyecto B de la auditoría original).
7. `continuum init --detect` (auto-detección de proveedores instalados) —
   el problema que resuelve en CBM no existe en la arquitectura de
   Continuum (sus entrypoints ya son archivos versionados dentro del repo).

Detalle completo del razonamiento en `docs/decision-log.md` ADR-012 y
`docs/investigacion-2026.md` §10.

## 3. Artículo de ahorro de tokens — qué aplica y qué no

| Recomendación del artículo | Veredicto | Por qué |
|---|---|---|
| Documentar contexto técnico en una carpeta del repo | Ya implementado, con más rigor | Continuum ya hace esto (`AI_COLLABORATION.md` + `.ai/state/topics/`), pero además lo verifica mecánicamente (`doctor`) — el artículo se queda en "créala", sin el paso de "y detecta si se desactualiza". |
| Modelo caro solo para planificación, barato para ejecutar | Fuera de alcance de Continuum como mecanismo — posible como nota advisory | Es selección de modelo dentro de una sesión, no orquestación entre proveedores — no choca con ADR-003, pero tampoco es algo que Continuum deba automatizar. A lo sumo, una línea de guía en `AI_COLLABORATION.md` §2 ligada al tamaño de tarea ya existente. |
| Prompt caching: estático primero, dinámico al final | Ya implementado | `AI_COLLABORATION.md` §3, ya revisado con fuentes en `docs/investigacion-2026.md` §8. |
| Plugins de compresión (`rtk`, `codegraph`, `caveman`, `ponytail`, `Headroom`) | No recomendado adoptar ninguno | Cifras de ahorro sin metodología citada. `codegraph` es el mismo dominio que CBM, ya descartado (ADR-012). `caveman` y `ponytail` prometen exactamente lo que Continuum **ya construyó por su cuenta** esta misma sesión — ver §5. |
| Enrutamiento automático de modelos (Cursor Auto, OpenRouter, LiteLLM) | Fuera de alcance — no hay nada que construir | Es una decisión de qué cliente/gateway usa la persona, externa al protocolo. Continuum ya es compatible con cualquiera de estos por ser agnóstico de proveedor, sin cambiar nada. |
| "El ahorro viene de mejor contexto, no de ejecutar menos IA" (tesis central) | Confirma la tesis de `ARCHITECTURE.md` §6 | Sin acción nueva — es la misma premisa de diseño de Continuum, dicha con otras palabras. |

## 4. Auditoría del código: orquestación y multi-agente

Se buscó explícitamente en todo `tools/_continuum/` cualquier llamada de red,
invocación de otro agente, o lógica de reparto de tareas. Resultado: **cero**
— ni `import requests`/`urllib`/`socket`, ni `subprocess` que lance
`claude`/`codex`/`gemini`, ni ninguna función que decida qué proveedor
atiende qué tarea.

Lo único que existe relacionado con "múltiples agentes" es aislamiento
físico y visibilidad social, nunca reparto de trabajo:

| Mecanismo | Qué hace realmente |
|---|---|
| `continuum task start <slug> --worktree` | Un `git worktree add` nativo. Crea la carpeta/rama y termina ahí — Continuum no vuelve a coordinar nada entre worktrees. |
| `continuum task claim <slug> <owner>` | Escribe una línea de texto en `task.md`. No es un lock: no impide que otra persona edite la misma carpeta. |
| Aviso de `doctor` sobre tareas concurrentes | Cuenta worktrees con `git worktree list` y avisa (`c.warn`, nunca bloquea) si hay más tareas activas que worktrees. |
| Rol `orquestador` | Texto markdown puro — una lente que una sesión adopta, no un proceso que reparte trabajo (ADR-009). |

**Conclusión: cero divergencia entre lo documentado y lo implementado.**

## 5. Patrón ya aplicado, nunca formalizado: construir en vez de depender

Dos veces esta sesión, ante una necesidad real que coincidía con lo que
promete una herramienta externa, se construyó una versión propia mínima y
específica al dominio de Continuum en vez de agregar la dependencia:

- **CBM (ADR-012):** en vez de adoptar un grafo de código como
  `codebase-memory-mcp`/`codegraph`, se construyeron verificaciones
  puntuales en `doctor` y el comando `adr new` — resuelven el problema real
  (numeración de ADR, conflictos de handoff) sin traer una dependencia de
  infraestructura ajena al dominio de Continuum.
- **Estándares de código por defecto (tarea `afinar-roles-software`):** en
  vez de instalar un plugin de "respuestas comprimidas" (`caveman`) o
  "reduce sobreingeniería" (`ponytail`), se escribió contenido específico y
  verificable directamente en los roles `backend`/`frontend`/
  `devops-infraestructura` — con la misma evidencia (`docs/investigacion-
  2026.md` §4) que explica por qué un plugin genérico no aportaría nada que
  el modelo no supiera ya.

**Propuesta:** formalizar esto como ADR explícito (borrador de título:
*"Construir versión propia mínima antes que depender de terceros"*), para
que sea un criterio consciente y no una coincidencia. Sin esto documentado,
dos personas distintas podrían decidir diferente la próxima vez que se
presente el mismo dilema.

## 6. Roadmap propuesto, priorizado

| # | Acción | Tamaño | Por qué en ese orden |
|---|---|---|---|
| 1 | **Correr `docs/metodologia-medicion.md` sobre uno de los 4 proyectos dependientes reales** | Requiere trabajo fuera de este repo | Es la prioridad real: todo lo demás en este reporte sigue siendo razonamiento, no medición. Sin esto, no sabemos si Continuum "de verdad sirve" o solo suena bien en el diseño. |
| 2 | Formalizar ADR-013 con el principio de §5 | Chico | Una vez acordado con el equipo, evita reabrir el mismo debate cada vez. |
| 3 | Enriquecer el aviso de `doctor` (>8k tokens) con las 3 categorías de diagnóstico del artículo (contexto ruidoso / demasiadas herramientas / especificación poco clara) | Chico | Mejora de mensaje, cero riesgo, coincide con la tesis que Continuum ya sostiene. |
| 4 | Línea advisory en `AI_COLLABORATION.md` §2 sobre nivel de modelo por fase de tarea (`large` → modelo de mayor razonamiento para el `execution-plan.md`) | Chico | Documental, no mecanismo — no requiere tocar ninguna restricción. |

## 7. Lo que NO cambia

Ninguna restricción arquitectónica se libera con la evidencia revisada:

- **ADR-003 (sin orquestación entre agentes de IA)** se mantiene — ni CBM ni
  el artículo aportaron un caso de concurrencia real entre proveedores.
- **ADR-006 (sin memoria vectorial/embeddings)** se mantiene — nada
  revisado cambia el volumen o la naturaleza del contenido de Continuum.
- **ADR-008 (sin GitHub Spec Kit)** se mantiene — no se revisó, no aplica
  a esta ronda.

## 8. Qué necesita decidir el equipo

1. ¿Se prioriza correr la medición piloto (ítem 1) antes que cualquier otro
   cambio de código?
2. ¿Se está de acuerdo con formalizar el principio de §5 como ADR-013, con
   esa redacción o una distinta?
3. ¿Los ítems 3 y 4 se implementan ya, se agrupan en una sola tarea, o se
   posponen hasta después de la medición piloto?

Nada de este reporte se implementó todavía — queda a la espera de esta
conversación.
