# Plan de ejecución: lifecycle-completo

Solo para tareas `medium`/`large`. Es una cola persistente de pasos: márcalos
al avanzar para que, si la sesión se corta a medio camino, la siguiente sepa
exactamente dónde retomar sin releer todo desde cero.

- [x] Paso 1 — Hecho 2026-09-12. `VERSION` en la raíz y `template/VERSION`,
      ambos con `1.4.1` — deben coincidir porque `template/VERSION` es lo
      que un proyecto consumidor hereda en su propio `VERSION` al hacer
      `git subtree add`/`pull`; mismo espejo raíz/`template` que ya usa
      `AI_COLLABORATION.md`. `common.read_version()`, comando `continuum
      version` (subcomando, en `status.py`) y flag `--version` en el parser
      top-level, ambos reportando el contenido de `VERSION`; si falta,
      advertencia clara. `release._write_version()`: `continuum release
      <version> --no-dry-run` escribe la nueva versión en `VERSION` (raíz
      siempre, `template/VERSION` solo si ese directorio existe — un
      proyecto consumidor no tiene uno propio). 12 tests nuevos entre
      `test_version_cmd.py` y `test_release_cmd.py`.
      Nota de proceso: al escribir los tests de `_write_version` pisé por
      accidente dos aserciones reales de un test existente
      (`test_release_validation_and_dry_run`) al hacer un `Edit` cuyo
      `old_string` no cubría todo el bloque — quedaron huérfanas debajo de
      mi test nuevo en vez de perderse silenciosamente porque `python3 -m
      unittest` las siguió ejecutando y fallaron con `NameError` en el
      lugar equivocado; se detectó al correr la suite, no al escribir el
      código. Restauradas en su lugar original antes de seguir.

- [x] Paso 2 — Hecho 2026-09-12. `common.generated_role_slug(text)` detecta
      si un archivo fue generado por `continuum roles sync` (huella de
      preámbulo `GENERATED_ROLE_MARKER` + `name:` del frontmatter) sin
      depender de su nombre de archivo. `roles.py`:
      `_prune_orphaned_files`/`_prune_orphaned_skill_dirs` al final de
      `sync()` para las 4 convenciones (claude/copilot archivo plano,
      codex/gemini directorio-por-skill) — borran solo lo que tiene la
      huella y cuyo slug ya no está en el catálogo activo. Reportado en la
      salida del comando. 3 tests nuevos: poda al desactivar un rol
      (claude y gemini), y un archivo sin huella escrito a mano sobrevive
      intacto. Efecto colateral menor detectado y corregido: el suffix de
      claude/copilot se calculaba dos veces (una vez por rol dentro del
      loop, redundante) — se sacó del loop de una vez de paso.

- [x] Paso 3 — Hecho 2026-09-12. `tools/_continuum/uninstall.py` nuevo
      (+ espejo). Validado dos veces: 17 tests automatizados (incluido un
      test de "drift" que compara el manifiesto de nivel 2 contra el
      `template/` real de este repositorio, para detectar si se agrega un
      archivo nuevo a la plantilla y se olvida cubrirlo aquí) y una prueba
      de humo manual completa en `/tmp` (proyecto sintético real, git init,
      `install-hooks`, `roles sync`, remoto `continuum`, hook editado a
      mano) ejecutando la desinstalación de verdad con los tres niveles —
      confirmado con `git status`/`find` que sobrevivió exactamente lo que
      debía (`docs/architecture/`, el hook editado) y desapareció el resto,
      sin ningún commit automático. Detalle:
      - Función que arma el plan de los 3 niveles (mecanismo/protocolo/
        memoria) inspeccionando qué existe realmente en el proyecto — no
        una lista estática, porque no todo proyecto tiene todo (p. ej. sin
        `codex` activo no hay `.agents/skills/`).
      - Nivel 1 (mecanismo): usa `generated_role_slug` para los subagentes;
        verifica contenido exacto/huella para `.githooks/pre-commit` y
        `.githooks/README.md` antes de borrar (si fueron editados, se
        excluyen del nivel 1 y se listan en el nivel 2 con una nota).
      - Si se borra `.githooks/pre-commit` y `core.hooksPath` sigue
        apuntando ahí, revertir la config (`git config --unset
        core.hooksPath`) — solo si el valor actual es exactamente
        `.githooks`.
      - Remoto git `continuum` (por nombre exacto, el que documenta
        `README.md`): eliminarlo en el nivel 1 si existe.
      - `cmd_uninstall(root, dry_run=True, yes=False, purge_memory=False,
        json_output=False)`: rechaza si el working tree está sucio: exit 1
        con mensaje claro. Dry-run (por defecto) solo imprime el plan de los
        3 niveles con conteo de archivos por nivel. `--no-dry-run` sin
        `--yes` borra solo nivel 1 e imprime nivel 2/3 como "no incluidos,
        agrega --yes / --yes --purge-memory". `--no-dry-run --yes` borra
        1+2. `--no-dry-run --yes --purge-memory` borra 1+2+3. Nunca
        commitea; mensaje final siempre recuerda revisar `git status`/`git
        diff` y commitear a mano.
      - Registrar `continuum uninstall` en `__main__.py` con esos flags.
      - Tests cubriendo: dry-run no borra nada; nivel 1 solo; nivel 1+2 con
        `--yes`; nivel 1+2+3 con `--purge-memory`; rechazo con tree sucio;
        `.githooks/pre-commit` editado a mano se excluye del nivel 1;
        subagente ajeno sin huella sobrevive.

- [x] Paso 4 — Hecho 2026-09-12. `AI_COLLABORATION.md` §8 (+ espejo)
      menciona `version`/`uninstall`/poda de roles. `README.md` +
      `README.en.md`: `--version` agregado a "Diagnóstico y Sesión",
      sección nueva "Desinstalación"/"Uninstall" con los 3 niveles.
      `CHANGELOG.md`: entrada bajo `[Unreleased]` — **hallazgo de proceso**:
      al escribirla noté que ninguna tarea anterior de esta sesión
      (adopcion-ideas-cbm/ADR-012, afinar-roles-software, diseño atómico)
      había quedado registrada en el changelog, pese a que
      `continuum release` exige una entrada ahí para poder liberar — se
      completó todo de una vez en este paso, no solo lo de esta tarea.

- [x] Paso 5 — Hecho 2026-09-12. Suite completa: 158 tests, 0 fallos.
      `doctor`: 0 críticos. `continuum uninstall` (dry-run, nunca aplicado)
      corrido sobre este mismo repositorio: el plan generado tiene sentido
      exacto con el estado real — nivel 1 con 65 elementos (subagentes
      generados en los 4 proveedores porque se corrió `roles sync` para
      los 4 durante esta y tareas anteriores, más el CLI y las plantillas),
      nivel 2 con 17 (solo lo que de verdad existe en la raíz de este
      repo — algunos docs de `template/docs/` no tienen copia en la raíz
      aquí, y correctamente no aparecen), nivel 3 con la memoria real
      (`HANDOFF.md`, `state/`, `tasks/`). No se aplicó — es prueba de humo,
      no una desinstalación real.

## Estado actual
Tarea completa: pasos 1-5 hechos el 2026-09-12. Las 4 piezas identificadas
en la auditoría original (`version`, poda de `roles sync`, `uninstall`,
reverso de `install-hooks`) están implementadas, documentadas y probadas.
Ver `.ai/HANDOFF.md` para el detalle completo de la sesión.
