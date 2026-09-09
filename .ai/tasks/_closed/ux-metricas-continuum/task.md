# Tarea: ux-metricas-continuum

**Creada:** 2026-09-09 · **Tamaño:** large · **Owner:** (sin asignar) · **Rol:** Producto (Jobs to be Done) (`software/producto-jtbd`)

## Objetivo
Diseñar la evolución de Continuum desde un protocolo que el desarrollador debe
recordar hacia un sistema idempotente, guiado por Jobs To Be Done, heurísticas
de Nielsen y optimización de tokens. La tarea también define métricas locales
para evaluar si Continuum realmente mejora continuidad, costo de contexto y
coordinación, con potencial de publicación científica.

## Incluido en el alcance
- Jobs principales por actor: desarrollador, agente IA, mantenedor de
  Continuum e investigador/creador.
- Indicadores de UX, continuidad, tokens, fricción y coordinación.
- Roadmap por sprints con entregables concretos.
- Diseño inicial de comandos idempotentes (`status`, `context`, `tokens`,
  `doctor --fix`, `session`, `sync`, `release`, `metrics`).
- Reglas de privacidad para medición local y export explícito.

## Explícitamente fuera de alcance
- Implementar los comandos nuevos en esta tarea inicial de diseño.
- Definir telemetría remota por defecto.
- Hacer un estudio científico completo sin datos de uso reales.
- Rediseñar documentación pública fuera de los puntos necesarios para capturar
  el plan.

## Write-set (archivos que se espera tocar)
No editar fuera de esta lista sin actualizarla primero. Evita refactors oportunistas.

- `.ai/tasks/ux-metricas-continuum/task.md`
- `.ai/tasks/ux-metricas-continuum/execution-plan.md`
- `.ai/tasks/ux-metricas-continuum/notes.md`
- `docs/ux-metrics-roadmap.md`
- `docs/ux-metrics-sprints.md`
- `.ai/state/topics/pendientes.md`
- `.ai/HANDOFF.md`

## Fuentes de verdad a leer antes de empezar
- `.ai/state/estado-dev.md`
- `.ai/roles/software/producto-jtbd.md`
- `AI_COLLABORATION.md`
- `ARCHITECTURE.md` si se cambian decisiones de diseño de fondo
- `docs/investigacion-2026.md` si se formaliza el marco científico

## Contexto mínimo sugerido
Según el tamaño declarado arriba, no cargues más de lo necesario:

| Tamaño  | Techo de lectura inicial orientativo |
|---------|----------------------------------------|
| small   | 1-3 archivos concretos, sin explorar carpetas completas |
| medium  | 1 módulo/dominio, usar `rg`/`grep` para localizar antes de leer |
| large   | fragmentar con `continuum packetize`; considerar dividir en subtareas |
