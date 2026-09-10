# Tarea: evaluation-pilot-fixture

**Creada:** 2026-09-10 · **Tamaño:** large · **Owner:** (sin asignar) · **Rol:** (sin asignar)

## Objetivo
Crear un proyecto piloto aislado que permita verificar la restauración de un
estado parcial y las condiciones A/B/C antes de cualquier estudio de eficacia.

## Incluido en el alcance
- Una tarea de software pequeña con pruebas de aceptación reproducibles.
- Preparación aislada de las condiciones control, guía mínima y Continuum.
- Registro local mínimo y guion de ejecución para una persona evaluadora.

## Explícitamente fuera de alcance
- Ejecutar ensayos confirmatorios, recolectar conversaciones o publicar datos.
- Afirmar eficacia de Continuum a partir del piloto.

## Write-set (archivos que se espera tocar)
No editar fuera de esta lista sin actualizarla primero. Evita refactors oportunistas.

- `evaluation/pilot/**`
- `tests/test_evaluation_pilot.py`
- `.gitignore`
- `.ai/tasks/evaluation-pilot-fixture/*`
- `.ai/HANDOFF.md`

## Fuentes de verdad a leer antes de empezar
- `.ai/state/estado-dev.md`
- `docs/research-protocol.md`
- `docs/evaluation-plan.md`

## Contexto mínimo sugerido
Según el tamaño declarado arriba, no cargues más de lo necesario:

| Tamaño  | Techo de lectura inicial orientativo |
|---------|----------------------------------------|
| small   | 1-3 archivos concretos, sin explorar carpetas completas |
| medium  | 1 módulo/dominio, usar `rg`/`grep` para localizar antes de leer |
| large   | fragmentar con `continuum packetize`; considerar dividir en subtareas |
