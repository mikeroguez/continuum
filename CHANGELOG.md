# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/),
versionado según [SemVer](https://semver.org/lang/es/) (ver `CONTRIBUTING.md`
§ Versionado).

## [Unreleased]

### Added

- `continuum task start <slug> --worktree` crea la tarea y aísla el
  directorio de trabajo en un `git worktree` propio, para agentes o
  personas trabajando en paralelo sobre el mismo repositorio (ver
  ADR-011).
- `continuum doctor` advierte cuando detecta varias tareas activas sin
  evidencia de aislamiento por worktree.

### Changed

- `AI_COLLABORATION.md` y las guías de uso documentan `--worktree` y
  advierten contra `git stash` con otros worktrees activos (la lista de
  stash es del repositorio, no de cada worktree).
- `.claude/settings.json` agrega un hook `SessionStart` que corre
  `continuum context` al arrancar o resumir una sesión de Claude Code,
  simétrico al `SessionEnd`/`PreCompact` que ya escribía el handoff.

## [1.4.0] - 2026-09-10

### Added

- Integración verificable con GitHub Copilot mediante
  `.github/copilot-instructions.md`, instrucciones por ruta y agentes
  personalizados generados desde `.ai/roles/`.
- Criterios y fixture seguro para revisión asistida de cambios.
- Validación de huella de `AI_COLLABORATION.md`, paridad de artefactos Copilot
  y handoff con proveedor `copilot`.

### Changed

- La documentación separa el protocolo común agnóstico del modelo de los
  adaptadores específicos de cada cliente.

## [1.3.2] - 2026-09-10

### Changed

- Rediseño estético y estandarización visual limpia y minimalista en toda la documentación (`README.md`, `README.en.md`, `CONTRIBUTING.md`, `CONTRIBUTING.en.md`, `guia-para-agentes.md`, `guide-for-agents.md`).

## [1.3.1] - 2026-09-10

### Added

- Mapa de navegación de documentación (`docs/README.md`) para orientar la diferencia entre la arquitectura interna de metadesarrollo (`docs/`) y la documentación distribuida (`template/docs/`).
- Actualizado `template/docs/README.md` con navegación explícita destacando las secciones de casos de uso para equipos de desarrollo y plantillas de prompts.

### Fixed

- Soporte de configuración `template_branch` en `.ai/config.json` con fallback automático a la rama `export`.

## [1.3.0] - 2026-09-10

### Added

- `docs/evaluation-plan.md`: plan operativo prerregistrable derivado de
  `docs/research-protocol.md` (presupuesto, aleatorización, exclusiones y
  análisis), separado de las hipótesis y el modelo de privacidad.
- Piloto local de instrumentación (`evaluation/pilot/`,
  `tests/test_evaluation_pilot.py`) que verifica las condiciones A/B/C del
  protocolo de relevo entre sesiones con un fixture sin red ni datos
  personales; el registro de ejecución queda fuera de Git
  (`evaluation/pilot/local-runs/`).
- Guías de uso bilingües distribuidas en `template/docs/` (para personas y
  para agentes), enlazadas desde ambos README.

### Changed

- `AI_COLLABORATION.md` (y su copia en `template/`) recorta el detalle
  operativo hacia las nuevas guías de `template/docs/`, para no convertir el
  protocolo canónico en una enciclopedia.
- `docs/ux-metrics-roadmap.md` ya no afirma hipótesis científicas
  directamente: remite a `docs/research-protocol.md` como fuente canónica.
- `docs/research-protocol.md` revisado y ampliado.

## [1.2.0] - 2026-09-10

### Added

- `continuum sync` ahora acepta `template_branch` en `.ai/config.json` y usa
  `export` como valor predeterminado. Así los proyectos pueden sincronizar una
  rama de plantilla explícita sin depender de que se llame `main`.

## [1.1.1] - 2026-09-09

### Fixed

- `continuum status` y `continuum metrics report` ya detectan correctamente
  el hook de pre-commit cuando fue instalado vía `core.hooksPath` (como hace
  `continuum install-hooks`), en vez de asumir siempre `.git/hooks/pre-commit`.
