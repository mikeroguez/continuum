# Handoff: lifecycle-completo

**Fecha:** 2026-09-12 · **Rol:** (sin asignar)

## Objetivo
El owner notó que no existe forma de desinstalar Continuum y preguntó si
había mecanismos similares faltantes. Se confirmaron 4 huecos (mismo
patrón: "instala/genera pero nunca limpia") y se pidió implementar todos:
`continuum version`/`--version`, poda de subagentes huérfanos en
`continuum roles sync`, `continuum uninstall` (con reverso de
`install-hooks` incluido), y la documentación correspondiente.

## Archivos revisados
- `README.md` (flujo de instalación exacto: `git subtree add --prefix=.`)
- `tools/_continuum/bootstrap.py` (`install_hooks`, `cmd_sync`)
- `tools/_continuum/roles.py` (formato exacto de subagentes generados)
- `docs/rollout-guide.md` Caso 1 (evidencia de que los entrypoints sí se
  personalizan en la práctica)
- Listado completo de `template/` (qué trae de verdad la instalación)

## Archivos modificados
Ver write-set en `task.md`. Resumen: `VERSION` + `template/VERSION`
(nuevos), `common.py` (`read_version`, `generated_role_slug`,
`GENERATED_ROLE_MARKER`), `status.py` (`cmd_version`), `release.py`
(`_write_version`), `roles.py` (poda de huérfanos), `uninstall.py` (nuevo),
`__main__.py`, todos + espejo en `template/`. Documentación:
`AI_COLLABORATION.md` + espejo, `README.md` + `README.en.md`,
`CHANGELOG.md`. Tests: `test_version_cmd.py` (nuevo), `test_uninstall.py`
(nuevo, incluye un test de "drift" contra `template/` real),
`test_release_cmd.py`, `test_roles.py`.

## Decisión(es) tomada(s)
- **`VERSION` en `template/` se mantiene sincronizado con el de la raíz**
  (no es un punto de partida distinto tipo "0.0.0") — es lo que un proyecto
  consumidor hereda al instalar/actualizar, así que debe decir la versión
  real de Continuum, no un placeholder. `_write_version()` solo escribe
  `template/VERSION` si ese directorio existe (un proyecto consumidor no
  tiene uno propio).
- **`uninstall` en 3 niveles de seguridad, no una lista plana**: nivel 1
  (mecanismo, detectado por huella de contenido o verificación exacta, no
  por nombre de archivo) se borra con `--no-dry-run` solo; nivel 2
  (protocolo/config, puede estar personalizado) exige `--yes`; nivel 3
  (memoria real del proyecto: `HANDOFF.md`/`state/`/`tasks/`) exige
  `--purge-memory` explícito y nunca se incluye por accidente. Nunca
  reescribe historia de git ni commitea — solo borra en disco.
- **`docs/architecture/` nunca aparece en ningún nivel**: ahí vive el ADR
  propio de un proyecto consumidor (AI_COLLABORATION.md §5); es lo más
  peligroso de tocar por error y quedó con un test dedicado
  (`test_docs_architecture_never_appears_in_any_tier`).
- **Poda de subagentes por huella de contenido, no por nombre**: mismo
  criterio en `roles.sync()` (huérfanos) y `uninstall` (todos) — un archivo
  sin la huella `GENERATED_ROLE_MARKER` nunca se toca, sin importar su
  nombre o ubicación.
- **Test de "drift" nuevo, no planeado originalmente**: comparar
  `TIER2_PROTOCOL_PATHS` contra el `template/` real de este repositorio,
  para detectar si se agrega un archivo nuevo a la plantilla y se olvida
  cubrirlo en `uninstall.py`. Encontró 3 categorías de directorios que
  faltaban en el set de "cubiertos como unidad" del propio test
  (`.github/instructions`, `.github/ISSUE_TEMPLATE`,
  `.github/PULL_REQUEST_TEMPLATE`) antes de pasar limpio.
- **`CHANGELOG.md` completado para varias tareas atrás, no solo esta**: al
  escribir la entrada de esta tarea se notó que ninguna tarea anterior de
  la sesión (ADR-012, refuerzo de roles, diseño atómico) había quedado
  registrada, pese a que `continuum release` exige una entrada para poder
  liberar. Se completó todo de una vez.

## Suposiciones vigentes
- No se implementó actualización automática del badge de versión del
  README (problema real pero distinto — cosmético, registrado en
  `pendientes.md` si hace falta).
- `uninstall` no tiene confirmación interactiva (y/N) — consistente con que
  ningún comando del CLI la tiene; todo es por flags.

## Validación
- Ejecutada: `python3 -m unittest discover -s tests -t .` → 158 tests, 0
  fallos. `tools/continuum doctor` → 0 críticos.
- **Prueba de humo manual real** (no solo tests unitarios): proyecto
  sintético en `/tmp` con `git init` real, `install-hooks`, `roles sync`,
  un remoto `continuum`, y un hook `.githooks/pre-commit` editado a mano —
  se corrió la desinstalación completa (niveles 1+2+3) de verdad y se
  verificó con `git status`/`find` que sobrevivió exactamente lo esperado
  (el hook editado, `docs/architecture/`) y desapareció el resto, sin
  ningún commit automático.
- `continuum uninstall` (dry-run, nunca aplicado) corrido sobre este mismo
  repositorio de Continuum como verificación adicional — el plan generado
  coincide exactamente con el estado real.

## Siguiente paso recomendado
Tarea completa, sin trabajo bloqueado. Cerrar con `continuum task close
lifecycle-completo`. Pendiente real de seguimiento (no bloqueante,
registrado en `pendientes.md`): aplicar `docs/metodologia-medicion.md`
sobre un proyecto real, y considerar automatizar el badge de versión del
README si la deriva vuelve a ser un problema notado.
