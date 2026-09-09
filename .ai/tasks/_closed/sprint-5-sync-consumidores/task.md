# Tarea: sprint-5-sync-consumidores

**Creada:** 2026-09-09 · **Tamaño:** medium · **Owner:** gemini · **Rol:** Backend (`software/backend`)

## Objetivo
Facilitar la actualización y sincronización de Continuum en proyectos consumidores mediante el nuevo comando `continuum sync` (con opciones `--check`, `--dry-run`, y `--apply`), sin exigir que el usuario recuerde los comandos exactos de `git subtree`.

## Incluido en el alcance
- Subcomando `continuum sync`:
  - `--check`: Valida la configuración (`template_remote`, `template_prefix`), estado del *working tree* y conectividad remota si hay red.
  - `--dry-run` (por defecto): Muestra el plan y comando exacto de sincronización.
  - `--apply`: Ejecuta la actualización `git subtree pull` asegurando *working tree* limpio y registrando eventos/mensajes claros.
- Redirección / alias deprecado para `sync-template`.
- Tests unitarios en `tests/test_sync_cmd.py`.
- Documentación en `README.md` y `.ai/state/topics/comandos.md`.

## Explícitamente fuera de alcance
- Auto-resolución a ciegas de conflictos complejos de `git merge`.
- Operaciones destructivas sin confirmación.

## Write-set (archivos que se espera tocar)
- `template/tools/_continuum/bootstrap.py`
- `template/tools/_continuum/__main__.py`
- `tools/_continuum/bootstrap.py`
- `tools/_continuum/__main__.py`
- `tests/test_sync_cmd.py`
- `README.md`
- `.ai/state/topics/comandos.md`
- `.ai/tasks/sprint-5-sync-consumidores/*`
- `.ai/HANDOFF.md`

## Fuentes de verdad a leer antes de empezar
- `.ai/state/estado-dev.md`
- `docs/ux-metrics-sprints.md` (Sprint 5)
- `tools/_continuum/bootstrap.py`
- `tools/_continuum/common.py`

## Criterios de salida
- `continuum sync --check` audita la validez de los campos de config y el estado de git.
- `continuum sync --dry-run` o `sync` sin flags describe de forma transparente la acción a tomar.
- `continuum sync --apply` bloquea si el working tree está sucio, y ejecuta `git subtree` si está limpio.
- Todos los tests unitarios pasan (`python3 -m unittest discover -s tests -t . -v`).
- `python3 tools/continuum doctor` pasa limpio.
