# Handoff: (general)

**Fecha:** 2026-09-09 · **Proveedor:** claude

## Objetivo de la sesión

Diseñar y construir Continuum (arquitectura de memoria de IA transportada
por git), investigar su validez frente a evidencia externa 2026, hacer la
documentación apta para un repositorio público (sin narrativa personal, con
los casos de estudio anonimizados), nombrar el proyecto, y por último
instalar Continuum sobre sí mismo (autoalojamiento).

## Archivos modificados

Prácticamente todo el repositorio. Los más relevantes por si hace falta
revisar algo puntual:

- `ARCHITECTURE.md`, `README.md`, `docs/decision-log.md` (ADR-001 a
  ADR-005), `docs/rollout-guide.md`, `docs/investigacion-2026.md`.
- `template/` completo (protocolo, CLI, plantillas) — es la fuente de
  verdad; la raíz de este repositorio es una copia autoalojada de eso mismo.
- Raíz del repositorio: `AGENTS.md`, `AI_COLLABORATION.md`, `CLAUDE.md`,
  `GEMINI.md`, `.ai/`, `.claude/`, `.githooks/`, `.github/`, `tools/` — todo
  copiado desde `template/` como instancia activa (ver
  `.ai/state/topics/arquitectura.md` para la relación entre ambas copias).

## Decisiones tomadas

- Framework propio (CLI `continuum`) en vez de solo convención — ADR-002.
- Distribución vía `git subtree` — ADR-001.
- Sin orquestación real entre agentes de IA — ADR-003.
- Memoria como índice corto + temas bajo demanda (no un snapshot que crece),
  regla contra contenido inferible en entrypoints, hook `SessionEnd` en vez
  de `Stop`, `packetize` degradado a último recurso, `git worktree` por
  tarea concurrente — ADR-004, con fuentes en `docs/investigacion-2026.md`.
- Nombre del proyecto: Continuum — ADR-005.

## Suposiciones vigentes

- Los cinco proyectos que motivaron el diseño (anonimizados como "Proyecto
  A–E" en `ARCHITECTURE.md` §1) siguen sin recibir el rollout — el diseño
  se validó contra su estado auditado, no se aplicó de vuelta a ellos.
- El repositorio no tiene remoto de git ni licencia elegida; varias
  instrucciones de `README.md` (`git subtree add`, `sync-template`) no son
  ejecutables todavía tal cual, hasta que exista una URL real.

## Validación

- **Ejecutada:** ciclo completo del CLI probado manualmente en copias
  descartables (`task start/claim/close`, `handoff` manual y `--auto`,
  `compact --topic`, `memory-split-legacy` incluyendo el caso de colisión de
  nombres, `install-hooks` con un commit real pasando por el hook). Los dos
  diagramas Mermaid de `ARCHITECTURE.md` se renderizaron de verdad con
  `@mermaid-js/mermaid-cli` para confirmar sintaxis válida.
- **No ejecutada:** no hay suite de tests automatizada; toda la validación
  fue manual. No se probó el flujo de `git subtree add/pull/push` contra un
  remoto real (no existe todavía).

## Riesgos / dudas abiertas

- El framework (`continuum`) se construyó pese a evidencia de que un
  toolkit similar se abandonó dos veces en los proyectos auditados — ver
  ADR-002 para las mitigaciones aplicadas y la señal a monitorear si se
  repite el patrón.
- La adopción de GitHub Spec Kit como alternativa al sistema de tareas
  propio quedó sin resolver (ADR-004) — afectaría la forma del subsistema de
  tareas si se decide adoptarlo más adelante.

## Siguiente paso recomendado

1. Elegir licencia y crear el remoto de git para poder publicar.
2. Decidir sobre GitHub Spec Kit (ADR-004) antes de que el sistema de tareas
   propio acumule más uso — el costo de cambiarlo crece con el tiempo.
3. Cuando se quiera aplicar esto a un proyecto real, seguir
   `docs/rollout-guide.md` — no se ha ejecutado ese procedimiento todavía.
