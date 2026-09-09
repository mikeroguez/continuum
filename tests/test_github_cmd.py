"""Tests para _continuum.github."""
from __future__ import annotations

import contextlib
import io
import json
import unittest

from unittest.mock import patch

from .helpers import temp_project
from _continuum import github


class TestGithubCmd(unittest.TestCase):
    def test_detect_github_info(self):
        with temp_project() as tmp:
            info = github.detect_github_info(tmp)
            self.assertIn("is_github", info)
            self.assertIn("recommended_rules", info)
            self.assertEqual(len(info["recommended_rules"]), 3)

    @patch("shutil.which", return_value="/usr/bin/gh")
    @patch("subprocess.run")
    def test_detect_github_info_with_gh(self, mock_run, mock_which):
        mock_run.return_value.returncode = 0
        with temp_project() as tmp:
            info = github.detect_github_info(tmp)
            self.assertTrue(info["has_gh_cli"])
            self.assertTrue(info["gh_authenticated"])

    def test_cmd_protect_human_and_apply(self):
        with temp_project() as tmp:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                res = github.cmd_protect(tmp, apply=False, json_output=False)
            self.assertEqual(res, 0)
            self.assertIn("Protección de Repositorio", out.getvalue())
            self.assertIn("Reglas de Protección Recomendadas", out.getvalue())

            out_apply = io.StringIO()
            with contextlib.redirect_stdout(out_apply):
                res_app = github.cmd_protect(tmp, apply=True, json_output=False)
            self.assertEqual(res_app, 0)
            self.assertIn("Modo --apply", out_apply.getvalue())

    def test_cmd_protect_json(self):
        with temp_project() as tmp:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                res = github.cmd_protect(tmp, json_output=True)
            self.assertEqual(res, 0)
            data = json.loads(out.getvalue())
            self.assertIn("is_github", data)
            self.assertIn("has_gh_cli", data)


if __name__ == "__main__":
    unittest.main()
