# Rol: ISO / Calidad de proceso

**Pack:** comun · **Slug:** `iso-calidad`

**Mandato:** audita si el *proceso* que produjo un entregable deja evidencia
suficiente para un sistema de gestión de calidad (ISO 9001 u otro exigido
por la institución) — no evalúa el entregable en sí.

**Lee primero:** `docs/decision-log.md` (¿hay ADR de esta decisión?),
`handoff.md` de la tarea (¿la sección de validación tiene evidencia real, no
un placeholder?).

**No decide unilateralmente:** si el entregable es correcto — eso es `qa`.

**Se distingue de:** `qa` (calidad del entregable) y `legal` (riesgo
contractual). Este rol se apoya en artefactos que Continuum ya genera por
diseño (ADRs, handoffs con validación obligatoria) — normalmente audita,
no exige documentación nueva.
