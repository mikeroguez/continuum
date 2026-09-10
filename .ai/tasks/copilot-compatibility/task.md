# Tarea: copilot-compatibility

**Creada:** 2026-09-10 · **Tamaño:** large · **Owner:** por asignar · **Rol:** gestion-proyecto

## Objetivo

Hacer que Continuum sea compatible de forma verificable con GitHub Copilot
Coding Agent, Copilot Chat/Agent en VS Code y Copilot Code Review, manteniendo
`AI_COLLABORATION.md` como fuente única de verdad y distribuyendo la
integración mediante `template/`.

## Incluido en el alcance

- Definir una matriz de compatibilidad y criterios observables por superficie.
- Incorporar `.github/copilot-instructions.md` como proyección verificable del
  protocolo canónico.
- Añadir instrucciones específicas por ruta solo donde aporten valor.
- Modelar `copilot` en configuración, handoff y diagnóstico sin inventar un
  `COPILOT.md` no reconocido por GitHub.
- Generar agentes personalizados de Copilot desde `.ai/roles/`, sin romper la
  generación existente para Claude.
- Validar Copilot Code Review con un fixture de defectos conocidos.
- Mantener paridad entre la raíz, `template/`, CI y documentación.
- Validar primero un consumidor canary antes del rollout general.

## Explícitamente fuera de alcance

- Construir un orquestador entre Copilot, Claude, Gemini u otros proveedores.
- Activar aprobaciones automáticas de Copilot o cambiar reglas de protección de
  ramas.
- Garantizar soporte idéntico para todos los IDEs sin una matriz aprobada.
- Añadir prompt files específicos de VS Code salvo necesidad confirmada.
- Introducir servidores MCP, secretos, dependencias externas o infraestructura
  de ejecución.

## Write-set (archivos que se espera tocar)

La lista se concretará por sprint antes de editar:

- `.ai/config.json`
- `AI_COLLABORATION.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`
- `.github/copilot-instructions.md`
- `.github/instructions/`
- `.github/agents/`
- `template/.ai/config.json`
- `template/AI_COLLABORATION.md`, `template/AGENTS.md`,
  `template/CLAUDE.md`, `template/GEMINI.md`
- `template/.github/`
- `tools/_continuum/common.py`, `doctor.py`, `handoff.py`, `roles.py`,
  `__main__.py`
- `tests/`
- `README.md`, `README.en.md`, `ARCHITECTURE.md`, `CHANGELOG.md` y guías
  relacionadas

## Fuentes de verdad a leer antes de empezar

- `.ai/HANDOFF.md`
- `.ai/state/estado-dev.md`
- `AI_COLLABORATION.md`
- `ARCHITECTURE.md`
- `tools/_continuum/common.py`
- `tools/_continuum/doctor.py`
- `tools/_continuum/handoff.py`
- `tools/_continuum/roles.py`
- `template/`

## Contexto mínimo sugerido

Por su tamaño y por cruzar protocolo, CLI, plantilla, CI y documentación,
tratar como tarea `large`. Ejecutar cada sprint en una rama o worktree propio
y cerrar cada sprint con handoff, pruebas y revisión de drift.
