# {{NOMBRE_DEL_PROYECTO}} — índice de memoria

> Léeme antes de cualquier tarea de alcance medio o mayor — pero **solo
> léeme a mí**. Este archivo es un índice corto (patrón MEMORY.md + temas,
> igual al que usa Auto Memory de Claude Code); el detalle vive en
> `.ai/state/topics/*.md` y se abre bajo demanda, según lo que diga la
> descripción de una línea de cada tema. No dupliques aquí el contenido de
> los temas — si este archivo empieza a crecer más allá de ~80 líneas, algo
> se está metiendo aquí que debería ser un tema aparte.

## Temas

- **Resumen y stack** → `.ai/state/topics/resumen.md`
- **Arquitectura y dominio** → `.ai/state/topics/arquitectura.md`
- **Decisiones tomadas** → `.ai/state/topics/decisiones.md`
- **Pendientes por prioridad** → `.ai/state/topics/pendientes.md`
- **Comandos de referencia** → `.ai/state/topics/comandos.md`

Cuando un tema acumula entradas fechadas viejas, `continuum compact --topic
<nombre>` las archiva dentro del propio archivo de tema (no aquí en el
índice) y deja un puntero a `.ai/state/archive/<tema>-YYYY-MM.md`.
