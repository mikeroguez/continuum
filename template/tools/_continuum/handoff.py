"""El "buzón" de continuidad: .ai/HANDOFF.md

Es el único archivo que debe estar SIEMPRE actualizado, incluso si no hay una
carpeta de tarea formal. Se diseñó para dos disparadores:

1. Manual: la IA o la persona lo actualiza al terminar una sesión o notar que
   se está por agotar el contexto/tokens.
2. Automático: un hook (Claude Code SessionEnd o un git pre-push) llama
   `continuum handoff --auto`, que arma un borrador desde `git status`/`git diff`
   aunque nadie se acuerde de hacerlo a mano. Esto es lo que faltaba en los
   proyectos previos: la disciplina dependía 100% de la memoria humana/del
   agente, y por eso el handoff quedaba desactualizado.
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

from . import common as c

# Prefijos de encabezado "## " que write_auto intenta heredar del handoff
# anterior en vez de dejar en blanco. Prefijo, no texto exacto, porque el
# handoff manual usa "## Objetivo" y el propio write_auto históricamente
# escribe "## Objetivo de esta sesión" — ambos deben reconocerse.
_CARRY_SECTIONS = {
    "objetivo": "Objetivo",
    "siguiente_paso": "Siguiente paso",
}

# Placeholders sin completar de las plantillas (`.ai/templates/HANDOFF.md`
# y el propio write_auto) — si una sección solo contiene esto, no hay nada
# real que heredar.
_PLACEHOLDER_PREFIXES = (
    "_(completar manualmente)_",
    "_(qué se pidió hacer)_",
    "_(lo primero que debería hacer",
)

# Marca la nota que write_auto agrega al heredar una sección — se usa para
# despojarla ANTES de heredar de nuevo, así dos hooks seguidos sin edición
# manual entre medio no la anidan.
_CARRIED_NOTE_MARKER = "> Heredado del handoff anterior"


def _extract_carried_section(text: str, header_prefix: str) -> str | None:
    """Extrae el cuerpo de la primera sección markdown de nivel 2 cuyo
    encabezado empieza con `header_prefix` (case-insensitive). Devuelve
    None si la sección no existe, está vacía, o solo tiene un placeholder
    sin completar — en esos casos no hay nada útil que heredar."""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if re.match(rf"^##\s+{re.escape(header_prefix)}", line, re.IGNORECASE):
            start = i + 1
            break
    if start is None:
        return None

    end = len(lines)
    for j in range(start, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break

    body = "\n".join(lines[start:end]).strip()

    marker_idx = body.find(_CARRIED_NOTE_MARKER)
    if marker_idx != -1:
        body = body[:marker_idx].rstrip()

    if not body:
        return None
    if any(body.startswith(p) for p in _PLACEHOLDER_PREFIXES):
        return None
    return body


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
    handoff_path = root / cfg["handoff"]["path"]
    previous_text = c.read_text(handoff_path) if handoff_path.exists() else ""
    _archive_previous(root, cfg)

    status = c.git("status", "--porcelain").stdout.strip()
    diff_stat = c.git("diff", "--stat", "HEAD").stdout.strip()
    last_commit = c.git("log", "-1", "--format=%h %s").stdout.strip()
    branch = c.git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()

    carried_note = (
        "\n\n> Heredado del handoff anterior (archivado en "
        f"`{cfg['handoff']['archive_dir']}/`) — esta sesión se cortó sin "
        "confirmarlo, revisa si sigue vigente."
    )
    carried_objetivo = _extract_carried_section(previous_text, _CARRY_SECTIONS["objetivo"])
    carried_siguiente = _extract_carried_section(previous_text, _CARRY_SECTIONS["siguiente_paso"])

    objetivo_block = (
        f"{carried_objetivo}{carried_note}" if carried_objetivo else "_(completar manualmente)_"
    )
    siguiente_block = (
        f"{carried_siguiente}{carried_note}" if carried_siguiente else "_(completar manualmente)_"
    )

    lines = [
        "# Handoff (auto-generado)",
        "",
        f"**Fecha:** {c.date_str()} · **Proveedor:** {provider or 'desconocido'} · "
        f"**Rol:** {role or 'desconocido'} · **Branch:** {branch}",
        "",
        "> Este borrador se generó automáticamente al cortar la sesión "
        "(hook SessionEnd o pre-push). Complementa manualmente el "
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
        objetivo_block,
        "",
        "## Siguiente paso recomendado",
        siguiente_block,
    ]
    c.write_text(root / cfg["handoff"]["path"], "\n".join(lines) + "\n")
    if carried_objetivo or carried_siguiente:
        c.ok(f"Handoff automático escrito en {cfg['handoff']['path']} "
             f"(Objetivo/Siguiente paso heredados del handoff anterior — revísalos).")
    else:
        c.ok(f"Handoff automático escrito en {cfg['handoff']['path']}. "
             f"Faltan por completar 'Objetivo' y 'Siguiente paso'.")
    return 0


def compact_handoff(root: Path) -> int:
    """Compacta .ai/HANDOFF.md reduciendo secciones hipertrofiadas/historiales viejos.

    Archiva una copia completa en .ai/state/archive/handoffs/ y conserva únicamente
    las secciones activas (objetivo, decisiones vigentes, siguiente paso) acotadas.
    """
    cfg = c.load_config(root)
    handoff_path = root / cfg["handoff"]["path"]
    if not handoff_path.exists():
        c.err(f"No existe {cfg['handoff']['path']}")
        return 1

    text = c.read_text(handoff_path)
    lines = text.splitlines()
    tokens = c.estimate_tokens(text)

    if len(lines) <= 45 and tokens <= 500:
        c.info(f"{cfg['handoff']['path']} ya está acotado ({len(lines)} líneas, ~{tokens} tokens). Nada que compactar.")
        return 0

    _archive_previous(root, cfg)

    carried_objetivo = _extract_carried_section(text, _CARRY_SECTIONS["objetivo"])
    carried_siguiente = _extract_carried_section(text, _CARRY_SECTIONS["siguiente_paso"])

    header_lines = []
    for line in lines[:6]:
        if line.startswith("# ") or line.startswith("**Fecha:**") or line.startswith("> "):
            header_lines.append(line)

    last_commit = c.git("log", "-1", "--format=%h %s").stdout.strip()
    status = c.git("status", "--porcelain").stdout.strip()

    compact_content = [
        header_lines[0] if header_lines else "# Handoff",
        "",
        f"**Fecha:** {c.date_str()} · **Estado:** Compactado por continuum compact",
        "",
        "## Último commit",
        f"`{last_commit}`" if last_commit else "(sin commits)",
        "",
        "## Cambios sin commitear",
        f"```\n{status}\n```" if status else "(working tree limpio)",
        "",
        "## Objetivo de esta sesión",
        carried_objetivo or "_(completar manualmente)_",
        "",
        "## Siguiente paso recomendado",
        carried_siguiente or "_(completar manualmente)_",
    ]

    new_text = "\n".join(compact_content) + "\n"
    c.write_text(handoff_path, new_text)
    c.ok(f"Handoff compactado en {cfg['handoff']['path']} (~{c.estimate_tokens(new_text)} tokens). Copia completa archivada en {cfg['handoff']['archive_dir']}/.")
    return 0


def lint_handoff(root: Path) -> list[str]:
    cfg = c.load_config(root)
    handoff_path = root / cfg["handoff"]["path"]
    warnings = []
    if not handoff_path.exists():
        warnings.append(f"No existe {cfg['handoff']['path']}.")
        return warnings

    text = c.read_text(handoff_path)
    tokens = c.estimate_tokens(text)

    if tokens > 400:
        warnings.append(f"El handoff tiene ~{tokens} tokens estimados (límite recomendado: ~400 tokens). "
                        "Considera resumir secciones redundantes o diffs largos con 'continuum compact --handoff'.")

    if "_(completar manualmente)_" in text:
        warnings.append("El handoff contiene secciones sin completar ('_(completar manualmente)_').")

    return warnings
