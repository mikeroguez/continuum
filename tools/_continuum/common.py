"""Utilidades compartidas por continuum. Sin dependencias externas (solo stdlib)."""
from __future__ import annotations

import json
import re
import subprocess
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

ADR_HEADER_RE = re.compile(r"^##\s+ADR-(\d+)\b")
ADR_FILENAME_RE = re.compile(r"^ADR-(\d+)")

CANONICAL_FILE = "AI_COLLABORATION.md"
PROVIDER_FILES = {
    "claude": "CLAUDE.md",
    "codex": "AGENTS.md",
    "gemini": "GEMINI.md",
    "copilot": ".github/copilot-instructions.md",
}
DEFAULT_CONFIG = {
    "project": "",
    "providers": ["claude", "codex", "gemini", "copilot"],
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


def pre_commit_hook_installed(root: Path) -> bool:
    """True si git invocará un pre-commit hook que corre `continuum doctor`.

    Resuelve la ruta real con `git rev-parse --git-path hooks/pre-commit`,
    que respeta `core.hooksPath` (p. ej. `.githooks/` instalado por
    `continuum install-hooks`) en vez de asumir siempre `.git/hooks/`.
    """
    r = git("rev-parse", "--git-path", "hooks/pre-commit")
    if r.returncode != 0:
        return False
    hook_path = root / r.stdout.strip()
    if not hook_path.exists():
        return False
    return "continuum doctor" in read_text(hook_path)


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


def slugify(text: str) -> str:
    """Reduce un título libre a un slug de archivo: minúsculas, sin acentos,
    solo [a-z0-9-]. Usado por `continuum adr new` para nombrar el archivo
    cuando no se pasa `--slug` explícito."""
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")
    return slug or "sin-titulo"


def collect_adr_numbers(root: Path) -> list[int]:
    """Junta números de ADR de las dos convenciones que este protocolo
    admite: un log único (`docs/decision-log.md`, con encabezados
    `## ADR-###` — la que usa este mismo repositorio autoalojado) y archivos
    sueltos (`docs/architecture/ADR-###-*.md`, la que recomienda
    `AI_COLLABORATION.md` §5 a un proyecto que instala la plantilla). Un
    proyecto real solo usa una de las dos, pero nada impide verificar o
    numerar contra ambas fuentes a la vez (ver `docs/decision-log.md`
    ADR-012)."""
    numbers: list[int] = []

    decision_log = root / "docs" / "decision-log.md"
    if decision_log.exists():
        for line in read_text(decision_log).splitlines():
            m = ADR_HEADER_RE.match(line)
            if m:
                numbers.append(int(m.group(1)))

    arch_dir = root / "docs" / "architecture"
    if arch_dir.exists():
        for f in arch_dir.glob("ADR-*.md"):
            m = ADR_FILENAME_RE.match(f.name)
            if m:
                numbers.append(int(m.group(1)))

    return numbers


def adr_numbering_issues(numbers: list[int]) -> tuple[list[int], list[int]]:
    """Devuelve (duplicados, huecos) a partir de una lista de números de ADR
    — ADR-012, punto 3: la numeración depende hoy de que quien escribe un
    ADR recuerde revisar a mano lo que ya existe."""
    if not numbers:
        return [], []
    seen: set[int] = set()
    duplicates: list[int] = []
    for n in numbers:
        if n in seen:
            duplicates.append(n)
        seen.add(n)
    gaps = [n for n in range(min(numbers), max(numbers) + 1) if n not in seen]
    return duplicates, gaps
