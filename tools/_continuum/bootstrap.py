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


CONTINUUM_SHIM = """#!/usr/bin/env python3
\"\"\"Punto de entrada ejecutable: `tools/continuum <comando>`.\"\"\"
import sys
from pathlib import Path

def main():
    root_dir = Path(__file__).resolve().parent.parent
    dot_continuum = root_dir / ".continuum" / "tools"
    if dot_continuum.is_dir():
        sys.path.insert(0, str(dot_continuum))
        from _continuum.__main__ import main as continuum_main
        return continuum_main()

    local_tools = Path(__file__).resolve().parent
    sys.path.insert(0, str(local_tools))
    from _continuum.__main__ import main as continuum_main
    return continuum_main()

if __name__ == "__main__":
    sys.exit(main())
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
            ".claude/settings.json",
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
    channel: str = "",
    version: str = "",
    mode: str = "",
    json_output: bool = False,
) -> int:
    import io
    import json
    import shutil
    import subprocess
    import tarfile

    cfg = c.load_config(root)
    remote = cfg.get("template_remote") or ""
    prefix = cfg.get("template_prefix") or ""
    sync_mode = mode or cfg.get("template_sync_mode") or "vendoring"

    if not prefix and (root / ".continuum").is_dir():
        prefix = ".continuum"

    target_branch = cfg.get("template_branch") or "export"
    if channel in ("dev", "develop"):
        target_branch = "export-develop"
    elif channel in ("stable", "main", "release"):
        target_branch = "export"

    if version:
        target_ref = version
    else:
        target_ref = target_branch

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

    pull_cmd = f"git subtree pull --prefix={display_prefix} {display_remote} {target_ref} --squash"
    push_cmd = f"git subtree push --prefix={display_prefix} {display_remote} {target_ref}"

    if json_output:
        res = {
            "valid_config": len(errors) == 0,
            "working_tree_clean": is_clean,
            "remote": remote if has_remote else None,
            "prefix": prefix if has_prefix else None,
            "branch": target_branch,
            "target_ref": target_ref,
            "sync_mode": sync_mode,
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
        lines.append(f"Modo preferido: {sync_mode}")
        lines.append(f"Objetivo: {target_ref} en {display_remote}")
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

        if sync_mode == "subtree":
            c.info(f"Ejecutando (modo subtree): {pull_cmd}")
            res_pull = c.git("subtree", "pull", f"--prefix={prefix}", remote, target_ref, "--squash")
            if res_pull.returncode == 0:
                c.ok("Sincronización completada con éxito.")
                from . import roles
                roles.sync(root)
                return 0
            else:
                c.err(f"Error al ejecutar git subtree pull:\n{res_pull.stderr}")
                return res_pull.returncode

        # Modo vendoring lineal (por defecto)
        c.info(f"Obteniendo actualización limpia desde {remote} ({target_ref})...")
        res_fetch = c.git("fetch", remote, target_ref)
        if res_fetch.returncode != 0:
            c.err(f"Error al obtener actualización desde el remoto:\n{res_fetch.stderr}")
            return res_fetch.returncode

        proc = subprocess.Popen(
            ["git", "archive", "FETCH_HEAD"],
            cwd=str(root),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        archive_bytes, err = proc.communicate()
        if proc.returncode != 0:
            c.err(f"Error al generar archivo desde FETCH_HEAD:\n{err.decode('utf-8', errors='replace')}")
            return proc.returncode

        dest_dir = root / prefix
        if dest_dir.is_dir():
            for child in dest_dir.iterdir():
                if child.is_dir():
                    shutil.rmtree(child)
                else:
                    child.unlink()
        else:
            dest_dir.mkdir(parents=True, exist_ok=True)

        with tarfile.open(fileobj=io.BytesIO(archive_bytes)) as tar:
            if hasattr(tarfile, "data_filter"):
                tar.extractall(path=dest_dir, filter="data")
            else:
                tar.extractall(path=dest_dir)

        shim = dest_dir / "tools" / "continuum"
        if shim.exists():
            try:
                shim.chmod(0o755)
            except OSError:
                pass

        detected_version = ""
        ver_file = dest_dir / "VERSION"
        if ver_file.exists():
            detected_version = ver_file.read_text(encoding="utf-8").strip()

        cfg["template_remote"] = remote
        cfg["template_prefix"] = prefix
        cfg["template_branch"] = target_branch
        if version:
            cfg["template_version"] = version
        elif detected_version:
            cfg["template_version"] = detected_version
        cfg["template_sync_mode"] = "vendoring"
        c.save_config(root, cfg)

        from . import roles
        roles.sync(root)

        c.ok(f"Sincronización completada con éxito ({prefix}/ actualizado a {detected_version or target_ref}).")
        c.ok("Historial de git preservado: sin merge commits artificiales ni ramas huérfanas.")
        c.info("\nSiguiente paso: Revisa 'git status' / 'git diff' y commitea normalmente:")
        c.info(f"  git add {prefix} .ai/config.json && git commit -m 'chore(continuum): actualiza a {detected_version or target_ref}'")
        return 0

    lines = [
        "== Sincronización de Plantilla Continuum (modo lectura / plan) ==",
        f"Remoto: {remote or '(sin configurar)'}",
        f"Carpeta destino: {prefix or '(sin configurar)'}",
        f"Modo: {sync_mode} (lineal, sin merge commits)",
        f"Canal / Ref: {target_ref}",
        f"Working Tree: {'Limpio' if is_clean else 'Cambios sin commitear'}",
        "",
        "Para actualizar limpiamente:",
        "  continuum sync --apply",
        "",
        "Opciones disponibles:",
        "  continuum sync --channel dev --apply       # Cambia a canal de desarrollo (export-develop)",
        "  continuum sync --version v1.5.0 --apply    # Fija una versión específica por tag",
        "",
        "Alternativa tradicional (git subtree):",
        f"  {pull_cmd}",
    ]
    if errors:
        lines.append("\n⚠️ Configuración incompleta en .ai/config.json. Completa 'template_remote' y 'template_prefix'.")
    else:
        lines.append("\nUsa 'continuum sync --apply' para ejecutar la actualización directamente si el árbol está limpio.")

    print("\n".join(lines))
    return 0
