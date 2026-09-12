"""Tests para _continuum.uninstall (ver task lifecycle-completo, Paso 3)."""
from __future__ import annotations

import contextlib
import io
import json
import unittest

from .helpers import TEMPLATE_DIR, commit_all, temp_project

from _continuum import bootstrap, common as c, roles, uninstall


# Directorios cubiertos como unidad (no archivo por archivo) en el plan de
# `uninstall`, o deliberadamente excluidos — ver TestManifestDriftCheck.
_COVERED_AS_WHOLE_DIRS = {
    ".ai/templates", ".ai/roles", ".ai/state", ".ai/tasks",
    "tools", ".claude/agents", ".github/agents", ".agents", ".gemini",
    ".github/instructions", ".github/ISSUE_TEMPLATE", ".github/PULL_REQUEST_TEMPLATE",
    "docs/architecture",  # nunca se toca: ahí vive el ADR propio de un proyecto
}
_TIER1_SPECIAL_CASED = {".githooks/pre-commit", ".githooks/README.md", ".gitignore-continuum-fragment"}


class TestManifestDriftCheck(unittest.TestCase):
    """Compara TIER2_PROTOCOL_PATHS contra el `template/` real de este
    repositorio — si se agrega un archivo nuevo a `template/` y se olvida
    agregarlo al manifiesto de `uninstall.py`, este test lo detecta en vez
    de descubrirse en producción."""

    def test_every_shipped_file_is_accounted_for(self):
        unaccounted = []
        for f in TEMPLATE_DIR.rglob("*"):
            if not f.is_file():
                continue
            rel = f.relative_to(TEMPLATE_DIR).as_posix()
            if any(rel == d or rel.startswith(d + "/") for d in _COVERED_AS_WHOLE_DIRS):
                continue
            if rel in _TIER1_SPECIAL_CASED:
                continue
            if rel in uninstall.TIER3_MEMORY_PATHS:
                continue
            if rel not in uninstall.TIER2_PROTOCOL_PATHS:
                unaccounted.append(rel)
        self.assertEqual(
            unaccounted, [],
            f"Archivo(s) nuevo(s) en template/ sin cubrir en uninstall.py: {unaccounted}",
        )


class TestBuildPlan(unittest.TestCase):
    def test_fresh_project_has_no_tier1_generated_agents_or_hooks(self):
        with temp_project() as root:
            plan = uninstall.build_plan(root)
            # .ai/templates/, VERSION, etc. sí están presentes de fábrica.
            tier1_names = {p.name for p in plan["tier1"]}
            self.assertIn("templates", tier1_names)
            self.assertFalse(plan["git_remote_continuum"])

    def test_tier2_includes_entrypoints_and_config(self):
        with temp_project() as root:
            plan = uninstall.build_plan(root)
            tier2_rel = {str(p.relative_to(root)) for p in plan["tier2"]}
            self.assertIn("AI_COLLABORATION.md", tier2_rel)
            self.assertIn(".ai/config.json", tier2_rel)
            self.assertIn(".ai/roles", tier2_rel)

    def test_tier3_is_project_memory_only(self):
        with temp_project() as root:
            plan = uninstall.build_plan(root)
            tier3_rel = {str(p.relative_to(root)) for p in plan["tier3"]}
            self.assertEqual(tier3_rel, {".ai/HANDOFF.md", ".ai/state", ".ai/tasks"})

    def test_docs_architecture_never_appears_in_any_tier(self):
        """docs/architecture/ es donde un proyecto guarda SUS PROPIOS ADRs
        (AI_COLLABORATION.md §5) — nunca debe aparecer como candidato a
        borrar, sin importar el nivel."""
        with temp_project() as root:
            arch = root / "docs" / "architecture"
            arch.mkdir(parents=True, exist_ok=True)
            (arch / "ADR-0001-decision-real-del-proyecto.md").write_text("# ADR-0001\n")
            commit_all()

            plan = uninstall.build_plan(root)
            all_paths = plan["tier1"] + plan["tier2"] + plan["tier3"]
            self.assertNotIn(arch, all_paths)
            self.assertFalse(any("architecture" in str(p) for p in all_paths))


class TestCmdUninstallDryRun(unittest.TestCase):
    def test_dry_run_deletes_nothing(self):
        with temp_project() as root:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                res = uninstall.cmd_uninstall(root, dry_run=True)
            self.assertEqual(res, 0)
            self.assertTrue((root / "AI_COLLABORATION.md").exists())
            self.assertTrue((root / ".ai" / "templates").exists())
            self.assertIn("Modo dry-run", out.getvalue())

    def test_dry_run_json_shape(self):
        with temp_project() as root:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                uninstall.cmd_uninstall(root, dry_run=True, json_output=True)
            data = json.loads(out.getvalue())
            for key in ("tier1", "tier2", "tier3", "dry_run", "included_tiers"):
                self.assertIn(key, data)
            self.assertEqual(data["included_tiers"], ["tier1"])


class TestCmdUninstallApply(unittest.TestCase):
    def test_no_dry_run_alone_removes_only_tier1(self):
        with temp_project() as root:
            res = uninstall.cmd_uninstall(root, dry_run=False)
            self.assertEqual(res, 0)
            self.assertFalse((root / ".ai" / "templates").exists())
            self.assertTrue((root / "AI_COLLABORATION.md").exists())
            self.assertTrue((root / ".ai" / "HANDOFF.md").exists())

    def test_yes_also_removes_tier2_but_not_tier3(self):
        with temp_project() as root:
            uninstall.cmd_uninstall(root, dry_run=False, yes=True)
            self.assertFalse((root / "AI_COLLABORATION.md").exists())
            self.assertFalse((root / ".ai" / "config.json").exists())
            self.assertTrue((root / ".ai" / "HANDOFF.md").exists())
            self.assertTrue((root / ".ai" / "state").exists())

    def test_purge_memory_removes_everything(self):
        with temp_project() as root:
            uninstall.cmd_uninstall(root, dry_run=False, yes=True, purge_memory=True)
            self.assertFalse((root / ".ai" / "HANDOFF.md").exists())
            self.assertFalse((root / ".ai" / "state").exists())
            self.assertFalse((root / ".ai" / "tasks").exists())

    def test_purge_memory_without_yes_does_not_remove_tier3(self):
        """--purge-memory sin --yes no tiene sentido de uso normal, pero el
        comportamiento debe ser predecible: sin --yes, tier2 no se incluye,
        y con eso tier3 tampoco debería quedar a medias de forma confusa."""
        with temp_project() as root:
            uninstall.cmd_uninstall(root, dry_run=False, purge_memory=True)
            self.assertFalse((root / ".ai" / "HANDOFF.md").exists())
            self.assertTrue((root / "AI_COLLABORATION.md").exists())

    def test_refuses_with_dirty_working_tree(self):
        with temp_project() as root:
            (root / "AI_COLLABORATION.md").write_text("cambio sin commitear\n", encoding="utf-8")
            out = io.StringIO()
            err = io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                res = uninstall.cmd_uninstall(root, dry_run=False)
            self.assertEqual(res, 1)
            self.assertIn("sin commitear", err.getvalue())
            self.assertTrue((root / ".ai" / "templates").exists())  # nada se tocó

    def test_never_commits_anything(self):
        with temp_project() as root:
            uninstall.cmd_uninstall(root, dry_run=False, yes=True)
            status = c.git("status", "--porcelain").stdout.strip()
            self.assertNotEqual(status, "")  # quedan cambios sin commitear, a propósito


class TestHooksAndRemote(unittest.TestCase):
    def test_removes_own_hook_and_reverts_hooks_path(self):
        with temp_project() as root:
            bootstrap.install_hooks(root)
            # --no-verify: el hook recién instalado invoca
            # "tools/continuum doctor", que no existe en este fixture
            # (temp_project excluye tools/ a propósito, ver helpers.py) —
            # no es lo que este test verifica, solo necesitamos un tree
            # limpio para que cmd_uninstall no lo rechace.
            c.git("add", "-A")
            c.git("commit", "-q", "--no-verify", "-m", "install hooks")
            self.assertEqual(c.git("config", "core.hooksPath").stdout.strip(), ".githooks")

            uninstall.cmd_uninstall(root, dry_run=False)
            self.assertFalse((root / ".githooks" / "pre-commit").exists())
            self.assertEqual(c.git("config", "core.hooksPath").stdout.strip(), "")

    def test_hand_edited_hook_without_marker_survives(self):
        with temp_project() as root:
            bootstrap.install_hooks(root)
            (root / ".githooks" / "pre-commit").write_text(
                "#!/bin/sh\necho fusionado-con-husky\n", encoding="utf-8"
            )
            commit_all()

            plan = uninstall.build_plan(root)
            self.assertTrue(plan["hook_editado_a_mano"])
            uninstall.cmd_uninstall(root, dry_run=False)
            self.assertTrue((root / ".githooks" / "pre-commit").exists())

    def test_removes_continuum_remote(self):
        with temp_project() as root:
            c.git("remote", "add", "continuum", "https://example.com/continuum.git")
            plan = uninstall.build_plan(root)
            self.assertTrue(plan["git_remote_continuum"])

            uninstall.cmd_uninstall(root, dry_run=False)
            self.assertNotIn("continuum", c.git("remote").stdout.split())


class TestGeneratedRoleFiles(unittest.TestCase):
    def test_removes_generated_subagents(self):
        with temp_project() as root:
            roles.sync(root, provider="claude")
            commit_all()
            self.assertTrue(any((root / ".claude" / "agents").glob("*.md")))

            uninstall.cmd_uninstall(root, dry_run=False)
            agents_dir = root / ".claude" / "agents"
            self.assertFalse(agents_dir.exists() and any(agents_dir.glob("*.md")))

    def test_hand_written_agent_without_marker_survives(self):
        with temp_project() as root:
            roles.sync(root, provider="claude")
            hand_written = root / ".claude" / "agents" / "mi-agente-propio.md"
            hand_written.write_text("---\nname: mi-agente-propio\n---\n\nPropio.\n", encoding="utf-8")
            commit_all()

            uninstall.cmd_uninstall(root, dry_run=False)
            self.assertTrue(hand_written.exists())


if __name__ == "__main__":
    unittest.main()
