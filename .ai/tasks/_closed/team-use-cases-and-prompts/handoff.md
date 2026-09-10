# Handoff: team-use-cases-and-prompts

**Fecha:** 2026-09-10 · **Rol:** documentación

## Objetivo

Convertir las guías instalables en un manual práctico para equipos de
desarrollo con personas y varios asistentes.

## Archivos revisados

- `AI_COLLABORATION.md`
- `template/docs/como-usar-continuum.md`
- `template/docs/using-continuum.md`

## Archivos modificados

- `template/docs/como-usar-continuum.md`
- `template/docs/using-continuum.md`

## Decisión(es) tomada(s)

- Los ejemplos viven en el manual de personas, no en el protocolo canónico,
  para mantener liviano el contexto de arranque.
- Cada prompt define resultado, límites y autorización, y remite al protocolo,
  handoff y contexto del repositorio en vez de duplicarlos.
- Los casos cubren inicio, continuidad, trabajo paralelo, revisión y cierre.

## Suposiciones vigentes

- La persona usuaria conserva la autoridad sobre commits, merges y
  publicaciones salvo que autorice expresamente otra cosa.

## Validación

- Ejecutada: equivalencia editorial español/inglés, `git diff --check` y
  `tools/continuum doctor` (0 problemas y 0 advertencias).
- No ejecutada / pendiente: revisión humana del conjunto completo de
  documentación y, si se aprueba publicación, validación de release.

## Riesgos / dudas abiertas

- Los prompts son plantillas: cada equipo debe concretar el objetivo, el
  alcance y la autorización; no sustituyen coordinación ni revisión humana.

## Siguiente paso recomendado

Revisar los nuevos casos y prompts junto con los demás cambios pendientes de
documentación. Si se aprueban, incluirlos en el commit y decidir la siguiente
versión de la plantilla antes de generar `export` o publicar.
