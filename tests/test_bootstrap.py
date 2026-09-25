import contextlib
import io
import json
import os
import shutil
import stat
import unittest

from .helpers import TEMPLATE_DIR, temp_project

from _continuum import bootstrap, common as c  # noqa: E402


class TestInstallHooks(unittest.TestCase):
    def test_writes_executable_hook_and_sets_hooks_path(self):
        with temp_project() as root:
            code = bootstrap.install_hooks(root)
            self.assertEqual(code, 0)
            hook = root / ".githooks" / "pre-commit"
            self.assertTrue(hook.exists())
            self.assertTrue(os.stat(hook).st_mode & stat.S_IXUSR)

            result = c.git("config", "core.hooksPath")
            self.assertEqual(result.stdout.strip(), ".githooks")

    def test_hook_actually_runs_on_commit(self):
        # A diferencia del resto de las pruebas, esta necesita el CLI de
        # verdad en disco: el propio hook lo invoca por ruta
        # (`tools/continuum doctor --quiet`), y `temp_project()` no copia
        # `tools/` a propósito (las demás pruebas importan `_continuum`
        # directo desde `template/tools/`, no necesitan la copia).
        with temp_project() as root:
            shutil.copytree(TEMPLATE_DIR / "tools", root / "tools")
            c.git("add", "-A")
            c.git("commit", "-q", "-m", "agrega tools/ para esta prueba")

            bootstrap.install_hooks(root)
            (root / "nuevo.txt").write_text("contenido\n")
            c.git("add", "-A")
            result = c.git("commit", "-q", "-m", "prueba con hook activo")
            self.assertEqual(result.returncode, 0, result.stderr)


class TestSyncTemplateInstructions(unittest.TestCase):
    def test_prints_subtree_commands_with_placeholders_when_unconfigured(self):
        with temp_project() as root:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = bootstrap.sync_template_instructions(root)
            self.assertEqual(code, 0)
            self.assertIn("git subtree pull", buf.getvalue())
            self.assertIn("<url-del-repo-plantilla>", buf.getvalue())

    def test_auto_detects_dot_continuum_prefix(self):
        with temp_project() as root:
            (root / ".continuum").mkdir(parents=True, exist_ok=True)
            # template_prefix no configurado
            cfg = c.load_config(root)
            cfg["template_prefix"] = ""
            cfg["template_remote"] = "https://github.com/mikeroguez/continuum.git"
            (root / ".ai" / "config.json").write_text(json.dumps(cfg))

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = bootstrap.sync_template_instructions(root)
            self.assertEqual(code, 0)
            self.assertIn("--prefix=.continuum", buf.getvalue())


class TestInit(unittest.TestCase):
    def test_init_scaffolds_project_from_dot_continuum(self):
        with temp_project() as root:
            # Simular instalación de .continuum
            dot_continuum = root / ".continuum"
            shutil.copytree(TEMPLATE_DIR, dot_continuum)

            # Limpiar archivos de la raíz para simular un repo nuevo donde solo se hizo git subtree add en .continuum
            for p in list(root.iterdir()):
                if p.name != ".continuum" and p.name != ".git":
                    if p.is_dir():
                        shutil.rmtree(p)
                    else:
                        p.unlink()

            code = bootstrap.init(root)
            self.assertEqual(code, 0)
            self.assertTrue((root / "tools" / "continuum").exists())
            self.assertTrue((root / "AI_COLLABORATION.md").exists())
            self.assertTrue((root / "AGENTS.md").exists())
            self.assertTrue((root / "CLAUDE.md").exists())
            self.assertTrue((root / "GEMINI.md").exists())
            self.assertTrue((root / ".claude" / "settings.json").exists())
            self.assertTrue((root / ".ai" / "config.json").exists())
            self.assertTrue((root / ".ai" / "HANDOFF.md").exists())
            self.assertTrue((root / ".ai" / "state" / "estado-dev.md").exists())

            # Verificar que config.json tiene prefix .continuum
            cfg = c.load_config(root)
            self.assertEqual(cfg["template_prefix"], ".continuum")


class TestClaudeSettingsShape(unittest.TestCase):
    """`.claude/settings.json` no tiene tests unitarios de comportamiento
    (Claude Code interpreta el JSON, no este repo) — esto solo valida que
    el archivo distribuido sea JSON válido y tenga los 3 hooks esperados
    con el comando correcto, para no depender solo de probarlo a mano
    contra un proyecto real cada vez que alguien lo edite."""

    def _load(self):
        return json.loads((TEMPLATE_DIR / ".claude" / "settings.json").read_text(encoding="utf-8"))

    def _hook_command(self, settings: dict, event: str) -> str:
        return settings["hooks"][event][0]["hooks"][0]["command"]

    def test_is_valid_json_with_expected_hook_events(self):
        settings = self._load()
        self.assertIn("SessionStart", settings["hooks"])
        self.assertIn("SessionEnd", settings["hooks"])
        # No PreCompact ni Stop: evitan escrituras en disco a mitad de sesión que rompen Prompt Caching.
        self.assertNotIn("PreCompact", settings["hooks"])
        self.assertNotIn("Stop", settings["hooks"])

    def test_session_start_calls_context_hook_flag(self):
        settings = self._load()
        cmd = self._hook_command(settings, "SessionStart")
        self.assertIn("tools/continuum", cmd)
        self.assertIn("context", cmd)
        self.assertIn("--hook", cmd)

    def test_session_end_calls_handoff_auto(self):
        settings = self._load()
        cmd = self._hook_command(settings, "SessionEnd")
        self.assertIn("handoff --auto", cmd)


if __name__ == "__main__":
    unittest.main()
