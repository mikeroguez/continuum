# Handoff: bilingual-documentation

**Fecha:** 2026-09-10 · **Rol:** documentación

## Objetivo

Establecer documentación bilingüe sostenible para Continuum, conservando el
español como fuente canónica y ofreciendo una ruta de incorporación en inglés.

## Archivos revisados

- `README.md`, `CONTRIBUTING.md`, `ARCHITECTURE.md`
- `AI_COLLABORATION.md`, `docs/research-protocol.md`
- `docs/ux-metrics-roadmap.md` y la estructura de `docs/`

## Archivos modificados

- `README.md`, `README.en.md`
- `CONTRIBUTING.md`, `CONTRIBUTING.en.md`
- `docs/LANGUAGE_POLICY.md`, `docs/LANGUAGE_POLICY.en.md`
- `docs/en/README.md`

## Decisión(es) tomada(s)

- El español conserva la autoridad editorial.
- README y guía de contribución tienen paridad de incorporación en inglés.
- La documentación especializada queda canónica en español y se orienta en
  inglés desde un índice; sus traducciones completas esperan estabilidad y la
  revisión pertinente de material de investigación.

## Suposiciones vigentes

- El equipo inicial seguirá trabajando principalmente en español.
- Un paper futuro puede requerir proteger hipótesis, protocolo y resultados
  hasta su publicación.

## Validación

- Ejecutada: `git diff --check`; comprobación de enlaces locales;
  `tools/continuum doctor` (0 críticos, 0 advertencias);
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -t . -v`
  (93 pruebas correctas).
- No ejecutada / pendiente: revisión humana de estilo de las traducciones.

## Riesgos / dudas abiertas

- Los documentos especializados no tienen aún traducción inglesa completa; el
  índice declara ese límite de manera explícita.
- Cambios futuros a un documento emparejado exigen revisar su equivalente.

## Siguiente paso recomendado

Revisar el diff editorial y, cuando se apruebe, hacer un commit de
documentación. Antes de traducir protocolos o métricas, definir la estrategia
de publicación del paper.
