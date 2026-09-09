"""Gestión del ciclo de sesiones e handoff optimizado."""
from __future__ import annotations

import json
from pathlib import Path

from . import common as c, context, handoff


def build_session_start(root: Path) -> dict:
    cfg = c.load_config(root)

    # 1. Handoff info
    handoff_path = root / cfg["handoff"]["path"]
    handoff_info = {
        "path": cfg["handoff"]["path"],
        "exists": handoff_path.exists(),
        "tokens": 0,
        "content_preview": None,
    }
    if handoff_path.exists():
        text = c.read_text(handoff_path)
        handoff_info["tokens"] = c.estimate_tokens(text)
        handoff_info["content_preview"] = text.strip()

    # 2. Active tasks
    tasks_dir = root / cfg["tasks"]["dir"]
    active_tasks = []
    if tasks_dir.exists():
        active_tasks = [p.name for p in sorted(tasks_dir.iterdir()) if p.is_dir() and p.name != "_closed"]

    # 3. Context
    task_slug = active_tasks[0] if active_tasks else None
    ctx_data = context.build_context(root, task_slug=task_slug)

    # 4. Handoff warnings (linting)
    warnings = handoff.lint_handoff(root) if handoff_path.exists() else []

    return {
        "handoff": handoff_info,
        "active_tasks": active_tasks,
        "suggested_context": ctx_data,
        "warnings": warnings,
    }


def format_human_session_start(data: dict) -> str:
    lines = [
        "== Inicio de Sesión Continuum ==",
        "",
    ]
    h = data["handoff"]
    if h["exists"]:
        lines.append(f"[Handoff Vigente] ({h['path']} - ~{h['tokens']} tokens)")
        if h["content_preview"]:
            preview_lines = h["content_preview"].splitlines()[:10]
            for pl in preview_lines:
                lines.append(f"  {pl}")
            if len(h["content_preview"].splitlines()) > 10:
                lines.append("  ...")
    else:
        lines.append("[Handoff Vigente] Ausente (no se encontró .ai/HANDOFF.md)")

    lines.append("")
    tasks = data["active_tasks"]
    if tasks:
        lines.append(f"[Tareas Activas] ({len(tasks)}): {', '.join(tasks)}")
    else:
        lines.append("[Tareas Activas] Ninguna")

    lines.append("")
    lines.append(context.format_human_context(data["suggested_context"]))

    if data["warnings"]:
        lines.append("")
        lines.append("[Advertencias de Handoff]")
        for w in data["warnings"]:
            lines.append(f"  ⚠️  {w}")

    return "\n".join(lines)


def cmd_session_start(root: Path, json_output: bool = False) -> int:
    data = build_session_start(root)
    if json_output:
        print(json.dumps(data, indent=2))
    else:
        print(format_human_session_start(data))
    return 0


def cmd_session_end(
    root: Path,
    message: str | None = None,
    auto: bool = False,
    provider: str | None = None,
    role: str | None = None,
    json_output: bool = False,
) -> int:
    import contextlib
    import io

    if json_output:
        with contextlib.redirect_stdout(io.StringIO()):
            if auto:
                handoff.write_auto(root, provider=provider, role=role)
            else:
                handoff.write_manual(root, message=message, role=role)
    else:
        if auto:
            handoff.write_auto(root, provider=provider, role=role)
        else:
            handoff.write_manual(root, message=message, role=role)

    warnings = handoff.lint_handoff(root)

    cfg = c.load_config(root)

    if json_output:
        result = {
            "status": "ok",
            "handoff_path": cfg["handoff"]["path"],
            "auto": auto,
            "warnings": warnings,
        }
        print(json.dumps(result, indent=2))
    else:
        if warnings:
            c.warn("Validación de Handoff (lint):")
            for w in warnings:
                print(f"  ⚠️  {w}")

    return 0

