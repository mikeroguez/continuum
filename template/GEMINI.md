# GEMINI.md

Sigue `AGENTS.md` y `AI_COLLABORATION.md`. No hay reglas propias divergentes
para Gemini aquí.

Antes de cualquier tarea de alcance medio o mayor, lee en este orden:
`.ai/HANDOFF.md` → `.ai/state/estado-dev.md` → `.ai/tasks/<slug>/task.md` (si aplica).

Al terminar la sesión o si notas que el contexto se está por agotar, corre
manualmente `tools/continuum handoff --auto --provider gemini` antes de cortar
(Gemini CLI no expone hooks equivalentes a los de Claude Code al momento de
escribir esto — verifica si ya existen en tu versión).
