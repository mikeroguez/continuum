# Tarea: sprint-4-tareas-guiadas

**Creada:** 2026-09-09 · **Tamaño:** medium · **Owner:** gemini · **Rol:** Backend (`software/backend`)

## Objetivo
Reducir la ceremonia en el flujo de tareas medianas y grandes, agregando los subcomandos `continuum task current` y `continuum task resume <slug>`, y mejorando la integración con `task close` y `context --task`.

## Incluido en el alcance
- Subcomando `continuum task current`: Muestra la tarea activa actual o lista las opciones si hay varias.
- Subcomando `continuum task resume <slug>`: Muestra el objetivo, write-set, siguiente paso recomendado y sugiere el contexto necesario para retomar.
- Subcomando `continuum task close <slug>`: Mejora la validación del handoff de tarea y su integración con el handoff global.
- Pruebas unitarias en `tests/test_tasks_guided.py`.
- Documentación en `README.md` y `.ai/state/topics/comandos.md`.

## Explícitamente fuera de alcance
- Obligar el uso de tareas para cambios pequeños (`small`).
- Modificaciones a repositorios o ramas remotas.

## Write-set (archivos que se espera tocar)
- `template/tools/_continuum/tasks.py`
- `template/tools/_continuum/__main__.py`
- `tools/_continuum/tasks.py`
- `tools/_continuum/__main__.py`
- `tests/test_tasks_guided.py`
- `README.md`
- `.ai/state/topics/comandos.md`
- `.ai/tasks/sprint-4-tareas-guiadas/*`
- `.ai/HANDOFF.md`

## Fuentes de verdad a leer antes de empezar
- `.ai/state/estado-dev.md`
- `docs/ux-metrics-sprints.md` (Sprint 4)
- `tools/_continuum/tasks.py`
- `tools/_continuum/context.py`

## Criterios de salida
- `continuum task current` reporta la tarea activa o sugiere iniciar una.
- `continuum task resume <slug>` presenta el resumen operativo para retomar la tarea.
- All unit tests pass (`python3 -m unittest discover -s tests -t . -v`).
- `python3 tools/continuum doctor` pasa con 0 errores y 0 advertencias.
