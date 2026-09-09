# Bitácora de decisiones de arquitectura

Decisiones sobre el diseño de Continuum en sí — no sobre el código de un
proyecto que lo adopte. Formato ADR abreviado (contexto, decisión,
consecuencias), orden cronológico. Las referencias "Proyecto A–E" remiten a
la tabla de `ARCHITECTURE.md` §1.

## ADR-001 — Distribución vía `git subtree`

**Contexto.** El sistema debe distribuirse a varios proyectos y mantenerse
sincronizado entre ellos. La auditoría inicial mostró divergencia real
cuando no existe un mecanismo de sincronización explícito: un archivo de
registro de cambios con contenido distinto entre dos copias del mismo
proyecto (Proyecto D), y un directorio de configuración de agente copiado a
mano y nunca vuelto a sincronizar (Proyecto B).

**Decisión.** Este repositorio es la fuente única; cada proyecto destino lo
incorpora con `git subtree`.

**Alternativas descartadas.** `git submodule` requiere un checkout separado
y añade fricción para proponer una mejora desde dentro de un proyecto real
mientras se trabaja en él. Copiar archivos a mano es la práctica que la
auditoría mostró que diverge.

## ADR-002 — CLI propio (`continuum`) en lugar de solo convención documental

**Contexto.** La evidencia disponible en el momento de esta decisión era, en
principio, contraria a construir una herramienta: en dos de los cinco
proyectos auditados (B, C) un toolkit de gestión de tareas se usó de forma
intensiva durante pocos días y luego se abandonó a favor de disciplina
manual.

**Decisión.** Construir un CLI con verificación activa (`doctor`, `compact`,
hooks), no solo un conjunto de documentos con reglas.

**Mitigación del riesgo conocido.** El diseño incorpora contramedidas
directas al patrón de abandono observado: las tareas son opcionales por
debajo de un umbral de tamaño, `doctor` sin argumentos es el comando por
defecto de mayor valor con menor esfuerzo, y la automatización se apoya en
hooks de cliente en lugar de depender de la ejecución manual de comandos.

**Consecuencia a monitorear.** La señal de que este riesgo se materializó de
nuevo sería la misma que en los proyectos auditados: `.ai/tasks/` sin
contenido real y `continuum doctor` fuera de los hooks activos.

## ADR-003 — Sin orquestación real entre agentes de IA

**Decisión.** No se construye un enrutador de modelos, cola de tareas entre
agentes, ni bloqueos duros.

**Justificación.** Ningún proyecto auditado mostró concurrencia real entre
proveedores de IA; en los cinco casos, una persona alternaba manualmente
entre distintos clientes sobre el mismo repositorio. Construir orquestación
sin un caso de uso concreto es diseño especulativo. Ver `ARCHITECTURE.md`
§§5 y 8.

## ADR-004 — Correcciones a partir de revisión de literatura e industria

**Contexto.** Tras la primera versión del diseño se realizó una revisión de
literatura académica y práctica de industria (`docs/investigacion-2026.md`)
para contrastarlo con evidencia externa.

**Decisión.** Se aplicaron seis correcciones concretas a `template/`:

1. **Memoria como índice más archivos de tema.** `estado-dev.md` deja de ser
   un archivo que crece sin límite y pasa a ser un índice acotado (≤80
   líneas) que remite a `.ai/state/topics/*.md`, cargados bajo demanda —
   mismo patrón que la función de memoria nativa de Claude Code (índice más
   archivos por tema). Se añadió `continuum memory-split-legacy` para migrar
   proyectos con el formato anterior (relevante para el Proyecto C, cuyo
   archivo de memoria alcanzó ~90 KB).
2. **Regla explícita contra contenido inferible** en los entrypoints y el
   índice: prohibido repetir información recuperable leyendo el código, el
   README o la configuración de pruebas. Motivo: evidencia publicada de que
   ese tipo de contenido reduce la tasa de éxito de la tarea y aumenta el
   costo de inferencia (ver fuente en `docs/investigacion-2026.md` §4).
3. **Corrección del hook de cliente**: se reemplazó `Stop` (dispara en cada
   turno de respuesta) por `SessionEnd` (una vez por sesión) como disparador
   del handoff automático en Claude Code; se mantiene `PreCompact` como
   señal de agotamiento de contexto.
4. **`packetize` pasa a ser un último recurso**, no parte del flujo por
   defecto — la técnica en la que se inspiró (Recursive Language Models)
   propone exploración activa del contexto, no fragmentación estática previa
   (ver `docs/investigacion-2026.md` §9).
5. **Guía de caching de prompts más específica**: no modificar el bloque
   estable de contexto a mitad de sesión; orden estable-primero,
   variable-al-final.
6. **Recomendación explícita de `git worktree` por tarea concurrente**,
   formalizando una práctica que ya existía de facto en el Proyecto A sin
   estar documentada en su protocolo.

**Decisión abierta, no resuelta por esta revisión.** La adopción de GitHub
Spec Kit (`/specify`, `/plan`, `/tasks`) en lugar del sistema de tareas
propio de `template/.ai/tasks/` queda documentada como alternativa madura y
más ampliamente adoptada, pero no se implementó: cambiaría la forma del
subsistema de tareas, no solo su contenido, y esa decisión corresponde al
equipo que mantiene este repositorio. Ver `docs/investigacion-2026.md` §6.

## ADR-005 — Nombre del proyecto: Continuum

**Contexto.** El proyecto se distribuiría como repositorio público bajo el
nombre de trabajo interno `ai-arch`, que coincidía con el nombre del CLI y
del paquete Python.

**Decisión.** Se adoptó el nombre **Continuum**. Se renombró el ejecutable
(`tools/ai-arch` → `tools/continuum`) y el paquete interno (`ai_arch` →
`_continuum`, con guion bajo inicial para evitar la colisión de nombre entre
el ejecutable de nivel superior y el directorio del paquete).

**Alternativas consideradas.** Mantener `ai-arch` como nombre público tenía
costo de cambio nulo (cero archivos que renombrar) pero se consideró menos
distintivo como identidad de proyecto público. `Handoff` se consideró y se
descartó por remitir a una sola pieza del diseño en lugar del sistema
completo.

**Consecuencia.** El repositorio se autoalojó (ver `.ai/`, `AI_COLLABORATION.md`,
etc. en la raíz de este mismo repositorio) usando ya el nombre `continuum`
para el CLI, de forma que no quedó una migración de nombre pendiente sobre
el propio proyecto.

## ADR-006 — Licencia: MIT

**Decisión.** El repositorio se publica bajo licencia MIT (`LICENSE`, en la
raíz).

**Contexto.** El repositorio se publicó en
`git@github.com:mikeroguez/continuum.git` sin licencia explícita, lo que
legalmente reserva todos los derechos y no permite a terceros reutilizar el
código pese a tratarse de un repositorio público.

**Alcance.** La licencia cubre el contenido de este repositorio (protocolo,
plantillas, CLI en `template/` y su instancia autoalojada en la raíz). No se
duplicó el archivo `LICENSE` dentro de `template/`: un proyecto que
incorpore la plantilla vía `git subtree` queda regido por la licencia de su
propio repositorio; los términos de MIT ya permiten esa redistribución sin
necesidad de un archivo adicional.
