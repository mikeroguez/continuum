# Revisión de evidencia externa (septiembre de 2026)

Contraste del diseño descrito en `ARCHITECTURE.md` con literatura académica,
telemetría publicada por proveedores de modelos y terceros, y práctica de
industria vigente a la fecha de esta revisión. Objetivo: identificar con
evidencia, no con intuición, qué conservar, qué corregir y qué haya quedado
obsoleto.

## Veredicto

El principio central del diseño no está obsoleto: coincide con el consenso
de industria observado en 2026 — memoria como archivos de texto versionados
en git, cargados bajo demanda, en lugar de bases vectoriales o
orquestadores de agentes. La revisión sí identificó errores concretos y
medibles en la primera versión del diseño, y una función nueva de Claude
Code (memoria automática) que conviene diferenciar con precisión de lo que
este sistema resuelve. El detalle, a continuación.

## 1. Memoria en markdown versionado frente a bases vectoriales / RAG

Diversas fuentes de 2026 documentan un giro explícito de la industria en
esta dirección: *"el estándar para el contexto de un agente ahora es un
archivo markdown, no un índice vectorial"*, y *"un sistema de recuperación
simple sobre memoria limpia y estructurada supera de forma consistente a un
pipeline RAG complejo sobre memoria ruidosa"*
([Epsilla](https://www.epsilla.com/blogs/markdown-memory-death-of-vector-databases-agentic-memory),
[voxos.ai](https://voxos.ai/blog/how-to-give-ai-coding-agents-long-term-m/index.html)).
Una base vectorial o RAG solo resulta ventajosa con corpus grandes y no
estructurados, o datos multi-tenant regulados — no es el perfil de un
repositorio de código de un equipo pequeño o mediano. Esto confirma la
decisión de no incorporar memoria vectorial.

**Hallazgo relevante.** Claude Code implementa nativamente este mismo
patrón: *"un archivo índice (`MEMORY.md`) más archivos por tema, cargados
bajo demanda"*, y *"la práctica converge en limitar los archivos de memoria
a aproximadamente 30 elementos, con poda regular"*. Es, en esencia, el mismo
patrón que este sistema implementa (`estado-dev.md` más
`.ai/state/archive/`), aunque la implementación de referencia usa índice más
temas en lugar de un único archivo snapshot — corregido en la §6.

## 2. Memoria automática de Claude Code — complementa este sistema, no lo sustituye

Desde 2026, Claude Code incorpora por defecto un sistema de memoria propio:
registra observaciones en segundo plano durante la sesión, y un proceso de
consolidación periódico (disparado manualmente o tras un umbral de actividad)
relee sesiones recientes, funde entradas duplicadas, elimina hechos
contradichos y reconstruye el índice
([claudefa.st](https://claudefa.st/blog/guide/mechanics/auto-dream),
[moeed.app](https://moeed.app/posts/claude-code-dreaming-guide/)).

Esta función no sustituye a este sistema: es memoria local, por usuario, por
máquina, y exclusiva de un proveedor. No se transporta por git, no es visible
para otros proveedores de IA ni para otras personas del equipo. Resuelve un
problema distinto y más acotado — continuidad de un asistente entre sus
propias sesiones en una máquina — del que resuelve este sistema: memoria
transportada por el repositorio, compartida entre proveedores y entre
personas. La existencia de esta función nativa respalda, más que
contradice, la necesidad de una capa de memoria compartida: si el problema
ya estuviera resuelto de fábrica para el caso de equipo, no haría falta
construir nada adicional.

## 3. `AGENTS.md` como estándar de industria

`AGENTS.md` dejó de ser una convención informal. En diciembre de 2025, su
gobernanza se transfirió a la **Agentic AI Foundation**, un proyecto de la
Linux Foundation, y para 2026 lo leen de forma nativa Codex, Cursor,
Copilot, Gemini CLI, Aider, Windsurf, Zed, Jules y más de veinte
herramientas adicionales, con adopción registrada en más de 60.000
repositorios ([OpenAI](https://openai.com/index/agentic-ai-foundation/),
[AAIF](https://aaif.io/blog/writing-an-effective-agents-md)). La
especificación oficial no exige secciones fijas, pero recomienda: resumen
del proyecto, comandos de build/test, estilo de código, pruebas, seguridad,
y reglas de commit/PR — un patrón prácticamente idéntico al observado en los
cinco proyectos auditados antes de esta revisión. Esto confirma el uso de
`AGENTS.md`/`CLAUDE.md`/`GEMINI.md` como entrypoints delgados: es el
estándar vigente de la industria, no una convención propia sujeta a
reconsideración.

## 4. El contenido del archivo de contexto importa más que su existencia

Este es el punto en el que la revisión obliga a corregir el diseño, no solo
a confirmarlo. Dos estudios con metodología rigurosa arrojan resultados en
apariencia contradictorios:

- **Gloaguen et al., febrero de 2026** ("Evaluating AGENTS.md", ETH
  Zürich/LogicStar, [arXiv:2602.11988](https://arxiv.org/html/2602.11988v1)):
  archivos de contexto **generados por IA** redujeron la tasa de éxito de la
  tarea en torno al 3% y aumentaron el costo de inferencia en más del 20%
  (un modelo evaluado gastó 22% más tokens de razonamiento con el archivo
  presente que sin él). Causa identificada: *"los archivos generados por un
  modelo de lenguaje mayormente repiten lo que ya está en el repositorio —
  el README, la configuración de pruebas, la documentación existente— que
  el agente puede encontrar y leer durante la ejecución de la tarea de
  todos modos."*
- **Estudio de enero de 2026**, sobre 124 cambios reales en 10 repositorios:
  con `AGENTS.md` presente, el tiempo de ejecución cayó 28.64% y los tokens
  de salida cayeron 16.58% — el efecto contrario, y de magnitud considerable.
- **McMillan et al.** ("Instruction Adherence in Coding Agent Configuration
  Files", [arXiv:2605.10039](https://arxiv.org/abs/2605.10039)), 1.650
  sesiones reales de Claude Code CLI: ni el tamaño del archivo (25, 100, 250
  o 500 líneas), ni la posición de la instrucción, ni la arquitectura de
  archivos (uno solo frente a `AGENTS.md` más `CLAUDE.md` frente a archivos
  anidados por carpeta) produjeron un efecto medible sobre si el agente
  cumple una regla concreta.

**Conciliación de los resultados.** El tamaño del archivo no es la variable
determinante — el estudio factorial lo confirma con datos controlados; la
recomendación difundida de "menos de 200 líneas" no tiene respaldo empírico
directo. La variable que sí importa es si el contenido es información que
el agente **no podría inferir** leyendo el repositorio. Un archivo extenso
pero compuesto por decisiones no evidentes, comandos exactos y advertencias
del tipo "esto ya se intentó y no funcionó" resulta útil. Un archivo de
cualquier tamaño que reescribe lo que ya dice el README o el código,
perjudica el resultado y encarece la ejecución. La guía oficial de la AAIF
coincide con esta lectura: instrucciones humanas específicas y no
inferibles —por ejemplo, el gestor de paquetes exigido o la versión mínima
de un lenguaje— son útiles; contenido genérico generado por un modelo, no.

**Corrección aplicada.** Se incorporó una regla explícita en
`AI_COLLABORATION.md` que prohíbe contenido inferible o genérico en los
entrypoints y en el índice de memoria, con el mismo criterio que estos
estudios.

## 5. Trabajo concurrente de varios agentes o personas sobre un mismo repositorio

La práctica de industria documentada para este escenario no es orquestación
de agentes (ver §7), sino aislar cada tarea o agente en su propio `git
worktree`, acotar cada tarea a una especificación concreta, y mantener una
revisión humana antes de fusionar cambios
([Augment Code](https://www.augmentcode.com/guides/how-to-run-a-multi-agent-coding-workspace)).
Uno de los proyectos auditados ya usaba ramas y worktrees de git de facto
para este propósito, sin que el patrón estuviera documentado en su
protocolo. Se incorporó como recomendación explícita en el diseño, como
complemento al mecanismo de visibilidad social existente (`continuum task
claim`), que no aísla archivos en disco.

## 6. GitHub Spec Kit — alternativa madura, evaluada y rechazada

**Spec Kit** (github.com/github/spec-kit), mantenido por GitHub, cuenta con
más de 111.000 estrellas, comandos estandarizados (`/specify`, `/plan`,
`/tasks`) compatibles con más de 30 agentes (Copilot, Claude Code, Gemini
CLI, entre otros), y reportes de *"3 a 10 veces más éxito en el primer
intento en tareas no triviales"*
([GitHub Blog](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)).
Es, en esencia, una alternativa considerablemente más adoptada y validada
que el sistema de tareas construido en este proyecto
(`TASK.md`/`EXECUTION_PLAN.md`/`NOTES.md`).

Esta alternativa se evaluó y se rechazó: resuelve la planeación de una
feature, no la continuidad entre sesiones/proveedores/personas que es el
problema central de Continuum, e implicaría una dependencia externa y más
ceremonia que el sistema actual. Ver `docs/decision-log.md` ADR-008 para el
razonamiento completo y las condiciones bajo las que se reconsideraría.

## 7. Frameworks de orquestación multi-agente — no aplican a este problema

LangGraph, CrewAI y AutoGen siguen en expansión en 2026, pero resuelven la
construcción de una aplicación de IA con varios agentes coordinados en
tiempo de ejecución (agentes como nodos de un grafo, con estado compartido)
— un problema de producto, distinto al de una persona alternando de forma
manual entre distintos clientes de IA sobre un mismo repositorio, con otras
personas en el equipo. Ninguna fuente consultada describe el uso de estos
frameworks para ese segundo escenario. Se confirma la decisión de no
construir orquestación (`ARCHITECTURE.md` §8).

## 8. Caching de prompts: guía más específica

La guía original se limitaba a indicar que el bloque de arranque debía
mantenerse estable, sin más detalle. La práctica de industria en 2026 es más
concreta: colocar todo lo estable al inicio y lo variable al final, con el
system prompt como el bloque más estable, seguido de las definiciones de
herramientas; un bloque cacheado de 50.000 tokens reutilizado durante una
sesión reduce el costo del input cacheado al 10% del precio base en cada
solicitud posterior a la primera
([Agentbrisk](https://agentbrisk.com/blog/prompt-caching-deep-dive-2026/)).
Claude Code aplica esto automáticamente al system prompt, a `CLAUDE.md` y a
las definiciones de herramientas; la guía se actualizó para ser explícita
sobre qué evitar: modificar el protocolo o el índice de memoria a mitad de
sesión invalida el caching de ese bloque para el resto de la sesión.

## 9. `packetize`: el fundamento técnico propone algo distinto a lo implementado

El trabajo de *Recursive Language Models*
([arXiv:2512.24601](https://arxiv.org/abs/2512.24601), descrito como *"el
paradigma de 2026"* por PrimeIntellect) no propone fragmentar archivos en
markdown estático de antemano: propone proveer al modelo un entorno de
ejecución (REPL) y dejar que decida en tiempo real cómo explorar y recortar
el contexto de forma programática. La utilidad `packetize` de este sistema
es una versión estática y precomputada de esa idea, útil en un contexto
específico (proveer un fragmento acotado a un subproceso o a un modelo sin
herramientas de archivo), pero redundante cuando el agente ya cuenta con
lectura por rango y búsqueda por patrones nativas — el caso de los clientes
agénticos considerados en este diseño. La guía se corrigió para reflejar
esto.

## 10. `codebase-memory-mcp`: qué aplica de un motor de intelligence de código y qué no (actualización 2026-09-12)

Revisión adicional, no programada en la primera pasada de esta
investigación: comparación con
[`codebase-memory-mcp`](https://github.com/DeusData/codebase-memory-mcp)
(CBM, DeusData, arXiv:2603.27277), un motor de grafo de conocimiento de
código para agentes de IA vía MCP (tree-sitter, embeddings, LSP híbrido,
daemon de indexado). Dominio distinto al de Continuum — CBM indexa código,
Continuum persiste decisiones y estado de sesión en Markdown — pero resuelve
una faceta del mismo problema: que un agente arranque con el contexto
correcto sin depender de que decida buscarlo por su cuenta. Cada idea
candidata se evaluó contra los principios de `ARCHITECTURE.md` §2 y el job
central de Continuum (recuperar el contexto correcto al cambiar de
sesión/proveedor/persona, con ceremonia proporcional al tamaño real del
cambio) — no se adopta nada solo porque le funcione a CBM en su propio
dominio.

**Implementar sin ajustes — `continuum context` debe empujar el contenido de
los archivos obligatorios en `SessionStart`, no solo su lista.** Hoy el hook
imprime nombre y tokens estimados de cada archivo obligatorio (~3.280 tokens
en este mismo repositorio) y confía en que el agente decida abrir cada uno
— exactamente el patrón de falla más frecuente de la auditoría original:
"ninguna automatización real: el cumplimiento depende de que alguien
recuerde seguir el protocolo" (`ARCHITECTURE.md` §1). CBM resuelve el mismo
problema entregando contenido directamente como `additionalContext` en vez
de solo indicar dónde buscarlo. El costo en tokens no cambia — ese contenido
ya se leía, solo cambia quién lo entrega — y no compromete el caching de
prompt porque ocurre una sola vez al inicio de sesión, no a mitad de turno
(`ARCHITECTURE.md` §6).

**No implementar — sincronizar la estrategia de merge de `.ai/HANDOFF.md` a
`merge=ours`**, el patrón que usa CBM para su artefacto
`.codebase-memory/graph.db.zst`. Descartado tras revisar el mecanismo, no
solo por analogía superficial: `merge=ours` no fusiona contenido — ante un
conflicto descarta en silencio la versión entrante completa, sin marcador ni
aviso. Para CBM eso es seguro porque ese archivo es un índice derivado y
regenerable desde el código fuente: perder una versión cuesta un
reindexado, no un dato. `.ai/HANDOFF.md` es lo opuesto — es la narrativa de
continuidad, irremplazable, y el principio raíz del diseño es justamente que
"el repositorio es la memoria" (`ARCHITECTURE.md` §2.1) y que el handoff "no
tiene excepciones... deja constancia de qué se hizo" (§2.6). Aplicar
`merge=ours` aquí arriesgaría perder handoffs sin que nadie lo note — peor
que el conflicto manual que hoy resuelve `AI_COLLABORATION.md` §6, porque un
conflicto de git al menos obliga a alguien a mirar. Ajuste real que sí se
adopta, de alcance menor: que `continuum doctor` detecte marcadores de
conflicto de git (`<<<<<<<`) sin resolver dentro de `.ai/HANDOFF.md` —
mecaniza la alerta (principio 3) sin el riesgo de pérdida silenciosa.

**No implementar — contrato de evidencia por tamaño de tarea al estilo
Scout/Verify/Auditor de CBM** (qué tan exhaustiva debe ser una búsqueda
antes de una afirmación negativa tipo "esto no se usa en ningún lado"). CBM
puede exigir ese contrato porque tiene una herramienta mecánica de
verificación (`check_index_coverage`) capaz de probar la diferencia entre
"no se encontró" y "no se buscó". Continuum no tiene, ni debería construir,
un equivalente: no indexa código, y una norma de cuánto buscar antes de
afirmar algo, sin ninguna forma de verificarla mecánicamente, es exactamente
el patrón que ya fracasó en el Proyecto B ("una regla de proceso sin
verificación mecánica deja de cumplirse en semanas", §2.3). Tampoco ataca el
job central de Continuum — es un problema de otro dominio. Se descarta.

**Implementar, con la prioridad invertida respecto a la propuesta original —
verificación de numeración de ADRs antes que un comando de generación.**
`AGENTS.md` ya prohíbe "renumerar ni reutilizar identificadores... aunque se
hayan cerrado o descartado", pero esa regla depende hoy al cien por ciento
de que la persona la recuerde al escribir un ADR a mano — el mismo patrón de
falla del principio 3. CBM expone esto como una tool (`manage_adr`); la
adaptación de mayor valor por menor esfuerzo no es un comando de generación
de contenido (ceremonia adicional, principio 2) sino que `continuum doctor`
detecte números de ADR duplicados o no consecutivos en
`docs/decision-log.md` — mecaniza la verificación del riesgo real sin
agregar un paso nuevo al flujo de trabajo. Un comando `continuum adr new`
que además scaffoldee la entrada queda como extensión opcional, no como el
núcleo de esta adopción.

**Implementar, con alcance solo documental — metodología de medición
antes/después inspirada en `docs/MEASURING_SAVINGS.md` de CBM.** `continuum
metrics` (`tools/_continuum/metrics.py`) hoy mide exclusivamente estado
estático del repositorio — tokens estimados de archivos, conteo de
tareas/temas — nunca el consumo real de tokens o tool-calls de una sesión de
agente real. Es un vacío genuino, no una duplicación de algo que ya existe.
Se adopta como documento nuevo (`docs/metodologia-medicion.md`), no como
paso obligatorio de ningún flujo (principio 2): un protocolo opt-in para
quien quiera cuantificar la adopción con rigor — commit congelado,
condiciones aisladas, calidad reportada aparte de eficiencia, sin
extrapolar de un solo repositorio. Los 4 proyectos que ya usan Continuum en
producción (`seguimiento-talleres`, `seguimiento-deportes`,
`seguimiento-clubes`, `SISETAP`) son el terreno natural para la primera
aplicación piloto, fuera del alcance de esta ronda de cambios.

**No implementar ni dejar como pendiente — auto-detección de proveedores
instalados (`continuum init --detect`, inspirado en el instalador de 45
clientes de CBM).** Evaluado a fondo, no solo diferido: se descarta por
completo. La complejidad que CBM resuelve con detección existe porque cada
uno de sus 45 clientes vive en una ruta de configuración distinta *fuera*
del repositorio (`~/.claude.json`, `$CODEX_HOME/config.toml`, etc.), y
activar la integración equivocada tiene costo real (archivos huérfanos,
flags experimentales). Los entrypoints de Continuum (`AGENTS.md`,
`CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`) son archivos
versionados *dentro* del propio repositorio, sin ninguna combinación
insegura que activar, y su costo cuando un proveedor no se usa es marginal
(~100-150 tokens estimados cada uno, según la propia salida de `continuum
doctor`). No hay problema real, en la arquitectura actual de Continuum, que
este mecanismo resuelva.

**Sin cambio de diseño, solo redacción — postura de confianza explícita.**
Continuum ya cumple lo que CBM declara como diferenciador (100% local, sin
dependencias externas más allá de la librería estándar de Python, sin
telemetría) — confirmado en `.ai/state/topics/resumen.md`. Se añade como
frase explícita al README de cara a adopción externa; no es una decisión de
arquitectura, es comunicación de algo que ya era cierto.

Ver `docs/decision-log.md`, ADR-012, para el detalle de cada cambio adoptado
y el razonamiento completo de lo descartado.

## Cambios aplicados a la plantilla

Ver `docs/decision-log.md`, ADR-004 y ADR-012, para el detalle de cada
cambio aplicado a `template/` a partir de esta revisión, con su
justificación.

## Fuentes

- [Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents? (arXiv:2602.11988)](https://arxiv.org/html/2602.11988v1)
- [On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents (arXiv:2601.20404)](https://arxiv.org/abs/2601.20404)
- [Instruction Adherence in Coding Agent Configuration Files (arXiv:2605.10039)](https://arxiv.org/abs/2605.10039)
- [Recursive Language Models (arXiv:2512.24601)](https://arxiv.org/abs/2512.24601)
- [The research is in: your AGENTS.md is probably too long — Upsun](https://developer.upsun.com/posts/ai/agents-md-less-is-more)
- [AGENTS.md Files: The Research Says You're Probably Doing Them Wrong — Allstacks](https://www.allstacks.com/blog/agents-md-files-the-research-says-youre-probably-doing-them-wrong)
- [OpenAI co-founds the Agentic AI Foundation](https://openai.com/index/agentic-ai-foundation/)
- [Writing an Effective AGENTS.md — Agentic AI Foundation](https://aaif.io/blog/writing-an-effective-agents-md)
- [Claude Code Auto Dream Explained](https://claudefa.st/blog/guide/mechanics/auto-dream)
- [Claude Code AutoDream: MEMORY.md Cleanup and the /dream Command](https://moeed.app/posts/claude-code-dreaming-guide/)
- [Claude Code Auto Memory: How Your AI Learns Your Project](https://claudefa.st/blog/guide/mechanics/auto-memory)
- [The Death of the Vector Database: Why Top Agents Are Reverting to Markdown — Epsilla](https://www.epsilla.com/blogs/markdown-memory-death-of-vector-databases-agentic-memory)
- [Forget RAG: The Best AI Agent Memory Is a Plain Text File — voxos.ai](https://voxos.ai/blog/how-to-give-ai-coding-agents-long-term-m/index.html)
- [Memory Bank — Cline docs](https://docs.cline.bot/prompting/cline-memory-bank)
- [Cline Memory Bank: how our power users are creating unique variations](https://www.threads.com/@cline.bot/post/DJHq0ODRlH-/)
- [GitHub Spec Kit — repositorio](https://github.com/github/spec-kit)
- [Spec-driven development with AI — GitHub Blog](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
- [How to Run a Multi-Agent Coding Workspace (2026) — Augment Code](https://www.augmentcode.com/guides/how-to-run-a-multi-agent-coding-workspace)
- [Prompt Caching Deep Dive 2026 — Agentbrisk](https://agentbrisk.com/blog/prompt-caching-deep-dive-2026/)
- [Claude Code Hooks: Complete 2026 Production Reference — The Prompt Shelf](https://thepromptshelf.dev/blog/claude-code-hooks-complete-reference-2026/)
- [SKILL.md vs CLAUDE.md vs AGENTS.md Compared — Termdock](https://www.termdock.com/blog/skill-md-vs-claude-md-vs-agents-md)
- [CrewAI vs LangGraph vs AutoGen — DataCamp](https://www.datacamp.com/tutorial/crewai-vs-langgraph-vs-autogen)
- [`codebase-memory-mcp` — repositorio (DeusData)](https://github.com/DeusData/codebase-memory-mcp)
- [Codebase-Memory: Tree-Sitter-Based Knowledge Graphs for LLM Code Exploration via MCP (arXiv:2603.27277)](https://arxiv.org/abs/2603.27277)
