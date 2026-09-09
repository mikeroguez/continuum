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
