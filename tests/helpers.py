"""Fixtures compartidas para probar `template/tools/_continuum/`.

Importa el paquete directo desde `template/tools/` (la fuente de verdad,
ver `docs/decision-log.md` ADR-007) en vez de la copia autoalojada en la
raíz — así un test nunca queda "verde" por casualidad contra la copia
equivocada.

No se prueba contra pytest ni ninguna dependencia externa: solo
`unittest` + `subprocess` + `tempfile`, consistente con que
`tools/_continuum/` en sí no tiene dependencias.
"""
from __future__ import annotations

import contextlib
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = REPO_ROOT / "template"
TEMPLATE_TOOLS_DIR = TEMPLATE_DIR / "tools"

if str(TEMPLATE_TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TEMPLATE_TOOLS_DIR))


def run_git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True)


@contextlib.contextmanager
def temp_project(git_init: bool = True, commit: bool = True):
    """Copia la carga útil de `template/` (sin el código de `tools/`) a un
    directorio temporal, hace `cd` ahí (varias funciones de `_continuum`
    dependen del cwd del proceso vía `git`, no de un parámetro explícito),
    y limpia todo al salir.
    """
    tmp = Path(tempfile.mkdtemp(prefix="continuum-test-"))
    shutil.copytree(
        TEMPLATE_DIR, tmp, dirs_exist_ok=True,
        ignore=shutil.ignore_patterns("tools", "__pycache__"),
    )
    prev_cwd = os.getcwd()
    os.chdir(tmp)
    try:
        if git_init:
            run_git("init", "-q")
            run_git("config", "user.email", "test@example.com")
            run_git("config", "user.name", "Continuum Test")
            if commit:
                run_git("add", "-A")
                run_git("commit", "-q", "-m", "init")
        yield tmp
    finally:
        os.chdir(prev_cwd)
        shutil.rmtree(tmp, ignore_errors=True)


def commit_all(message: str = "wip") -> None:
    run_git("add", "-A")
    run_git("commit", "-q", "-m", message)
