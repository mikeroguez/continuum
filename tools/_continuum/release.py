"""Gestión del ciclo de exportación y release del meta-repositorio Continuum."""
from __future__ import annotations

import json
import re
from pathlib import Path

from . import common as c, doctor


def cmd_export_status(root: Path, json_output: bool = False) -> int:
    res_branch = c.git("branch", "--list", "export")
    has_export_branch = bool(res_branch.stdout.strip())

    status_str = c.git("status", "--porcelain").stdout.strip()
    is_clean = (status_str == "")

    in_sync = False
    if has_export_branch:
        tree_export = c.git("rev-parse", "export^{tree}").stdout.strip()
        tree_template = c.git("rev-parse", "HEAD:template").stdout.strip()
        in_sync = bool(tree_export and tree_template and tree_export == tree_template)

    data = {
        "export_branch_exists": has_export_branch,
        "working_tree_clean": is_clean,
        "in_sync_with_template": in_sync,
    }

    if json_output:
        print(json.dumps(data, indent=2))
        return 0 if (has_export_branch and in_sync) else 1

    lines = ["== Estado de Rama Export (meta-Continuum) =="]
    lines.append(f"Rama 'export': {'✓ Presente' if has_export_branch else '✗ Ausente'}")
    lines.append(f"Sincronía con template/: {'✓ En sincronía' if in_sync else '⚠️ Requiere refresh'}")
    lines.append(f"Working Tree: {'✓ Limpio' if is_clean else '⚠️ Cambios pendientes'}")

    if not has_export_branch or not in_sync:
        lines.append("\nSiguiente acción: Ejecuta 'continuum export refresh' para actualizar la rama export.")

    print("\n".join(lines))
    return 0 if (has_export_branch and in_sync) else 1


def cmd_export_refresh(
    root: Path,
    dry_run: bool = True,
    json_output: bool = False,
) -> int:
    cmd_str = "git subtree split --prefix=template -b export"

    status_str = c.git("status", "--porcelain").stdout.strip()
    is_clean = (status_str == "")

    if json_output:
        res = {
            "dry_run": dry_run,
            "working_tree_clean": is_clean,
            "command": cmd_str,
        }
        print(json.dumps(res, indent=2))
        return 0

    if dry_run:
        lines = [
            "== Plan de Actualización de Rama Export (modo dry-run) ==",
            f"Working Tree: {'Limpio' if is_clean else 'Cambios pendientes'}",
            "",
            "Comando a ejecutar:",
            f"  {cmd_str}",
            "",
            "Usa 'continuum export refresh --no-dry-run' para ejecutar la regeneración de la rama export.",
        ]
        print("\n".join(lines))
        return 0

    if not is_clean:
        c.err("No se puede ejecutar 'export refresh' con un working tree sucio. Haz commit de tus cambios primero.")
        return 1

    c.info(f"Ejecutando: {cmd_str}")
    res = c.git("subtree", "split", "--prefix=template", "-b", "export")
    if res.returncode == 0:
        c.ok("Rama 'export' actualizada con éxito a partir de template/.")
        return 0
    else:
        c.err(f"Error al actualizar la rama export:\n{res.stderr}")
        return res.returncode


def cmd_release(
    root: Path,
    version: str,
    dry_run: bool = True,
    json_output: bool = False,
) -> int:
    clean_version = version.lstrip("v")
    semver_pattern = r"^\d+\.\d+\.\d+(-[0-9A-Za-z.-]+)?$"
    valid_version = bool(re.match(semver_pattern, clean_version))
    tag_name = f"v{clean_version}"

    changelog_path = root / "CHANGELOG.md"
    has_changelog_entry = False
    if changelog_path.exists():
        text = c.read_text(changelog_path)
        has_changelog_entry = (clean_version in text or tag_name in text)

    doc_problems = doctor.run(root, quiet=True)
    doctor_ok = (doc_problems == 0)

    res_tag = c.git("tag", "-l", tag_name)
    tag_exists = bool(res_tag.stdout.strip())

    errors = []
    if not valid_version:
        errors.append(f"La versión '{version}' no tiene un formato SemVer válido (ej. v1.0.0).")
    if not has_changelog_entry:
        errors.append(f"No se encontró la versión '{tag_name}' en CHANGELOG.md.")
    if not doctor_ok:
        errors.append("El diagnóstico 'continuum doctor' encontró problemas.")

    warnings = []
    if tag_exists:
        warnings.append(f"El tag '{tag_name}' ya existe en el repositorio.")

    tag_cmd = f"git tag -a {tag_name} export -m 'Release {tag_name}'"

    if json_output:
        res = {
            "version": tag_name,
            "valid_semver": valid_version,
            "in_changelog": has_changelog_entry,
            "doctor_ok": doctor_ok,
            "tag_exists": tag_exists,
            "tag_command": tag_cmd,
            "errors": errors,
            "warnings": warnings,
            "dry_run": dry_run,
        }
        print(json.dumps(res, indent=2))
        return 0 if len(errors) == 0 else 1

    if dry_run:
        lines = [
            f"== Plan de Release Meta-Continuum ({tag_name}) (modo dry-run) ==",
            f"Formato SemVer: {'✓ OK' if valid_version else '✗ INVÁLIDO'}",
            f"Registro en CHANGELOG.md: {'✓ Presente' if has_changelog_entry else '✗ AUSENTE'}",
            f"Diagnóstico Doctor: {'✓ OK' if doctor_ok else '✗ PROBLEMAS'}",
            f"Estado de Tag: {'⚠️ Ya existe' if tag_exists else '✓ Disponible'}",
            "",
            "Comando de etiquetado previsto:",
            f"  {tag_cmd}",
        ]
        if errors:
            lines.append("\n[Errores que impiden la liberación]")
            for e in errors:
                lines.append(f"  ✗ {e}")
        else:
            lines.append("\nUsa 'continuum release <versión> --no-dry-run' para aplicar el tag localmente.")

        print("\n".join(lines))
        return 0 if len(errors) == 0 else 1

    if errors:
        c.err("No se puede proceder con el release debido a los siguientes errores:")
        for e in errors:
            print(f"  - {e}")
        return 1

    if tag_exists:
        c.info(f"El tag '{tag_name}' ya está creado e idempotente.")
        return 0

    c.info(f"Ejecutando: {tag_cmd}")
    res = c.git("tag", "-a", tag_name, "export", "-m", f"Release {tag_name}")
    if res.returncode == 0:
        c.ok(f"Release '{tag_name}' creado con éxito localmente sobre la rama export.")
        return 0
    else:
        c.err(f"Error al crear el tag {tag_name}:\n{res.stderr}")
        return res.returncode
