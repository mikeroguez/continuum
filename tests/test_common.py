import json
import unittest
from pathlib import Path

from .helpers import temp_project

from _continuum import common as c  # noqa: E402


class TestEstimateTokens(unittest.TestCase):
    def test_counts_words_with_factor(self):
        text = "una dos tres cuatro"
        self.assertEqual(c.estimate_tokens(text), int(4 * 1.3))

    def test_empty_string_is_zero(self):
        self.assertEqual(c.estimate_tokens(""), 0)


class TestReadWriteText(unittest.TestCase):
    def test_round_trip_and_missing_file(self):
        with temp_project(git_init=False) as root:
            target = root / "nuevo" / "archivo.md"
            self.assertEqual(c.read_text(target), "")
            c.write_text(target, "contenido")
            self.assertEqual(c.read_text(target), "contenido")


class TestLoadConfig(unittest.TestCase):
    def test_defaults_when_no_config_file(self):
        with temp_project(git_init=False) as root:
            (root / ".ai" / "config.json").unlink()
            cfg = c.load_config(root)
            self.assertEqual(cfg["estado_dev"]["max_index_lines"], 80)
            self.assertEqual(cfg["providers"], ["claude", "codex", "gemini"])

    def test_partial_override_merges_not_replaces(self):
        with temp_project(git_init=False) as root:
            cfg_path = root / ".ai" / "config.json"
            data = json.loads(cfg_path.read_text())
            data["project"] = "mi-proyecto"
            data["estado_dev"]["max_index_lines"] = 40
            cfg_path.write_text(json.dumps(data))

            cfg = c.load_config(root)
            self.assertEqual(cfg["project"], "mi-proyecto")
            self.assertEqual(cfg["estado_dev"]["max_index_lines"], 40)
            # el resto de estado_dev no se pierde por el merge parcial
            self.assertEqual(cfg["estado_dev"]["topics_dir"], ".ai/state/topics")

    def test_malformed_json_falls_back_to_defaults(self):
        with temp_project(git_init=False) as root:
            (root / ".ai" / "config.json").write_text("{ esto no es json")
            cfg = c.load_config(root)
            self.assertEqual(cfg["providers"], ["claude", "codex", "gemini"])


class TestGitHelpers(unittest.TestCase):
    def test_repo_root_matches_temp_project(self):
        with temp_project() as root:
            self.assertEqual(c.repo_root().resolve(), root.resolve())

    def test_is_tracked_false_until_committed(self):
        with temp_project(git_init=True, commit=False) as root:
            f = root / "AI_COLLABORATION.md"
            self.assertFalse(c.is_tracked(f))
            c.git("add", "-A")
            c.git("commit", "-q", "-m", "init")
            self.assertTrue(c.is_tracked(f))


class TestPreCommitHookInstalled(unittest.TestCase):
    def test_false_without_hook(self):
        with temp_project() as root:
            self.assertFalse(c.pre_commit_hook_installed(root))

    def test_true_with_default_git_hooks_path(self):
        with temp_project() as root:
            hook = root / ".git" / "hooks" / "pre-commit"
            hook.write_text("#!/bin/sh\ncontinuum doctor --quiet\n")
            hook.chmod(0o755)
            self.assertTrue(c.pre_commit_hook_installed(root))

    def test_true_with_custom_core_hooks_path(self):
        # Regresión: antes solo se miraba `.git/hooks/pre-commit`, así que
        # un hook instalado vía `core.hooksPath` (como hace
        # `bootstrap.install_hooks`, en `.githooks/`) se reportaba como "no
        # instalado" aunque git sí lo fuera a ejecutar.
        with temp_project() as root:
            hooks_dir = root / ".githooks"
            hooks_dir.mkdir(exist_ok=True)
            hook = hooks_dir / "pre-commit"
            hook.write_text("#!/bin/sh\ncontinuum doctor --quiet\n")
            hook.chmod(0o755)
            c.git("config", "core.hooksPath", ".githooks")

            self.assertTrue(c.pre_commit_hook_installed(root))

    def test_false_when_custom_hooks_path_has_no_matching_content(self):
        with temp_project() as root:
            hooks_dir = root / ".githooks"
            hooks_dir.mkdir(exist_ok=True)
            hook = hooks_dir / "pre-commit"
            hook.write_text("#!/bin/sh\necho otra cosa\n")
            hook.chmod(0o755)
            c.git("config", "core.hooksPath", ".githooks")

            self.assertFalse(c.pre_commit_hook_installed(root))


if __name__ == "__main__":
    unittest.main()
