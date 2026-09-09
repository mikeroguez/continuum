# Plan de ejecución: sprint-0-baseline-metricas

Implementar primero el baseline sin introducir reporting pesado.

- [x] Paso 1 — Leer `doctor.py`, `common.py` y tests existentes para reutilizar estimacion de tokens, lectura de config y helpers git.
- [x] Paso 2 — Definir modelo de snapshot en `metrics.py` con funciones puras testeables.
- [x] Paso 3 — Agregar subcomando `metrics snapshot` con `--dry-run` y `--json`.
- [x] Paso 4 — Agregar `.ai/metrics/events.jsonl` a `.gitignore` y al fragmento de plantilla si se crea escritura futura de eventos.
- [x] Paso 5 — Agregar tests en `tests/test_metrics.py` usando repos temporales.
- [x] Paso 6 — Actualizar docs si el contrato final difiere del roadmap.
- [x] Paso 7 — Correr `tools/continuum doctor` y `python3 -m unittest discover -s tests -t . -v`.

## Estado actual
Implementación completada. 57 tests pasados OK y `continuum doctor` verificado sin advertencias ni errores.
