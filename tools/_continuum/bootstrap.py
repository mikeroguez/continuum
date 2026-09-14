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


CONTINUUM_SHIM = """#!/bin/sh
# Continuum launcher shim — delega al motor instalado en .continuum/
ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
if [ -f "$ROOT_DIR/.continuum/tools/continuum" ]; then
  exec python3 "$ROOT_DIR/.continuum/tools/continuum" "$@"
elif [ -f "$ROOT_DIR/tools/_continuum/__main__.py" ]; then
  exec python3 "$ROOT_DIR/tools/continuum" "$@"
else
  echo "No se encontró instalación de Continuum en .continuum/ o tools/" >&2
  exit 1
fi
"""


def init(root: Path, force: bool = False) -> int:
    """Inicializa un proyecto consumidor configurando shim, entrypoints y githooks."""
    import json
    from . import roles

    cdir = c.continuum_dir(root)
    shim_path = root / "tools" / "continuum"
    shim_path.parent.mkdir(parents=True, exist_ok=True)
    if not shim_path.exists() or force or cdir != root:
        c.write_text(shim_path, CONTINUUM_SHIM)
        shim_path.chmod(0o755)
        c.ok(f"Launcher shim configurado en {shim_path.relative_to(root)}")

    # Archivos canónicos y entrypoints a copiar si no existen
    source_dir = cdir if cdir != root else (root / "template")
    if source_dir.exists():
        files_to_copy = [
            "AI_COLLABORATION.md",
            "AGENTS.md",
            "CLAUDE.md",
            "GEMINI.md",
            ".github/copilot-instructions.md",
        ]
        for rel in files_to_copy:
            target = root / rel
            src = source_dir / rel
            if src.exists() and (not target.exists() or force):
                c.write_text(target, c.read_text(src))
                c.ok(f"Creado {rel}")

    # Inicializar .ai/config.json si falta
    cfg_path = root / ".ai" / "config.json"
    if not cfg_path.exists():
        new_cfg = json.loads(json.dumps(c.DEFAULT_CONFIG))
        new_cfg["project"] = root.name
        new_cfg["template_remote"] = "https://github.com/mikeroguez/continuum.git"
        new_cfg["template_prefix"] = ".continuum"
        c.write_text(cfg_path, json.dumps(new_cfg, indent=2) + "\n")
        c.ok("Creado .ai/config.json con prefijo .continuum")
    else:
        # Asegurar template_prefix si .continuum existe
        cfg = c.load_config(root)
        if (root / ".continuum").is_dir() and cfg.get("template_prefix") != ".continuum":
            cfg["template_prefix"] = ".continuum"
            c.write_text(cfg_path, json.dumps(cfg, indent=2) + "\n")

    # Inicializar memoria viva mínima
    handoff_path = root / ".ai" / "HANDOFF.md"
    if not handoff_path.exists():
        src_handoff = source_dir / ".ai" / "HANDOFF.md" if source_dir.exists() else None
        content = c.read_text(src_handoff) if src_handoff and src_handoff.exists() else "# Handoff\n\nSin sesiones previas.\n"
        c.write_text(handoff_path, content)
        c.ok("Creado .ai/HANDOFF.md")

    estado_path = root / ".ai" / "state" / "estado-dev.md"
    if not estado_path.exists():
        c.write_text(estado_path, f"# {root.name} — índice de memoria\n\n## Temas\n\n- **Resumen y stack** → `.ai/state/topics/resumen.md`\n")
        c.ok("Creado .ai/state/estado-dev.md")

    (root / ".ai" / "state" / "topics").mkdir(parents=True, exist_ok=True)
    (root / ".ai" / "tasks" / "_closed").mkdir(parents=True, exist_ok=True)

    install_hooks(root)
    roles.sync(root)

    c.ok("Continuum inicializado con éxito en el proyecto.")
    return 0


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

    if not prefix and (root / ".continuum").is_dir():
        prefix = ".continuum"

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
            from . import roles
            roles.sync(root)
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

