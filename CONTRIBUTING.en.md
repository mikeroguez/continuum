# Contributing Guide

> [Leer en español](CONTRIBUTING.md) · [Language Policy](docs/LANGUAGE_POLICY.en.md)

This manual defines the workflow for contributing to Continuum: branching convention, commits, Pull Requests, and the release process (SemVer).

> [!NOTE]
> Teamwork rules and commit conventions are specified in [`AI_COLLABORATION.md`](AI_COLLABORATION.md) (§§6-7). This document specifically governs contributions to the Continuum meta-repository.

---

## Before Proposing a Change

- **Architecture or protocol changes**: Open an issue first to discuss the approach before writing code (affects `ARCHITECTURE.md`, `template/AI_COLLABORATION.md`, or the CLI).
- **Minor fixes or documentation**: You can open a Pull Request directly.

---

## Branching Convention

| Prefix | Purpose | Example |
| :--- | :--- | :--- |
| `feat/` | New feature | `feat/sync-branch-option` |
| `fix/` | Bug fix | `fix/memory-split-overwrite` |
| `docs/` | Documentation changes only | `docs/add-team-use-cases` |
| `refactor/` | Internal refactoring without behavioral change | `refactor/doctor-checks` |
| `chore/` | Maintenance, dependencies, and housekeeping | `chore/bump-deps` |
| `test/` | Unit testing | `test/session-start` |

### Primary Branches

- **`develop`**: Integration and active development branch. All work-in-progress commits are made here.
- **`main`**: Production and stable release branch. Only receives merges from `develop` when a release is authorized.
- **`export`**: Distributed branch maintained automatically via `git subtree split --prefix=template -b export`. No manual commits are made directly on this branch.

## Voting and `main` Protection

`main` is the production branch and does not accept direct pushes. Every
change must enter through a Pull Request with green CI checks, resolved
conversations, and CODEOWNERS review.

Integration decisions are made between **mikeroguez** and **wada8a**:

- The PR author does not count their own vote.
- The other owner must approve; when both owners review, the result must be
  two affirmative votes.
- A rejection keeps the PR open until the objections are addressed and it is
  reviewed again.
- If disagreement persists, keep the PR unmerged and open a Discussion or
  issue to record the decision.

The technical configuration lives in `.github/CODEOWNERS` and in the remote
branch protection for `main`; both must remain aligned with this policy.

---

## Commit Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/): type in English, short description in Spanish or English.

```text
feat: add template sync subcommand
fix: fix name collision in memory-split-legacy
docs: update adoption guide for teams
```

Allowed types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`, `ci`.

---

## Unit Testing

The test suite (`tests/`) uses only the Python 3 standard `unittest` library and tests the distributed source code in `template/tools/_continuum/`.

```bash
# Run full test suite
python3 -m unittest
```

> [!TIP]
> Any change to the CLI engine or protocol altering behavior should include a corresponding regression test.

---

## SemVer Versioning

Continuum follows [SemVer 2.0.0](https://semver.org/):

- **MAJOR** (`X.0.0`): Incompatible changes to `.ai/` structure or CLI breaking existing installations.
- **MINOR** (`1.X.0`): Backwards-compatible new features (subcommands, templates, modules).
- **PATCH** (`1.0.X`): Bug fixes or documentation adjustments.

Version truth lives in `__version__` in `template/tools/_continuum/__init__.py`, mirrored in `CHANGELOG.md` and tagged in Git (`vX.Y.Z`).

---

## Release Process

1. Open a Pull Request into `main` and obtain the required approval.
2. Update `__version__` in `tools/_continuum/__init__.py` and `template/tools/_continuum/__init__.py`.
3. Update `CHANGELOG.md` recording changes under `## [X.Y.Z] - YYYY-MM-DD`.
4. Run automated CLI release commands:
   ```bash
   python3 tools/continuum export refresh --no-dry-run
   python3 tools/continuum release vX.Y.Z --no-dry-run
   ```
5. Publish branches and tags to GitHub:
   ```bash
   git push origin main develop export --tags
   ```

---

<div align="center">

Continuum is maintained by [Mike Roguez](https://mikeroguez.me) under the [MIT License](LICENSE).

</div>
