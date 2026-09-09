# Tarea: sprint-0-baseline-metricas

**Creada:** 2026-09-09 · **Tamaño:** medium · **Owner:** (sin asignar) · **Rol:** Producto (Jobs to be Done) (`software/producto-jtbd`)

## Objetivo
Definir e implementar la linea base minima de metricas locales de Continuum
antes de modificar la UX del CLI. El resultado debe permitir medir tokens,
estado de memoria y friccion basica sin pedir datos manuales ni activar
telemetria remota.

## Incluido en el alcance
- `metrics snapshot --dry-run` como comando de baseline local.
- Esquema de snapshot y eventos locales.
- Clasificacion de metricas en automaticas, opcionales e investigacion.
- Checklist heuristico para evaluar comandos nuevos.
- Tests unitarios del snapshot minimo.
- Documentacion corta del uso de baseline.

## Explícitamente fuera de alcance
- Reportes historicos completos.
- Export CSV/JSON.
- Anonimizacion avanzada.
- Encuestas, entrevistas o diarios de investigacion.
- Telemetria remota.
- Implementar `context` o `tokens` completos; eso pertenece a
  `sprint-1-context-tokens`.

## Write-set (archivos que se espera tocar)
No editar fuera de esta lista sin actualizarla primero. Evita refactors oportunistas.

- `template/tools/_continuum/metrics.py`
- `template/tools/_continuum/__main__.py`
- `tools/_continuum/metrics.py`
- `tools/_continuum/__main__.py`
- `tests/test_metrics.py`
- `docs/ux-metrics-roadmap.md`
- `docs/ux-metrics-sprints.md`
- `.gitignore`
- `template/.gitignore-continuum-fragment`
- `.ai/tasks/sprint-0-baseline-metricas/*`
- `.ai/HANDOFF.md`

## Fuentes de verdad a leer antes de empezar
- `.ai/state/estado-dev.md`
- `docs/ux-metrics-roadmap.md`
- `docs/ux-metrics-sprints.md` Sprint 0
- `tools/_continuum/doctor.py`
- `tools/_continuum/common.py`
- `tests/helpers.py`

## Contexto mínimo sugerido
Según el tamaño declarado arriba, no cargues más de lo necesario:

| Tamaño  | Techo de lectura inicial orientativo |
|---------|----------------------------------------|
| small   | 1-3 archivos concretos, sin explorar carpetas completas |
| medium  | 1 módulo/dominio, usar `rg`/`grep` para localizar antes de leer |
| large   | fragmentar con `continuum packetize`; considerar dividir en subtareas |

## Criterios de salida

- `tools/continuum metrics snapshot --dry-run` imprime un snapshot humano sin
  escribir archivos.
- `tools/continuum metrics snapshot --json --dry-run` emite JSON estable para
  pruebas y automatizacion.
- El snapshot incluye commit, rama, tokens de arranque, lineas/tokens de
  memoria, tareas abiertas/cerradas, edad del handoff y estado de hooks.
- `.ai/metrics/events.jsonl` queda ignorado por git si se introduce la ruta.
- No se pide ninguna pregunta al usuario en el flujo normal.
- `python3 -m unittest discover -s tests -t . -v` pasa.
- `tools/continuum doctor` pasa.
