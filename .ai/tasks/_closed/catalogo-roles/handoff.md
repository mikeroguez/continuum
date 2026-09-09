# Handoff: catalogo-roles

**Fecha:** 2026-09-09 · **Rol:** orquestador (coordinó las piezas de esta tarea)

## Objetivo

Construir un catálogo de roles/personas versionado, definido conversacionalmente
con el usuario a lo largo de varios turnos (software, investigación,
contenido educativo, con énfasis en UCD/JTBD dado el contexto de software
educativo universitario), más la mecánica para usarlo desde el CLI.

## Archivos revisados

Los 23 archivos de rol propuestos y acordados en la conversación antes de
escribirlos; `template/tools/_continuum/{tasks,handoff,doctor,__main__}.py`
para decidir dónde enganchar `--role` sin duplicar estado.

## Archivos modificados

- `.ai/roles/<pack>/<slug>.md` × 23 (comun=9, software=6, investigacion=3,
  contenido-educativo=5), en `template/` y sincronizados a la raíz.
- `template/tools/_continuum/roles.py` (nuevo): `discover_roles`,
  `find_role`, `list_roles`, `sync` (subagentes de Claude Code).
- `common.py` (config `roles.dir`/`roles.packs`), `doctor.py` (valida packs
  activos), `tasks.py`/`handoff.py` (`--role`), `__main__.py` (subcomando
  `roles list`/`roles sync`).
- Plantillas `TASK.md`/`HANDOFF.md`: nuevo campo "Rol" en el encabezado.
- `.ai/config.json` (raíz): `roles.packs: ["comun", "software"]`.
- `.gitignore` + fragmento de plantilla: `.claude/agents/` (generado, no se
  commitea).
- Docs: `AI_COLLABORATION.md` §9, `ARCHITECTURE.md` (Capa 2 + párrafo),
  `docs/decision-log.md` ADR-009, `README.md`, `CHANGELOG.md`, temas
  `arquitectura.md`/`comandos.md`.
- `tests/test_roles.py` (nuevo) + extensiones en `test_tasks.py`/`test_handoff.py`.

## Decisión tomada

Roles como personas versionadas que una sesión adopta por tarea — no
agentes concurrentes (consistente con ADR-003). `.claude/agents/` se generó
como artefacto de `continuum roles sync` y se decidió **no commitearlo**
para que nunca pueda divergir del canónico en `.ai/roles/` — mismo tipo de
riesgo de duplicación que ya se había combatido en otros lados del proyecto
(CHANGELOG duplicado, `docs/estado-dev.md` obsoleto).

## Suposiciones vigentes

El catálogo de 23 roles se definió por criterio conversacional (evidencia
de los proyectos reales del usuario cuando existía: seguridad, DevOps,
normativa curricular; criterio general cuando no: UX Research separado de
diseño, metodólogo). No se ha usado todavía en una tarea real fuera de esta
misma — validar en la práctica si el catálogo es el correcto una vez que se
use, y podar lo que no se use.

## Validación

- **Ejecutada:** 53/53 tests (`python3 -m unittest discover -s tests -t .`),
  `continuum doctor` en 0 problemas/0 advertencias, `roles sync` probado
  generando 15 subagentes reales con frontmatter válido, `--role` probado
  en `task start` (rol existente e inexistente) y en `handoff` manual/auto.
- **No ejecutada:** no se probó `roles sync` dentro de una sesión real de
  Claude Code invocando uno de los subagentes generados (solo se verificó
  que el archivo se genera con el formato correcto).

## Riesgos / dudas abiertas

23 roles es un catálogo amplio — el riesgo real no es de ceremonia (los
packs inactivos no cuestan nada), sino de que algunos terminen sin usarse
nunca. Revisar en unos meses cuáles se usaron de verdad vía
`grep -r "Rol:" .ai/tasks/_closed/*/task.md` y podar los que no.

## Siguiente paso recomendado

Ninguno bloqueante. La próxima vez que se inicie una tarea real de
software, usar `--role <slug>` y ver si el catálogo se siente correcto en
la práctica antes de agregar más roles.
