# GEMINI.md

Sigue `AGENTS.md` y `AI_COLLABORATION.md`. No hay reglas propias divergentes para Gemini aquí.

Antes de cualquier tarea de alcance medio o mayor, lee en este orden:
`.ai/HANDOFF.md` → `.ai/state/estado-dev.md` → `.ai/tasks/<slug>/task.md` (si aplica).

## Directivas Operativas para Gemini / Antigravity

- **Persistencia Proactiva:** Aunque la ventana de contexto de Gemini sea amplia (1M+ tokens), escribe avances y decisiones en disco (`.ai/HANDOFF.md` o `.ai/tasks/<slug>/handoff.md`) al completar cada sub-hito o cada 15-20 intercambios para evitar pérdida de progreso en la conversación.
- **Skills y Roles:** Los roles del catálogo `.ai/roles/` están proyectados como skills nativas en `.gemini/skills/<slug>/SKILL.md`.
- **Cierre de Sesión:** Al terminar la sesión o si vas a reiniciar la conversación, corre `tools/continuum handoff --auto --provider gemini` antes de cortar.
