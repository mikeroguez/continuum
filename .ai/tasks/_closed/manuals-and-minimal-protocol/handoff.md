# Handoff: manuals-and-minimal-protocol

**Fecha:** 2026-09-10 · **Rol:** documentación

## Objetivo

Afinar Continuum según evidencia sobre instrucciones de agentes y añadir guías
instalables para personas y agentes.

## Archivos modificados

- `AI_COLLABORATION.md`, `template/AI_COLLABORATION.md`
- `README.md`, `README.en.md`, `docs/LANGUAGE_POLICY*.md`
- `template/docs/README.md` y cuatro guías bilingües

## Decisión(es) tomada(s)

- El protocolo mantiene reglas operativas y comandos; el detalle se consulta en
  manuales bajo demanda.
- Las reglas críticas y repetidas se orientan hacia pruebas, hooks, linters o
  CI, en vez de crecer como prosa.
- El catálogo explicativo de roles salió del arranque y quedó en la guía para
  agentes.

## Validación

- Ejecutada: enlaces locales, `git diff --check`, `tools/continuum doctor`
  (0 problemas), `tools/continuum tokens` (arranque de ~3,051 a ~2,886 tokens)
  y 93 pruebas automatizadas correctas.
- Pendiente: revisión humana, commit y release de la plantilla si se aprueba.

## Riesgos / dudas abiertas

- La reducción de contexto es una mejora de diseño, no evidencia de eficacia;
  el protocolo experimental debe evaluarlo mediante el harness futuro.
- Cambiar `template/` requerirá una nueva versión y regenerar `export` al
  publicar.

## Siguiente paso recomendado

Revisar manuales y protocolo. Si se aprueban, incluir también los borradores
del protocolo experimental en un commit de documentación y decidir una versión
menor para la plantilla distribuible.
