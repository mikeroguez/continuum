"""Instalación de hooks locales y ayuda para sincronizar la plantilla.

No usa librerías de terceros: escribe un hook de git plano en .githooks/ y
apunta core.hooksPath ahí (no pisa un hooksPath existente sin avisar).
"""
from __future__ import annotations

from pathlib import Path

from . import common as c

PRE_COMMIT_HOOK = """#!/bin/sh
# Instalado por continuum install-hooks. Corre en <1s, no bloquea el commit
# (solo advierte) salvo que falte el archivo canónico del protocolo.
python3 "$(git rev-parse --show-toplevel)/tools/continuum" doctor --quiet
status=$?
if [ $status -ne 0 ]; then
  echo ""
  echo "continuum doctor encontró problemas críticos (ver arriba)."
  echo "Corrige o usa 'git commit --no-verify' si es intencional."
  exit 1
fi
exit 0
"""


def install_hooks(root: Path) -> int:
    hooks_dir = root / ".githooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    hook_path = hooks_dir / "pre-commit"
    c.write_text(hook_path, PRE_COMMIT_HOOK)
    hook_path.chmod(0o755)

    r = c.git("config", "core.hooksPath", ".githooks")
    if r.returncode != 0:
        c.err("No se pudo configurar core.hooksPath (¿estás dentro de un repo git?).")
        return 1

    c.ok(f"Hook instalado en {hook_path.relative_to(root)} y "
         f"core.hooksPath apuntado ahí.")
    c.info("Si ya usabas otro hooksPath (p. ej. husky), revisa que no se pise: "
           "puedes fusionar ambos hooks a mano.")
    return 0


def sync_template_instructions(root: Path) -> int:
    cfg = c.load_config(root)
    remote = cfg.get("template_remote") or "<url-del-repo-plantilla>"
    prefix = cfg.get("template_prefix") or "<carpeta-donde-vive-la-plantilla-en-este-repo>"
    print(
        "Este proyecto trae la plantilla vía `git subtree`. Para traer actualizaciones:\n\n"
        f"  git subtree pull --prefix={prefix} {remote} main --squash\n\n"
        "Para aportar un cambio de vuelta a la plantilla compartida:\n\n"
        f"  git subtree push --prefix={prefix} {remote} main\n\n"
        "Configura 'template_remote' y 'template_prefix' en .ai/config.json "
        "para no tener que escribir la URL cada vez."
    )
    return 0
