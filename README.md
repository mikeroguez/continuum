<p align="center"><strong>Continuum</strong></p>

<p align="center">Protocolo y herramientas de memoria para equipos que trabajan con múltiples asistentes de IA (Claude, Codex, Gemini) sobre el mismo repositorio.</p>

<p align="center">
  <a href="https://github.com/mikeroguez/continuum/actions/workflows/continuum-doctor.yml"><img alt="continuum doctor" src="https://github.com/mikeroguez/continuum/actions/workflows/continuum-doctor.yml/badge.svg"></a>
  <a href="https://github.com/mikeroguez/continuum/actions/workflows/tests.yml"><img alt="tests" src="https://github.com/mikeroguez/continuum/actions/workflows/tests.yml/badge.svg"></a>
  <a href="LICENSE"><img alt="Licencia MIT" src="https://img.shields.io/badge/licencia-MIT-blue.svg"></a>
</p>

---

## Qué es

Continuum es una plantilla de referencia, más un CLI ligero, para persistir
el contexto de un proyecto de software en el propio repositorio de git —
en lugar de en el historial de una conversación con un asistente de IA — de
forma que:

- Cualquier proveedor de IA compatible con la convención [`AGENTS.md`](https://agents.md)
  (Claude Code, Codex, Gemini CLI, y otros) puede leer y actualizar el mismo
  contexto, sin traducción ni duplicación.
- Una sesión puede terminar de forma abrupta — por límite de tokens, cambio
  de proveedor o cambio de persona — sin perder el hilo del trabajo.
- Varias personas o varios agentes pueden trabajar sobre el mismo repositorio
  sin pisarse ni duplicar esfuerzo.
- El costo en tokens del contexto que cada sesión nueva tiene que cargar se
  mide y se mantiene acotado.

El razonamiento completo — qué problema resuelve, qué alternativas se
descartaron y por qué, y qué evidencia respalda cada decisión — está en
[`ARCHITECTURE.md`](ARCHITECTURE.md) y en [`docs/investigacion-2026.md`](docs/investigacion-2026.md).
Este README cubre solo instalación y operación.

## Contenido del repositorio

| Ruta                         | Contenido                                                                                                                                                                  |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `template/`                  | Todo lo que se instala en un proyecto destino: protocolo, plantillas de tarea/handoff/ADR, el CLI `continuum`, hooks de git, configuración de Claude Code, workflow de CI. |
| `ARCHITECTURE.md`            | Diseño: diagnóstico, principios, capas del sistema, alcance explícito (qué se decidió no construir).                                                                       |
| `docs/investigacion-2026.md` | Revisión de literatura e industria que valida o corrige el diseño, con fuentes.                                                                                            |
| `docs/decision-log.md`       | Historial de decisiones sobre la arquitectura misma, en formato ADR.                                                                                                       |
| `docs/rollout-guide.md`      | Procedimiento para adoptar la plantilla en un proyecto ya existente.                                                                                                       |
| `CONTRIBUTING.md`            | Manual de colaboración: ramas, commits, Pull Requests, versionado y releases.                                                                                              |
| `CHANGELOG.md`               | Historial de cambios por versión (Keep a Changelog).                                                                                                                       |

## Instalación (git subtree)

Este repositorio se distribuye como fuente única; cada proyecto destino lo
incorpora con `git subtree`, no copiando archivos a mano — la copia manual
diverge con el tiempo (ver `ARCHITECTURE.md` §1 para la evidencia).

Una sola vez por proyecto destino:

```bash
git remote add continuum <url-de-este-repositorio>
git subtree add --prefix=. continuum v1.0.0 --squash -m "chore: instala Continuum"
```

`--prefix=.` monta el contenido de `template/` en la raíz del proyecto
destino. Ver la nota técnica sobre `git subtree split` más abajo para cómo
se logra que solo el contenido de `template/`, y no el repositorio completo,
termine en la raíz del proyecto destino.

También puedes seguir la rama flotante `export` si quieres recibir siempre la
plantilla instalable más reciente:

```bash
git subtree add --prefix=. continuum export --squash -m "chore: instala Continuum"
```

Después de instalar, completar el nombre del proyecto, los proveedores en
uso y los datos de sincronización (`template_remote` / `template_prefix`):

```bash
$EDITOR .ai/config.json
```

Fusionar el fragmento de `.gitignore` con el del proyecto y eliminarlo:

```bash
cat .gitignore-continuum-fragment >> .gitignore
rm .gitignore-continuum-fragment
```

Instalar los hooks locales y verificar el estado:

```bash
tools/continuum install-hooks
tools/continuum doctor
```

### Nota técnica: aislar `template/` en la distribución

`git subtree` trae el repositorio de origen completo bajo el prefix
indicado. Para que solo el contenido de `template/` —y no esa carpeta como
subdirectorio— termine en la raíz del proyecto destino, este repositorio
mantiene una rama `export` generada con:

```bash
git subtree split --prefix=template -b export
```

Los proyectos destino deben apuntar su subtree a la rama `export`, no a
`main`, o a un tag de release (`v1.0.0`, `v1.1.0`, etc.) si quieren una
versión fija y reproducible.

### ¿El historial de desarrollo de Continuum se mezcla con el de mi proyecto?

No, siempre que se instale con `--squash` (como en el comando de arriba —
es la razón por la que está ahí, no es opcional). Verificado de forma
empírica, no solo por documentación de `git subtree`:

- **`git log` del proyecto destino** solo gana **un commit** por instalación
  (o por actualización), sin importar cuántos commits tenga Continuum en su
  propio historial. Los commits individuales de Continuum nunca aparecen
  intercalados con los del proyecto.
- **Nadie que clone el proyecto después ve ese historial.** Se probó con un
  clon real (forzando el mecanismo de transferencia por red, el mismo que
  usa GitHub): el `.git` de un clon fresco no contiene los commits
  individuales de Continuum — ni con `git log --all`, ni pidiéndolos por
  hash directamente. Solo se transfieren los blobs/árboles necesarios para
  el commit "squash", no la historia completa.
- El único lugar donde el historial completo de Continuum existe de forma
  temporal es el `.git` local de quien ejecuta `git subtree add` por
  primera vez (queda referenciado por la rama de seguimiento
  `continuum/main`, necesaria para poder hacer `subtree pull`/`push`
  después). No se sube a ningún remoto compartido ni le llega a nadie más
  del equipo.

**Sin `--squash`**, en cambio, sí ocurre lo que se quiere evitar: los
commits de Continuum quedan intercalados en el historial real del proyecto
de forma permanente, visibles para siempre en `git log`.

Si aun así se prefiere cero rastro —ni siquiera esa presencia local y
temporal—, la alternativa es no usar `git subtree` en absoluto: copiar
`template/` a mano (`cp -r`/`rsync`) y comitearlo como archivos nuevos del
proyecto, sin agregar el remoto `continuum`. El costo es perder
`git subtree pull`/`push` para sincronizar actualizaciones — cada
actualización futura sería copiar de nuevo y revisar el diff a mano.

## Actualizar un proyecto que ya tiene Continuum instalado

```bash
tools/continuum sync-template
```

Imprime el comando exacto de `git subtree pull`, usando `template_remote` y
`template_prefix` desde `.ai/config.json`.

## Contribuir una mejora de vuelta

Un cambio genérico del protocolo o del CLI hecho mientras se trabaja en un
proyecto concreto se propaga de vuelta con `git subtree push` (el mismo
comando que imprime `sync-template`, en sentido inverso). Ver
[`CONTRIBUTING.md`](CONTRIBUTING.md) para ramas, commits, cuándo hace falta
un Pull Request, y cómo se versiona y libera.

## Uso del CLI

```bash
tools/continuum                          # doctor: estado general en segundos
tools/continuum session start [--json]   # inicio de sesión: handoff, tareas activas y contexto sugerido
tools/continuum session end [--message "..."] [--auto] [--provider <p>] [--role <r>] [--json] # cierre de sesión y lint
tools/continuum status [--json]          # estado compacto y siguiente acción sugerida
tools/continuum doctor --fix [--dry-run|--no-dry-run] # plan o ejecución de auto-reparaciones seguras

tools/continuum context [--task <slug>] [--why] [--json] # lectura recomendada inicial
tools/continuum tokens [--json]          # desglose de presupuesto de tokens
tools/continuum metrics snapshot [--dry-run|--no-dry-run] [--json] # baseline de métricas
tools/continuum metrics report [--json]    # reporte de impacto y métricas
tools/continuum metrics export [--format json|csv] [--anonymize] [--json] # exportar métricas
tools/continuum metrics compare [--json]   # comparación vs baseline
tools/continuum task start <slug> --size small|medium|large [--role <slug>]
tools/continuum task claim <slug> <owner>
tools/continuum task current [--json]
tools/continuum task resume [<slug>] [--json]
tools/continuum task close <slug>

tools/continuum handoff --message "..." [--role <slug>]
tools/continuum handoff --auto --provider claude|codex|gemini [--role <slug>]
tools/continuum compact --topic <nombre>
tools/continuum memory-split-legacy
tools/continuum packetize <archivo> [--slug <slug>]
tools/continuum install-hooks
tools/continuum sync [--check|--dry-run|--apply] [--json] # sincronización con repositorio plantilla
tools/continuum export status|refresh      # gestión de la rama export del meta-repositorio
tools/continuum release <versión> [--dry-run|--no-dry-run] # liberación e id de versión SemVer
tools/continuum github protect [--print|--apply] [--json] # auditoría y protección de ramas/tags en GitHub
tools/continuum roles list                # roles disponibles en los packs activos



tools/continuum roles sync                # genera subagentes de Claude Code (.claude/agents/)
```

Requiere únicamente Python 3 (sin dependencias externas) y git. Ver
`AI_COLLABORATION.md` §9 para el catálogo de roles/personas por dominio
(software, investigación, contenido educativo).

## Licencia

[MIT](LICENSE).

## Autor

Mike Roguez — [mikeroguez.me](https://mikeroguez.me/) · [github.com/mikeroguez](https://github.com/mikeroguez/)
