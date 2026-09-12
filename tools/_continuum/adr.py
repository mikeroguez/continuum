"""Gestión de ADRs (Architecture Decision Records) — ADR-012, punto 3.

Extensión opcional sobre la verificación de `continuum doctor`: la
verificación (números duplicados o con huecos) es el núcleo de valor real
porque cubre ADRs que ya existen y que alguien pudo haber escrito a mano.
Este módulo cubre el otro extremo — crear uno nuevo sin tener que calcular
el siguiente número disponible a mano.
"""
from __future__ import annotations

from pathlib import Path

from . import common as c


def next_number(root: Path) -> int:
    numbers = c.collect_adr_numbers(root)
    return max(numbers) + 1 if numbers else 1


def new(root: Path, title: str, slug: str | None = None) -> int:
    title = (title or "").strip()
    if not title:
        c.err("El título del ADR no puede estar vacío: `continuum adr new \"Título de la decisión\"`.")
        return 1

    number = next_number(root)
    decision_log = root / "docs" / "decision-log.md"

    # Convención de log único (docs/decision-log.md) — la que usa este
    # mismo repositorio autoalojado. Si existe, se prioriza sobre la
    # convención de archivo por ADR (mismo orden que `doctor` al detectar).
    if decision_log.exists():
        entry = (
            f"\n## ADR-{number:03d} — {title}\n\n"
            f"**Contexto.** \n\n"
            f"**Decisión.** \n\n"
            f"**Consecuencias.** \n"
        )
        text = c.read_text(decision_log).rstrip("\n") + "\n" + entry
        c.write_text(decision_log, text)
        c.ok(f"ADR-{number:03d} agregado a {decision_log.relative_to(root)}. "
             f"Completa Contexto/Decisión/Consecuencias antes de commitear.")
        return 0

    # Convención de archivo por ADR (AI_COLLABORATION.md §5), la que se
    # recomienda a un proyecto que instala la plantilla por primera vez.
    arch_dir = root / "docs" / "architecture"
    file_slug = slug or c.slugify(title)
    number_str = f"{number:04d}"
    fname = f"ADR-{number_str}-{file_slug}.md"
    fpath = arch_dir / fname
    if fpath.exists():
        c.err(f"{fpath.relative_to(root)} ya existe — pasa otro --slug.")
        return 1

    template_path = root / ".ai" / "templates" / "ADR.md"
    template_text = c.read_text(template_path)
    if not template_text:
        template_text = (
            "# ADR-XXXX: {{TITULO}}\n\n"
            "**Fecha:** {{DATE}} · **Estado:** Propuesta | Aceptada | Reemplazada por ADR-YYYY\n\n"
            "## Contexto\n_(qué situación obliga a decidir algo)_\n\n"
            "## Decisión\n_(qué se decidió, en una frase clara)_\n\n"
            "## Alternativas consideradas\n-\n\n"
            "## Consecuencias\n_(qué se gana, qué se sacrifica, qué queda pendiente de revisar)_\n"
        )
    text = template_text.replace("ADR-XXXX", f"ADR-{number_str}")
    text = text.replace("{{TITULO}}", title)
    text = text.replace("{{DATE}}", c.date_str())

    c.write_text(fpath, text)
    c.ok(f"{fpath.relative_to(root)} creado. "
         f"Completa Contexto/Decisión/Consecuencias antes de commitear.")
    return 0
