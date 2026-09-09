"""Lógica de métricas locales y baseline de Continuum."""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

from . import common as c


def build_snapshot(root: Path) -> dict:
    cfg = c.load_config(root)

    # 1. Git info
    commit_res = c.git("log", "-1", "--format=%h")
    commit = commit_res.stdout.strip() if commit_res.returncode == 0 else ""
    branch_res = c.git("rev-parse", "--abbrev-ref", "HEAD")
    branch = branch_res.stdout.strip() if branch_res.returncode == 0 else ""

    # 2. Startup tokens
    always_loaded = [c.CANONICAL_FILE] + [c.PROVIDER_FILES[p] for p in cfg["providers"] if p in c.PROVIDER_FILES]
    always_loaded.append(cfg["estado_dev"]["path"])
    always_loaded.append(cfg["handoff"]["path"])
    startup_tokens = 0
    for rel in always_loaded:
        p = root / rel
        if p.exists():
            startup_tokens += c.estimate_tokens(c.read_text(p))

    # 3. Memory stats
    estado_path = root / cfg["estado_dev"]["path"]
    index_lines = 0
    index_tokens = 0
    if estado_path.exists():
        index_text = c.read_text(estado_path)
        index_lines = index_text.count("\n") + (1 if index_text else 0)
        index_tokens = c.estimate_tokens(index_text)

    topics_dir = root / cfg["estado_dev"]["topics_dir"]
    topics_count = 0
    topics_total_lines = 0
    topics_total_tokens = 0
    if topics_dir.exists():
        topic_files = sorted(list(topics_dir.glob("*.md")))
        topics_count = len(topic_files)
        for tf in topic_files:
            t_text = c.read_text(tf)
            topics_total_lines += t_text.count("\n") + (1 if t_text else 0)
            topics_total_tokens += c.estimate_tokens(t_text)

    # 4. Tasks stats
    tasks_dir = root / cfg["tasks"]["dir"]
    active_tasks = 0
    closed_tasks = 0
    if tasks_dir.exists():
        active_tasks = len([p for p in tasks_dir.iterdir() if p.is_dir() and p.name != "_closed"])
        closed_dir = root / cfg["tasks"]["closed_dir"]
        if closed_dir.exists():
            closed_tasks = len([p for p in closed_dir.iterdir() if p.is_dir()])

    # 5. Handoff stats
    handoff_path = root / cfg["handoff"]["path"]
    handoff_exists = handoff_path.exists()
    handoff_age_hours: float | None = None
    if handoff_exists:
        handoff_age_hours = round((time.time() - handoff_path.stat().st_mtime) / 3600, 1)

    # 6. Hooks status
    hook_path = root / ".git" / "hooks" / "pre-commit"
    hook_installed = False
    if hook_path.exists():
        content = c.read_text(hook_path)
        if "continuum doctor" in content:
            hook_installed = True

    return {
        "timestamp": c.stamp(),
        "git": {
            "commit": commit,
            "branch": branch,
        },
        "startup_tokens": startup_tokens,
        "memory": {
            "index_lines": index_lines,
            "index_tokens": index_tokens,
            "topics_count": topics_count,
            "topics_total_lines": topics_total_lines,
            "topics_total_tokens": topics_total_tokens,
        },
        "tasks": {
            "active": active_tasks,
            "closed": closed_tasks,
        },
        "handoff": {
            "exists": handoff_exists,
            "age_hours": handoff_age_hours,
        },
        "hooks": {
            "pre_commit_installed": hook_installed,
        },
    }


def format_human_snapshot(snap: dict) -> str:
    lines = [
        "== Snapshot de métricas locales de Continuum ==",
        f"Fecha: {snap['timestamp']}",
        f"Git: branch '{snap['git']['branch']}' @ {snap['git']['commit']}",
        f"Tokens de arranque estimados: ~{snap['startup_tokens']}",
        "",
        "== Memoria viva ==",
        f"Índice ({snap['memory']['index_lines']} líneas, ~{snap['memory']['index_tokens']} tokens)",
        f"Temas: {snap['memory']['topics_count']} archivo(s) ({snap['memory']['topics_total_lines']} líneas, ~{snap['memory']['topics_total_tokens']} tokens totales)",
        "",
        "== Tareas y Handoff ==",
        f"Tareas activas: {snap['tasks']['active']} | Cerradas: {snap['tasks']['closed']}",
    ]
    h_age = snap['handoff']['age_hours']
    h_str = f"presente ({h_age}h de antigüedad)" if snap['handoff']['exists'] else "no existe"
    lines.append(f"Handoff: {h_str}")
    lines.append(f"Hook pre-commit: {'instalado' if snap['hooks']['pre_commit_installed'] else 'no instalado'}")
    return "\n".join(lines)


def cmd_snapshot(root: Path, dry_run: bool = True, json_output: bool = False) -> int:
    snap = build_snapshot(root)
    if dry_run:
        if json_output:
            print(json.dumps(snap, indent=2))
        else:
            print(format_human_snapshot(snap))
            print("\n(Modo --dry-run: no se escribió ningún archivo en disco).")
        return 0

    dest_dir = root / ".ai" / "metrics" / "snapshots"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_file = dest_dir / f"{snap['timestamp']}.json"
    dest_file.write_text(json.dumps(snap, indent=2), encoding="utf-8")

    if json_output:
        print(json.dumps(snap, indent=2))
    else:
        print(format_human_snapshot(snap))
        c.ok(f"\nSnapshot guardado en {dest_file.relative_to(root)}")

    return 0


def cmd_report(root: Path, json_output: bool = False) -> int:
    snap = build_snapshot(root)
    report_data = {
        "title": "Reporte de Métricas e Impacto de Continuum",
        "snapshot": snap,
        "efficiency": {
            "startup_budget_ok": snap["startup_tokens"] <= 3500,
            "memory_topics_fragmented": snap["memory"]["topics_count"] > 0,
        },
    }

    if json_output:
        print(json.dumps(report_data, indent=2))
        return 0

    lines = [
        "# Reporte de Métricas e Impacto de Continuum",
        "",
        f"**Fecha de extracción:** {snap['timestamp']}",
        f"**Rama Git:** `{snap['git']['branch']}` (@ `{snap['git']['commit']}`)",
        "",
        "## Resumen Ejecutivo",
        f"- Presupuesto de arranque: ~{snap['startup_tokens']} tokens (archivos obligatorios cargados al inicio)",
        f"- Memoria viva: {snap['memory']['index_lines']} líneas en índice (`estado-dev.md`), {snap['memory']['topics_count']} tema(s) bajo demanda (~{snap['memory']['topics_total_tokens']} tokens totales)",
        f"- Tareas: {snap['tasks']['active']} activa(s), {snap['tasks']['closed']} archivada(s)",
        f"- Handoff de continuidad: {'Presente' if snap['handoff']['exists'] else 'Ausente'}",
        f"- Hook pre-commit local: {'✓ Instalado' if snap['hooks']['pre_commit_installed'] else '✗ No instalado'}",
        "",
        "## Indicadores de Eficiencia",
        f"- Presupuesto de arranque acotado (<= 3500 tokens): {'✓ CUMPLIDO' if snap['startup_tokens'] <= 3500 else '⚠️ EXCEDE TECHO RECOMENDADO'}",
        f"- Memoria viva modularizada en temas: {'✓ CUMPLIDO' if snap['memory']['topics_count'] > 0 else '⚠️ MEMORIA MONOLÍTICA'}",
    ]
    print("\n".join(lines))
    return 0


def cmd_export(
    root: Path,
    format_type: str = "json",
    anonymize: bool = False,
    json_output: bool = False,
) -> int:
    snap = build_snapshot(root)
    export_data = dict(snap)

    if anonymize:
        commit_hash = hashlib.sha256(snap["git"]["commit"].encode("utf-8")).hexdigest()[:7] if snap["git"]["commit"] else "anonymized"
        export_data["git"] = {
            "commit": commit_hash,
            "branch": "anonymized-branch",
        }
        export_data["anonymized"] = True

    if format_type == "csv":
        header = "timestamp,commit,branch,startup_tokens,index_lines,topics_count,active_tasks,closed_tasks,handoff_exists"
        row = f"{export_data['timestamp']},{export_data['git']['commit']},{export_data['git']['branch']},{export_data['startup_tokens']},{export_data['memory']['index_lines']},{export_data['memory']['topics_count']},{export_data['tasks']['active']},{export_data['tasks']['closed']},{export_data['handoff']['exists']}"
        print(f"{header}\n{row}")
        return 0

    print(json.dumps(export_data, indent=2))
    return 0


def cmd_compare(root: Path, json_output: bool = False) -> int:
    current_snap = build_snapshot(root)
    snapshots_dir = root / ".ai" / "metrics" / "snapshots"

    baseline_snap = None
    if snapshots_dir.exists():
        files = sorted(list(snapshots_dir.glob("*.json")))
        if files:
            try:
                baseline_snap = json.loads(c.read_text(files[0]))
            except Exception:
                pass

    if not baseline_snap:
        baseline_snap = {
            "timestamp": "initial-baseline",
            "startup_tokens": 3500,
            "memory": {"index_lines": 50, "topics_count": 0, "topics_total_tokens": 0},
            "tasks": {"active": 0, "closed": 0},
            "handoff": {"exists": False, "age_hours": None},
        }

    diff_tokens = current_snap["startup_tokens"] - baseline_snap["startup_tokens"]
    diff_closed_tasks = current_snap["tasks"]["closed"] - baseline_snap["tasks"]["closed"]

    comparison = {
        "baseline_timestamp": baseline_snap.get("timestamp"),
        "current_timestamp": current_snap.get("timestamp"),
        "startup_tokens": {
            "baseline": baseline_snap["startup_tokens"],
            "current": current_snap["startup_tokens"],
            "delta": diff_tokens,
        },
        "closed_tasks": {
            "baseline": baseline_snap["tasks"]["closed"],
            "current": current_snap["tasks"]["closed"],
            "delta": diff_closed_tasks,
        },
    }

    if json_output:
        print(json.dumps(comparison, indent=2))
        return 0

    lines = [
        "== Comparación de Métricas vs Baseline ==",
        f"Baseline: {baseline_snap.get('timestamp')}",
        f"Actual:   {current_snap.get('timestamp')}",
        "",
        f"Presupuesto de arranque: ~{current_snap['startup_tokens']} tokens (Baseline: ~{baseline_snap['startup_tokens']} tokens | Delta: {diff_tokens:+d})",
        f"Tareas completadas y archivadas: {current_snap['tasks']['closed']} (Baseline: {baseline_snap['tasks']['closed']} | Delta: {diff_closed_tasks:+d})",
    ]
    print("\n".join(lines))
    return 0

