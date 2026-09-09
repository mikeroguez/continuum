"""Chunking estático a Markdown — ÚLTIMO RECURSO, no el flujo por defecto.

El paper de Recursive Language Models (arXiv:2512.24601, "el paradigma de
2026" según la investigación en docs/investigacion-2026.md §9) no propone
trocear archivos de antemano: propone darle al modelo un REPL y dejar que
decida en tiempo real cómo explorar el contexto. Un agente con `Read`
(offset/límite) y `grep` nativos —Claude Code, Codex CLI, Gemini CLI— ya
tiene esa capacidad; usar este comando encima es ceremonia redundante.

Úsalo solo cuando de verdad haga falta: alimentar un sub-proceso o un modelo
sin herramientas de archivo con un fragmento acotado de un archivo enorme.
"""
from __future__ import annotations

from pathlib import Path

from . import common as c


def packetize(root: Path, target: Path, slug: str | None, chunk_lines: int = 200) -> int:
    # Resolver ambos (no solo target) evita que `relative_to` falle cuando
    # `root` cuelga de un symlink que `target.resolve()` sí sigue -- p. ej.
    # macOS resuelve /tmp como /private/tmp.
    root = root.resolve()
    target = target.resolve()
    if not target.exists():
        c.err(f"No existe {target}")
        return 1

    lines = c.read_text(target).splitlines(keepends=True)
    total_lines = len(lines)
    if total_lines <= chunk_lines:
        c.info(f"{target} tiene {total_lines} líneas (<= {chunk_lines}). "
               f"No hace falta trocearlo, léelo directo.")
        return 0

    chunks = [lines[i:i + chunk_lines] for i in range(0, total_lines, chunk_lines)]
    total = len(chunks)

    cfg = c.load_config(root)
    if slug:
        out_dir = root / cfg["tasks"]["dir"] / slug / "packets"
    else:
        out_dir = root / ".ai" / "state" / "packets"
    out_dir.mkdir(parents=True, exist_ok=True)

    safe_name = str(target.relative_to(root)).replace("/", "__")
    index_lines = [f"# Índice de fragmentos — {target.relative_to(root)}", "",
                   f"Total: {total_lines} líneas en {total} fragmento(s) de ~{chunk_lines} líneas.", ""]

    for i, chunk in enumerate(chunks, start=1):
        first_line = (i - 1) * chunk_lines + 1
        last_line = min(i * chunk_lines, total_lines)
        chunk_name = f"{safe_name}__chunk-{i:03d}-of-{total:03d}.md"
        header = (
            f"<!-- fuente: {target.relative_to(root)} | líneas {first_line}-{last_line} "
            f"| fragmento {i}/{total} -->\n\n```\n"
        )
        body = "".join(chunk)
        c.write_text(out_dir / chunk_name, header + body + "\n```\n")
        index_lines.append(f"- [{chunk_name}](./{chunk_name}) — líneas {first_line}-{last_line}")

    c.write_text(out_dir / f"{safe_name}__index.md", "\n".join(index_lines) + "\n")
    c.ok(f"{total} fragmento(s) generados en {out_dir.relative_to(root)}")
    return 0
