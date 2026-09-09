# Handoff de Tarea: sprint-4-tareas-guiadas

**Fecha:** 2026-09-09 · **Owner:** gemini · **Rol:** Backend (`software/backend`)

## Objetivo completado
Implementación de los subcomandos `continuum task current` (detección de tarea activa actual) y `continuum task resume <slug>` (resumen operativo y sugerencia de contexto para retomar tareas sin ceremonia).

## Entregables y cambios
- Funciones `current()` y `resume()` en `tools/_continuum/tasks.py` (y `template/tools/_continuum/tasks.py`).
- Integración de los subcomandos `current` y `resume` (con soporte `--json`) bajo `task` en `__main__.py` (y plantilla).
- Pruebas unitarias en `tests/test_tasks_guided.py` (3 funciones de prueba con múltiples aserciones).
- Actualización de documentación en `README.md` y `.ai/state/topics/comandos.md`.

## Validación ejecutada
- `python3 tools/continuum task current`: probado con 0, 1 y múltiples tareas activas, en terminal y JSON.
- `python3 tools/continuum task resume sprint-4-tareas-guiadas`: probado en terminal y JSON.
- `python3 -m unittest discover -s tests -t . -v`: 73/73 tests pasados OK.
- `python3 tools/continuum doctor`: 0 problemas críticos, 0 advertencias.
