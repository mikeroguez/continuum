<p align="center"><strong>Continuum</strong></p>

<p align="center">Protocolo y herramientas de memoria para equipos que trabajan con múltiples asistentes de IA (Claude, Codex, Gemini) sobre el mismo repositorio.</p>

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

## Instalación (git subtree)

Este repositorio se distribuye como fuente única; cada proyecto destino lo
incorpora con `git subtree`, no copiando archivos a mano — la copia manual
diverge con el tiempo (ver `ARCHITECTURE.md` §1 para la evidencia).

Una sola vez por proyecto destino:

```bash
git remote add continuum <url-de-este-repositorio>
git subtree add --prefix=. continuum main --squash -m "chore: instala Continuum"
```

`--prefix=.` monta el contenido de `template/` en la raíz del proyecto
destino. Ver la nota técnica sobre `git subtree split` más abajo para cómo
se logra que solo el contenido de `template/`, y no el repositorio completo,
termine en la raíz del proyecto destino.

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
`main`.

## Actualizar un proyecto que ya tiene Continuum instalado

```bash
tools/continuum sync-template
```

Imprime el comando exacto de `git subtree pull`, usando `template_remote` y
`template_prefix` desde `.ai/config.json`.

## Contribuir una mejora de vuelta

Un cambio genérico del protocolo o del CLI hecho mientras se trabaja en un
proyecto concreto se propaga de vuelta con `git subtree push` (el mismo
comando que imprime `sync-template`, en sentido inverso), para que el resto
de los proyectos se beneficien en su próxima sincronización.

## Uso del CLI

```bash
tools/continuum                          # doctor: estado general en segundos
tools/continuum task start <slug> --size small|medium|large
tools/continuum task claim <slug> <owner>
tools/continuum task close <slug>
tools/continuum handoff --message "..."
tools/continuum handoff --auto --provider claude
tools/continuum compact --topic <nombre>
tools/continuum memory-split-legacy
tools/continuum packetize <archivo> [--slug <slug>]
tools/continuum install-hooks
```

Requiere únicamente Python 3 (sin dependencias externas) y git.

## Licencia

Pendiente de definir antes de la publicación pública del repositorio.
