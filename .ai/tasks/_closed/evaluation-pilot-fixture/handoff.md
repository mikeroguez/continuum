# Handoff: evaluation-pilot-fixture

**Fecha:** 2026-09-10 · **Rol:** evaluación

## Objetivo

Construir un piloto local para comprobar la instrumentación de un relevo entre
sesiones bajo las condiciones A, B y C del protocolo.

## Archivos revisados

- `docs/research-protocol.md`
- `docs/evaluation-plan.md`
- `template/`

## Archivos modificados

- `evaluation/pilot/`
- `tests/test_evaluation_pilot.py`
- `.gitignore`

## Decisión(es) tomada(s)

- El fixture es un proyecto Python sin dependencias ni red, con un estado
  parcial deliberado y pruebas de aceptación separadas.
- `prepare_trial.py` nunca sobrescribe un directorio existente y crea A, B o C
  desde el mismo baseline; C instala la plantilla real y un handoff específico.
- `verify_trial.py` registra únicamente campos mínimos permitidos en un archivo
  local ignorado por Git.

## Suposiciones vigentes

- Los ensayos con agentes se harán en sesiones nuevas, con directorios y
  conversaciones aisladas, antes de atribuir cualquier resultado a una
  condición.

## Validación

- Ejecutada: tres pruebas del piloto (estado compartido, fallo esperado y
  solución correcta), suite completa de 96 pruebas, `git diff --check` y
  `tools/continuum doctor` (0 problemas, 0 advertencias).
- No ejecutada / pendiente: ensayos reales con agentes sucesores y revisión de
  privacidad del registro antes de cualquier exportación.

## Riesgos / dudas abiertas

- El piloto confirma la instrumentación, no la eficacia ni el tamaño de un
  efecto. Sus resultados no deben mezclarse con una muestra confirmatoria.

## Siguiente paso recomendado

Ejecutar cada condición con agentes o personas independientes siguiendo
`evaluation/pilot/README.md`; comprobar primero integridad y privacidad. Solo
después decidir cambios al harness y, antes de una fase confirmatoria,
prerregistrar presupuesto, aleatorización, exclusiones y análisis.
