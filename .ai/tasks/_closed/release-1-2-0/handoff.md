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
- Pendiente: ninguna.

## Riesgos / dudas abiertas

- El archivo archivado previo no relacionado se excluyó usando un árbol de
  trabajo limpio para generar la distribución.

## Siguiente paso recomendado

El release se publicó: `main` contiene el commit de versión, `export` se
regeneró desde `template/`, el tag `v1.2.0` apunta a esa exportación y GitHub
incluye el release público con las notas del changelog.
