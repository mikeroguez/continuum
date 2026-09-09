import contextlib
import io
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


if __name__ == "__main__":
    unittest.main()
