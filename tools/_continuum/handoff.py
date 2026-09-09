"""El "buzón" de continuidad: .ai/HANDOFF.md

Es el único archivo que debe estar SIEMPRE actualizado, incluso si no hay una
carpeta de tarea formal. Se diseñó para dos disparadores:

1. Manual: la IA o la persona lo actualiza al terminar una sesión o notar que
   se está por agotar el contexto/tokens.
2. Automático: un hook (Claude Code SessionEnd/PreCompact, o un git pre-push) llama
   `continuum handoff --auto`, que arma un borrador desde `git status`/`git diff`
   aunque nadie se acuerde de hacerlo a mano. Esto es lo que faltaba en los
   proyectos previos: la disciplina dependía 100% de la memoria humana/del
   agente, y por eso el handoff quedaba desactualizado.
"""
from __future__ import annotations

import shutil
from pathlib import Path

from . import common as c


def _archive_previous(root: Path, cfg: dict) -> None:
    handoff_path = root / cfg["handoff"]["path"]
    if not handoff_path.exists():
        return
    archive_dir = root / cfg["handoff"]["archive_dir"]
    archive_dir.mkdir(parents=True, exist_ok=True)
    dest = archive_dir / f"{c.stamp()}.md"
    shutil.copy2(handoff_path, dest)


def write_manual(root: Path, message: str | None, role: str | None = None) -> int:
    cfg = c.load_config(root)
    _archive_previous(root, cfg)
    templates_dir = root / ".ai" / "templates"
    text = c.read_text(templates_dir / "HANDOFF.md")
    if not text:
        text = "# Handoff\n\n**Fecha:** {{DATE}} · **Rol:** {{ROLE}}\n\n{{MESSAGE}}\n"
    text = text.replace("{{DATE}}", c.date_str()).replace("{{SLUG}}", "(general)")
    text = text.replace("{{ROLE}}", role or "(sin asignar)")
    text = text.replace("{{MESSAGE}}", message or "")
    c.write_text(root / cfg["handoff"]["path"], text)
    c.ok(f"Handoff escrito en {cfg['handoff']['path']}. Complétalo con objetivo, "
         f"decisión, validación y siguiente paso antes de cortar la sesión.")
    return 0


def write_auto(root: Path, provider: str | None, role: str | None = None) -> int:
    """Genera un borrador de handoff a partir del estado real de git.

    No reemplaza el juicio de la IA/persona (no sabe "por qué" se hizo algo),
    pero garantiza que SIEMPRE quede un rastro mínimo aunque se corte la
    sesión sin aviso (p. ej. se acaban los tokens a media tarea).
    """
    cfg = c.load_config(root)
    _archive_previous(root, cfg)

    status = c.git("status", "--porcelain").stdout.strip()
    diff_stat = c.git("diff", "--stat", "HEAD").stdout.strip()
    last_commit = c.git("log", "-1", "--format=%h %s").stdout.strip()
    branch = c.git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()

    lines = [
        "# Handoff (auto-generado)",
        "",
        f"**Fecha:** {c.date_str()} · **Proveedor:** {provider or 'desconocido'} · "
        f"**Rol:** {role or 'desconocido'} · **Branch:** {branch}",
        "",
        "> Este borrador se generó automáticamente al cortar la sesión "
        "(hook SessionEnd/PreCompact o pre-push). Complementa manualmente el "
        "'por qué' y el 'siguiente paso' antes de continuar en otra sesión.",
        "",
        "## Último commit",
        f"`{last_commit}`" if last_commit else "(sin commits en este branch)",
        "",
        "## Cambios sin commitear",
        f"```\n{status}\n```" if status else "(working tree limpio)",
        "",
        "## Resumen de diff vs HEAD",
        f"```\n{diff_stat}\n```" if diff_stat else "(sin diferencias)",
        "",
        "## Objetivo de esta sesión",
        "_(completar manualmente)_",
        "",
        "## Siguiente paso recomendado",
        "_(completar manualmente)_",
    ]
    c.write_text(root / cfg["handoff"]["path"], "\n".join(lines) + "\n")
    c.ok(f"Handoff automático escrito en {cfg['handoff']['path']}. "
         f"Faltan por completar 'Objetivo' y 'Siguiente paso'.")
    return 0
