"""Comando status: visión compacta de preparación y siguiente acción."""
from __future__ import annotations

import json
import time
from pathlib import Path

from . import common as c, doctor


def build_status(root: Path) -> dict:
    cfg = c.load_config(root)

    doc_problems = doctor.run(root, quiet=True)
    ready = (doc_problems == 0)

    estado_path = root / cfg["estado_dev"]["path"]
    index_lines = 0
    if estado_path.exists():
        index_text = c.read_text(estado_path)
        index_lines = index_text.count("\n") + (1 if index_text else 0)

    topics_dir = root / cfg["estado_dev"]["topics_dir"]
    topics_count = len(list(topics_dir.glob("*.md"))) if topics_dir.exists() else 0

    handoff_path = root / cfg["handoff"]["path"]
    handoff_exists = handoff_path.exists()
    handoff_age_hours: float | None = None
    if handoff_exists:
        handoff_age_hours = round((time.time() - handoff_path.stat().st_mtime) / 3600, 1)

    hook_installed = c.pre_commit_hook_installed(root)

    tasks_dir = root / cfg["tasks"]["dir"]
    active_tasks = []
    if tasks_dir.exists():
        active_tasks = [p.name for p in tasks_dir.iterdir() if p.is_dir() and p.name != "_closed"]

    if not ready:
        next_action = "Ejecuta 'continuum doctor --fix' para auto-reparar problemas seguras."
    elif active_tasks:
        next_action = f"Ejecuta 'continuum context --task {active_tasks[0]}' para iniciar trabajo en la tarea activa."
    else:
        next_action = "Ejecuta 'continuum context' para revisar el contexto sugerido o 'continuum task start <slug>' para crear una tarea."

    return {
        "ready": ready,
        "memory": {
            "index_lines": index_lines,
            "topics_count": topics_count,
        },
        "handoff": {
            "exists": handoff_exists,
            "age_hours": handoff_age_hours,
        },
        "hooks": {
            "pre_commit_installed": hook_installed,
        },
        "tasks": {
            "active_count": len(active_tasks),
            "active_list": active_tasks,
        },
        "next_action": next_action,
    }


def format_human_status(status_data: dict) -> str:
    lines = [
        "== Estado de Continuum ==",
        f"Preparación: {'✓ LISTO' if status_data['ready'] else '✗ REQUIERE ATENCIÓN'}",
        f"Memoria viva: Índice ({status_data['memory']['index_lines']} líns), {status_data['memory']['topics_count']} tema(s)",
    ]

    h = status_data["handoff"]
    h_str = f"presente ({h['age_hours']}h)" if h["exists"] else "ausente"
    lines.append(f"Handoff: {h_str}")
    lines.append(f"Hook pre-commit: {'instalado' if status_data['hooks']['pre_commit_installed'] else 'no instalado'}")

    tasks_info = f"{status_data['tasks']['active_count']} activa(s)"
    if status_data['tasks']['active_list']:
        tasks_info += f" ({', '.join(status_data['tasks']['active_list'])})"
    lines.append(f"Tareas: {tasks_info}")

    lines.append("")
    lines.append(f"Siguiente acción: {status_data['next_action']}")
    return "\n".join(lines)


def cmd_status(root: Path, json_output: bool = False) -> int:
    status_data = build_status(root)
    if json_output:
        print(json.dumps(status_data, indent=2))
    else:
        print(format_human_status(status_data))
    return 0


def cmd_version(root: Path, json_output: bool = False) -> int:
    version = c.read_version(root)
    if json_output:
        print(json.dumps({"version": version}, indent=2))
        return 0
    if version:
        print(f"continuum {version}")
    else:
        c.warn("Sin archivo VERSION — instalación anterior a su introducción. "
               "Corre 'continuum sync --apply' para traer la versión actual.")
    return 0
