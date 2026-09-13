# Reporte y propuesta de roadmap — septiembre 2026

Documento de discusión, no de decisión. Reúne tres revisiones de evidencia
externa hechas sobre Continuum en septiembre de 2026, una auditoría del
propio código, y una propuesta de hacia dónde llevar el producto. Antes de
tomar cualquiera de estas decisiones como definitiva, este documento debe
leerlo el equipo completo (@mikeroguez, @8Wada) y acordarse en conjunto.

## Resumen ejecutivo

Se revisaron tres rondas de evidencia externa — el proyecto
`codebase-memory-mcp` (motor de grafo de código), un artículo de blog sobre
ahorro de tokens, y una investigación adicional con papers y estudios de
industria verificables (no blogs) hecha explícitamente para no quedarnos con
lo ya citado — contra la evidencia que Continuum ya tenía documentada
(`docs/investigacion-2026.md`) y contra lo que el código realmente
implementa hoy. Conclusión central: **no hay evidencia nueva que justifique
relajar ninguna restricción arquitectónica existente** (ADR-003, ADR-006,
ADR-008). Lo que sí hay es un patrón que Continuum ya aplicó dos veces sin
nombrarlo como principio — construir una versión propia y mínima en vez de
depender de una herramienta de terceros, **ahora con un matiz importante**:
la evidencia nueva (McKinsey/Oxford sobre proyectos de TI a medida) obliga a
acotar ese principio explícitamente a construcciones mínimas y puntuales,
nunca a subsistemas grandes. También se confirma con un experimento
controlado ajeno (Sourcegraph) lo que Continuum ya diseñó por razonamiento
propio: menos tokens bien elegidos rinde mejor que más tokens por defecto.
Y sigue en pie la brecha real ya identificada: la metodología de medición de
ahorro de tokens (`docs/metodologia-medicion.md`) existe desde hace días y
nunca se corrió sobre un proyecto real.

## 1. Qué se revisó y por qué

| Fuente | Qué es | Resultado ya aplicado |
|---|---|---|
| [`codebase-memory-mcp`](https://github.com/DeusData/codebase-memory-mcp) | Motor de grafo de conocimiento de código para agentes de IA (dominio distinto: indexa código, Continuum indexa decisiones/estado) | ADR-012 — 5 ideas adoptadas, 2 descartadas. Ya implementado y en producción en la rama `mikeroguez` / PR #6. |
| [Artículo lidr.co — "Cómo ahorrar tokens en desarrollo de software"](https://www.lidr.co/blog/como-ahorrar-tokens-en-desarrollo-de-software/) | Blog de industria, sin metodología citada en sus cifras de ahorro | Analizado en esta sesión — ninguna acción aplicada todavía, ver §3. |
| Auditoría del código propio | Búsqueda exhaustiva de cualquier lógica de orquestación/concurrencia real en `tools/_continuum/` | Confirmó que el código coincide al 100% con lo documentado en ADR-003/009/011 — ver §5. |
| Investigación adicional (papers/estudios, no blogs) | Búsqueda explícita de fuentes distintas a las ya citadas en `docs/investigacion-2026.md`, para no repetir lo mismo | Confirma y matiza — no cambia ninguna conclusión de fondo. Ver §4. |

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
   (ver §7, es la prioridad #1 de este reporte).
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
| Plugins de compresión (`rtk`, `codegraph`, `caveman`, `ponytail`, `Headroom`) | No recomendado adoptar ninguno | Cifras de ahorro sin metodología citada. `codegraph` es el mismo dominio que CBM, ya descartado (ADR-012). `caveman` y `ponytail` prometen exactamente lo que Continuum **ya construyó por su cuenta** esta misma sesión — ver §6. |
| Enrutamiento automático de modelos (Cursor Auto, OpenRouter, LiteLLM) | Fuera de alcance — no hay nada que construir | Es una decisión de qué cliente/gateway usa la persona, externa al protocolo. Continuum ya es compatible con cualquiera de estos por ser agnóstico de proveedor, sin cambiar nada. |
| "El ahorro viene de mejor contexto, no de ejecutar menos IA" (tesis central) | Confirma la tesis de `ARCHITECTURE.md` §6 | Sin acción nueva — es la misma premisa de diseño de Continuum, dicha con otras palabras. |

## 4. Investigación adicional (papers y estudios, no blogs)

A pedido explícito de no quedarnos con la evidencia ya citada, se buscaron
fuentes nuevas — papers y estudios de industria verificables, no blogs de
marketing — específicamente sobre los puntos que el análisis anterior dejaba
más débiles.

| Hallazgo | Fuente | Implicación para Continuum |
|---|---|---|
| Agentes con un resumen de 100K tokens de la base de código rindieron peor que agentes con 5K tokens de recuperación dirigida, en benchmarks de Sourcegraph sobre las mismas tareas. | Benchmark de Sourcegraph, citado en Glean (fuente secundaria — no se verificó el benchmark original) | Confirma con un experimento controlado ajeno — no solo razonamiento propio — que el diseño de índice + temas bajo demanda (`ARCHITECTURE.md` §5/§6) es la dirección correcta. Refuerza no volcar más contenido por defecto del estrictamente necesario. |
| Anthropic formalizó el término "context engineering" en septiembre de 2025: "el conjunto de estrategias para curar y mantener el conjunto óptimo de tokens durante la inferencia". El consenso de industria en 2026 es que la reducción estratégica de tokens supera a la expansión. | Anthropic Applied AI Team, citado en Glean | Confirma terminología y consenso de industria — Continuum ya hace esto; ahora hay un nombre reconocido para referenciarlo. |
| En un estudio de mecanismos de configuración en Claude Code/Copilot/Cursor/Gemini/Codex sobre repositorios reales, los archivos de contexto estático "dominan el panorama" y suelen ser el único mecanismo usado; pocos repos adoptan mecanismos avanzados como Skills/Subagents, que además dependen mayormente de instrucciones estáticas, no scripts ejecutables. | "Harness Engineering for Agentic AI Coding Tools" (arXiv:2602.14690) | Dato en contra de sobre-invertir en generar más variantes de subagentes por proveedor — lo que de verdad se usa en la práctica es el archivo de contexto simple. No contradice lo que Continuum ya tiene (`roles` → subagentes generados), pero sugiere que no es ahí donde hay más retorno por esfuerzo adicional. |
| Optimizar sin medir primero (perfilar/instrumentar antes de intervenir) es práctica establecida en ingeniería de software — el riesgo documentado de intervenir sin datos es optimizar una parte del sistema que no es el cuello de botella real. | Consenso amplio de ingeniería de software (principio de Knuth; ver fuentes) | Refuerza directamente la Prioridad #1 del roadmap (§7): correr `docs/metodologia-medicion.md` antes de seguir construyendo. |
| Proyectos grandes de TI construidos a medida corren en promedio 45% sobre presupuesto y entregan 56% menos valor del prometido; 17% amenazan la continuidad de la empresa. | McKinsey & University of Oxford, estudio sobre más de 5,400 proyectos de TI | **Matiz importante al principio de §6**: es evidencia de riesgo en construcciones GRANDES y a medida, no en adiciones mínimas y puntuales como las que Continuum ya hizo (unas funciones en `doctor.py`, no una plataforma). El principio debe quedar acotado explícitamente a "mínimo y puntual" — no es licencia para construir subsistemas grandes en vez de adoptar herramientas ya probadas cuando el problema es genuinamente grande. |

**Efecto sobre la propuesta de ADR-013 (§6):** el nombre y alcance del ADR
deben dejar el límite explícito — algo como *"construir una versión propia
solo cuando el esfuerzo es mínimo (una función, una verificación puntual —
no un subsistema) y específico al dominio de Continuum; para cualquier cosa
de mayor tamaño, evaluar herramientas existentes primero"* — no un mandato
general de "construir siempre".

Fuentes:
- [How to optimize token efficiency in agentic systems — Glean (cita el benchmark de Sourcegraph y la formalización de Anthropic)](https://www.glean.com/perspectives/how-to-optimize-token-efficiency-in-agentic-systems)
- [Harness Engineering for Agentic AI Coding Tools: An Exploratory Study (arXiv:2602.14690)](https://arxiv.org/abs/2602.14690)
- [Build vs Buy Software in 2026: A Practical Guide — pptssolutions (cita el estudio McKinsey/Oxford)](https://www.pptssolutions.com/blogs/build-vs-buy-software-2026)
- [Premature Optimization — minware](https://www.minware.com/guide/anti-patterns/premature-optimization)

## 5. Auditoría del código: orquestación y multi-agente

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

## 6. Patrón ya aplicado, nunca formalizado: construir en vez de depender (acotado)

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

**Propuesta, ya acotada con la evidencia de §4:** formalizar esto como ADR
explícito, con el límite explícito de tamaño — no "construir siempre",
solo cuando la construcción es mínima y puntual (una función, una
verificación — nunca un subsistema) y específica al dominio de Continuum.
Para cualquier necesidad de mayor tamaño, el ADR debe pedir evaluar
herramientas existentes primero, citando el riesgo documentado de
sobrecostos en construcciones grandes a medida (McKinsey/Oxford, §4). Sin
esto documentado, dos personas distintas podrían decidir diferente la
próxima vez que se presente el mismo dilema — y sin el límite explícito, el
principio podría usarse para justificar construir algo grande que debería
evaluarse contra alternativas ya probadas.

## 7. Roadmap propuesto, priorizado

| # | Acción | Tamaño | Por qué en ese orden |
|---|---|---|---|
| 1 | **Correr `docs/metodologia-medicion.md` sobre uno de los 4 proyectos dependientes reales** | Requiere trabajo fuera de este repo | Es la prioridad real: todo lo demás en este reporte sigue siendo razonamiento, no medición. Sin esto, no sabemos si Continuum "de verdad sirve" o solo suena bien en el diseño. |
| 2 | Formalizar ADR-013 con el principio de §6 (ya acotado a construcciones mínimas) | Chico | Una vez acordado con el equipo, evita reabrir el mismo debate cada vez. |
| 3 | Enriquecer el aviso de `doctor` (>8k tokens) con las 3 categorías de diagnóstico del artículo (contexto ruidoso / demasiadas herramientas / especificación poco clara) | Chico | Mejora de mensaje, cero riesgo, coincide con la tesis que Continuum ya sostiene. |
| 4 | Línea advisory en `AI_COLLABORATION.md` §2 sobre nivel de modelo por fase de tarea (`large` → modelo de mayor razonamiento para el `execution-plan.md`) | Chico | Documental, no mecanismo — no requiere tocar ninguna restricción. |

**Nota de la investigación adicional (§4), no un ítem del roadmap:** el
hallazgo de que los repos reales rara vez usan Skills/Subagents avanzados
sugiere que invertir más esfuerzo en generar variantes de subagentes por
proveedor (más allá de lo que `roles.py` ya hace) tiene bajo retorno
comparado con seguir invirtiendo en la calidad del contenido de contexto
simple. No es una acción — es una razón para no priorizar esa dirección si
alguien la propone después.

## 8. Lo que NO cambia

Ninguna restricción arquitectónica se libera con la evidencia revisada:

- **ADR-003 (sin orquestación entre agentes de IA)** se mantiene — ni CBM ni
  el artículo aportaron un caso de concurrencia real entre proveedores.
- **ADR-006 (sin memoria vectorial/embeddings)** se mantiene — nada
  revisado cambia el volumen o la naturaleza del contenido de Continuum.
- **ADR-008 (sin GitHub Spec Kit)** se mantiene — no se revisó, no aplica
  a esta ronda.

## 9. Qué necesita decidir el equipo

1. ¿Se prioriza correr la medición piloto (ítem 1) antes que cualquier otro
   cambio de código?
2. ¿Se está de acuerdo con formalizar el principio de §6 como ADR-013 —
   ya acotado a construcciones mínimas por la evidencia de §4 —, con esa
   redacción o una distinta?
3. ¿Los ítems 3 y 4 se implementan ya, se agrupan en una sola tarea, o se
   posponen hasta después de la medición piloto?

Nada de este reporte se implementó todavía — queda a la espera de esta
conversación.
