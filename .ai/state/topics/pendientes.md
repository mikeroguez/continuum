# Pendientes por prioridad

## Mayores

- Elegir licencia antes de publicar el repositorio (bloqueante para
  publicación pública — ver `README.md` § Licencia).
- Crear el remoto de git y publicar el repositorio (hoy no tiene remoto
  configurado; `git subtree`, `sync-template` y la instalación en otros
  proyectos dependen de que exista una URL real).
- Decidir sobre adoptar GitHub Spec Kit en lugar del sistema de tareas
  propio (`docs/decision-log.md` ADR-004, decisión abierta).
- Aplicar el rollout (`docs/rollout-guide.md`) a los proyectos reales que
  motivaron este diseño — no se ha aplicado a ninguno todavía.

## Menores

- No hay suite de tests automatizada para `tools/_continuum/` — la
  validación hasta ahora fue manual (smoke tests en `/tmp`, ver
  `.ai/state/topics/comandos.md`).
- Revisar si persiste el bug de Google Antigravity IDE (preview de Markdown
  no se refresca tras ediciones de un agente) si se sigue usando esa IDE
  para trabajar en este repositorio — no bloqueante, es un problema del
  editor, no del contenido.
