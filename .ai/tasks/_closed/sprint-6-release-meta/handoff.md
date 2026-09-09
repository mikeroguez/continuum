# Handoff de Tarea: sprint-6-release-meta

**Fecha:** 2026-09-09 · **Owner:** gemini · **Rol:** Backend (`software/backend`)

## Objetivo completado
Implementación de las herramientas de *release* y *export* del propio proyecto Continuum: `continuum export status`, `continuum export refresh` y `continuum release <version>`, validando la consistencia entre SemVer, `CHANGELOG.md`, la rama `export` y la salud general (`doctor`).

## Entregables y cambios
- Módulo `tools/_continuum/release.py` (y `template/tools/_continuum/release.py`) con `cmd_export_status()`, `cmd_export_refresh()` y `cmd_release()`.
- Registro de subcomandos `export` (`status`, `refresh`) y `release` (con opciones `--dry-run`, `--no-dry-run` y `--json`) en `__main__.py` (y plantilla).
- Pruebas unitarias en `tests/test_release_cmd.py` (3 casos de prueba).
- Actualización de documentación en `README.md` y `.ai/state/topics/comandos.md`.

## Validación ejecutada
- `python3 tools/continuum export status`: verificado en terminal y JSON.
- `python3 tools/continuum export refresh --dry-run`: probado.
- `python3 tools/continuum release v1.0.0 --dry-run`: probado formato SemVer, changelog y doctor health.
- `python3 -m unittest discover -s tests -t . -v`: 80/80 tests pasados OK.
- `python3 tools/continuum doctor`: 0 problemas críticos, 0 advertencias.
