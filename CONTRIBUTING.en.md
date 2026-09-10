# Contributing to Continuum

> [Leer en español](CONTRIBUTING.md) · [Language policy](docs/LANGUAGE_POLICY.en.md)

**Source version:** `1dacfc8` (2026-09-09). The Spanish guide is canonical if
the two versions differ.

This guide explains how to propose a change, name branches and commits, decide
when a pull request is required, and prepare a release. The shared working
protocol lives in `AI_COLLABORATION.md`; this document links to it rather than
duplicating its task and team-work rules.

## Before proposing a change

Open an issue first when the proposal changes the design, the template protocol,
or CLI behaviour. Small fixes—such as a typo, a focused bug fix, or a narrow
documentation change—can go straight to a pull request.

## Branches

Use a short, single-purpose branch with one of these prefixes:

| Prefix | Use |
| --- | --- |
| `feat/` | New functionality |
| `fix/` | Bug fix |
| `docs/` | Documentation-only change |
| `refactor/` | Internal behaviour-preserving change |
| `chore/` | Maintenance |
| `test/` | Tests only |

`main` is the long-lived development branch. `export` is generated from
`template/` with `git subtree split`; do not commit to it directly.

## Pull requests

External contributions always use a pull request. A pull request is also
required for changes to `template/tools/_continuum/` or to the shared protocol
and provider entrypoints, even when made by a maintainer. This protects projects
that later import the template.

Focused documentation changes and updates to self-hosted working memory may be
committed directly to `main` when appropriate.

Before merging, run:

```bash
tools/continuum doctor
python3 -m unittest discover -s tests -t . -v
```

Changes to CLI behaviour should include a regression test where practical.

## Commits

Use Conventional Commit types in English:

```text
feat | fix | docs | refactor | test | chore | perf | ci
```

Write the message in the working language of the team. When a task exists,
prefix the message with its slug so that its history stays searchable.

## Documentation languages

Spanish is Continuum’s canonical documentation language. English versions are
maintained for onboarding and contribution. When changing a paired document,
review its counterpart and follow the [language policy](docs/LANGUAGE_POLICY.en.md)
instead of silently allowing the two versions to drift.

## Versioning and releases

Continuum follows [Semantic Versioning](https://semver.org/):

- **MAJOR** for incompatible changes to `.ai/` structure or removed/renamed
  CLI commands without a compatibility alias;
- **MINOR** for backward-compatible functionality;
- **PATCH** for fixes and documentation changes within `template/`.

The source of truth for the version is
`template/tools/_continuum/__init__.py`, reflected in a Git tag and the
changelog. A release updates both the template and the self-hosted CLI copy,
updates `CHANGELOG.md`, regenerates `export`, pushes its tag, and creates the
GitHub release.

Destination projects should normally install a released tag rather than follow
the floating `main` or `export` branches.

## Branch protection

Protect `main` against deletion and force-pushes, and require these checks for
pull requests when there is more than one active maintainer:

- `doctor`
- `unittest (3.10)`
- `unittest (3.12)`

`export` is generated only during a release. If branch rules cannot express a
controlled release-only force push, treat release tags as the stable consumer
surface instead.
