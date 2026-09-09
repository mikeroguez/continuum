# Handoff de Tarea: sprint-7-github-proteccion

**Fecha:** 2026-09-09 · **Owner:** gemini · **Rol:** Backend (`software/backend`)

## Objetivo completado
Implementación de la herramienta de inspección y guía de protección de repositorios en GitHub (`continuum github protect`), ofreciendo recomendaciones para `main`, `export` y tags `v*`, e integrando detección de `gh` CLI y estado de autenticación.

## Entregables y cambios
- Módulo `tools/_continuum/github.py` (y `template/tools/_continuum/github.py`) con `detect_github_info()` y `cmd_protect()`.
- Registro del subcomando `github protect` (con opciones `--print`, `--apply` y `--json`) en `__main__.py` (y plantilla).
- Pruebas unitarias en `tests/test_github_cmd.py` (3 casos de prueba).
- Actualización de documentación en `README.md` y `.ai/state/topics/comandos.md`.

## Validación ejecutada
- `python3 tools/continuum github protect`: probado en modo humano y JSON.
- `python3 tools/continuum github protect --apply`: verificado despliegue de ayuda e instrucciones CLI.
- `python3 -m unittest discover -s tests -t . -v`: 83/83 tests pasados OK.
- `python3 tools/continuum doctor`: 0 problemas críticos, 0 advertencias.
