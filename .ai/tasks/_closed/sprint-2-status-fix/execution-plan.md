# Plan de ejecución: sprint-2-status-fix

Solo para tareas `medium`/`large`. Es una cola persistente de pasos: márcalos
al avanzar para que, si la sesión se corta a medio camino, la siguiente sepa
exactamente dónde retomar sin releer todo desde cero.

- [x] Paso 1 — Crear `status.py` y `template/tools/_continuum/status.py` con `build_status()`, `format_human_status()` y `cmd_status()`.
- [x] Paso 2 — Implementar `run_fix()` en `doctor.py` para auto-reparaciones seguras (`.ai/state/topics/`, `.ai/tasks/`, `.ai/state/archive/`, `.ai/HANDOFF.md`, `.githooks/pre-commit`, `.claude/agents/`).
- [x] Paso 3 — Agregar subcomando `status` y opciones `--fix`, `--dry-run`, `--no-dry-run` a `__main__.py` (y plantilla).
- [x] Paso 4 — Crear suite de pruebas unitarias `tests/test_status_fix.py`.
- [x] Paso 5 — Actualizar documentación en `README.md` y `.ai/state/topics/comandos.md`.
- [x] Paso 6 — Correr `tools/continuum doctor` y `python3 -m unittest discover -s tests -t . -v`.

## Estado actual
Implementación completada. 66 tests pasados OK y `continuum doctor` verificado sin advertencias ni errores.
