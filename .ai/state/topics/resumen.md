# Resumen y stack

Continuum es un protocolo más un CLI para persistir la memoria de un
proyecto de software en su propio repositorio de git, compartida entre
proveedores de IA (Claude, Codex, Gemini) y entre las personas de un equipo.
Este mismo repositorio es a la vez la fuente distribuible (`template/`) y
una instancia autoalojada de sí mismo (los archivos en la raíz) — ver
`docs/decision-log.md` ADR-005.

**Estado actual (2026-09-10):** versión v1.3.2 publicada oficialmente. Remoto `origin` en `git@github.com:mikeroguez/continuum.git`, suite automatizada de 96 tests unitarios superada sin errores. `continuum doctor` verificado con 0 errores y 0 advertencias. Propagación de v1.3.2 mediante subtree pull a los 4 proyectos dependientes (`seguimiento-talleres`, `seguimiento-deportes`, `seguimiento-clubes`, `SISETAP`) completada con exito.

## Stack

- CLI (`tools/continuum` + paquete interno `tools/_continuum/`): Python 3,
  solo librería estándar, sin dependencias externas.
- Tests automatizados: `unittest` estándar en `tests/`, ejecutados también en
  GitHub Actions para Python 3.10 y 3.12.
- Protocolo y plantillas: Markdown.
- Diagramas de documentación: Mermaid (validados con `@mermaid-js/mermaid-cli`
  vía `npx`, no instalado como dependencia del proyecto).
