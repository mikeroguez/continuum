# Resumen y stack

Continuum es un protocolo más un CLI para persistir la memoria de un
proyecto de software en su propio repositorio de git, compartida entre
proveedores de IA (Claude, Codex, Gemini) y entre las personas de un equipo.
Este mismo repositorio es a la vez la fuente distribuible (`template/`) y
una instancia autoalojada de sí mismo (los archivos en la raíz) — ver
`docs/decision-log.md` ADR-005.

**Estado actual (2026-09-09):** diseño completo y CLI probado de punta a
punta con pruebas manuales de humo (no hay suite de tests automatizada
todavía). No publicado: sin remoto de git configurado, sin licencia
elegida, no aplicado a ningún proyecto externo.

## Stack

- CLI (`tools/continuum` + paquete interno `tools/_continuum/`): Python 3,
  solo librería estándar, sin dependencias externas.
- Protocolo y plantillas: Markdown.
- Diagramas de documentación: Mermaid (validados con `@mermaid-js/mermaid-cli`
  vía `npx`, no instalado como dependencia del proyecto).
