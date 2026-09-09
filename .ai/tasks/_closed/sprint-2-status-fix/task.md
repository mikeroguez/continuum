# Tarea: sprint-2-status-fix

**Creada:** 2026-09-09 · **Tamaño:** medium · **Owner:** gemini · **Rol:** Backend (`software/backend`)

## Objetivo
Convertir el diagnóstico de salud en orientación directa mediante el nuevo comando `continuum status` (visión compacta de una pantalla con la siguiente acción) y la funcionalidad de auto-reparación segura e idempotente `continuum doctor --fix` (con soporte para `--dry-run` y `--no-dry-run`).

## Incluido en el alcance
- `continuum status`: Resumen compacto de estado (listo/no listo), salud de memoria viva, hooks, tareas activas y edad del handoff.
- `continuum doctor --fix`: Reparaciones seguras automáticas:
  - Crear carpetas de estructura faltantes (`.ai/state/topics/`, `.ai/tasks/`, `.ai/state/archive/`).
  - Instalar git hook de pre-commit si no está presente.
  - Sincronizar subagentes de Claude si el pack `comun` está activo.
  - Crear `.ai/HANDOFF.md` si falta.
- `--dry-run` por defecto en `--fix` para mostrar el plan de reparaciones sin tocar disco.
- `--no-dry-run` para ejecutar las reparaciones.
- Idempotencia: Una segunda corrida de `doctor --fix` no produce cambios.
- Tests unitarios en `tests/test_status_fix.py`.
- Documentación en `README.md` y `.ai/state/topics/comandos.md`.

## Explícitamente fuera de alcance
- Fixes no seguros o destructivos (borrar temas con contenido, hacer push, modificar ramas).
- Telemetría remota.
- Refactors no relacionados con diagnóstico o reparaciones.

## Write-set (archivos que se espera tocar)
- `template/tools/_continuum/doctor.py`
- `template/tools/_continuum/status.py`
- `template/tools/_continuum/__main__.py`
- `tools/_continuum/doctor.py`
- `tools/_continuum/status.py`
- `tools/_continuum/__main__.py`
- `tests/test_status_fix.py`
- `README.md`
- `.ai/state/topics/comandos.md`
- `.ai/tasks/sprint-2-status-fix/*`
- `.ai/HANDOFF.md`

## Fuentes de verdad a leer antes de empezar
- `.ai/state/estado-dev.md`
- `docs/ux-metrics-sprints.md` Sprint 2
- `tools/_continuum/doctor.py`
- `tools/_continuum/common.py`
- `tools/_continuum/bootstrap.py`

## Criterios de salida
- `continuum status` muestra una salida compacta de estado y siguiente acción.
- `continuum doctor --fix` (con `--dry-run` por defecto) lista las reparaciones planificadas.
- `continuum doctor --fix --no-dry-run` aplica las reparaciones seguras y la segunda ejecución es un no-op.
- Tests automatizados en `tests/test_status_fix.py` pasan 100%.
- `python3 -m unittest discover -s tests -t . -v` pasa.
- `python3 tools/continuum doctor` pasa limpio.
