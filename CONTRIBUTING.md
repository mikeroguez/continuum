# Guía de Contribución

> [Read in English](CONTRIBUTING.en.md) · [Política de Idiomas](docs/LANGUAGE_POLICY.md)

Este manual establece el flujo de trabajo para colaborar en Continuum: convención de ramas, commits, Pull Requests y el proceso de lanzamientos (SemVer).

> [!NOTE]
> Las reglas de trabajo en equipo y convenciones de commits ya están especificadas en [`AI_COLLABORATION.md`](AI_COLLABORATION.md) (§§6-7). Este documento norma específicamente las contribuciones al meta-repositorio de Continuum.

---

## Antes de Proponer un Cambio

- **Cambios de arquitectura o protocolo**: Abre un issue previo para discutir el enfoque antes de escribir código (afecta `ARCHITECTURE.md`, `template/AI_COLLABORATION.md` o el CLI).
- **Correcciones menores o documentación**: Puedes abrir directamente un Pull Request.

---

## Convención de Ramas

| Prefijo | Propósito | Ejemplo |
| :--- | :--- | :--- |
| `feat/` | Funcionalidad nueva | `feat/sync-branch-option` |
| `fix/` | Corrección de errores | `fix/memory-split-overwrite` |
| `docs/` | Cambios de documentación exclusivamente | `docs/add-team-use-cases` |
| `refactor/` | Refactorización interna sin cambio de comportamiento | `refactor/doctor-checks` |
| `chore/` | Mantenimiento, dependencias y housekeeping | `chore/bump-deps` |
| `test/` | Pruebas unitarias | `test/session-start` |

### Ramas Principales

- **`develop`**: Rama de integración y desarrollo activo. Todos los commits de trabajo en progreso se realizan en esta rama.
- **`main`**: Rama de producción y lanzamientos estables. Solo recibe merges desde `develop` cuando un release es autorizado.
- **`export`**: Rama distribuida mantenida automáticamente vía `git subtree split --prefix=template -b export`. Ninguna persona realiza commits manuales directos sobre ella.

## Votación y Protección de `main`

`main` es la rama de producción y no acepta pushes directos. Cada cambio debe
entrar mediante Pull Request con los checks de CI en verde, conversaciones
resueltas y revisión de CODEOWNERS.

La decisión de integrar se toma entre **mikeroguez** y **wada8a**:

- Quien abre el PR no cuenta su propio voto.
- Se requiere la aprobación del otro propietario; si ambos revisan, el
  resultado debe ser 2 votos favorables.
- Un voto en contra mantiene el PR abierto hasta que se atiendan las
  objeciones y se vuelva a revisar.
- En caso de desacuerdo persistente, el PR no se integra y se abre una
  Discussion o issue para registrar la decisión.

La configuración técnica vive en `.github/CODEOWNERS` y en la protección
remota de la rama `main`; ambas deben mantenerse alineadas con esta política.

---

## Convención de Commits

Seguimos [Conventional Commits](https://www.conventionalcommits.org/es/v1.0.0/): tipo en inglés, descripción breve en español.

```text
feat: agrega subcomando de sincronización de plantilla
fix: corrige colisión de nombres en memory-split-legacy
docs: actualiza guía de adopción para equipos
```

Tipos permitidos: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`, `ci`.

---

## Pruebas Unitarias

La suite de pruebas (`tests/`) utiliza únicamente la biblioteca estándar `unittest` de Python 3 y prueba el código fuente distribuido en `template/tools/_continuum/`.

```bash
# Ejecutar la suite completa de pruebas
python3 -m unittest
```

> [!TIP]
> Todo cambio en el motor CLI o en el protocolo que altere comportamiento debe incluir su correspondiente prueba unitaria de regresión.

---

## Versionado SemVer

Continuum utiliza [SemVer 2.0.0](https://semver.org/lang/es/):

- **MAJOR** (`X.0.0`): Cambios incompatibles en la estructura de `.ai/` o en el CLI que romperían proyectos ya instalados.
- **MINOR** (`1.X.0`): Funcionalidad nueva retrocompatible (nuevos subcomandos, plantillas o módulos).
- **PATCH** (`1.0.X`): Correcciones de errores o mejoras de documentación.

La fuente de verdad de la versión es `__version__` en `template/tools/_continuum/__init__.py`, reflejada en `CHANGELOG.md` y etiquetada en Git (`vX.Y.Z`).

---

## Proceso de Lanzamiento (Release)

1. Abrir un Pull Request hacia `main` y obtener la aprobación requerida.
2. Actualizar `__version__` en `tools/_continuum/__init__.py` y `template/tools/_continuum/__init__.py`.
3. Actualizar `CHANGELOG.md` registrando los cambios bajo `## [X.Y.Z] - YYYY-MM-DD`.
4. Ejecutar los comandos automatizados del CLI:
   ```bash
   python3 tools/continuum export refresh --no-dry-run
   python3 tools/continuum release vX.Y.Z --no-dry-run
   ```
5. Publicar ramas y tags en GitHub:
   ```bash
   git push origin main develop export --tags
   ```

---

<div align="center">

Continuum está mantenido por [Mike Roguez](https://mikeroguez.me) bajo Licencia [MIT](LICENSE).

</div>
