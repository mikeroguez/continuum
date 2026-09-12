"""Catálogo de roles/personas (ver docs/decision-log.md ADR-009).

Un rol es un archivo Markdown corto que una sesión adopta como lente para
una tarea — no es un agente que corre de forma concurrente ni un proceso
separado. `sync()` genera, para los proveedores que lo soportan de forma nativa, un
subagente real a partir del archivo canónico, sin duplicar el contenido a mano.
"""
from __future__ import annotations

import json
import re
import shutil
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


def _prune_orphaned_files(agents_dir: Path, suffix: str, valid_slugs: set[str]) -> list[str]:
    """Borra archivos que `roles.sync()` generó (huella verificada) para un
    slug que ya no existe en el catálogo activo — un rol eliminado no debe
    dejar su subagente huérfano para siempre. Nunca toca un archivo sin la
    huella de Continuum, sin importar su nombre."""
    removed = []
    if not agents_dir.exists():
        return removed
    for f in agents_dir.glob(f"*{suffix}"):
        slug = c.generated_role_slug(c.read_text(f))
        if slug and slug not in valid_slugs:
            f.unlink()
            removed.append(f.name)
    return removed


def _prune_orphaned_skill_dirs(skills_dir: Path, valid_slugs: set[str]) -> list[str]:
    """Misma poda que `_prune_orphaned_files`, para la convención de
    directorio-por-skill de Codex/Gemini (`<slug>/SKILL.md`)."""
    removed = []
    if not skills_dir.exists():
        return removed
    for d in skills_dir.iterdir():
        skill_md = d / "SKILL.md"
        if not d.is_dir() or not skill_md.exists():
            continue
        slug = c.generated_role_slug(c.read_text(skill_md))
        if slug and slug not in valid_slugs:
            shutil.rmtree(d)
            removed.append(d.name)
    return removed


def sync(root: Path, provider: str = "claude") -> int:
    if provider not in {"claude", "codex", "copilot", "gemini"}:
        c.err(f"Sin soporte de subagentes nativos para '{provider}' todavía "
              f"— el rol sigue siendo una instrucción de texto que el "
              f"entrypoint de ese proveedor referencia, no un archivo generado.")
        return 1

    cfg = c.load_config(root)
    roles = discover_roles(root, cfg)
    if not roles:
        c.warn("No hay roles activos que sincronizar.")
        return 0

    if provider in {"codex", "gemini"}:
        skills_dir = (
            root / ".agents" / "skills"
            if provider == "codex"
            else root / ".gemini" / "skills"
        )
        skills_dir.mkdir(parents=True, exist_ok=True)
        for role in roles:
            description = role["mandato"] or role["title"]
            frontmatter = (
                "---\n"
                f"name: {role['slug']}\n"
                f"description: {json.dumps(description, ensure_ascii=False)}\n"
                "---\n\n"
            )
            body = (
                f"Eres el rol \"{role['title']}\" del catálogo de Continuum "
                f"(pack: {role['pack']}). Actúa según lo que dice este archivo - "
                f"no te salgas de su mandato ni tomes las decisiones reservadas "
                f"a otros roles.\n\n{role['text']}"
            )
            role_skill_dir = skills_dir / role["slug"]
            role_skill_dir.mkdir(parents=True, exist_ok=True)
            c.write_text(role_skill_dir / "SKILL.md", frontmatter + body)
        pruned = _prune_orphaned_skill_dirs(skills_dir, {r["slug"] for r in roles})
        provider_name = "Codex" if provider == "codex" else "Gemini CLI / Antigravity"
        c.ok(f"{len(roles)} skill(s) de {provider_name} generados en "
             f"{skills_dir.relative_to(root)}/ a partir de {cfg['roles']['dir']}/.")
        if pruned:
            c.ok(f"{len(pruned)} skill(s) huérfano(s) podado(s) (rol ya no está en el catálogo): "
                 f"{', '.join(pruned)}.")
        return 0

    agents_dir = (
        root / ".claude" / "agents"
        if provider == "claude"
        else root / ".github" / "agents"
    )
    agents_dir.mkdir(parents=True, exist_ok=True)
    suffix = ".md" if provider == "claude" else ".agent.md"
    for role in roles:
        description = role["mandato"] or role["title"]
        frontmatter = (
            "---\n"
            f"name: {role['slug']}\n"
            f"description: {json.dumps(description, ensure_ascii=False)}\n"
            "---\n\n"
        )
        body = (
            f"Eres el rol \"{role['title']}\" del catálogo de Continuum "
            f"(pack: {role['pack']}). Actúa según lo que dice este archivo - "
            f"no te salgas de su mandato ni tomes las decisiones reservadas "
            f"a otros roles.\n\n{role['text']}"
        )
        c.write_text(agents_dir / f"{role['slug']}{suffix}", frontmatter + body)

    pruned = _prune_orphaned_files(agents_dir, suffix, {r["slug"] for r in roles})

    provider_name = "Claude Code" if provider == "claude" else "GitHub Copilot"
    c.ok(f"{len(roles)} subagente(s) de {provider_name} generados en "
         f"{agents_dir.relative_to(root)}/ a partir de {cfg['roles']['dir']}/.")
    if pruned:
        c.ok(f"{len(pruned)} subagente(s) huérfano(s) podado(s) (rol ya no está en el catálogo): "
             f"{', '.join(pruned)}.")
    return 0
