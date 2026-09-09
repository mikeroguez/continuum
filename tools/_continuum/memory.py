"""Compactación de memoria y migración desde el formato legado.

Modelo vigente (revisión 2026-09, ver docs/investigacion-2026.md): el índice
(`estado-dev.md`) es corto y solo apunta a archivos de tema en
`.ai/state/topics/*.md`, que se cargan bajo demanda — el mismo patrón que
usa nativamente Claude Code (MEMORY.md + temas) y que "Cline Memory Bank"
documenta de forma independiente. Un tema individual puede seguir creciendo
con entradas fechadas ("## CAMBIO (2026-08-30): ..."); `compact()` archiva
las viejas por mes. `split_legacy()` migra un `estado-dev.md` monolítico
(el formato de la revisión anterior) a este modelo.
"""
from __future__ import annotations

import re
from pathlib import Path

from . import common as c

# Reconoce encabezados de entrada cronológica tipo:
# "## CAMBIO RECIENTE (2026-08-30): CIERRE — Título"
# "## 2026-08-30 — Título"
ENTRY_HEADING_RE = re.compile(
    r"^##\s+.*?(\d{4}-\d{2}-\d{2}).*$", re.MULTILINE
)
STABLE_HEADING_RE = re.compile(r"^##\s+.*$", re.MULTILINE)


def _slugify(title: str) -> str:
    title = re.sub(r"^\d+[.\)]\s*", "", title).strip().lower()
    title = re.sub(r"[^a-z0-9]+", "-", title).strip("-")
    return title or "tema"


def compact(root: Path, topic: str | None = None, keep_last: int = 5) -> int:
    cfg = c.load_config(root)
    if topic:
        target_path = root / cfg["estado_dev"]["topics_dir"] / f"{topic}.md"
        archive_prefix = topic
    else:
        target_path = root / cfg["estado_dev"]["path"]
        archive_prefix = "indice"

    if not target_path.exists():
        c.err(f"No existe {target_path}")
        return 1

    text = c.read_text(target_path)
    matches = list(ENTRY_HEADING_RE.finditer(text))
    if len(matches) <= keep_last:
        c.info(f"Solo hay {len(matches)} entrada(s) cronológica(s) detectada(s) "
               f"(<= {keep_last}). Nada que archivar en {target_path.relative_to(root)}.")
        return 0

    blocks = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else _first_stable_heading(text, start)
        blocks.append((m.group(1), text[start:end]))

    to_archive = blocks[keep_last:]
    to_keep = blocks[:keep_last]

    archive_dir = root / ".ai" / "state" / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    by_month: dict[str, list[str]] = {}
    for date, block in to_archive:
        month = date[:7]
        by_month.setdefault(month, []).append(block)

    pointers = []
    for month, month_blocks in sorted(by_month.items()):
        archive_file = archive_dir / f"{archive_prefix}-{month}.md"
        prior = c.read_text(archive_file)
        header = f"# Historial archivado — {archive_prefix} — {month}\n\n" if not prior else ""
        c.write_text(archive_file, prior + header + "\n".join(month_blocks) + "\n")
        pointers.append(f"- Ver `.ai/state/archive/{archive_prefix}-{month}.md` "
                         f"({len(month_blocks)} entrada(s) de {month})")

    preamble = text[: matches[0].start()]
    kept_text = "".join(block for _, block in to_keep)
    stable_tail = text[_first_stable_heading(text, matches[-1].start()):]

    new_text = (
        preamble.rstrip() + "\n\n"
        + "## Historial archivado\n\n" + "\n".join(pointers) + "\n\n"
        + kept_text.rstrip() + "\n\n"
        + stable_tail
    )
    c.write_text(target_path, new_text)
    c.ok(f"Archivadas {len(to_archive)} entrada(s) de {target_path.relative_to(root)}, "
         f"quedaron las últimas {len(to_keep)}.")
    return 0


def _first_stable_heading(text: str, from_pos: int) -> int:
    for m in re.finditer(r"^##\s+.*$", text[from_pos:], re.MULTILINE):
        abs_pos = from_pos + m.start()
        if abs_pos == from_pos:
            continue
        if not re.search(r"\d{4}-\d{2}-\d{2}", m.group(0)):
            return abs_pos
    return len(text)


def split_legacy(root: Path) -> int:
    """Migra un estado-dev.md monolítico (formato pre-2026-09) a índice + temas.

    Uso previsto: una vez, al adoptar la plantilla en un proyecto que ya
    tenía un estado-dev.md grande (ver docs/rollout-guide.md, Caso A/B).
    No borra nada del archivo original salvo que ya no exista contenido
    después de mover todo — revisa el resultado a mano, esto es asistido,
    no automático al 100%.
    """
    cfg = c.load_config(root)
    legacy_path = root / cfg["estado_dev"]["path"]
    if not legacy_path.exists():
        c.err(f"No existe {legacy_path}")
        return 1

    text = c.read_text(legacy_path)
    chrono_matches = list(ENTRY_HEADING_RE.finditer(text))
    stable_start = _first_stable_heading(text, chrono_matches[-1].start()) if chrono_matches else 0

    # 1. Archiva entradas cronológicas viejas tal como compact() lo haría,
    #    pero aquí simplemente las movemos todas al archive (es una migración,
    #    no una poda incremental).
    if chrono_matches:
        archive_dir = root / ".ai" / "state" / "archive"
        archive_dir.mkdir(parents=True, exist_ok=True)
        by_month: dict[str, list[str]] = {}
        for i, m in enumerate(chrono_matches):
            start = m.start()
            end = chrono_matches[i + 1].start() if i + 1 < len(chrono_matches) else stable_start
            by_month.setdefault(m.group(1)[:7], []).append(text[start:end])
        for month, blocks in sorted(by_month.items()):
            archive_file = archive_dir / f"historial-{month}.md"
            c.write_text(archive_file, f"# Historial archivado — {month}\n\n" + "\n".join(blocks) + "\n")
        c.ok(f"{len(chrono_matches)} entrada(s) cronológica(s) movidas a .ai/state/archive/")

    # 2. Cada sección estable "## N. Título" se vuelve un archivo de tema.
    stable_text = text[stable_start:]
    topics_dir = root / cfg["estado_dev"]["topics_dir"]
    topics_dir.mkdir(parents=True, exist_ok=True)

    headings = list(STABLE_HEADING_RE.finditer(stable_text))
    index_lines = [
        f"# {cfg['project'] or 'Proyecto'} — índice de memoria",
        "",
        "> Índice corto. El detalle vive en `.ai/state/topics/*.md` — ábrelos",
        "> solo si la tarea los necesita. Generado por `continuum memory split-legacy`.",
        "",
    ]
    seen_slugs: set[str] = set()
    collisions = []
    for i, h in enumerate(headings):
        title = h.group(0).lstrip("#").strip()
        start = h.start()
        end = headings[i + 1].start() if i + 1 < len(headings) else len(stable_text)
        body = stable_text[start:end].strip() + "\n"
        slug = _slugify(title)
        while slug in seen_slugs:
            slug += "-2"
        seen_slugs.add(slug)
        topic_path = topics_dir / f"{slug}.md"

        existing = c.read_text(topic_path)
        if existing.strip():
            # No pisamos un tema que ya tiene contenido real (típico: la
            # plantilla ya trae resumen.md/pendientes.md/etc. por defecto).
            # Se anexa con separador y se marca para revisión manual.
            c.write_text(
                topic_path,
                existing.rstrip() + "\n\n---\n\n"
                + f"<!-- fusionado desde estado-dev.md legado por memory-split-legacy, revisar y limpiar -->\n\n"
                + body,
            )
            collisions.append(str(topic_path.relative_to(root)))
        else:
            c.write_text(topic_path, body)
        index_lines.append(f"- **{title}** → `.ai/state/topics/{slug}.md`")

    c.write_text(legacy_path, "\n".join(index_lines) + "\n")
    c.ok(f"{len(headings)} sección(es) migradas a {topics_dir.relative_to(root)}/, "
         f"índice reescrito en {legacy_path.relative_to(root)}. Revísalo a mano.")
    if collisions:
        c.warn("Estos temas ya tenían contenido y se fusionó con '---' en vez de "
               "sobreescribir — revísalos y limpia el duplicado a mano: "
               + ", ".join(collisions))
    return 0
