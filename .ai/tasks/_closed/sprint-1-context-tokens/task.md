# Tarea: sprint-1-context-tokens

**Creada:** 2026-09-09 · **Tamaño:** medium · **Owner:** (sin asignar) · **Rol:** Backend (`software/backend`)

## Objetivo
Implementar los comandos que reducen costo de contexto al inicio de una sesion:
`continuum context` indica que leer y que evitar; `continuum tokens` muestra el
presupuesto de tokens sin obligar a ejecutar `doctor` completo.

## Incluido en el alcance
- `continuum context` con categorias de lectura.
- `continuum context --why`.
- `continuum context --task <slug>`.
- `continuum context --json`.
- `continuum tokens` con desglose de arranque, handoff, indice y temas.
- Reglas anti-bloat iniciales en `doctor` o helpers compartidos.
- Tests unitarios para salida humana y JSON.
- Documentacion corta.

## Explícitamente fuera de alcance
- `doctor --fix`.
- `status`.
- `session start/end`.
- Seleccion semantica avanzada de temas con IA.
- Telemetria remota.
- Modificar el protocolo canónico salvo que una prueba demuestre una brecha.

## Write-set (archivos que se espera tocar)
No editar fuera de esta lista sin actualizarla primero. Evita refactors oportunistas.

- `template/tools/_continuum/context.py`
- `template/tools/_continuum/metrics.py`
- `template/tools/_continuum/doctor.py`
- `template/tools/_continuum/__main__.py`
- `tools/_continuum/context.py`
- `tools/_continuum/metrics.py`
- `tools/_continuum/doctor.py`
- `tools/_continuum/__main__.py`
- `tests/test_context.py`
- `tests/test_metrics.py`
- `README.md`
- `.ai/state/topics/comandos.md`
- `.ai/tasks/sprint-1-context-tokens/*`
- `.ai/HANDOFF.md`

## Fuentes de verdad a leer antes de empezar
- `.ai/state/estado-dev.md`
- `docs/ux-metrics-roadmap.md`
- `docs/ux-metrics-sprints.md` Sprint 1
- `.ai/tasks/sprint-0-baseline-metricas/task.md`
- `tools/_continuum/doctor.py`
- `tools/_continuum/tasks.py`
- `tools/_continuum/common.py`
- `tests/test_doctor.py`
- `tests/test_tasks.py`

## Contexto mínimo sugerido
Según el tamaño declarado arriba, no cargues más de lo necesario:

| Tamaño  | Techo de lectura inicial orientativo |
|---------|----------------------------------------|
| small   | 1-3 archivos concretos, sin explorar carpetas completas |
| medium  | 1 módulo/dominio, usar `rg`/`grep` para localizar antes de leer |
| large   | fragmentar con `continuum packetize`; considerar dividir en subtareas |

## Dependencias

- Idealmente implementar despues de `sprint-0-baseline-metricas`, para
  reutilizar el snapshot y evitar duplicar calculo de tokens.

## Criterios de salida

- `tools/continuum context` muestra una lista corta de archivos obligatorios,
  recomendados, bajo demanda y evitables por ahora.
- `tools/continuum context --task <slug>` incorpora la tarea si existe y falla
  con mensaje claro si no existe.
- `tools/continuum context --json` emite estructura estable.
- `tools/continuum tokens` muestra presupuesto de arranque y desglose por
  memoria.
- `doctor` mantiene salida compacta y no duplica el reporte completo de
  `tokens`.
- Tests cubren repos sin `.ai`, repo minimo, tarea existente y memoria obesa.
- `python3 -m unittest discover -s tests -t . -v` pasa.
- `tools/continuum doctor` pasa.
