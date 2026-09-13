# Plan de ejecución: adopcion-ideas-cbm

Solo para tareas `medium`/`large`. Es una cola persistente de pasos: márcalos
al avanzar para que, si la sesión se corta a medio camino, la siguiente sepa
exactamente dónde retomar sin releer todo desde cero.

Cada paso de protocolo/CLI incluye su propia actualización de documentación
— no hay un paso final separado de "documentar todo". La cola de abajo ya
refleja la investigación hecha antes de tocar código (ver
`docs/investigacion-2026.md` §10 y `docs/decision-log.md` ADR-012): tres
ideas de la propuesta original se descartaron ahí (contrato de evidencia por
tamaño, `merge=ours` en `HANDOFF.md`, `continuum init --detect`) y no
aparecen en esta cola.

- [x] Paso 0 — Reconciliar `pendientes.md` (rollout vs. propagación de
      versión). Hecho 2026-09-12.
- [x] Paso 1 — ADR-012 en `docs/decision-log.md`. Hecho 2026-09-12.
- [x] Paso 2 — Sección 10 en `docs/investigacion-2026.md`. Hecho 2026-09-12.

- [x] Paso 3 — Hecho 2026-09-12. `cmd_context`/`build_context` en
      `tools/_continuum/context.py` (y espejo en `template/`) ahora vuelcan
      el contenido completo de `AI_COLLABORATION.md`, `estado-dev.md` y
      `HANDOFF.md` (marcados `inline: True`); los entrypoints por proveedor
      quedan explícitamente `inline: False` con la nota "cargado nativamente
      por el cliente", porque ya los carga su propio cliente (ver el
      comentario nuevo en `build_context` y ADR-012). Actualizado
      `AI_COLLABORATION.md` §0 y §3 (y espejo en `template/`). 4 tests
      nuevos en `tests/test_context.py` (inline de obligatorios, no-inline
      de entrypoints, formato humano con delimitadores, nota de "cargado
      nativamente" ausente en temas bajo demanda). Efecto colateral
      detectado y corregido: el cambio a `AI_COLLABORATION.md` invalidó la
      huella sha256 que `.github/copilot-instructions.md` guarda de ese
      archivo (ADR-010) — recalculada y actualizada en la raíz y en
      `template/`. Suite completa: 117 tests, 0 fallos. `doctor`: 0
      críticos (el presupuesto de arranque subió de ~3280 a ~3461 tokens,
      por la prosa añadida a `AI_COLLABORATION.md`, no por el cambio de
      `context.py` en sí).

- [x] Paso 4 — Hecho 2026-09-12. `continuum doctor` (y espejo en
      `template/`) detecta marcadores de conflicto de git (`<<<<<<<`,
      `=======`, `>>>>>>>`) sin resolver en `.ai/HANDOFF.md`, reportado como
      problema crítico. Documentado en `AI_COLLABORATION.md` §6 (y espejo).
      2 tests nuevos.

- [x] Paso 5 — Hecho 2026-09-12, con un ajuste sobre lo planeado: la
      verificación de `doctor` cubre **las dos convenciones de ADR que el
      protocolo admite**, no solo `docs/decision-log.md` — también
      `docs/architecture/ADR-###-*.md` (la que `AI_COLLABORATION.md` §5
      recomienda a un proyecto que instala la plantilla; este mismo
      repositorio usa la otra). Detectado al ir a documentar el cambio: la
      verificación original solo habría servido para el propio Continuum
      autoalojado, no para ningún proyecto que lo instale. Números
      duplicados → crítico; huecos → advertencia. Documentado en
      `AI_COLLABORATION.md` §5 y §8 (y espejo). 4 tests nuevos (duplicado en
      log único, duplicado en archivos sueltos, hueco, numeración limpia).
      Extensión opcional del comando `continuum adr new <slug>` (scaffold +
      numeración automática) **no implementada** — la verificación en
      `doctor` es el núcleo de valor real (ADR-012); queda como mejora
      futura, no bloquea el cierre de esta tarea.
      Efecto colateral repetido: cada edición a `AI_COLLABORATION.md`
      invalida la huella sha256 de `.github/copilot-instructions.md`
      (ADR-010) — recalculada 2 veces en esta tarea; registrado en
      `pendientes.md` como candidato a `doctor --fix` si se sigue repitiendo.

- [x] Paso 6 — Hecho 2026-09-12. `template/docs/metodologia-medicion.md`
      (nuevo, genérico — sin nombrar proyectos de este repositorio, es
      contenido distribuible) + `docs/metodologia-medicion.md` en la raíz
      (copia con una sección final que sí nombra los 4 proyectos reales, el
      mismo patrón de divergencia intencional raíz/`template/` que ya usa
      `AI_COLLABORATION.md`). Definición del escenario adaptada al job real
      de Continuum (reanudar trabajo tras una discontinuidad de
      sesión/proveedor/persona), no al de CBM (exploración de código).
      Extra no planeado originalmente: enlazado desde
      `continuum metrics report` (`tools/_continuum/metrics.py` y espejo)
      con una nota que aclara que ese reporte es un snapshot estático, no
      consumo real — costo de una línea, valor real, no ameritaba esperar a
      una tarea aparte.

- [x] Paso 7 — Hecho 2026-09-12. Frase de postura de confianza añadida a
      "Principios Clave" en `README.md` y su espejo `README.en.md` (política
      de idiomas exige mantener ambos, `docs/LANGUAGE_POLICY.md`). Extra no
      planeado: la cifra "~2.5k tokens" de ese mismo bloque ya estaba
      desactualizada por los cambios de los pasos 3-5 (arranque real:
      ~3.631 tokens) — corregida para apuntar a `continuum doctor` como
      fuente de verdad en vez de hardcodear un número que se sabe que va a
      volver a quedar obsoleto.

- [x] Paso 8 — Hecho 2026-09-12. Suite completa: 122 tests, 0 fallos.
      `doctor`: 0 críticos contra este mismo repositorio (1 advertencia
      esperada e informativa). Confirmado sin falsos positivos: numeración
      de ADRs de `docs/decision-log.md` limpia, `.ai/HANDOFF.md` sin
      marcadores de conflicto. Handoff completo escrito en `.ai/HANDOFF.md`.
      Observación registrada, sin corregir por estar fuera de alcance: el
      techo de 3500 tokens hardcodeado en `continuum metrics report`
      (`tools/_continuum/metrics.py:151`) ahora se reporta excedido por el
      aumento esperado del presupuesto de arranque (ADR-012).

- [x] Paso 9 (agregado, fuera del plan original) — Hecho 2026-09-12.
      Implementado `continuum adr new "<título>"` (`tools/_continuum/adr.py`
      nuevo, registrado en `__main__.py`, espejo en `template/`), a pedido
      explícito del owner tras el cierre inicial de la tarea. Refactor
      necesario: la lógica de numeración de ADR que vivía como funciones
      privadas en `doctor.py` se movió a `common.py`
      (`collect_adr_numbers`/`adr_numbering_issues`, funciones públicas) para
      que `doctor.py` y `adr.py` la compartan sin duplicar código. El comando
      detecta cuál convención usa el proyecto (log único vs. archivo por
      ADR) y escribe en la que corresponda; `--slug` opcional para el
      nombre de archivo en la segunda. 8 tests nuevos en `tests/test_adr.py`.
      Documentado en `AI_COLLABORATION.md` §5 (y espejo).

- [x] Paso 10 (agregado, fuera del plan original) — Hecho 2026-09-12.
      Corregido el efecto colateral repetido de esta misma tarea: la huella
      sha256 de `.github/copilot-instructions.md` (ADR-010) ahora se
      recalcula sola con `continuum doctor --fix --no-dry-run`
      (`_refresh_copilot_fingerprint` en `doctor.py`, solo reemplaza el
      comentario de huella, nunca la prosa curada a mano). Validado en
      producción real sobre este mismo repositorio, no solo en tests: se
      usó el propio mecanismo nuevo para corregir la huella que la edición
      del Paso 9 había dejado stale. Limitación aceptada y documentada en
      `pendientes.md`: no alcanza a `template/.github/copilot-instructions.md`
      porque `doctor` siempre opera sobre la raíz git — sigue siendo manual
      solo para ese mirror, y solo en este repositorio autoalojado (un
      proyecto que consume la plantilla no tiene ese problema). Test nuevo
      en `tests/test_status_fix.py`. Documentado en `AI_COLLABORATION.md`
      §8 (y espejo).

## Estado actual
Tarea completa: pasos 0-10 hechos el 2026-09-12 (8 del plan original + 2
agregados a pedido del owner tras el primer cierre). Todo lo adoptado en
ADR-012 está implementado, documentado y probado, incluida la extensión
opcional del subcomando `adr new` que originalmente se había dejado fuera.
Suite completa: 131 tests, 0 fallos. `doctor`: 0 críticos. Ver
`.ai/HANDOFF.md` para el detalle completo de la sesión.
