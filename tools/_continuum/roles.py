"""Catálogo de roles/personas (ver docs/decision-log.md ADR-009).

Un rol es un archivo Markdown corto que una sesión adopta como lente para
una tarea — no es un agente que corre de forma concurrente ni un proceso
separado. `sync()` genera, para los proveedores que lo soportan de forma
nativa (hoy: Claude Code), un subagente real a partir del archivo canónico,
sin duplicar el contenido a mano.
"""
from __future__ import annotations

import re
from pathlib import Path

from . import common as c

TITLE_RE = re.compile(r"^#\s*Rol:\s*(.+)$", re.MULTILINE)
# Captura el párrafo completo del mandato (puede envolver varias líneas en
# el markdown), hasta la línea en blanco que lo cierra.
MANDATO_RE = re.compile(r"\*\*Mandato:\*\*\s*(.+?)(?:\n\n|\Z)", re.DOTALL)


def _parse_role(path: Path, pack: str) -> dict:
    text = c.read_text(path)
    title_m = TITLE_RE.search(text)
    mandato_m = MANDATO_RE.search(text)
    return {
        "pack": pack,
        "slug": path.stem,
        "path": path,
        "title": title_m.group(1).strip() if title_m else path.stem,
        "mandato": " ".join(mandato_m.group(1).split()) if mandato_m else "",
        "text": text,
    }


def discover_roles(root: Path, cfg: dict | None = None) -> list[dict]:
    cfg = cfg or c.load_config(root)
    roles_dir = root / cfg["roles"]["dir"]
    found = []
    for pack in cfg["roles"]["packs"]:
        pack_dir = roles_dir / pack
        if not pack_dir.is_dir():
            continue
        for role_path in sorted(pack_dir.glob("*.md")):
            found.append(_parse_role(role_path, pack))
    return found


def find_role(root: Path, slug: str, cfg: dict | None = None) -> dict | None:
    for role in discover_roles(root, cfg):
        if role["slug"] == slug:
            return role
    return None


def list_roles(root: Path) -> int:
    cfg = c.load_config(root)
    roles = discover_roles(root, cfg)
    if not roles:
        c.warn(f"Ningún rol activo. Packs declarados en .ai/config.json: "
               f"{cfg['roles']['packs']} — revisa que existan en "
               f"{cfg['roles']['dir']}/.")
        return 1
    by_pack: dict[str, list[dict]] = {}
    for r in roles:
        by_pack.setdefault(r["pack"], []).append(r)
    for pack, pack_roles in by_pack.items():
        print(f"[{pack}]")
        for r in pack_roles:
            print(f"  {r['slug']:<24} {r['mandato']}")
    return 0


def sync(root: Path, provider: str = "claude") -> int:
    if provider != "claude":
        c.err(f"Sin soporte de subagentes nativos para '{provider}' todavía "
              f"— el rol sigue siendo una instrucción de texto que el "
              f"entrypoint de ese proveedor referencia, no un archivo generado.")
        return 1

    cfg = c.load_config(root)
    roles = discover_roles(root, cfg)
    if not roles:
        c.warn("No hay roles activos que sincronizar.")
        return 0

    agents_dir = root / ".claude" / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    for role in roles:
        description = role["mandato"] or role["title"]
        frontmatter = (
            "---\n"
            f"name: {role['slug']}\n"
            f"description: {description}\n"
            "---\n\n"
        )
        body = (
            f"Eres el rol \"{role['title']}\" del catálogo de Continuum "
            f"(pack: {role['pack']}). Actúa según lo que dice este archivo — "
            f"no te salgas de su mandato ni tomes las decisiones reservadas "
            f"a otros roles.\n\n{role['text']}"
        )
        c.write_text(agents_dir / f"{role['slug']}.md", frontmatter + body)

    c.ok(f"{len(roles)} subagente(s) de Claude Code generados en "
         f"{agents_dir.relative_to(root)}/ a partir de {cfg['roles']['dir']}/.")
    return 0
