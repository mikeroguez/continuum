# Tarea: sprint-3-sesiones-handoff

**Creada:** 2026-09-09 · **Tamaño:** medium · **Owner:** gemini · **Rol:** Backend (`software/backend`)

## Objetivo
Optimizar el ciclo de inicio y cierre de sesiones preservando continuidad sin producir memoria redundante ni obesa mediante `continuum session start` y `continuum session end`.

## Incluido en el alcance
- `continuum session start`: Muestra el handoff vigente, tareas activas y el contexto sugerido inicial para la sesión.
- `continuum session end`: Genera o actualiza el handoff con un mensaje opcional, proveedor/rol y resumen de git status/diff.
- Lint de Handoff: Validación no bloqueante para advertir si el handoff supera los ~400 tokens estimados o contiene diffs extensos.
- Tests unitarios en `tests/test_session.py`.
- Documentación en `README.md` y `.ai/state/topics/comandos.md`.

## Explícitamente fuera de alcance
- Interfaz gráfica o TUI compleja.
- Telemetría remota.
- Refactors fuera de la gestión de sesiones y handoffs.

## Write-set (archivos que se espera tocar)
- `template/tools/_continuum/session.py`
- `template/tools/_continuum/handoff.py`
- `template/tools/_continuum/__main__.py`
- `tools/_continuum/session.py`
- `tools/_continuum/handoff.py`
- `tools/_continuum/__main__.py`
- `tests/test_session.py`
- `README.md`
- `.ai/state/topics/comandos.md`
- `.ai/tasks/sprint-3-sesiones-handoff/*`
- `.ai/HANDOFF.md`

## Fuentes de verdad a leer antes de empezar
- `.ai/state/estado-dev.md`
- `docs/ux-metrics-sprints.md` Sprint 3
- `tools/_continuum/handoff.py`
- `tools/_continuum/context.py`
- `tools/_continuum/common.py`

## Criterios de salida
- `continuum session start` resume el handoff previo y sugiere contexto para arrancar.
- `continuum session end --message "..."` genera un handoff conciso y ejecuta linting de tokens.
- Tests automatizados en `tests/test_session.py` pasan 100%.
- `python3 -m unittest discover -s tests -t . -v` pasa.
- `python3 tools/continuum doctor` pasa limpio.
