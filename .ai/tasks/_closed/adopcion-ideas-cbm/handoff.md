# Handoff: adopcion-ideas-cbm

**Fecha:** 2026-09-12 · **Rol:** (sin asignar)

## Objetivo
Análisis comparativo con el proyecto externo
[`codebase-memory-mcp`](https://github.com/DeusData/codebase-memory-mcp)
(CBM) para identificar ideas adaptables a Continuum, seguido de una
investigación dedicada (con el rigor de `docs/investigacion-2026.md`) antes
de implementar nada, la implementación de lo que sobrevivió esa
investigación, y dos extensiones agregadas a pedido explícito del owner
después del primer cierre de la tarea. Todo el trabajo vive en
`.ai/tasks/adopcion-ideas-cbm/` (`task.md` + `execution-plan.md`, 11 pasos,
todos hechos).

## Archivos revisados
- Todo `codebase-memory-mcp` en `~/Projects/Personal/codebase-memory-mcp`
  (README.md, docs/MEASURING_SAVINGS.md, docs/CONFIGURATION.md).
- `ARCHITECTURE.md` completo — usado como criterio de admisión de cada idea.
- `docs/decision-log.md`, `docs/investigacion-2026.md`,
  `.ai/state/topics/*.md`.

## Archivos modificados
Ver el write-set completo en `.ai/tasks/adopcion-ideas-cbm/task.md`. Resumen:
`AI_COLLABORATION.md` + espejo, `tools/_continuum/{context,doctor,metrics,
common,adr,__main__}.py` + espejos (`adr.py` es nuevo), `.github/
copilot-instructions.md` + espejo (huella sha256 recalculada varias veces),
`docs/decision-log.md` (ADR-012), `docs/investigacion-2026.md` (§10),
`docs/metodologia-medicion.md` + `template/docs/metodologia-medicion.md`
(nuevos), `README.md` + `README.en.md`, `.ai/state/topics/pendientes.md`,
`tests/test_context.py`, `tests/test_doctor.py`, `tests/test_adr.py` (nuevo),
`tests/test_status_fix.py` (14 tests nuevos en total).

## Decisión(es) tomada(s)
De 7 ideas candidatas de CBM: 5 adoptadas (2 con ajustes de diseño), 2
descartadas — ver `docs/decision-log.md` ADR-012 para el razonamiento
completo. Más dos extensiones agregadas después, a pedido del owner:

1. `continuum context` vuelca el contenido completo de
   `AI_COLLABORATION.md`/`estado-dev.md`/`HANDOFF.md` en `SessionStart`,
   pero no el de los entrypoints por proveedor (ya los carga el cliente
   nativamente).
2. `.gitattributes merge=ours` en `HANDOFF.md` se descartó (arriesgaba
   perder handoffs en silencio); reemplazado por verificación en `doctor`
   de marcadores de conflicto sin resolver.
3. Verificación de numeración de ADRs en `doctor`, cubriendo **las dos
   convenciones** del protocolo (`docs/decision-log.md` y
   `docs/architecture/ADR-*.md`).
4. `docs/metodologia-medicion.md`, documento opt-in.
5. Frase de postura de confianza en el README (ambos idiomas).
6. Contrato de evidencia por tamaño de tarea: descartado — no verificable
   mecánicamente en Continuum.
7. `continuum init --detect`: descartado por completo — el problema que
   resuelve en CBM no existe en la arquitectura de Continuum.
8. **[extensión agregada tras el cierre inicial]** `continuum adr new
   "<título>"` — calcula el siguiente número libre y escribe en la
   convención que el proyecto ya use. Requirió mover
   `collect_adr_numbers`/`adr_numbering_issues`/`slugify` de `doctor.py` a
   `common.py` (refactor, ambos módulos los comparten ahora).
9. **[extensión agregada tras el cierre inicial]** `continuum doctor --fix
   --no-dry-run` ahora corrige solo la huella sha256 de
   `.github/copilot-instructions.md` cuando queda vieja, sin tocar su prosa
   — automatiza el efecto colateral que esta misma tarea encontró y corrigió
   a mano varias veces antes de esta extensión. Validado en producción real:
   se usó para corregir la huella que la propia edición del punto 8 había
   dejado stale.

## Suposiciones vigentes
- La aplicación piloto de `docs/metodologia-medicion.md` sobre uno de los 4
  proyectos reales dependientes (nombres omitidos por privacidad) no se
  ejecutó — es trabajo de seguimiento explícitamente fuera de esta tarea.
- El auto-fix de la huella sha256 solo alcanza a la copia de la raíz de
  este repositorio: `template/.github/copilot-instructions.md` sigue
  necesitando el ajuste a mano al sincronizar `template/AI_COLLABORATION.md`
  (`doctor` siempre opera sobre la raíz git, nunca sobre `template/`). Es
  una limitación conocida y aceptada, específica de la doble copia
  autoalojada de este repositorio — un proyecto que solo consume la
  plantilla no la tiene.

## Validación
- Ejecutada: `python3 -m unittest discover -s tests -t .` → 131 tests, 0
  fallos. `tools/continuum doctor` → 0 problemas críticos (1 advertencia
  esperada e informativa: 2 tareas activas en serie sin worktree).
  `continuum doctor --fix --no-dry-run` probado en producción real sobre
  este mismo repositorio, no solo en tests.
- No ejecutada / pendiente: piloto real de `docs/metodologia-medicion.md`
  (ver "Suposiciones vigentes").

## Riesgos / dudas abiertas
- El presupuesto de arranque subió de ~3.280 a ~4.490 tokens a lo largo de
  la tarea (esperado, documentado en ADR-012 "Consecuencias" — no es una
  regresión de eficiencia, la métrica ahora es exacta, y buena parte del
  incremento final es el propio `HANDOFF.md` detallado de esta sesión, que
  la próxima sesión debería reemplazar por uno más corto en cuanto cierre
  su propio trabajo). Efecto colateral no buscado y sin corregir, fuera de
  alcance: `continuum metrics report` tiene un techo hardcodeado de 3500
  tokens (`tools/_continuum/metrics.py:151`) que ahora se reporta excedido.

## Siguiente paso recomendado
La tarea `adopcion-ideas-cbm` está completa: 11 pasos del execution-plan,
todos hechos, sin trabajo bloqueado. Cerrar con `continuum task close
adopcion-ideas-cbm` cuando el owner lo confirme. Repositorio limpio de
trabajo a medias: no hay tests fallando ni `doctor` en rojo.
