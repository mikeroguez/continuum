# CLAUDE.md

Sigue `AGENTS.md` y `AI_COLLABORATION.md`. No hay reglas propias divergentes
para Claude aquí.

El hook `SessionStart` (`.claude/settings.json`) ya te mostró
`AI_COLLABORATION.md`, `.ai/HANDOFF.md` y `.ai/state/estado-dev.md` al
arrancar esta conversación — busca el bloque "Contexto Sugerido de
Continuum" arriba en vez de releerlos con Read. Si no ves ese bloque (hook
no instalado, o cliente sin soporte), lee en este orden antes de cualquier
tarea de alcance medio o mayor: `.ai/HANDOFF.md` → `.ai/state/estado-dev.md`
→ `.ai/tasks/<slug>/task.md` (si aplica).

Este proyecto tiene hooks configurados en `.claude/settings.json` para
escribir `.ai/HANDOFF.md` automáticamente al terminar la sesión o antes de
compactar contexto — no lo desactives sin motivo.
