# Arquitectura y dominio

El diseño completo (capas, principios, alcance) está en `ARCHITECTURE.md` en
la raíz — no se duplica aquí para no arriesgar que este archivo diverja de
ese al actualizarse por separado.

Particularidad de este repositorio frente a un proyecto que solo *consume*
Continuum: aquí conviven dos copias de los mismos archivos operativos
(`AI_COLLABORATION.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.ai/`,
`tools/`) — una en la raíz (instancia autoalojada, la que rige el trabajo
real sobre este repositorio) y otra dentro de `template/` (la fuente
distribuible que otros proyectos incorporan vía `git subtree`). `tools/
_continuum/doctor.py` excluye explícitamente la carpeta `template/` de su
chequeo de duplicados por este motivo — es la única excepción conocida a esa
regla.

**Regla de mantenimiento:** un cambio al protocolo o al CLI se hace primero
en `template/`, y luego se sincroniza a la raíz copiando los archivos
afectados (no al revés) — `template/` es la fuente de verdad. `.ai/roles/`
sigue la misma regla.

Este repositorio declara `roles.packs: ["comun", "software"]` en
`.ai/config.json` (Continuum es software, no investigación ni contenido
educativo). `.claude/agents/` (generado por `continuum roles sync`) está en
`.gitignore` — no es parte de lo que se sincroniza entre `template/` y la
raíz, se regenera localmente.
