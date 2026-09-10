# Plan de ejecución: release-1-2-0

Solo para tareas `medium`/`large`. Es una cola persistente de pasos: márcalos
al avanzar para que, si la sesión se corta a medio camino, la siguiente sepa
exactamente dónde retomar sin releer todo desde cero.

- [x] Paso 1 — Identificar la versión requerida y preparar metadatos.
- [x] Paso 2 — Validar el release y preparar la rama export y el tag.
- [x] Paso 3 — Publicar el release público y cerrar el registro de tarea.

## Estado actual
Completado. La rama `export`, el tag `v1.2.0` y el release de GitHub se
publicaron después de validar las 93 pruebas y `continuum doctor`.
