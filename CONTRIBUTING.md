# Guía de contribución

Manual de colaboración de Continuum: cómo proponer cambios, convención de
ramas y commits, cuándo hace falta un PR, y cómo se versiona y libera. La
convención de commits detallada y las reglas de trabajo en equipo (incluido
el uso de `git worktree` para trabajo concurrente) ya están en
`AI_COLLABORATION.md` §§6-7 — no se duplican aquí, solo se referencian.

## Antes de proponer un cambio

Abre un issue si el cambio es de diseño (afecta `ARCHITECTURE.md`, el
protocolo en `template/AI_COLLABORATION.md`, o el comportamiento del CLI) —
así se discute el enfoque antes de escribir código. Para una corrección
puntual (typo, bug pequeño, ajuste de documentación) se puede ir directo a
un PR.

## Convención de ramas

| Prefijo   | Uso                                             |
|-----------|--------------------------------------------------|
| `feat/`   | Funcionalidad nueva                              |
| `fix/`    | Corrección de bugs                               |
| `docs/`   | Cambios de documentación (sin tocar código)      |
| `refactor/` | Cambio interno sin alterar comportamiento      |
| `chore/`  | Mantenimiento (dependencias, CI, housekeeping)   |
| `test/`   | Solo pruebas                                     |

Ejemplo: `fix/memory-split-legacy-overwrite`. Ramas cortas y de un solo
propósito — igual que el criterio de tarea en `AI_COLLABORATION.md` §2.

`main` es la única rama de desarrollo de larga duración. No hay `develop`
ni ramas de staging: el proyecto es un CLI más plantillas, no un servicio
con entornos que desplegar — mantener una sola rama larga es coherente con
el principio de "ceremonia proporcional al riesgo" (`ARCHITECTURE.md` §2).

`export` es una rama especial, generada por `git subtree split
--prefix=template -b export` (ver README.md). Nadie commitea directamente
ahí: se regenera en cada release (ver más abajo).

## Cuándo hace falta un Pull Request

- **Contribuciones externas:** siempre vía PR.
- **Cambios que tocan `template/tools/_continuum/` (el CLI) o el protocolo**
  (`template/AI_COLLABORATION.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`):
  vía PR aunque lo abra quien mantiene el repositorio — el objetivo es que
  el check de CI (`continuum doctor`, `.github/workflows/continuum-doctor.yml`)
  corra antes de mergear, porque un bug ahí se propaga a todo proyecto que
  haga `git subtree pull` después.
- **Documentación menor o ajustes en `docs/` o en la memoria autoalojada**
  (`.ai/state/topics/*.md`): commit directo a `main` es aceptable.

El PR debe dejar `tools/continuum doctor` en cero problemas críticos antes
de mergear (el hook de pre-commit y el workflow de CI ya lo verifican).

## Tests

Suite de tests (`tests/`, stdlib `unittest`, sin dependencias nuevas) contra
el código fuente en `template/tools/_continuum/` — no contra la copia
autoalojada en la raíz. Vive solo en este meta-repositorio: no se distribuye
a los proyectos que incorporan Continuum (`.github/workflows/tests.yml` está
únicamente en la raíz, no en `template/`).

```bash
python3 -m unittest discover -s tests -t . -v
```

Cualquier cambio en `template/tools/_continuum/` que toque comportamiento
(no solo texto de ayuda) debería venir acompañado de un test — en particular
si corrige un bug: dos bugs reales encontrados durante el desarrollo
(`memory-split-legacy` sobreescribiendo un tema existente, `packetize` con
rutas relativas) quedaron como pruebas de regresión en `tests/test_memory.py`
y `tests/test_packets.py`, precisamente para que no vuelvan a aparecer.

## Convención de commits

Conventional Commits, tipo en inglés, mensaje en español — igual que
`AI_COLLABORATION.md` §7: `feat|fix|docs|refactor|test|chore|perf|ci`.
Ejemplo: `fix: corrige colisión de nombres en memory-split-legacy`.

## Versionado

Continuum se versiona con [SemVer](https://semver.org/lang/es/)
(`MAJOR.MINOR.PATCH`), en conjunto para el protocolo y el CLI —vive todo en
`template/`, así que se libera junto—:

- **MAJOR:** cambio incompatible en la estructura de `.ai/` que rompería un
  proyecto ya instalado, o un subcomando de `continuum` removido/renombrado
  sin alias de compatibilidad.
- **MINOR:** funcionalidad nueva retrocompatible (subcomando, plantilla).
- **PATCH:** corrección de bugs o ajustes de documentación dentro de
  `template/`.

La fuente de verdad de la versión es `template/tools/_continuum/__init__.py`
(`__version__`), reflejada en un tag de git y en `CHANGELOG.md`.

## Proceso de release

1. Mergear a `main` los cambios que forman parte de la versión.
2. Actualizar `__version__` en `template/tools/_continuum/__init__.py`
   **y** en la copia autoalojada `tools/_continuum/__init__.py`.
3. Mover las entradas correspondientes de `CHANGELOG.md`, de `[Unreleased]`
   a una sección nueva `## [X.Y.Z] - YYYY-MM-DD`.
4. Regenerar la rama `export`:
   ```bash
   git branch -D export
   git subtree split --prefix=template -b export
   git push origin export --force-with-lease
   ```
5. Etiquetar y publicar:
   ```bash
   git tag -a vX.Y.Z export -m "vX.Y.Z"
   git push origin vX.Y.Z
   ```
6. Crear el Release en GitHub a partir del tag, con las notas del
   `CHANGELOG.md`.

**Proyectos que consumen Continuum:** se recomienda fijar `git subtree
add`/`pull` a un tag (`vX.Y.Z`) en vez de seguir `main` o `export` de forma
flotante, para decidir de forma explícita cuándo se adopta una versión que
podría no ser retrocompatible (ver `README.md` § Instalación).

## Protección de rama (configuración en GitHub)

Recomendado en Settings -> Branches / Rulesets:

### `main`

- Exigir Pull Request antes de mergear.
- Exigir checks antes de mergear:
  - `doctor`
  - `unittest (3.10)`
  - `unittest (3.12)`
- No permitir force-push.
- No permitir borrado de la rama.
- Requerir que la rama esté actualizada antes de mergear cuando haya más de
  un mantenedor activo.

### `export`

`export` es una rama generada; nadie commitea directamente ahí.

- No exigir PR: no se desarrolla en esta rama.
- Permitir actualizaciones mediante `git push origin export --force-with-lease`
  desde el proceso de release.
- No permitir borrado accidental.
- Etiquetar cada release estable (`vX.Y.Z`) apuntando al commit de `export`.

Si GitHub Rulesets no permite expresar "solo force-push controlado durante
release", deja `export` sin protección estricta y trata los tags como la
superficie estable de consumo. Los proyectos destino deberían preferir tags
para instalaciones reproducibles.
