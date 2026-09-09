"""Utilidades compartidas por continuum. Sin dependencias externas (solo stdlib)."""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

CANONICAL_FILE = "AI_COLLABORATION.md"
PROVIDER_FILES = {
    "claude": "CLAUDE.md",
    "codex": "AGENTS.md",
    "gemini": "GEMINI.md",
}
DEFAULT_CONFIG = {
    "project": "",
    "providers": ["claude", "codex", "gemini"],
    "estado_dev": {
        # estado-dev.md es un INDICE corto (patrón MEMORY.md + temas, igual
        # al de Auto Memory de Claude Code): apunta a archivos de tema que
        # se cargan bajo demanda, no contiene el detalle él mismo.
        "path": ".ai/state/estado-dev.md",
        "max_index_lines": 80,
        "topics_dir": ".ai/state/topics",
        "max_topic_lines": 300,
    },
    "roles": {
        # Catálogo de "personas" que una sesión puede adoptar para una
        # tarea — no son agentes que corren de forma concurrente (ver
        # docs/decision-log.md ADR-009). "comun" aplica casi siempre;
        # los packs de dominio son opt-in por proyecto.
        "dir": ".ai/roles",
        "packs": ["comun"],
    },
    "tasks": {
        "dir": ".ai/tasks",
        "closed_dir": ".ai/tasks/_closed",
        "stale_after_days": 10,
    },
    "handoff": {
        "path": ".ai/HANDOFF.md",
        "archive_dir": ".ai/state/archive/handoffs",
        "stale_after_hours": 24,
    },
    "template_remote": "",
    "template_prefix": "",
}


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def stamp() -> str:
    return now_utc().strftime("%Y-%m-%dT%H%M%SZ")


def date_str() -> str:
    return now_utc().strftime("%Y-%m-%d")


def repo_root() -> Path:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True,
        )
        return Path(out.stdout.strip())
    except Exception:
        return Path.cwd()


def git(*args: str, check: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], capture_output=True, text=True, check=check)


def is_tracked(path: Path) -> bool:
    root = repo_root()
    try:
        rel = path.relative_to(root)
    except ValueError:
        rel = path
    r = git("ls-files", "--error-unmatch", str(rel))
    return r.returncode == 0


def load_config(root: Path) -> dict:
    cfg_path = root / ".ai" / "config.json"
    cfg = json.loads(json.dumps(DEFAULT_CONFIG))  # deep copy
    if cfg_path.exists():
        try:
            user_cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
            _deep_merge(cfg, user_cfg)
        except json.JSONDecodeError as e:
            warn(f"No se pudo leer {cfg_path}: {e}. Usando configuración por defecto.")
    return cfg


def _deep_merge(base: dict, override: dict) -> None:
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            _deep_merge(base[k], v)
        else:
            base[k] = v


def estimate_tokens(text: str) -> int:
    # Heurística: ~0.75 tokens por palabra en inglés, ~1.3 en español con LLMs
    # modernos suele rondar 1 token ~ 0.7 palabras. Usamos un factor conservador.
    words = len(text.split())
    return int(words * 1.3)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def info(msg: str) -> None:
    print(msg)


def warn(msg: str) -> None:
    print(f"⚠ {msg}", file=sys.stderr)


def err(msg: str) -> None:
    print(f"✗ {msg}", file=sys.stderr)


def ok(msg: str) -> None:
    print(f"✓ {msg}")
