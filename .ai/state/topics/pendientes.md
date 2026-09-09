# Pendientes por prioridad

## Mayores

- Aplicar el rollout (`docs/rollout-guide.md`) a los proyectos reales que
  motivaron este diseño — no se ha aplicado a ninguno todavía.
- Completar `template_remote` y `template_prefix` en `.ai/config.json` si este
  repositorio debe sincronizarse con otra plantilla mediante
  `tools/continuum sync-template`; hoy el comando funciona, pero imprime
  placeholders porque esos campos están vacíos.

## Menores

- Revisar si persiste el bug de Google Antigravity IDE (preview de Markdown
  no se refresca tras ediciones de un agente) si se sigue usando esa IDE
  para trabajar en este repositorio — no bloqueante, es un problema del
  editor, no del contenido.
