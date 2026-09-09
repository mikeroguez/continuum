# Tarea: sprint-7-github-proteccion

**Creada:** 2026-09-09 · **Tamaño:** medium · **Owner:** gemini · **Rol:** Backend (`software/backend`)

## Objetivo
Implementar herramientas para auditar y generar planes de protección de ramas y tags en GitHub (`continuum github protect`), ofreciendo guías paso a paso para la interfaz web o integración vía CLI/API si `gh` o tokens de GitHub están presentes.

## Incluido en el alcance
- Subcomando `continuum github protect`:
  - `--print` (por defecto): Genera la guía de configuración y reglas de protección recomendadas para las ramas `main`, `export` y los tags `v*`.
  - `--apply`: Intenta aplicar las reglas vía CLI `gh` si está disponible y autenticado, o indica los pasos si falta autenticación.
- Integración no bloqueante con `doctor` (advertencia optativa si falta detección).
- Pruebas unitarias en `tests/test_github_cmd.py`.
- Documentación en `README.md` y `.ai/state/topics/comandos.md`.

## Explícitamente fuera de alcance
- Requerir obligatoriamente GitHub para proyectos alojados en otros proveedores de Git.
- Modificaciones destructivas en configuraciones de remotos sin autorización explícita.

## Write-set (archivos que se espera tocar)
- `template/tools/_continuum/github.py`
- `template/tools/_continuum/__main__.py`
- `tools/_continuum/github.py`
- `tools/_continuum/__main__.py`
- `tests/test_github_cmd.py`
- `README.md`
- `.ai/state/topics/comandos.md`
- `.ai/tasks/sprint-7-github-proteccion/*`
- `.ai/HANDOFF.md`

## Fuentes de verdad a leer antes de empezar
- `.ai/state/estado-dev.md`
- `docs/ux-metrics-sprints.md` (Sprint 7)
- `tools/_continuum/release.py`

## Criterios de salida
- `continuum github protect --print` emite la guía de protección clara y estructurada.
- `continuum github protect --json` reporta la disponibilidad de `gh` y el plan de reglas en JSON.
- Todos los tests unitarios pasan (`python3 -m unittest discover -s tests -t . -v`).
- `python3 tools/continuum doctor` pasa limpio.
