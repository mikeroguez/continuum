# Tarea: sprint-6-release-meta

**Creada:** 2026-09-09 · **Tamaño:** medium · **Owner:** gemini · **Rol:** Backend (`software/backend`)

## Objetivo
Automatizar el proceso de preparación y liberación (*release*) del propio proyecto Continuum (`export status`, `export refresh` y `release <version>`), validando la consistencia entre SemVer, `CHANGELOG.md`, la rama `export` y los tags anotados.

## Incluido en el alcance
- Subcomandos `export`:
  - `export status`: Audita el estado de la rama `export` vs `template/`.
  - `export refresh`: Regenera la rama `export` local con `git subtree split --prefix=template -b export` (con `--dry-run` por defecto y `--no-dry-run`).
- Subcomando `release <version>`:
  - Valida formato SemVer de la versión.
  - Verifica presencia de la entrada en `CHANGELOG.md`.
  - Ejecuta validaciones previas (`doctor` y `unittest`).
  - Prepara o verifica el tag de release en modo seguro idempotente.
- Pruebas unitarias en `tests/test_release_cmd.py`.
- Documentación en `README.md` y `.ai/state/topics/comandos.md`.

## Explícitamente fuera de alcance
- `git push` forzado a remotos sin confirmación explícita.
- Creación remota de releases en GitHub (cubierto en Sprint 7).

## Write-set (archivos que se espera tocar)
- `template/tools/_continuum/release.py`
- `template/tools/_continuum/__main__.py`
- `tools/_continuum/release.py`
- `tools/_continuum/__main__.py`
- `tests/test_release_cmd.py`
- `README.md`
- `.ai/state/topics/comandos.md`
- `.ai/tasks/sprint-6-release-meta/*`
- `.ai/HANDOFF.md`

## Fuentes de verdad a leer antes de empezar
- `.ai/state/estado-dev.md`
- `docs/ux-metrics-sprints.md` (Sprint 6)
- `tools/_continuum/bootstrap.py`
- `tools/_continuum/doctor.py`

## Criterios de salida
- `continuum export status` reporta si la rama `export` coincide con `template/`.
- `continuum release <version> --dry-run` valida changelog, tests y tag sin alterar el repositorio.
- Todos los tests unitarios pasan (`python3 -m unittest discover -s tests -t . -v`).
- `python3 tools/continuum doctor` pasa limpio.
