# Tarea: sprint-8-evidencia-publicacion

**Creada:** 2026-09-09 · **Tamaño:** medium · **Owner:** gemini · **Rol:** Backend (`software/backend`)

## Objetivo
Implementar los comandos de análisis de métricas locales y exportación de evidencia (`continuum metrics report`, `continuum metrics export` y `continuum metrics compare`), y crear la documentación del protocolo de investigación en `docs/research-protocol.md`.

## Incluido en el alcance
- Subcomandos de `metrics`:
  - `metrics report`: Genera un informe Markdown estructurado con tendencias de consumo de tokens, estado de memoria viva y nivel de continuidad.
  - `metrics export`: Exporta los datos a JSON o CSV con opción `--anonymize` para eliminar rutas absolutas y nombres de usuario.
  - `metrics compare`: Compara el estado o snapshot actual contra el baseline inicial.
- Documento `docs/research-protocol.md` (y `template/docs/research-protocol.md` si aplica).
- Pruebas unitarias en `tests/test_metrics_evidence.py`.
- Documentación en `README.md` y `.ai/state/topics/comandos.md`.

## Explícitamente fuera de alcance
- Telemetría remota activa.
- Envío automático de datos por red.

## Write-set (archivos que se espera tocar)
- `template/tools/_continuum/metrics.py`
- `template/tools/_continuum/__main__.py`
- `tools/_continuum/metrics.py`
- `tools/_continuum/__main__.py`
- `docs/research-protocol.md`
- `tests/test_metrics_evidence.py`
- `README.md`
- `.ai/state/topics/comandos.md`
- `.ai/tasks/sprint-8-evidencia-publicacion/*`
- `.ai/HANDOFF.md`

## Fuentes de verdad a leer antes de empezar
- `.ai/state/estado-dev.md`
- `docs/ux-metrics-sprints.md` (Sprint 8)
- `tools/_continuum/metrics.py`

## Criterios de salida
- `continuum metrics report` emite un informe estructurado legible o en JSON.
- `continuum metrics export --anonymize` anonimiza campos sensibles como rutas absolutas.
- `continuum metrics compare` resume la evolución vs baseline.
- Todos los tests unitarios pasan (`python3 -m unittest discover -s tests -t . -v`).
- `python3 tools/continuum doctor` pasa limpio.
