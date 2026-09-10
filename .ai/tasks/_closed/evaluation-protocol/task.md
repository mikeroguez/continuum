# Tarea: evaluation-protocol

**Creada:** 2026-09-10 · **Tamaño:** medium · **Owner:** (sin asignar) · **Rol:** (sin asignar)

## Objetivo
Convertir el protocolo de investigación de Continuum en un diseño
prerregistrable que mida continuidad tras interrupciones sin adelantar ni
inventar resultados.

## Incluido en el alcance
- Revisar hipótesis, condiciones, métricas, análisis y privacidad.
- Añadir un plan operativo para implementar el harness en una tarea posterior.
- Alinear la hoja de ruta y el índice de documentación.

## Explícitamente fuera de alcance
- Implementar el harness, recolectar datos o modificar telemetría.
- Publicar resultados, un preprint o materiales de participantes.

## Write-set (archivos que se espera tocar)
No editar fuera de esta lista sin actualizarla primero. Evita refactors oportunistas.

- `docs/research-protocol.md`, `docs/evaluation-plan.md`
- `docs/ux-metrics-roadmap.md`, `docs/en/README.md`
- `.ai/tasks/evaluation-protocol/*`, `.ai/HANDOFF.md`

## Fuentes de verdad a leer antes de empezar
- `.ai/state/estado-dev.md`
- _(rutas específicas relevantes a esta tarea)_

## Contexto mínimo sugerido
Según el tamaño declarado arriba, no cargues más de lo necesario:

| Tamaño  | Techo de lectura inicial orientativo |
|---------|----------------------------------------|
| small   | 1-3 archivos concretos, sin explorar carpetas completas |
| medium  | 1 módulo/dominio, usar `rg`/`grep` para localizar antes de leer |
| large   | fragmentar con `continuum packetize`; considerar dividir en subtareas |
