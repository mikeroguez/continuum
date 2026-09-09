"""Tests para _continuum.bootstrap.cmd_sync."""
from __future__ import annotations

import contextlib
import io
import json
import unittest

from .helpers import temp_project
from _continuum import bootstrap, common as c


class TestSyncCmd(unittest.TestCase):
    def test_sync_check_incomplete_config(self):
        with temp_project() as tmp:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                res = bootstrap.cmd_sync(tmp, check_only=True)
            self.assertEqual(res, 1)
            text = out.getvalue()
            self.assertIn("INCOMPLETA", text)
            self.assertIn("template_remote", text)

    def test_sync_check_valid_config(self):
        with temp_project() as tmp:
            cfg_path = tmp / ".ai" / "config.json"
            cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
            cfg["template_remote"] = "https://github.com/mikeroguez/continuum.git"
            cfg["template_prefix"] = "template"
            c.write_text(cfg_path, json.dumps(cfg))

            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                res = bootstrap.cmd_sync(tmp, check_only=True)
            self.assertEqual(res, 0)
            self.assertIn("Configuración: ✓ OK", out.getvalue())

    def test_sync_json_output(self):
        with temp_project() as tmp:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                res = bootstrap.cmd_sync(tmp, json_output=True)
            self.assertEqual(res, 1)  # config is incomplete by default in temp_project
            data = json.loads(out.getvalue())
            self.assertFalse(data["valid_config"])
            self.assertIn("pull_command", data)

    def test_sync_apply_fails_on_dirty_tree(self):
        with temp_project() as tmp:
            cfg_path = tmp / ".ai" / "config.json"
            cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
            cfg["template_remote"] = "https://github.com/mikeroguez/continuum.git"
            cfg["template_prefix"] = "template"
            c.write_text(cfg_path, json.dumps(cfg))

            # Dirty tree by editing a file
            (tmp / "dirty.txt").write_text("cambio sucio", encoding="utf-8")

            out_err = io.StringIO()
            with contextlib.redirect_stderr(out_err):
                res = bootstrap.cmd_sync(tmp, apply=True)
            self.assertEqual(res, 1)
            self.assertIn("cambios sin commitear", out_err.getvalue())



if __name__ == "__main__":
    unittest.main()
