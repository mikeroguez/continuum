# Protocolo de colaboración con IA (Continuum)

Fuente única de verdad del flujo de trabajo con asistentes de IA. `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` y `.github/copilot-instructions.md` son entrypoints delgados que remiten aquí. Edita primero este archivo antes que los entrypoints.

Detalles y guías extensas en [`template/docs/guia-para-agentes.md`](template/docs/guia-para-agentes.md) y [`template/docs/como-usar-continuum.md`](template/docs/como-usar-continuum.md).

> **Principio rector:** El repositorio es la memoria; la conversación es solo el canal de ejecución. Toda decisión o hallazgo debe registrarse en archivos versionados.

## 0. Orden de lectura en sesión nueva

1. `.ai/HANDOFF.md` — pendiente de la sesión anterior.
2. `.ai/state/estado-dev.md` — índice corto de temas.
3. Temas de `.ai/state/topics/` señalados por el índice como relevantes.
4. `.ai/tasks/<slug>/task.md` (si hay tarea abierta relevante).

En clientes con `SessionStart` (`tools/continuum context --hook`), este contenido se inyecta automáticamente al arrancar.

## 1. Compatibilidad multi-proveedor

| Proveedor | Entrypoint | Config propia |
|---|---|---|
| Claude Code | `CLAUDE.md` | `.claude/settings.json` (permisos, hooks) |
| Codex / genérico | `AGENTS.md` | `.agents/skills/` (skills de roles) |
| Gemini CLI | `GEMINI.md` | `.gemini/settings.json` |
| GitHub Copilot | `.github/copilot-instructions.md` + `AGENTS.md` | Instrucciones y agentes Copilot |

`continuum doctor` valida la existencia y consistencia de cada entrypoint.

## 2. Ciclo de vida de una tarea

| Tamaño | Cuándo aplica | Qué se exige |
|---|---|---|
| small | 1-3 archivos, alcance claro | Actualizar `.ai/HANDOFF.md` al terminar |
| medium | 1 módulo/dominio, >3 archivos | `continuum task start <slug> --size medium`; cerrar con `continuum task close <slug>` |
| large | Cruza dominios, ambigua/riesgosa | Igual a medium + `execution-plan.md` |

```bash
tools/continuum task start pagos-recurrentes --size medium --owner ana
tools/continuum task claim pagos-recurrentes ana
tools/continuum task close pagos-recurrentes
```

Nunca reutilizar identificadores ni slugs de requisitos/tareas ya usados (RF-###, PA-##, slugs).

## 3. Contexto mínimo suficiente (eficiencia de tokens)

- Localiza antes de leer (`rg`/`grep`). Evita explorar carpetas completas.
- Lee índices/encabezados antes de archivos completos.
- Abre solo los temas de `.ai/state/topics/` necesarios.
- **Prompt caching:** Evita editar este archivo o el índice a media sesión para no invalidar el caché. Lo estable va primero, lo variable al final.
- `continuum doctor` verifica el costo del paquete de arranque (`STARTUP_TOKENS_LIMIT` = 3500 tokens).

### 3.1 Contenido inferible
No repitas código, README o configs que la IA pueda buscar por sí misma. En el arranque conserva solo información **no inferible** (comandos no obvios, riesgos, decisiones).

## 4. Handoff y continuidad

`.ai/HANDOFF.md` es el buzón único y siempre vigente:
- Actualízalo antes de cortar la sesión o al agotar tokens.
- Usa `SessionEnd` para borrador automático (`continuum handoff --auto`). **No mutar archivos en disco durante `PreCompact`** para no romper la caché.
- Formato: objetivo, cambios, decisiones, validaciones, riesgos, siguiente paso.
- Archiva handoffs viejos con `continuum compact --handoff` cuando supere ~50 líneas.

## 5. Memoria viva: índice + temas

`estado-dev.md` es un índice corto (≤80 líneas) que apunta a `.ai/state/topics/*.md`.
- Actualiza los temas, no el índice.
- Archiva entradas viejas con `tools/continuum compact --topic <nombre>`.
- Decisiones mayores van a ADRs en `docs/architecture/ADR-XXXX-*.md` o `docs/decision-log.md`. Usa `tools/continuum adr new "Título"` para asignar número.

## 6. Trabajo en equipo
Múltiples personas/agentes aislados por tareas y worktrees: ver [`template/docs/trabajo-en-equipo.md`](template/docs/trabajo-en-equipo.md).

## 7. Convención de commits
Conventional Commits en inglés (`feat|fix|docs|refactor|test|chore|perf|ci`), mensaje en idioma del equipo. Ejemplo: `feat: add recurring payment validation`.

## 8. Verificación automática
- `tools/continuum doctor`: Git pre-commit hook que valida entrypoints, temas, handoff, ADRs y presupuesto de tokens.
- `tools/continuum doctor --fix --no-dry-run`: Aplica auto-reparaciones seguras.

## 9. Roles: catálogo de expertos
Los roles viven en `.ai/roles/<pack>/` (declarados en `.ai/config.json`).
```bash
tools/continuum roles list
tools/continuum task start <slug> --role backend
tools/continuum roles sync --provider gemini
```
