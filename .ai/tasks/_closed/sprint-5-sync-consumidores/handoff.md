# Handoff de Tarea: sprint-5-sync-consumidores

**Fecha:** 2026-09-09 · **Owner:** gemini · **Rol:** Backend (`software/backend`)

## Objetivo completado
Implementación del subcomando `continuum sync` (con opciones `--check`, `--dry-run`, `--apply` y `--json`) para simplificar la sincronización de repositorios consumidores vía `git subtree` sin exigir memorizar URLs ni carpetas de prefix.

## Entregables y cambios
- Función `cmd_sync()` en `tools/_continuum/bootstrap.py` (y `template/tools/_continuum/bootstrap.py`).
- Registro del subcomando `sync` y alias `sync-template` en `__main__.py` (y plantilla).
- Pruebas unitarias en `tests/test_sync_cmd.py` (4 casos de prueba).
- Actualización de documentación en `README.md` y `.ai/state/topics/comandos.md`.

## Validación ejecutada
- `python3 tools/continuum sync --check`: probado en terminal y JSON.
- `python3 tools/continuum sync --dry-run`: verificado plan de sincronización.
- `python3 -m unittest discover -s tests -t . -v`: 77/77 tests pasados OK.
- `python3 tools/continuum doctor`: 0 errores críticos, 0 advertencias.
