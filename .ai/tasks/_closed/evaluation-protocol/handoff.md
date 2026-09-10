# Handoff: evaluation-protocol

**Fecha:** 2026-09-10 · **Rol:** investigación

## Objetivo

Transformar el protocolo de Continuum en un diseño prerregistrable que evalúe
relevos de sesión sin adelantar ni inventar eficacia.

## Archivos modificados

- `docs/research-protocol.md`
- `docs/evaluation-plan.md`
- `docs/ux-metrics-roadmap.md`, `docs/en/README.md`

## Decisión(es) tomada(s)

- Se reemplazó la hipótesis fija de reducción del 40% por comparaciones entre
  control, guía mínima y Continuum.
- La unidad de análisis es un agente sucesor que retoma el mismo árbol parcial
  congelado bajo condiciones distintas.
- El CLI actual se declara explícitamente insuficiente como harness
  experimental; no se implementaron ni se recolectaron datos.

## Validación

- Ejecutada: `git diff --check`, comprobación de referencias locales y
  `tools/continuum doctor` (0 problemas, 0 advertencias).
- Pendiente: revisión humana, prerregistro y creación de un harness probado.

## Riesgos / dudas abiertas

- La selección de tareas, presupuesto, tamaño de muestra y margen de no
  inferioridad no pueden fijarse hasta completar un piloto de instrumentación.
- Datos de repositorios privados o de personas requieren consentimiento y la
  revisión ética aplicable antes de cualquier recolección.

## Siguiente paso recomendado

Revisar y aprobar el diseño. Si se aprueba, crear una tarea separada para el
harness de piloto, sin iniciar todavía la fase confirmatoria.
