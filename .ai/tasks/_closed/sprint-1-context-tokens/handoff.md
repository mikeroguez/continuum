# Handoff de Tarea: sprint-1-context-tokens

**Fecha:** 2026-09-09 · **Owner:** gemini · **Rol:** Backend (`software/backend`)

## Objetivo completado
Implementación de los comandos `continuum context` (selección de contexto mínimo con categorías `mandatory`, `recommended`, `on_demand`, `avoid`) y `continuum tokens` (desglose del presupuesto de tokens).

## Entregables y cambios
- Módulo `tools/_continuum/context.py` (y `template/tools/_continuum/context.py`) con `build_context()`, `format_human_context()`, `build_tokens_report()`, `format_human_tokens()`, `cmd_context()` y `cmd_tokens()`.
- Subcomandos `context` y `tokens` en `tools/_continuum/__main__.py` (y en `template/`).
- Pruebas unitarias en `tests/test_context.py` (6 casos de prueba).
- Documentación actualizada en `README.md` y `.ai/state/topics/comandos.md`.

## Validación ejecutada
- `python3 tools/continuum context --why`: probado en terminal y JSON.
- `python3 tools/continuum context --task ux-metricas-continuum`: probado con tarea activa.
- `python3 tools/continuum tokens`: probado desglose de arranque y memoria viva.
- `python3 -m unittest discover -s tests -t . -v`: 63/63 tests pasados OK.
- `python3 tools/continuum doctor`: 0 errores, 0 advertencias.
