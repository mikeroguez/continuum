"""continuum doctor: valida en segundos el estado de la memoria/protocolo de IA.

Pensado para correr en <1s como git hook y para dar, sin memorizar subcomandos,
una foto clara de qué está desactualizado o roto. Es la pieza que reemplaza a
check-workflow.sh (que solo miraba que existieran archivos) con verificaciones
que sí importan: frescura, duplicados, tamaño en tokens, tareas abandonadas.
"""
from __future__ import annotations

import time
from pathlib import Path

from . import common as c


def run(root: Path, quiet: bool = False) -> int:
    cfg = c.load_config(root)
    problems = 0
    warnings = 0

    def section(title: str) -> None:
        if not quiet:
            print(f"\n== {title} ==")

    # 1. Archivo canónico
    section("Protocolo canónico")
    canonical = root / c.CANONICAL_FILE
    if not canonical.exists():
        c.err(f"Falta {c.CANONICAL_FILE} (fuente única de verdad del protocolo).")
        problems += 1
    elif not c.is_tracked(canonical):
        c.err(f"{c.CANONICAL_FILE} existe pero no está en git (no viaja con el repo).")
        problems += 1
    else:
        c.ok(f"{c.CANONICAL_FILE} presente y trackeado.")

    # 2. Entrypoints por proveedor
    section("Entrypoints por proveedor")
    for provider in cfg["providers"]:
        fname = c.PROVIDER_FILES.get(provider)
        if not fname:
            c.warn(f"Proveedor desconocido en config.json: {provider}")
            warnings += 1
            continue
        fpath = root / fname
        if not fpath.exists():
            c.err(f"{provider}: falta {fname}")
            problems += 1
            continue
        if not c.is_tracked(fpath):
            c.err(f"{provider}: {fname} existe pero no está trackeado en git")
            problems += 1
            continue
        content = c.read_text(fpath)
        if c.CANONICAL_FILE not in content:
            c.err(f"{provider}: {fname} no referencia {c.CANONICAL_FILE} "
                  f"(puede tener reglas divergentes)")
            problems += 1
        else:
            c.ok(f"{provider}: {fname} OK, remite a {c.CANONICAL_FILE}")

    # 3. Duplicados conocidos (mismo nombre de archivo en más de un lugar)
    section("Duplicados")
    watch_names = ["estado-dev.md", "estado-proyecto.md", "CHANGELOG.md", "AI_COLLABORATION.md"]
    # "template" queda excluido a propósito: un repo que distribuye su propia
    # plantilla (como este) mantiene ahí una copia fuente idéntica a la
    # instancia activa en la raíz — eso no es la divergencia accidental que
    # este chequeo busca detectar.
    for name in watch_names:
        matches = [p for p in root.rglob(name)
                   if ".git" not in p.parts and "_closed" not in p.parts
                   and "archive" not in p.parts and "node_modules" not in p.parts
                   and "vendor" not in p.parts and "template" not in p.parts]
        if len(matches) > 1:
            rels = ", ".join(str(m.relative_to(root)) for m in matches)
            c.warn(f"{name} aparece {len(matches)} veces: {rels} "
                   f"(riesgo de divergencia — debería haber una sola fuente + archivo(s) generado(s))")
            warnings += 1

    # 4. Índice (estado-dev.md) + temas: tamaño y frescura
    section("Memoria viva (índice + temas)")
    estado_path = root / cfg["estado_dev"]["path"]
    topics_dir = root / cfg["estado_dev"]["topics_dir"]
    if not estado_path.exists():
        c.err(f"Falta {cfg['estado_dev']['path']} (el índice)")
        problems += 1
    else:
        text = c.read_text(estado_path)
        lines = text.count("\n") + 1
        tokens = c.estimate_tokens(text)
        max_lines = cfg["estado_dev"]["max_index_lines"]
        if lines > max_lines:
            c.warn(f"{cfg['estado_dev']['path']} tiene {lines} líneas "
                   f"(un índice debería ser corto, límite {max_lines}; ~{tokens} tokens). "
                   f"Parece que le metiste contenido en vez de un puntero — muévelo a "
                   f"{cfg['estado_dev']['topics_dir']}/.")
            warnings += 1
        else:
            c.ok(f"Índice: {lines} líneas, ~{tokens} tokens estimados (límite {max_lines}).")

        mtime_days = (time.time() - estado_path.stat().st_mtime) / 86400
        last_code_commit = c.git("log", "-1", "--format=%ct")
        if last_code_commit.returncode == 0 and last_code_commit.stdout.strip():
            last_commit_days = (time.time() - int(last_code_commit.stdout.strip())) / 86400
            if mtime_days - last_commit_days > cfg["tasks"]["stale_after_days"]:
                c.warn(f"El índice no se toca hace {mtime_days:.0f} días pero hay "
                       f"commits más recientes en el repo. Puede estar desactualizado.")
                warnings += 1

    if topics_dir.exists():
        for topic_file in sorted(topics_dir.glob("*.md")):
            t_text = c.read_text(topic_file)
            t_lines = t_text.count("\n") + 1
            max_topic = cfg["estado_dev"]["max_topic_lines"]
            rel = topic_file.relative_to(root)
            if t_lines > max_topic:
                c.warn(f"{rel} tiene {t_lines} líneas (límite {max_topic}). "
                       f"Corre `continuum compact --topic {topic_file.stem}` o divide el tema.")
                warnings += 1
            else:
                c.ok(f"{rel}: {t_lines} líneas.")
    else:
        c.warn(f"No existe {cfg['estado_dev']['topics_dir']}/ — la memoria detallada "
               f"debería vivir ahí, no en el índice.")
        warnings += 1

    # 5. Roles activos
    section("Roles")
    roles_dir = root / cfg["roles"]["dir"]
    for pack in cfg["roles"]["packs"]:
        pack_dir = roles_dir / pack
        if not pack_dir.is_dir() or not any(pack_dir.glob("*.md")):
            c.warn(f"Pack de roles '{pack}' declarado en .ai/config.json pero "
                   f"no existe o está vacío en {roles_dir.relative_to(root)}/.")
            warnings += 1
        else:
            n = len(list(pack_dir.glob("*.md")))
            c.ok(f"Pack '{pack}': {n} rol(es).")

    # 6. Tareas abandonadas
    section("Tareas activas")
    tasks_dir = root / cfg["tasks"]["dir"]
    stale_days = cfg["tasks"]["stale_after_days"]
    if tasks_dir.exists():
        active = [p for p in tasks_dir.iterdir() if p.is_dir() and p.name != "_closed"]
        if not active:
            c.ok("No hay tareas activas abiertas.")
        for task_dir in active:
            task_md = task_dir / "task.md"
            handoff_md = task_dir / "handoff.md"
            if not task_md.exists():
                continue
            age_days = (time.time() - task_md.stat().st_mtime) / 86400
            if not handoff_md.exists() and age_days > stale_days:
                c.warn(f"Tarea '{task_dir.name}' abierta hace {age_days:.0f} días sin handoff.md "
                       f"(¿abandonada o a medio camino?). Revisa o cierra con `continuum task close {task_dir.name}`.")
                warnings += 1
            else:
                c.ok(f"Tarea '{task_dir.name}' — {'con' if handoff_md.exists() else 'sin'} handoff, {age_days:.0f}d")

    # 7. Handoff (mailbox) global
    section("Handoff de continuidad")
    handoff_path = root / cfg["handoff"]["path"]
    if not handoff_path.exists():
        c.warn(f"No existe {cfg['handoff']['path']} — créalo con `continuum handoff`. "
               f"Es el primer archivo que debe leer cualquier sesión nueva.")
        warnings += 1
    else:
        age_h = (time.time() - handoff_path.stat().st_mtime) / 3600
        dirty = c.git("status", "--porcelain").stdout.strip() != ""
        if dirty and age_h > cfg["handoff"]["stale_after_hours"]:
            c.warn(f"Hay cambios sin commitear y el handoff tiene {age_h:.0f}h de antigüedad. "
                   f"Si vas a cortar la sesión, actualiza {cfg['handoff']['path']} antes.")
            warnings += 1
        else:
            c.ok(f"Handoff con {age_h:.0f}h de antigüedad.")

    # 8. Tamaño en tokens de los archivos "siempre cargados"
    section("Costo de contexto (archivos que toda sesión nueva debería leer)")
    always_loaded = [c.CANONICAL_FILE] + [c.PROVIDER_FILES[p] for p in cfg["providers"] if p in c.PROVIDER_FILES]
    always_loaded.append(cfg["estado_dev"]["path"])
    always_loaded.append(cfg["handoff"]["path"])
    total_tokens = 0
    for rel in always_loaded:
        p = root / rel
        if p.exists():
            t = c.estimate_tokens(c.read_text(p))
            total_tokens += t
            if not quiet:
                print(f"  {rel}: ~{t} tokens")
    if not quiet:
        print(f"  TOTAL estimado de arranque: ~{total_tokens} tokens")
    if total_tokens > 8000:
        c.warn("El paquete de arranque supera ~8k tokens estimados. Con el índice "
               "acotado a temas separados esto no debería pasar salvo que los "
               "entrypoints (AGENTS.md/CLAUDE.md/GEMINI.md) tengan contenido "
               "inferible o boilerplate — revisa qué se puede borrar antes de "
               "asumir que hay que compactar más.")
        warnings += 1

    print(f"\n{problems} problema(s) crítico(s), {warnings} advertencia(s).")
    return 1 if problems > 0 else 0
