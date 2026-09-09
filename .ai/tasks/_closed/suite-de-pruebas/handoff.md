# Handoff: suite-de-pruebas

**Fecha:** 2026-09-09

## Objetivo

Construir una suite de tests automatizada para `template/tools/_continuum/`,
que hasta ahora solo se había validado a mano.

## Archivos revisados

Los 8 módulos de `template/tools/_continuum/` (`common.py`, `doctor.py`,
`tasks.py`, `handoff.py`, `memory.py`, `packets.py`, `bootstrap.py`,
`__main__.py`).

## Archivos modificados

- `tests/` (nuevo): `helpers.py`, `test_common.py`, `test_doctor.py`,
  `test_tasks.py`, `test_handoff.py`, `test_memory.py`, `test_packets.py`,
  `test_bootstrap.py` — 39 tests, stdlib `unittest`, sin dependencias nuevas.
- `.github/workflows/tests.yml` (nuevo, solo en la raíz — `tests/` no se
  distribuye a proyectos que incorporan Continuum).
- `CONTRIBUTING.md`: sección "Tests".
- `README.md`: badge de tests.
- `CHANGELOG.md`, `.ai/state/topics/pendientes.md`,
  `.ai/state/topics/comandos.md`: actualizados.

## Decisión tomada

Los tests importan `_continuum` directo desde `template/tools/` (la fuente
de verdad, no la copia autoalojada en la raíz), y corren contra copias
temporales de la carga útil de `template/` — sin copiar el código de
`tools/` a esas copias, salvo en el único test que necesita el CLI real en
disco (`test_hook_actually_runs_on_commit`, porque el propio hook invoca
`tools/continuum` por ruta).

## Suposiciones vigentes

- La plantilla siempre ships `.ai/HANDOFF.md` y los 5 temas por defecto con
  contenido no vacío — varios tests tuvieron que tenerlo en cuenta
  explícitamente (ver "Validación" abajo).

## Validación

- **Ejecutada:** `python3 -m unittest discover -s tests -t . -v` → 39/39
  OK. `continuum doctor` sigue en cero problemas críticos.
- **No ejecutada:** no se corrió todavía en el runner real de GitHub
  Actions (el workflow se agregó pero no hay push aún al momento de escribir
  este handoff).

## Riesgos / dudas abiertas

Ninguno nuevo. Se documentan aquí, para quien retome esto, dos hallazgos
del propio proceso de escribir los tests (no bugs nuevos, aclaraciones):

1. `doctor.warn()`/`doctor.err()` escriben a stderr, no a stdout — cualquier
   test o script que capture salida de `continuum doctor` necesita capturar
   ambos flujos, no solo stdout.
2. Las funciones de `common.py` que dependen de `git` (p. ej. `repo_root()`,
   `is_tracked()`) usan el cwd del proceso de forma implícita, no un
   parámetro explícito — los tests que las ejercitan necesitan `os.chdir()`
   al repositorio temporal (`tests/helpers.py` ya lo resuelve).

## Siguiente paso recomendado

Ninguno bloqueante. Cuando se agregue un subcomando nuevo a `continuum` o se
corrija un bug, agregar su test en el módulo correspondiente antes de cerrar
esa tarea — ver `CONTRIBUTING.md` § Tests.
