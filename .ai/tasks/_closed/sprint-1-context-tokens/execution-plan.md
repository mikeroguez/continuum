# Plan de ejecución: sprint-1-context-tokens

Implementar despues de Sprint 0 salvo que se decida fusionar ambos en una sola
rama de trabajo.

- [x] Paso 1 — Revisar implementacion de metricas/snapshot creada en Sprint 0.
- [x] Paso 2 — Diseñar estructura de `ContextItem` con categoria, ruta, tokens estimados y razon.
- [x] Paso 3 — Implementar seleccion base: entrypoints, handoff, indice y temas bajo demanda.
- [x] Paso 4 — Implementar `--task <slug>` leyendo `task.md` y `execution-plan.md` si existen.
- [x] Paso 5 — Implementar `--why` y `--json`.
- [x] Paso 6 — Implementar `tokens` reutilizando los calculos de snapshot.
- [x] Paso 7 — Agregar warnings anti-bloat no bloqueantes.
- [x] Paso 8 — Agregar tests de contexto, tokens y casos sin `.ai`.
- [x] Paso 9 — Actualizar documentacion corta y memoria de comandos.
- [x] Paso 10 — Correr `tools/continuum doctor` y `python3 -m unittest discover -s tests -t . -v`.

## Estado actual
Implementación completada. 63 tests pasados OK y `continuum doctor` verificado sin advertencias ni errores.
