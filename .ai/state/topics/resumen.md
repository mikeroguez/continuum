# Resumen y stack

Continuum es un protocolo más un CLI para persistir la memoria de un
proyecto de software en su propio repositorio de git, compartida entre
proveedores de IA (Claude, Codex, Gemini) y entre las personas de un equipo.
Este mismo repositorio es a la vez la fuente distribuible (`template/`) y
una instancia autoalojada de sí mismo (los archivos en la raíz) — ver
`docs/decision-log.md` ADR-005.

**Estado actual (2026-09-09):** diseño completo, licencia MIT presente,
remoto `origin` configurado en `git@github.com:mikeroguez/continuum.git` y
CLI verificado con suite automatizada (`python3 -m unittest discover -s tests
-t . -v`: 53 tests OK). `tools/continuum doctor` pasa sin problemas críticos
ni advertencias. El proyecto está correctamente adaptado para Codex mediante
`AGENTS.md` como entrypoint nativo y mantiene entrypoints delgados para
Claude y Gemini. Pendiente: aplicar el rollout a proyectos reales y completar
`template_remote` / `template_prefix` si se quiere usar `sync-template` sin
placeholders.

## Stack

- CLI (`tools/continuum` + paquete interno `tools/_continuum/`): Python 3,
  solo librería estándar, sin dependencias externas.
- Tests automatizados: `unittest` estándar en `tests/`, ejecutados también en
  GitHub Actions para Python 3.10 y 3.12.
- Protocolo y plantillas: Markdown.
- Diagramas de documentación: Mermaid (validados con `@mermaid-js/mermaid-cli`
  vía `npx`, no instalado como dependencia del proyecto).
