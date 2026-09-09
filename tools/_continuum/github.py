"""Inspección y protección de ramas/tags para proyectos alojados en GitHub."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from . import common as c


def detect_github_info(root: Path) -> dict:
    remote_res = c.git("remote", "get-url", "origin")
    remote_url = remote_res.stdout.strip()
    is_github = ("github.com" in remote_url)

    gh_binary = shutil.which("gh")
    has_gh = (gh_binary is not None)

    gh_authenticated = False
    if has_gh:
        r = c.git_cmd(["gh", "auth", "status"])
        gh_authenticated = (r.returncode == 0)

    rules = [
        {
            "target": "main",
            "type": "branch",
            "recommendations": [
                "Exigir Pull Requests antes de integrar en main.",
                "Requerir aprobación de al menos 1 revisor.",
                "Requerir checks de estado pasando (continuum doctor, unittest).",
            ],
        },
        {
            "target": "export",
            "type": "branch",
            "recommendations": [
                "Bloquear pases de código directos sin squash/subtree.",
                "Requerir que sólo los releases/tags anotados toquen export.",
            ],
        },
        {
            "target": "v*",
            "type": "tag",
            "recommendations": [
                "Proteger tags SemVer contra sobreescritura o eliminación accidental.",
                "Restringir la creación de tags a mantenedores autorizados.",
            ],
        },
    ]

    return {
        "is_github": is_github,
        "remote_url": remote_url or None,
        "has_gh_cli": has_gh,
        "gh_authenticated": gh_authenticated,
        "recommended_rules": rules,
    }


def cmd_protect(
    root: Path,
    apply: bool = False,
    json_output: bool = False,
) -> int:
    info = detect_github_info(root)

    if json_output:
        print(json.dumps(info, indent=2))
        return 0

    lines = ["== Protección de Repositorio (GitHub Rulesets) =="]
    if not info["is_github"]:
        lines.append("Nota: El remoto 'origin' no parece ser de GitHub.com.")
        if info["remote_url"]:
            lines.append(f"Remoto actual: {info['remote_url']}")
        lines.append("\nEstas recomendaciones aplican a GitHub. Adaptar según tu proveedor Git.")
        lines.append("")

    lines.append(f"Herramienta 'gh' CLI: {'✓ Instalada' if info['has_gh_cli'] else '✗ No encontrada (usar interfaz web)'}")
    lines.append(f"Estado de Autenticación: {'✓ Autenticado' if info['gh_authenticated'] else '⚠️ No autenticado'}")
    lines.append("")
    lines.append("[Reglas de Protección Recomendadas]")

    for rule in info["recommended_rules"]:
        lines.append(f"\n- Objeto '{rule['target']}' ({rule['type']}):")
        for rec in rule["recommendations"]:
            lines.append(f"    • {rec}")

    if apply:
        lines.append("\n== Modo --apply ==")
        if not info["has_gh_cli"]:
            lines.append("No se encontró el CLI 'gh'. Configura las reglas en la interfaz web de GitHub:")
            lines.append("  Settings -> Rulesets / Branches -> Add rule")
        elif not info["gh_authenticated"]:
            lines.append("El CLI 'gh' no está autenticado. Ejecuta 'gh auth login' para autenticarte y luego reintenta.")
        else:
            lines.append("Para aplicar los rulesets mediante la API de GitHub vía CLI 'gh':")
            lines.append("  gh api repos/{owner}/{repo}/rulesets -X POST -F name='Continuum Protection' ...")

    print("\n".join(lines))
    return 0
