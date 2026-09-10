from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import bootstrap, common as c, context, doctor, github, handoff, memory, metrics, packets, release, roles, session, status, tasks




def build_parser() -> argparse.ArgumentParser:

    p = argparse.ArgumentParser(prog="continuum", description=(
        "Framework de memoria de IA transportada por git. "
        "Sin argumentos, corre 'doctor' (foto rápida del estado)."
    ))
    sub = p.add_subparsers(dest="cmd")

    d = sub.add_parser("doctor", help="Valida protocolo, frescura, duplicados y costo en tokens.")
    d.add_argument("--quiet", action="store_true")
    d.add_argument("--fix", action="store_true", help="Planifica o ejecuta auto-reparaciones seguras.")
    d.add_argument("--dry-run", action="store_true", default=True, help="Muestra el plan de reparaciones sin modificar disco (por defecto).")
    d.add_argument("--no-dry-run", action="store_false", dest="dry_run", help="Aplica las reparaciones seguras en disco.")

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

    tcur = tsub.add_parser("current", help="Muestra la tarea activa actual.")
    tcur.add_argument("--json", action="store_true", help="Emite el resultado en formato JSON.")

    tres = tsub.add_parser("resume", help="Muestra el resumen y contexto recomendado para retomar una tarea.")
    tres.add_argument("slug", nargs="?", default=None, help="Slug de la tarea a retomar (opcional si solo hay 1 tarea activa).")
    tres.add_argument("--json", action="store_true", help="Emite el resultado en formato JSON.")


    h = sub.add_parser("handoff", help="Escribe/actualiza .ai/HANDOFF.md.")
    h.add_argument("--auto", action="store_true", help="Genera un borrador desde git status/diff.")
    h.add_argument("--provider", default=None, help="claude|codex|gemini|copilot|humano (informativo).")
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
    sub.add_parser("sync-template", help="Muestra los comandos de git subtree para sincronizar la plantilla (alias de continuum sync).")

    sy = sub.add_parser("sync", help="Sincronización de la plantilla Continuum en proyectos consumidores.")
    sy.add_argument("--check", action="store_true", help="Audita la configuración y el estado del repositorio.")
    sy.add_argument("--dry-run", action="store_true", default=False, help="Muestra el plan de sincronización.")
    sy.add_argument("--apply", action="store_true", help="Ejecuta git subtree pull en un working tree limpio.")
    sy.add_argument("--json", action="store_true", help="Emite el resultado en formato JSON.")


    ro = sub.add_parser("roles", help="Catálogo de roles/personas (ver AI_COLLABORATION.md §9).")
    rosub = ro.add_subparsers(dest="roles_cmd", required=True)
    rosub.add_parser("list", help="Lista los roles de los packs activos en .ai/config.json.")
    rsy = rosub.add_parser("sync", help="Genera subagentes nativos a partir del catálogo canónico.")
    rsy.add_argument("--provider", default="claude", choices=["claude", "copilot"])

    met = sub.add_parser("metrics", help="Métricas locales y baseline de Continuum.")
    metsub = met.add_subparsers(dest="metrics_cmd", required=True)
    snap = metsub.add_parser("snapshot", help="Genera o muestra un snapshot local de métricas.")
    snap.add_argument("--dry-run", action="store_true", default=True, help="Muestra el snapshot sin guardar en disco (por defecto).")
    snap.add_argument("--no-dry-run", action="store_false", dest="dry_run", help="Guarda el snapshot en disco bajo .ai/metrics/snapshots/.")
    snap.add_argument("--json", action="store_true", help="Emite el resultado en formato JSON.")

    mrep = metsub.add_parser("report", help="Genera un reporte de impacto e indicadores de eficiencia de Continuum.")
    mrep.add_argument("--json", action="store_true", help="Emite el resultado en formato JSON.")

    mexp = metsub.add_parser("export", help="Exporta datos de métricas a formato JSON o CSV.")
    mexp.add_argument("--format", choices=["json", "csv"], default="json", dest="format_type", help="Formato de exportación.")
    mexp.add_argument("--anonymize", action="store_true", help="Anonimiza hashes de commits, ramas y datos personales.")
    mexp.add_argument("--json", action="store_true", help="Emite el resultado en formato JSON.")

    mcmp = metsub.add_parser("compare", help="Compara el estado actual de métricas contra el baseline.")
    mcmp.add_argument("--json", action="store_true", help="Emite el resultado en formato JSON.")


    ctx = sub.add_parser("context", help="Muestra el contexto de lectura recomendado para iniciar la sesión.")
    ctx.add_argument("--task", default=None, help="Slug de una tarea para incorporar su contexto específico.")
    ctx.add_argument("--why", action="store_true", help="Muestra la razón de clasificación de cada archivo.")
    ctx.add_argument("--json", action="store_true", help="Emite el resultado en formato JSON.")

    tok = sub.add_parser("tokens", help="Muestra el presupuesto estimado de tokens de arranque y memoria.")
    tok.add_argument("--json", action="store_true", help="Emite el resultado en formato JSON.")

    st = sub.add_parser("status", help="Muestra el estado compacto del proyecto y la siguiente acción sugerida.")
    st.add_argument("--json", action="store_true", help="Emite el resultado en formato JSON.")

    ses = sub.add_parser("session", help="Gestión del ciclo de sesiones e handoff.")
    sessub = ses.add_subparsers(dest="session_cmd", required=True)

    sstart = sessub.add_parser("start", help="Muestra el handoff vigente, tareas activas y contexto inicial sugerido.")
    sstart.add_argument("--json", action="store_true", help="Emite el resultado en formato JSON.")

    send = sessub.add_parser("end", help="Genera/actualiza el handoff y ejecuta linting de calidad.")
    send.add_argument("--message", default=None, help="Resumen o mensaje de la sesión (para handoff manual).")
    send.add_argument("--auto", action="store_true", help="Genera un borrador desde git status/diff.")
    send.add_argument("--provider", default=None, help="Proveedor de la IA (claude|codex|gemini|copilot|humano).")
    send.add_argument("--role", default=None, help="Slug de rol del agente.")
    send.add_argument("--json", action="store_true", help="Emite el resultado en formato JSON.")

    exp = sub.add_parser("export", help="Gestión de la rama export del meta-repositorio.")
    expsub = exp.add_subparsers(dest="export_cmd", required=True)

    exp_st = expsub.add_parser("status", help="Muestra la sincronía de la rama export vs template/.")
    exp_st.add_argument("--json", action="store_true", help="Emite el resultado en formato JSON.")

    exp_rf = expsub.add_parser("refresh", help="Regenera la rama export usando git subtree split.")
    exp_rf.add_argument("--dry-run", action="store_true", default=True, help="Muestra el plan de regeneración (por defecto).")
    exp_rf.add_argument("--no-dry-run", action="store_false", dest="dry_run", help="Ejecuta git subtree split.")
    exp_rf.add_argument("--json", action="store_true", help="Emite el resultado en formato JSON.")

    rel = sub.add_parser("release", help="Preparación y liberación de una versión SemVer.")
    rel.add_argument("version", help="Versión SemVer a liberar (ej. v1.0.0).")
    rel.add_argument("--dry-run", action="store_true", default=True, help="Valida y muestra el plan de liberación (por defecto).")
    rel.add_argument("--no-dry-run", action="store_false", dest="dry_run", help="Crea el tag de release sobre la rama export.")
    rel.add_argument("--json", action="store_true", help="Emite el resultado en formato JSON.")

    gh_cmd = sub.add_parser("github", help="Herramientas e inspección de protección para GitHub.")
    gh_sub = gh_cmd.add_subparsers(dest="github_cmd", required=True)

    gh_prot = gh_sub.add_parser("protect", help="Audita y sugiere las reglas de protección para ramas y tags.")
    gh_prot.add_argument("--print", action="store_true", default=True, help="Muestra la guía recomendada (por defecto).")
    gh_prot.add_argument("--apply", action="store_true", help="Aplica o guía la configuración vía CLI gh si está autenticado.")
    gh_prot.add_argument("--json", action="store_true", help="Emite el resultado en formato JSON.")

    return p





def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = c.repo_root()

    if args.cmd is None or args.cmd == "doctor":
        quiet = getattr(args, "quiet", False)
        fix = getattr(args, "fix", False)
        dry_run = getattr(args, "dry_run", True)
        return doctor.run(root, quiet=quiet, fix=fix, dry_run=dry_run)

    if args.cmd == "status":
        return status.cmd_status(root, json_output=args.json)

    if args.cmd == "task":
        if args.task_cmd == "start":
            return tasks.start(root, args.slug, args.size, args.owner, args.role)
        if args.task_cmd == "claim":
            return tasks.claim(root, args.slug, args.owner)
        if args.task_cmd == "close":
            return tasks.close(root, args.slug, force=args.force)
        if args.task_cmd == "list":
            return tasks.list_tasks(root)
        if args.task_cmd == "current":
            return tasks.current(root, json_output=args.json)
        if args.task_cmd == "resume":
            return tasks.resume(root, slug=args.slug, json_output=args.json)


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

    if args.cmd in ("sync", "sync-template"):
        check_only = getattr(args, "check", False)
        apply = getattr(args, "apply", False)
        json_output = getattr(args, "json", False)
        return bootstrap.cmd_sync(root, check_only=check_only, apply=apply, json_output=json_output)


    if args.cmd == "roles":
        if args.roles_cmd == "list":
            return roles.list_roles(root)
        if args.roles_cmd == "sync":
            return roles.sync(root, provider=args.provider)

    if args.cmd == "metrics":
        if args.metrics_cmd == "snapshot":
            return metrics.cmd_snapshot(root, dry_run=args.dry_run, json_output=args.json)
        if args.metrics_cmd == "report":
            return metrics.cmd_report(root, json_output=args.json)
        if args.metrics_cmd == "export":
            return metrics.cmd_export(root, format_type=args.format_type, anonymize=args.anonymize, json_output=args.json)
        if args.metrics_cmd == "compare":
            return metrics.cmd_compare(root, json_output=args.json)


    if args.cmd == "context":
        return context.cmd_context(root, task_slug=args.task, show_why=args.why, json_output=args.json)

    if args.cmd == "tokens":
        return context.cmd_tokens(root, json_output=args.json)

    if args.cmd == "session":
        if args.session_cmd == "start":
            return session.cmd_session_start(root, json_output=args.json)
        if args.session_cmd == "end":
            return session.cmd_session_end(
                root,
                message=args.message,
                auto=args.auto,
                provider=args.provider,
                role=args.role,
                json_output=args.json,
            )

    if args.cmd == "export":
        if args.export_cmd == "status":
            return release.cmd_export_status(root, json_output=args.json)
        if args.export_cmd == "refresh":
            return release.cmd_export_refresh(root, dry_run=args.dry_run, json_output=args.json)

    if args.cmd == "release":
        return release.cmd_release(root, version=args.version, dry_run=args.dry_run, json_output=args.json)

    if args.cmd == "github":
        if args.github_cmd == "protect":
            return github.cmd_protect(root, apply=args.apply, json_output=args.json)

    return 1





if __name__ == "__main__":
    sys.exit(main())
