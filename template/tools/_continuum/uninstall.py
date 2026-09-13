"""continuum uninstall: reversa segura de lo que `git subtree add` +
`install-hooks` + `roles sync` trajeron a un proyecto.

`git subtree add --prefix=. ... --squash` mezcla el contenido de la
plantilla como si fueran archivos propios del proyecto — no hay un
"deshacer" nativo de git para eso. Este módulo borra en disco lo que
corresponde y deja que la persona revise y commitee; nunca reescribe
historia ni commitea por sí solo.

Tres niveles de seguridad, de menor a mayor riesgo de tocar algo que el
equipo personalizó (ver `docs/decision-log.md` para el razonamiento y
`rollout-guide.md` Caso 1, que documenta que los entrypoints sí se
personalizan en la práctica):

- **Nivel 1 (mecanismo)**: el CLI en sí, plantillas de generación, y
  cualquier archivo que lleve una huella verificable de que Continuum lo
  escribió (subagentes generados, el hook de pre-commit exacto). Se borra
  con solo `--no-dry-run`.
- **Nivel 2 (protocolo/config)**: entrypoints, configuración, catálogo de
  roles, docs shippeados. Requiere `--yes` además de `--no-dry-run`.
- **Nivel 3 (memoria del proyecto)**: `.ai/HANDOFF.md`, `.ai/state/`,
  `.ai/tasks/` — es historia real de decisiones, no algo que Continuum
  "instaló". Nunca se toca salvo `--purge-memory` explícito.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from . import common as c

# Archivos/directorios que la plantilla shippea y cuyo contenido no lleva
# una huella verificable propia — se listan a mano porque no hay forma
# mecánica de probar "esto lo trajo Continuum" sin ella. Si `template/`
# agrega un archivo nuevo, agrégalo aquí también (hay un test que compara
# esta lista contra `template/` real en este mismo repositorio).
TIER2_PROTOCOL_PATHS = [
    "AI_COLLABORATION.md",
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    ".github/copilot-instructions.md",
    ".github/ISSUE_TEMPLATE",
    ".github/PULL_REQUEST_TEMPLATE",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/instructions",
    ".github/workflows/continuum-doctor.yml",
    ".ai/config.json",
    ".ai/roles",
    ".claude/settings.json",
    "docs/README.md",
    "docs/como-usar-continuum.md",
    "docs/copilot-code-review.md",
    "docs/guia-para-agentes.md",
    "docs/guide-for-agents.md",
    "docs/metodologia-medicion.md",
    "docs/using-continuum.md",
    "VERSION",
]

TIER3_MEMORY_PATHS = [
    ".ai/HANDOFF.md",
    ".ai/state",
    ".ai/tasks",
]

_ROLE_AGENT_GLOBS = [
    (".claude/agents", "*.md"),
    (".github/agents", "*.agent.md"),
]
_ROLE_SKILL_DIRS = [".agents/skills", ".gemini/skills"]

_HOOK_MARKER = "Instalado por continuum install-hooks"
_HOOKS_README_MARKER = "Vacío a propósito en la plantilla"


def _generated_role_paths(root: Path) -> list[Path]:
    """Todo archivo/directorio que `roles.sync()` generó, en cualquiera de
    los 4 proveedores soportados — detectado por huella, no por ruta."""
    found: list[Path] = []
    for rel_dir, pattern in _ROLE_AGENT_GLOBS:
        d = root / rel_dir
        if not d.exists():
            continue
        for f in d.glob(pattern):
            if c.generated_role_slug(c.read_text(f)):
                found.append(f)
    for rel_dir in _ROLE_SKILL_DIRS:
        d = root / rel_dir
        if not d.exists():
            continue
        for sub in d.iterdir():
            skill_md = sub / "SKILL.md"
            if sub.is_dir() and skill_md.exists() and c.generated_role_slug(c.read_text(skill_md)):
                found.append(sub)
    return found


def _tier1_paths(root: Path) -> list[Path]:
    paths: list[Path] = []
    if (root / "tools" / "continuum").exists():
        paths.append(root / "tools" / "continuum")
    if (root / "tools" / "_continuum").exists():
        paths.append(root / "tools" / "_continuum")
    if (root / ".ai" / "templates").exists():
        paths.append(root / ".ai" / "templates")
    if (root / ".gitignore-continuum-fragment").exists():
        paths.append(root / ".gitignore-continuum-fragment")

    hook_path = root / ".githooks" / "pre-commit"
    if hook_path.exists() and _HOOK_MARKER in c.read_text(hook_path):
        paths.append(hook_path)
    readme_path = root / ".githooks" / "README.md"
    if readme_path.exists() and _HOOKS_README_MARKER in c.read_text(readme_path):
        paths.append(readme_path)

    paths.extend(_generated_role_paths(root))
    return paths


def _tier2_paths(root: Path) -> list[Path]:
    return [root / p for p in TIER2_PROTOCOL_PATHS if (root / p).exists()]


def _tier3_paths(root: Path) -> list[Path]:
    return [root / p for p in TIER3_MEMORY_PATHS if (root / p).exists()]


def build_plan(root: Path) -> dict:
    tier1 = _tier1_paths(root)
    tier2 = _tier2_paths(root)
    tier3 = _tier3_paths(root)

    hook_editado = (
        (root / ".githooks" / "pre-commit").exists()
        and (root / ".githooks" / "pre-commit") not in tier1
    )

    remote_res = c.git("remote")
    has_continuum_remote = "continuum" in remote_res.stdout.split()

    hooks_path_res = c.git("config", "core.hooksPath")
    hooks_path_is_ours = hooks_path_res.stdout.strip() == ".githooks"

    return {
        "tier1": tier1,
        "tier2": tier2,
        "tier3": tier3,
        "hook_editado_a_mano": hook_editado,
        "git_remote_continuum": has_continuum_remote,
        "revert_hooks_path": hooks_path_is_ours,
    }


def _rel(root: Path, paths: list[Path]) -> list[str]:
    return sorted(str(p.relative_to(root)) for p in paths)


def _remove(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()


def cmd_uninstall(
    root: Path,
    dry_run: bool = True,
    yes: bool = False,
    purge_memory: bool = False,
    json_output: bool = False,
) -> int:
    dirty = c.git("status", "--porcelain").stdout.strip() != ""
    if dirty and not dry_run:
        c.err("El working tree tiene cambios sin commitear. Commitea o descarta "
              "antes de desinstalar — una desinstalación se revisa más fácil "
              "sola, sin mezclarse con otros cambios.")
        return 1

    plan = build_plan(root)
    to_remove = list(plan["tier1"])
    included_tiers = ["tier1"]
    if yes:
        to_remove += plan["tier2"]
        included_tiers.append("tier2")
    if purge_memory:
        to_remove += plan["tier3"]
        included_tiers.append("tier3")

    if json_output:
        res = {
            "dry_run": dry_run,
            "tier1": _rel(root, plan["tier1"]),
            "tier2": _rel(root, plan["tier2"]),
            "tier3": _rel(root, plan["tier3"]),
            "hook_editado_a_mano": plan["hook_editado_a_mano"],
            "git_remote_continuum": plan["git_remote_continuum"],
            "included_tiers": included_tiers,
        }
        print(json.dumps(res, indent=2))
    else:
        lines = ["== Plan de desinstalación de Continuum =="]
        lines.append(f"\n[Nivel 1 · mecanismo — {len(plan['tier1'])} elemento(s)]")
        for p in _rel(root, plan["tier1"]):
            lines.append(f"  - {p}")
        lines.append(f"\n[Nivel 2 · protocolo/config — {len(plan['tier2'])} elemento(s)]"
                      + ("" if yes else " (no incluido — agrega --yes)"))
        for p in _rel(root, plan["tier2"]):
            lines.append(f"  - {p}")
        lines.append(f"\n[Nivel 3 · memoria del proyecto — {len(plan['tier3'])} elemento(s)]"
                      + ("" if purge_memory else " (no incluido — agrega --purge-memory)"))
        for p in _rel(root, plan["tier3"]):
            lines.append(f"  - {p}")
        if plan["hook_editado_a_mano"]:
            lines.append("\n⚠ .githooks/pre-commit existe pero su contenido no coincide con "
                          "el que instala Continuum (¿lo fusionaste con otro hook, p. ej. "
                          "Husky?) — no se toca, revísalo a mano.")
        if plan["git_remote_continuum"]:
            lines.append(f"\nRemoto git 'continuum' detectado — se elimina en el nivel 1.")
        print("\n".join(lines))

    if dry_run:
        if not json_output:
            print("\nModo dry-run (por defecto): nada se borró. "
                  "Usa --no-dry-run para aplicar el nivel 1, "
                  "+ --yes para el nivel 2, + --purge-memory para el nivel 3.")
        return 0

    for p in to_remove:
        _remove(p)

    if plan["git_remote_continuum"] and "tier1" in included_tiers:
        c.git("remote", "remove", "continuum")

    hook_removed = (root / ".githooks" / "pre-commit") in plan["tier1"]
    if hook_removed and plan["revert_hooks_path"]:
        c.git("config", "--unset", "core.hooksPath")
        githooks_dir = root / ".githooks"
        if githooks_dir.exists() and not any(githooks_dir.iterdir()):
            githooks_dir.rmdir()

    if not json_output:
        c.ok(f"Desinstalación aplicada: {len(to_remove)} elemento(s) eliminado(s) "
             f"({', '.join(included_tiers)}).")
        c.info("Nada se commiteó. Revisa 'git status'/'git diff' y commitea cuando estés conforme.")
    return 0
