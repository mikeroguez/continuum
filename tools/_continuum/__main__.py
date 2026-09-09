from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import bootstrap, common as c, doctor, handoff, memory, packets, roles, tasks


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="continuum", description=(
        "Framework de memoria de IA transportada por git. "
        "Sin argumentos, corre 'doctor' (foto rápida del estado)."
    ))
    sub = p.add_subparsers(dest="cmd")

    d = sub.add_parser("doctor", help="Valida protocolo, frescura, duplicados y costo en tokens.")
    d.add_argument("--quiet", action="store_true")

    t = sub.add_parser("task", help="Ciclo de vida de tareas.")
    tsub = t.add_subparsers(dest="task_cmd", required=True)

    ts = tsub.add_parser("start", help="Crea una carpeta de tarea desde las plantillas.")
    ts.add_argument("slug")
    ts.add_argument("--size", choices=["small", "medium", "large"], default="medium")
    ts.add_argument("--owner", default=None)
    ts.add_argument("--role", default=None, help="Slug de un rol de .ai/roles/ (ver `continuum roles list`).")

    tc = tsub.add_parser("claim", help="Marca quién está trabajando la tarea.")
    tc.add_argument("slug")
    tc.add_argument("owner")

    tcl = tsub.add_parser("close", help="Cierra y archiva una tarea (exige handoff.md completo).")
    tcl.add_argument("slug")
    tcl.add_argument("--force", action="store_true")

    tsub.add_parser("list", help="Lista tareas activas y cerradas.")

    h = sub.add_parser("handoff", help="Escribe/actualiza .ai/HANDOFF.md.")
    h.add_argument("--auto", action="store_true", help="Genera un borrador desde git status/diff.")
    h.add_argument("--provider", default=None, help="claude|codex|gemini|humano (informativo).")
    h.add_argument("--message", default=None, help="Texto libre a insertar en el handoff manual.")
    h.add_argument("--role", default=None, help="Slug de un rol de .ai/roles/ (informativo).")

    m = sub.add_parser("compact", help="Archiva entradas viejas de un tema (o del índice) por mes.")
    m.add_argument("--topic", default=None, help="Nombre del archivo en .ai/state/topics/ (sin .md). Sin esto, opera sobre el índice.")
    m.add_argument("--keep-last", type=int, default=5)

    sub.add_parser("memory-split-legacy", help=(
        "Migra un estado-dev.md monolítico (formato viejo) a índice + .ai/state/topics/."
    ))

    pk = sub.add_parser("packetize", help="Trocea un archivo grande en fragmentos legibles por partes.")
    pk.add_argument("file")
    pk.add_argument("--slug", default=None, help="Si se da, guarda los fragmentos dentro de esa tarea.")
    pk.add_argument("--chunk-lines", type=int, default=200)

    sub.add_parser("install-hooks", help="Instala el git hook local de pre-commit.")
    sub.add_parser("sync-template", help="Muestra los comandos de git subtree para sincronizar la plantilla.")

    ro = sub.add_parser("roles", help="Catálogo de roles/personas (ver AI_COLLABORATION.md §9).")
    rosub = ro.add_subparsers(dest="roles_cmd", required=True)
    rosub.add_parser("list", help="Lista los roles de los packs activos en .ai/config.json.")
    rsy = rosub.add_parser("sync", help="Genera subagentes nativos a partir del catálogo canónico.")
    rsy.add_argument("--provider", default="claude", choices=["claude"])

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = c.repo_root()

    if args.cmd is None or args.cmd == "doctor":
        quiet = getattr(args, "quiet", False)
        return doctor.run(root, quiet=quiet)

    if args.cmd == "task":
        if args.task_cmd == "start":
            return tasks.start(root, args.slug, args.size, args.owner, args.role)
        if args.task_cmd == "claim":
            return tasks.claim(root, args.slug, args.owner)
        if args.task_cmd == "close":
            return tasks.close(root, args.slug, force=args.force)
        if args.task_cmd == "list":
            return tasks.list_tasks(root)

    if args.cmd == "handoff":
        if args.auto:
            return handoff.write_auto(root, args.provider, args.role)
        return handoff.write_manual(root, args.message, args.role)

    if args.cmd == "compact":
        return memory.compact(root, topic=args.topic, keep_last=args.keep_last)

    if args.cmd == "memory-split-legacy":
        return memory.split_legacy(root)

    if args.cmd == "packetize":
        return packets.packetize(root, Path(args.file), args.slug, args.chunk_lines)

    if args.cmd == "install-hooks":
        return bootstrap.install_hooks(root)

    if args.cmd == "sync-template":
        return bootstrap.sync_template_instructions(root)

    if args.cmd == "roles":
        if args.roles_cmd == "list":
            return roles.list_roles(root)
        if args.roles_cmd == "sync":
            return roles.sync(root, provider=args.provider)

    return 1


if __name__ == "__main__":
    sys.exit(main())
