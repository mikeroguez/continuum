"""Ciclo de vida de tareas: start / claim / close / list.

Diseño clave (evita el patrón de abandono observado en proyectos previos):
las tareas NO son obligatorias para trabajo pequeño. `AI_COLLABORATION.md`
define el umbral (por líneas de diff / nº de archivos) a partir del cual una
tarea debe tener carpeta propia. Por debajo de eso, basta con el handoff
global (ver handoff.py). Esto reduce la ceremonia que causó que el toolkit
anterior (.ai/tasks/ + rlm_workflow.py) se dejara de usar.
"""
from __future__ import annotations

import shutil
from pathlib import Path

from . import common as c
from . import roles as r

TEMPLATE_FILES = ["task.md", "notes.md", "execution-plan.md"]


def _render(template_text: str, **kwargs) -> str:
    out = template_text
    for k, v in kwargs.items():
        out = out.replace("{{" + k + "}}", str(v))
    return out


def start(root: Path, slug: str, size: str, owner: str | None, role: str | None = None) -> int:
    cfg = c.load_config(root)
    tasks_dir = root / cfg["tasks"]["dir"]
    task_dir = tasks_dir / slug
    if task_dir.exists():
        c.err(f"La tarea '{slug}' ya existe en {task_dir.relative_to(root)}")
        return 1

    role_display = "(sin asignar)"
    if role:
        found = r.find_role(root, role, cfg)
        if found:
            role_display = f"{found['title']} (`{found['pack']}/{found['slug']}`)"
        else:
            c.warn(f"Rol '{role}' no encontrado en los packs activos "
                   f"({cfg['roles']['packs']}) — se guarda como texto libre. "
                   f"Corre `continuum roles list` para ver los disponibles.")
            role_display = role

    templates_dir = root / ".ai" / "templates"
    task_dir.mkdir(parents=True, exist_ok=True)

    common_vars = dict(
        SLUG=slug, DATE=c.date_str(), SIZE=size, OWNER=owner or "(sin asignar)",
        ROLE=role_display,
    )
    template_names = {
        "task.md": "TASK.md",
        "notes.md": "NOTES.md",
        "execution-plan.md": "EXECUTION_PLAN.md",
    }
    for fname in TEMPLATE_FILES:
        tpl_path = templates_dir / template_names[fname]
        text = c.read_text(tpl_path)
        if not text:
            text = f"# {fname}\n\n(plantilla {tpl_path.name} no encontrada)\n"
        c.write_text(task_dir / fname, _render(text, **common_vars))

    if size == "large":
        (task_dir / "packets").mkdir(exist_ok=True)

    c.ok(f"Tarea '{slug}' creada en {task_dir.relative_to(root)} (size={size})")
    return 0


def claim(root: Path, slug: str, owner: str) -> int:
    cfg = c.load_config(root)
    task_md = root / cfg["tasks"]["dir"] / slug / "task.md"
    if not task_md.exists():
        c.err(f"No existe {task_md}")
        return 1
    text = c.read_text(task_md)
    stamp_line = f"\n**Owner:** {owner} (reclamado {c.date_str()})\n"
    if "**Owner:**" in text:
        import re
        text = re.sub(r"\*\*Owner:\*\*.*", stamp_line.strip(), text)
    else:
        text += stamp_line
    c.write_text(task_md, text)
    c.ok(f"Tarea '{slug}' reclamada por {owner}")
    return 0


def close(root: Path, slug: str, force: bool = False) -> int:
    cfg = c.load_config(root)
    tasks_dir = root / cfg["tasks"]["dir"]
    task_dir = tasks_dir / slug
    handoff_md = task_dir / "handoff.md"

    if not task_dir.exists():
        c.err(f"No existe la tarea '{slug}'")
        return 1

    if not handoff_md.exists():
        templates_dir = root / ".ai" / "templates"
        text = c.read_text(templates_dir / "HANDOFF.md")
        c.write_text(handoff_md, _render(text, SLUG=slug, DATE=c.date_str()))
        c.warn(f"Se generó {handoff_md.relative_to(root)} desde la plantilla, vacío. "
               f"Complétalo antes de cerrar de verdad (o usa --force para cerrar igual).")
        if not force:
            return 1

    content = c.read_text(handoff_md)
    if not force and ("{{" in content or len(content.strip()) < 60):
        c.err(f"{handoff_md.relative_to(root)} parece vacío o con placeholders sin rellenar. "
              f"Complétalo o usa --force.")
        return 1

    closed_dir = root / cfg["tasks"]["closed_dir"]
    closed_dir.mkdir(parents=True, exist_ok=True)
    dest = closed_dir / slug
    if dest.exists():
        shutil.rmtree(dest)
    shutil.move(str(task_dir), str(dest))
    c.ok(f"Tarea '{slug}' cerrada y archivada en {dest.relative_to(root)}")
    return 0


def list_tasks(root: Path) -> int:
    cfg = c.load_config(root)
    tasks_dir = root / cfg["tasks"]["dir"]
    if not tasks_dir.exists():
        c.info("No hay directorio de tareas.")
        return 0
    active = sorted(p.name for p in tasks_dir.iterdir() if p.is_dir() and p.name != "_closed")
    closed_dir = tasks_dir / "_closed"
    closed = sorted(p.name for p in closed_dir.iterdir()) if closed_dir.exists() else []
    print("Activas:")
    for a in active:
        print(f"  - {a}")
    print(f"Cerradas: {len(closed)} (en {cfg['tasks']['closed_dir']})")
    return 0


def current(root: Path, json_output: bool = False) -> int:
    import json

    cfg = c.load_config(root)
    tasks_dir = root / cfg["tasks"]["dir"]
    active = []
    if tasks_dir.exists():
        active = sorted(p.name for p in tasks_dir.iterdir() if p.is_dir() and p.name != "_closed")

    if json_output:
        res = {
            "active_count": len(active),
            "active_tasks": active,
            "current_task": active[0] if len(active) == 1 else None,
        }
        print(json.dumps(res, indent=2))
        return 0

    if not active:
        c.info("No hay tareas activas. Usa 'continuum task start <slug>' para crear una.")
    elif len(active) == 1:
        print(f"== Tarea Actual ==\nSlug: {active[0]}\nSiguiente acción: 'continuum task resume {active[0]}'")
    else:
        print(f"== Tareas Activas ({len(active)}) ==")
        for a in active:
            print(f"  - {a}")
        print("\nSiguiente acción: Usa 'continuum task resume <slug>' para retomar la tarea que desees.")

    return 0


def resume(root: Path, slug: str | None = None, json_output: bool = False) -> int:
    import json
    from . import context

    cfg = c.load_config(root)
    tasks_dir = root / cfg["tasks"]["dir"]
    active = sorted(p.name for p in tasks_dir.iterdir() if p.is_dir() and p.name != "_closed") if tasks_dir.exists() else []

    if not slug:
        if len(active) == 1:
            slug = active[0]
        elif not active:
            c.err("No hay tareas activas para retomar. Especifica un slug o crea una tarea nueva.")
            return 1
        else:
            c.err(f"Hay {len(active)} tareas activas ({', '.join(active)}). Especifica cuál deseas retomar: 'continuum task resume <slug>'")
            return 1

    task_dir = tasks_dir / slug
    if not task_dir.exists():
        c.err(f"No existe la tarea '{slug}' en {cfg['tasks']['dir']}/")
        return 1

    task_md = task_dir / "task.md"
    plan_md = task_dir / "execution-plan.md"
    notes_md = task_dir / "notes.md"

    task_content = c.read_text(task_md) if task_md.exists() else None
    plan_content = c.read_text(plan_md) if plan_md.exists() else None
    notes_content = c.read_text(notes_md) if notes_md.exists() else None

    ctx_data = context.build_context(root, task_slug=slug)

    data = {
        "slug": slug,
        "path": str(task_dir.relative_to(root)),
        "task_md": task_content,
        "execution_plan": plan_content,
        "notes": notes_content,
        "suggested_context": ctx_data,
    }

    if json_output:
        print(json.dumps(data, indent=2))
        return 0

    lines = [
        f"== Retomando Tarea: {slug} ==",
        f"Ubicación: {data['path']}",
        "",
    ]
    if task_content:
        lines.append("[Definición de Tarea (task.md)]")
        for line in task_content.splitlines()[:15]:
            lines.append(f"  {line}")
        if len(task_content.splitlines()) > 15:
            lines.append("  ...")
        lines.append("")

    lines.append(context.format_human_context(ctx_data))
    print("\n".join(lines))
    return 0

