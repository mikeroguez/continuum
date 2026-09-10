# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/),
versionado según [SemVer](https://semver.org/lang/es/) (ver `CONTRIBUTING.md`
§ Versionado).

## [Unreleased]

Sin cambios todavía.

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
- `continuum packetize` ya no falla con `ValueError` cuando el directorio
  raíz del proyecto cuelga de un symlink (p. ej. macOS resuelve `/tmp` como
  `/private/tmp`).

## [1.1.0] - 2026-09-09

### Added

- Rediseño de UX y métricas completo (Sprints 0 al 8): `context`, `tokens`, `status`, `doctor --fix`, `session start/end`, `task current/resume`, `sync`, `export status/refresh`, `release`, `github protect` y `metrics report/export/compare`.
- Sistema de exportación y anonimización de métricas en JSON y CSV (`continuum metrics export --anonymize`).
- Protocolo de investigación y evidencia local (`docs/research-protocol.md`) con modelo ético y de privacidad Opt-In / Opt-Out.
- Reglas avanzadas de colaboración en equipo, resolución de conflictos de handoffs y aislamiento de tareas en `AI_COLLABORATION.md`.
- Cobertura completa de pruebas unitarias automatizadas (87 tests pasados).

## [1.0.0] - 2026-09-09

### Added

- Protocolo de colaboración con IA (`AI_COLLABORATION.md` + entrypoints
  `AGENTS.md`/`CLAUDE.md`/`GEMINI.md`) y CLI `continuum` (`doctor`, `task
  start/claim/close/list`, `handoff [--auto]`, `compact --topic`,
  `memory-split-legacy`, `packetize`, `install-hooks`, `sync-template`).
- Memoria como índice acotado (`estado-dev.md`) más archivos de tema
  (`.ai/state/topics/*.md`), con archivado por mes vía `continuum compact`.
- Hooks de Claude Code (`SessionEnd`, `PreCompact`) para generar el handoff
  de continuidad de forma automática.
- Diseño documentado en `ARCHITECTURE.md`, con diagnóstico basado en
  auditoría de cinco proyectos reales.
- Revisión de literatura e industria 2026 (`docs/investigacion-2026.md`)
  que valida y corrige el diseño inicial.
- Bitácora de decisiones en formato ADR (`docs/decision-log.md`,
  ADR-001 a ADR-008).
- Guía de adopción para proyectos existentes (`docs/rollout-guide.md`).
- Licencia MIT.
- El propio repositorio se autoaloja: corre su propia instancia de
  Continuum además de distribuirla como plantilla en `template/`.
- Manual de colaboración (`CONTRIBUTING.md`): ramas, commits, Pull
  Requests, versionado y proceso de release.
- Suite de tests (`tests/`, stdlib `unittest`) para
  `template/tools/_continuum/`, con workflow de CI (`tests.yml`).
- Catálogo de roles/personas (`.ai/roles/<pack>/<slug>.md`, 23 roles en 4
  packs: `comun`, `software`, `investigacion`, `contenido-educativo`),
  `--role` en `task start`/`handoff`, y `continuum roles list`/`roles sync`
  (subagentes nativos de Claude Code) — ver ADR-009.

Primer release estable de Continuum. El tag `v1.0.0` apunta a la rama
generada `export`, que contiene únicamente la plantilla instalable.
