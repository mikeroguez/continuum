# Tarea: lifecycle-completo

**Creada:** 2026-09-12 · **Tamaño:** large · **Owner:** mike · **Rol:** (sin asignar)

## Objetivo
El owner notó que no existe forma de desinstalar Continuum de un proyecto,
y preguntó si había mecanismos similares faltantes. Auditoría confirmó 4
huecos, todos con el mismo patrón ("instala/genera pero nunca limpia"):
`continuum uninstall`, `continuum version`/`--version`, poda de archivos
huérfanos en `continuum roles sync`, y reverso de `install-hooks`. El
owner pidió implementar los cuatro ("todo lo necesario").

## Incluido en el alcance
- `continuum version` / `--version`: nuevo archivo `VERSION` en la raíz
  (fuente única, sin dependencias) + comando que lo reporta. `continuum
  release --no-dry-run` lo actualiza automáticamente al liberar, para que
  no sea un tercer lugar más que sincronizar a mano (mismo patrón de
  ADR-012: mecanizar en vez de confiar en la memoria humana).
- `continuum roles sync`: al final de generar para un proveedor, poda los
  archivos generados por Continuum (detectados por una huella de contenido,
  no por nombre) que ya no correspondan a ningún rol activo del catálogo.
  Nunca toca un archivo que no lleve esa huella.
- `continuum uninstall`: comando nuevo con tres niveles de seguridad —
  1. **Mecanismo** (se borra directo con `--no-dry-run`): `tools/continuum`,
     `tools/_continuum/`, subagentes generados (huella verificada),
     `.githooks/pre-commit` y `.githooks/README.md` (solo si su contenido
     coincide con lo que Continuum instaló), `.gitignore-continuum-fragment`,
     `.ai/templates/`, y el remoto git `continuum` si existe.
  2. **Protocolo/config** (se lista, requiere `--yes` para incluirse):
     entrypoints (`AI_COLLABORATION.md`/`AGENTS.md`/`CLAUDE.md`/`GEMINI.md`/
     `.github/copilot-instructions.md`), `.ai/config.json`, `.ai/roles/`,
     `.claude/settings.json`, los docs que Continuum shippea en `docs/`,
     workflows de GitHub que Continuum shippea.
  3. **Memoria del proyecto** (nunca se toca salvo `--purge-memory`
     explícito, aparte de `--yes`): `.ai/HANDOFF.md`, `.ai/state/`,
     `.ai/tasks/` — es historia real de decisiones, no algo que Continuum
     "instaló".
  Dry-run por defecto (mismo patrón que `doctor --fix`/`sync --apply`/
  `release`). Rechaza correr con el working tree sucio. Nunca commitea por
  sí solo ni reescribe historia de git — solo borra en disco y deja que la
  persona revise `git status`/`git diff` y commitee.
- Detección de "archivo generado por Continuum" centralizada en
  `common.py` (`generated_role_slug`) para que `roles.py` y el nuevo
  `uninstall.py` compartan el mismo criterio, no dos implementaciones que
  puedan divergir.

## Explícitamente fuera de alcance
- Reescribir o deshacer el historial de `git subtree` — no hay forma segura
  de hacerlo automáticamente; el borrado queda como un commit normal más.
- Confirmación interactiva (prompt y/N) — el CLI no tiene ningún prompt
  interactivo en ningún comando existente (todo es flags: `--dry-run`,
  `--apply`, `--yes`); mantener esa consistencia en vez de introducir el
  único punto interactivo del CLI.
- Actualizar automáticamente el badge de versión del README — es un
  problema real pero distinto (cosmético, no de integridad de datos); se
  registra en pendientes si hace falta después.
- Prune de roles para más convenciones de agentes generadas que no sean
  las 4 ya soportadas (claude/copilot/codex/gemini).

## Write-set (archivos que se espera tocar)
No editar fuera de esta lista sin actualizarla primero. Evita refactors oportunistas.

- `VERSION` (nuevo) y `template/VERSION` (nuevo) — ambos con la versión
  actual (`1.4.1`), mismo espejo raíz/`template` que `AI_COLLABORATION.md`
- `tools/_continuum/common.py` y `template/tools/_continuum/common.py` (helper `generated_role_slug`)
- `tools/_continuum/roles.py` y `template/tools/_continuum/roles.py` (poda de huérfanos)
- `tools/_continuum/uninstall.py` (nuevo) y `template/tools/_continuum/uninstall.py` (nuevo)
- `tools/_continuum/release.py` y `template/tools/_continuum/release.py` (actualiza `VERSION` al liberar)
- `tools/_continuum/__main__.py` y `template/tools/_continuum/__main__.py` (registro de `version`/`--version` y `uninstall`)
- `AI_COLLABORATION.md` y `template/AI_COLLABORATION.md` (mención breve de `uninstall`/`version` donde ya se documenta el CLI)
- `README.md` y `README.en.md` (sección de instalación: mencionar `uninstall`; tabla de comandos)
- `CHANGELOG.md` (entrada nueva)
- `tests/test_uninstall.py` (nuevo), `tests/test_roles.py` (poda), `tests/test_release_cmd.py` (VERSION), y un test nuevo para `version`/`--version`

## Fuentes de verdad a leer antes de empezar
- `.ai/state/estado-dev.md`
- `README.md` (sección "Instalar en un proyecto existente" — qué trae
  exactamente `git subtree add --prefix=.`)
- `tools/_continuum/bootstrap.py` (`install_hooks`, `cmd_sync`)
- `tools/_continuum/roles.py` (formato exacto de los archivos generados —
  la huella a detectar)
- `docs/rollout-guide.md` Caso 1 (evidencia de que los entrypoints sí se
  personalizan en la práctica — por qué son Tier 2, no Tier 1)
- `docs/decision-log.md` ADR-010 (huella sha256 de copilot-instructions.md
  — mismo espíritu de detección mecánica que se reutiliza aquí)

## Contexto mínimo sugerido
Según el tamaño declarado arriba, no cargues más de lo necesario:

| Tamaño  | Techo de lectura inicial orientativo |
|---------|----------------------------------------|
| small   | 1-3 archivos concretos, sin explorar carpetas completas |
| medium  | 1 módulo/dominio, usar `rg`/`grep` para localizar antes de leer |
| large   | fragmentar con `continuum packetize`; considerar dividir en subtareas |

Considerar cerrar tras `version` + poda de roles (quick wins, bajo riesgo)
si el contexto se agota antes de llegar a `uninstall`, y abrir una tarea
`medium` aparte solo para `uninstall` (es la pieza más grande y riesgosa).
