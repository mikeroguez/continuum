"""Selección de contexto mínimo y presupuesto de tokens."""
from __future__ import annotations

import json
from pathlib import Path

from . import common as c


def build_context(root: Path, task_slug: str | None = None) -> dict:
    cfg = c.load_config(root)
    items: list[dict] = []

    # 1. Mandatory items.
    #
    # Los entrypoints por proveedor (CLAUDE.md, AGENTS.md, GEMINI.md,
    # .github/copilot-instructions.md) NO se vuelcan aquí: por diseño, el
    # cliente correspondiente ya los descubre y carga de forma nativa (por
    # eso existen con ese nombre y en esa ruta exacta) — incluir su
    # contenido otra vez sería duplicarlo, no complementarlo (ver
    # `docs/investigacion-2026.md` §10, ADR-012 punto 1). El canónico
    # (`AI_COLLABORATION.md`) y la memoria viva (`estado-dev.md`,
    # `HANDOFF.md`) sí se vuelcan completos: ningún cliente los descubre por
    # sí solo, y depender de que el agente decida abrirlos es exactamente el
    # patrón de falla que `ARCHITECTURE.md` §1 documenta como el más
    # frecuente.
    canonical = root / c.CANONICAL_FILE
    if canonical.exists():
        text = c.read_text(canonical)
        items.append({
            "path": c.CANONICAL_FILE,
            "category": "mandatory",
            "tokens": c.estimate_tokens(text),
            "reason": "Fuente única de verdad del protocolo de colaboración.",
            "inline": True,
            "content": text,
        })

    for p in cfg["providers"]:
        fname = c.PROVIDER_FILES.get(p)
        if fname:
            fpath = root / fname
            if fpath.exists():
                text = c.read_text(fpath)
                items.append({
                    "path": fname,
                    "category": "mandatory",
                    "tokens": c.estimate_tokens(text),
                    "reason": f"Entrypoint para proveedor '{p}'.",
                    "inline": False,
                })

    handoff_rel = cfg["handoff"]["path"]
    handoff_path = root / handoff_rel
    if handoff_path.exists():
        text = c.read_text(handoff_path)
        items.append({
            "path": handoff_rel,
            "category": "mandatory",
            "tokens": c.estimate_tokens(text),
            "reason": "Buzón de continuidad y estado de la sesión previa.",
            "inline": True,
            "content": text,
        })

    estado_rel = cfg["estado_dev"]["path"]
    estado_path = root / estado_rel
    if estado_path.exists():
        text = c.read_text(estado_path)
        items.append({
            "path": estado_rel,
            "category": "mandatory",
            "tokens": c.estimate_tokens(text),
            "reason": "Índice de memoria viva.",
            "inline": True,
            "content": text,
        })

    # 2. Recommended items (if task_slug provided)
    if task_slug:
        task_dir = root / cfg["tasks"]["dir"] / task_slug
        if not task_dir.exists():
            raise ValueError(f"No existe la tarea '{task_slug}' en {cfg['tasks']['dir']}/.")

        task_md = task_dir / "task.md"
        if task_md.exists():
            text = c.read_text(task_md)
            items.append({
                "path": str(task_md.relative_to(root)),
                "category": "recommended",
                "tokens": c.estimate_tokens(text),
                "reason": f"Definición y alcance de la tarea '{task_slug}'.",
            })

        plan_md = task_dir / "execution-plan.md"
        if plan_md.exists():
            text = c.read_text(plan_md)
            items.append({
                "path": str(plan_md.relative_to(root)),
                "category": "recommended",
                "tokens": c.estimate_tokens(text),
                "reason": f"Plan de ejecución de la tarea '{task_slug}'.",
            })

    # 3. On-demand items (topics)
    topics_dir = root / cfg["estado_dev"]["topics_dir"]
    if topics_dir.exists():
        for tf in sorted(topics_dir.glob("*.md")):
            text = c.read_text(tf)
            rel = str(tf.relative_to(root))
            items.append({
                "path": rel,
                "category": "on_demand",
                "tokens": c.estimate_tokens(text),
                "reason": "Tema de memoria detallada (abrir solo si la tarea lo requiere).",
            })

    startup_tokens = sum(it["tokens"] for it in items if it["category"] in ("mandatory", "recommended"))
    total_tokens = sum(it["tokens"] for it in items)

    return {
        "task": task_slug,
        "items": items,
        "startup_tokens": startup_tokens,
        "total_tokens": total_tokens,
    }


def format_human_context(data: dict, show_why: bool = False) -> str:
    categories = {
        "mandatory": "OBLIGATORIOS (Cargar siempre al inicio)",
        "recommended": "RECOMENDADOS (Relevantes para la tarea)",
        "on_demand": "BAJO DEMANDA (Abrir solo si es necesario)",
        "avoid": "EVITAR POR AHORA (Archivados o cerrados)",
    }
    grouped: dict[str, list[dict]] = {k: [] for k in categories}
    for item in data["items"]:
        grouped.setdefault(item["category"], []).append(item)

    lines = ["== Contexto Sugerido de Continuum =="]
    if data.get("task"):
        lines.append(f"Tarea activa: {data['task']}")
    lines.append(f"Presupuesto inicial estimado: ~{data['startup_tokens']} tokens\n")

    for cat_key, cat_title in categories.items():
        cat_items = grouped.get(cat_key, [])
        if not cat_items:
            continue
        lines.append(f"[{cat_title}]")
        for it in cat_items:
            if it.get("inline") is False:
                line = f"  - {it['path']} (~{it['tokens']} tokens, cargado nativamente por el cliente)"
            else:
                line = f"  - {it['path']} (~{it['tokens']} tokens)"
            if show_why:
                line += f"\n    ↳ Razón: {it['reason']}"
            lines.append(line)
            if it.get("inline") and it.get("content"):
                lines.append(f"--- {it['path']} (contenido completo) ---")
                lines.append(it["content"].rstrip("\n"))
                lines.append(f"--- fin {it['path']} ---")
        lines.append("")

    return "\n".join(lines).rstrip()


def build_tokens_report(root: Path) -> dict:
    cfg = c.load_config(root)

    mandatory_files = [c.CANONICAL_FILE] + [c.PROVIDER_FILES[p] for p in cfg["providers"] if p in c.PROVIDER_FILES]
    mandatory_files.append(cfg["estado_dev"]["path"])
    mandatory_files.append(cfg["handoff"]["path"])

    files_breakdown = []
    startup_tokens = 0

    for rel in mandatory_files:
        p = root / rel
        if p.exists():
            text = c.read_text(p)
            t = c.estimate_tokens(text)
            startup_tokens += t
            files_breakdown.append({"path": rel, "type": "mandatory", "tokens": t})

    topics_breakdown = []
    topics_dir = root / cfg["estado_dev"]["topics_dir"]
    topics_tokens = 0
    if topics_dir.exists():
        for tf in sorted(topics_dir.glob("*.md")):
            text = c.read_text(tf)
            t = c.estimate_tokens(text)
            topics_tokens += t
            rel = str(tf.relative_to(root))
            topics_breakdown.append({"path": rel, "tokens": t})

    return {
        "startup_tokens": startup_tokens,
        "mandatory_files": files_breakdown,
        "topics_tokens": topics_tokens,
        "topics_files": topics_breakdown,
        "total_estimated_tokens": startup_tokens + topics_tokens,
    }


def format_human_tokens(report: dict) -> str:
    lines = [
        "== Presupuesto de Tokens de Continuum ==",
        f"TOTAL de arranque (siempre cargados): ~{report['startup_tokens']} tokens",
        "",
        "[Archivos de arranque]",
    ]
    for item in report["mandatory_files"]:
        lines.append(f"  - {item['path']}: ~{item['tokens']} tokens")

    lines.append("")
    lines.append(f"[Temas de memoria viva (~{report['topics_tokens']} tokens totales)]")
    for topic in report["topics_files"]:
        lines.append(f"  - {topic['path']}: ~{topic['tokens']} tokens")

    lines.append("")
    lines.append(f"TOTAL GENERAL (arranque + todos los temas): ~{report['total_estimated_tokens']} tokens")
    return "\n".join(lines)


def cmd_context(root: Path, task_slug: str | None = None, show_why: bool = False, json_output: bool = False) -> int:
    try:
        data = build_context(root, task_slug=task_slug)
    except ValueError as e:
        c.err(str(e))
        return 1

    if json_output:
        print(json.dumps(data, indent=2))
    else:
        print(format_human_context(data, show_why=show_why))

    return 0


def cmd_tokens(root: Path, json_output: bool = False) -> int:
    report = build_tokens_report(root)
    if json_output:
        print(json.dumps(report, indent=2))
    else:
        print(format_human_tokens(report))
    return 0
