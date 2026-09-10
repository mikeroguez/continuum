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
    return cmd_sync(root)


def cmd_sync(
    root: Path,
    check_only: bool = False,
    apply: bool = False,
    json_output: bool = False,
) -> int:
    import json

    cfg = c.load_config(root)
    remote = cfg.get("template_remote") or ""
    prefix = cfg.get("template_prefix") or ""
    branch = cfg.get("template_branch") or "export"

    has_remote = bool(remote and not remote.startswith("<"))
    has_prefix = bool(prefix and not prefix.startswith("<"))

    display_remote = remote if has_remote else "<url-del-repo-plantilla>"
    display_prefix = prefix if has_prefix else "<carpeta-donde-vive-la-plantilla-en-este-repo>"

    git_status = c.git("status", "--porcelain").stdout.strip()
    is_clean = (git_status == "")

    errors = []
    if not has_remote:
        errors.append("Falta configurar 'template_remote' en .ai/config.json.")
    if not has_prefix:
        errors.append("Falta configurar 'template_prefix' en .ai/config.json.")

    warnings = []
    if not is_clean:
        warnings.append("El working tree de git tiene cambios sin commitear.")

    pull_cmd = f"git subtree pull --prefix={display_prefix} {display_remote} {branch} --squash"
    push_cmd = f"git subtree push --prefix={display_prefix} {display_remote} {branch}"


    if json_output:
        res = {
            "valid_config": len(errors) == 0,
            "working_tree_clean": is_clean,
            "remote": remote if has_remote else None,
            "prefix": prefix if has_prefix else None,
            "branch": branch,
            "pull_command": pull_cmd,
            "push_command": push_cmd,
            "errors": errors,
            "warnings": warnings,
        }
        print(json.dumps(res, indent=2))
        return 0 if len(errors) == 0 else 1

    if check_only:
        lines = ["== Diagnóstico de Sincronización de Continuum =="]
        lines.append(f"Configuración: {'✓ OK' if len(errors) == 0 else '✗ INCOMPLETA'}")
        lines.append(f"Working Tree: {'✓ Limpio' if is_clean else '⚠️ Cambios pendientes'}")
        if errors:
            lines.append("\n[Errores]")
            for err_msg in errors:
                lines.append(f"  ✗ {err_msg}")
        if warnings:
            lines.append("\n[Advertencias]")
            for w in warnings:
                lines.append(f"  ⚠️  {w}")
        print("\n".join(lines))
        return 0 if len(errors) == 0 else 1

    if apply:
        if errors:
            c.err("No se puede sincronizar automáticamente debido a errores de configuración:")
            for err_msg in errors:
                print(f"  - {err_msg}")
            return 1
        if not is_clean:
            c.err("No se puede aplicar 'sync' con cambios sin commitear. Limpia o haz commit de tus cambios antes de actualizar.")
            return 1

        c.info(f"Ejecutando: {pull_cmd}")
        res_pull = c.git("subtree", "pull", f"--prefix={prefix}", remote, branch, "--squash")
        if res_pull.returncode == 0:
            c.ok("Sincronización completada con éxito.")
            return 0
        else:
            c.err(f"Error al ejecutar git subtree pull:\n{res_pull.stderr}")
            return res_pull.returncode

    lines = [
        "== Sincronización de Plantilla Continuum (modo lectura / plan) ==",
        f"Remoto: {remote or '(sin configurar)'}",
        f"Carpeta prefix: {prefix or '(sin configurar)'}",
        f"Working Tree: {'Limpio' if is_clean else 'Cambios sin commitear'}",
        "",
        "Para traer actualizaciones:",
        f"  {pull_cmd}",
        "",
        "Para aportar un cambio de vuelta:",
        f"  {push_cmd}",
    ]
    if errors:
        lines.append("\n⚠️ Configuración incompleta en .ai/config.json. Completa 'template_remote' y 'template_prefix'.")
    if not apply:
        lines.append("\nUsa 'continuum sync --apply' para ejecutar la actualización directamente si el árbol está limpio.")

    print("\n".join(lines))
    return 0

