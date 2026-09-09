# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/),
versionado según [SemVer](https://semver.org/lang/es/) (ver `CONTRIBUTING.md`
§ Versionado).

## [Unreleased]

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
  ADR-001 a ADR-007).
- Guía de adopción para proyectos existentes (`docs/rollout-guide.md`).
- Licencia MIT.
- El propio repositorio se autoaloja: corre su propia instancia de
  Continuum además de distribuirla como plantilla en `template/`.

Sin releases todavía — no hay un tag previo contra el cual comparar. El
primer tag (`v1.0.0`) cierra esta sección `[Unreleased]`.
