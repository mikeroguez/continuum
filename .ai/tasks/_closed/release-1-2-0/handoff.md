# Handoff: release-1-2-0

**Fecha:** 2026-09-10 · **Rol:** release

## Objetivo

Liberar Continuum 1.2.0 para distribuir el soporte de `template_branch` en
`continuum sync`.

## Archivos modificados

- `template/tools/_continuum/__init__.py`
- `tools/_continuum/__init__.py`
- `CHANGELOG.md`, `README.en.md`

## Decisión(es) tomada(s)

Se eligió una versión menor porque `template_branch` añade una capacidad
retrocompatible a la plantilla distribuible; el valor predeterminado conserva
el comportamiento de `export`.

## Validación

- Ejecutada: `tools/continuum doctor` (0 problemas y 0 advertencias);
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -t . -v`
  (93 pruebas correctas); `git diff --check`.
- Pendiente: regenerar `export`, crear el tag `v1.2.0` y publicar el release.

## Riesgos / dudas abiertas

- Un archivo archivado previo no relacionado permanece sin seguimiento en el
  árbol de trabajo principal; el release debe ejecutarse desde un árbol limpio
  para excluirlo.

## Siguiente paso recomendado

Publicar el commit de versión, regenerar `export` desde un árbol limpio,
etiquetar `v1.2.0` y crear el release público con las notas del changelog.
