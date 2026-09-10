# Continuum

> [Leer en español](README.md) · [Language policy](docs/LANGUAGE_POLICY.en.md)

**Source version:** `1dacfc8` (2026-09-09). The Spanish README is the
canonical source if the two versions differ.

Continuum is a reference template and a small CLI for teams working with
multiple AI assistants (Claude, Codex, Gemini, and others) in the same Git
repository. It keeps project context in the repository rather than relying on
the history of one assistant conversation.

## Why it exists

Continuum provides a shared, versioned place for the decisions and handoffs a
new session needs. Its protocol is designed so that a session can end, a team
member can take over, or a team can switch tools without rebuilding all context
from a chat history.

It provides:

- one protocol and shared memory that compatible assistants can read and
  update;
- structured handoffs and task records for continuity between sessions;
- small, on-demand context files instead of an ever-growing startup prompt;
- checks for declared provider support, stale state, duplicate files, and
  context size.

Continuum does **not** automatically assign work to AI providers or promise a
particular productivity outcome. It is a repository-native protocol and a set
of lightweight checks; teams decide how to use it.

For the design rationale and scope boundaries, see the canonical Spanish
[architecture document](ARCHITECTURE.md) and [research review](docs/investigacion-2026.md).

## Repository contents

| Path | Contents |
| --- | --- |
| `template/` | Everything installed into a destination project: protocol, task/handoff/ADR templates, the `continuum` CLI, Git hooks, Claude Code configuration, and CI workflow. |
| `ARCHITECTURE.md` | Design rationale, system layers, and deliberately excluded scope. |
| `docs/` | Decision log, rollout guide, research and product-planning material. Browse it in English through [the documentation index](docs/en/README.md). |
| `CONTRIBUTING.md` | Branch, pull-request, versioning, and release guidance. |

## Install with Git subtree

Continuum is distributed from one source repository. A destination project
imports its `template/` using `git subtree`, rather than copying individual
files by hand.

Use a released tag when you need a fixed, reproducible version:

```bash
git remote add continuum <continuum-repository-url>
git subtree add --prefix=. continuum v1.1.1 --squash -m "chore: install Continuum"
```

You can instead follow the `export` branch for the latest installable template:

```bash
git subtree add --prefix=. continuum export --squash -m "chore: install Continuum"
```

`export` contains the contents of `template/` at the project root. Always use
`--squash`: it keeps the destination project’s history to one installation or
update commit rather than importing Continuum’s development history.

After installation, complete the project name, providers, and synchronisation
settings in `.ai/config.json`, merge `.gitignore-continuum-fragment` into your
own `.gitignore`, then run:

```bash
tools/continuum install-hooks
tools/continuum doctor
```

## Update an installed project

```bash
tools/continuum sync-template
```

The command prints the exact `git subtree pull` command using the destination
project’s configured template remote and prefix.

## Core commands

```bash
tools/continuum                                  # concise project health check
tools/continuum session start                    # suggested context and active work
tools/continuum session end --message "..."      # write a session handoff
tools/continuum status                           # state and suggested next action
tools/continuum doctor --fix --dry-run           # preview safe repairs

tools/continuum context --task <slug> --why      # recommended initial reading
tools/continuum tokens                           # startup-context token estimate
tools/continuum task start <slug> --size medium  # record medium/large work
tools/continuum task claim <slug> <owner>        # make ownership visible
tools/continuum task close <slug>                # close work with a handoff
tools/continuum handoff --auto --provider codex  # record continuity

tools/continuum metrics report                   # local measurement report
tools/continuum metrics export --anonymize       # anonymised local export
tools/continuum roles list                       # roles in enabled packs
```

Run `tools/continuum --help` for the complete command list. Continuum requires
only Python 3 and Git; it has no external Python dependencies.

## Contribute

Read the [English contributing guide](CONTRIBUTING.en.md) before opening a
pull request. Changes to the distributable template or CLI should be reviewed
through a pull request; small documentation fixes may go directly to `main`.

## Licence

[MIT](LICENSE).
