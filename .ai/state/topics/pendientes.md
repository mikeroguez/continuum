# Pendientes por prioridad

## Mayores

- [COMPLETADO] Implementados y cerrados los 9 Sprints del rediseño UX y métricas de Continuum (Sprints 0 a 8 en `docs/ux-metrics-sprints.md`), incluyendo `context`, `tokens`, `status`, `doctor --fix`, `session`, `task`, `sync`, `release`, `github` y `metrics report|export|compare`.
- Aplicar formalmente el procedimiento de `docs/rollout-guide.md` (migración
  de memoria legado, cierre de tareas históricas) a los proyectos reales que
  motivaron este diseño — no se ha aplicado ese procedimiento específico
  todavía. Distinto de la propagación de versión: Continuum ya está en uso
  activo en los 4 proyectos dependientes (`seguimiento-talleres`,
  `seguimiento-deportes`, `seguimiento-clubes`, `SISETAP`), confirmado
  2026-09-12 — ver `resumen.md`.
- Completar `template_remote` y `template_prefix` en `.ai/config.json` si este
  repositorio debe sincronizarse con otra plantilla mediante
  `tools/continuum sync-template`; hoy el comando funciona, pero imprime
  placeholders porque esos campos están vacíos.

## Menores

- Revisar si persiste el bug de Google Antigravity IDE (preview de Markdown
  no se refresca tras ediciones de un agente) si se sigue usando esa IDE
  para trabajar en este repositorio — no bloqueante, es un problema del
  editor, no del contenido.
- [RESUELTO 2026-09-12] La huella sha256 de `.github/copilot-instructions.md`
  (ADR-010) ya no se recalcula a mano: `continuum doctor --fix --no-dry-run`
  la detecta y la reemplaza sola cuando `AI_COLLABORATION.md` cambia, sin
  tocar la prosa curada de la proyección (`_refresh_copilot_fingerprint` en
  `tools/_continuum/doctor.py`). Limitación conocida y aceptada: `doctor`
  siempre opera sobre la raíz del repositorio git (`common.repo_root()`), así
  que en este repositorio autoalojado la copia de `template/.github/
  copilot-instructions.md` sigue necesitando el mismo ajuste a mano al
  sincronizar `template/AI_COLLABORATION.md` — es el mismo costo de
  mantenimiento de la doble copia raíz/`template/` que ya existía para todo
  lo demás (`arquitectura.md`), no un caso nuevo. Un proyecto que solo
  consume la plantilla (sin la doble copia) no tiene esta limitación.
- Extender el refuerzo de "Estándares de código por defecto" (tarea
  `afinar-roles-software`, 2026-09-12) a los roles de `producto-jtbd`/
  `ux-research`/`ux-ui` y al resto de `comun` — deliberadamente fuera de
  esa tarea porque no producen código, y el criterio de concisión para
  documentos de investigación/producto es distinto al de código. Solo
  vale la pena si el owner observa el mismo problema (entregables
  verbosos/genéricos) en esos roles.
- Correr `docs/metodologia-medicion.md` comparando la calidad/concisión del
  código que producen `backend`/`frontend` antes y después del refuerzo de
  `afinar-roles-software` — el cambio de texto está verificado (se propaga
  al subagente), pero su efecto real en el comportamiento del agente no se
  midió todavía.
