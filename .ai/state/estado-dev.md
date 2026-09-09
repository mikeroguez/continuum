# Continuum — índice de memoria

> Índice corto (patrón MEMORY.md + temas). El detalle vive en
> `.ai/state/topics/*.md` — ábrelos solo si la tarea los necesita.

## Temas

- **Resumen y stack** → `.ai/state/topics/resumen.md`
- **Arquitectura y dominio** → `.ai/state/topics/arquitectura.md`
- **Decisiones tomadas** → `.ai/state/topics/decisiones.md`
- **Pendientes por prioridad** → `.ai/state/topics/pendientes.md`
- **Comandos de referencia** → `.ai/state/topics/comandos.md`

Cuando un tema acumula entradas fechadas viejas, `tools/continuum compact
--topic <nombre>` las archiva dentro del propio archivo de tema y deja un
puntero a `.ai/state/archive/<tema>-YYYY-MM.md`.
