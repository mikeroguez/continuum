"""Tests para _continuum.status.cmd_version (lectura de VERSION)."""
from __future__ import annotations

import contextlib
import io
import json
import unittest

from .helpers import temp_project
from _continuum import status


class TestVersionCmd(unittest.TestCase):
    def test_reports_version_from_file(self):
        with temp_project() as tmp:
            (tmp / "VERSION").write_text("9.9.9\n", encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                res = status.cmd_version(tmp)
            self.assertEqual(res, 0)
            self.assertIn("9.9.9", out.getvalue())

    def test_json_output(self):
        with temp_project() as tmp:
            (tmp / "VERSION").write_text("9.9.9\n", encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                res = status.cmd_version(tmp, json_output=True)
            self.assertEqual(res, 0)
            self.assertEqual(json.loads(out.getvalue())["version"], "9.9.9")

    def test_missing_version_file_warns_but_does_not_fail(self):
        with temp_project() as tmp:
            version_file = tmp / "VERSION"
            if version_file.exists():
                version_file.unlink()
            out = io.StringIO()
            err = io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                res = status.cmd_version(tmp)
            self.assertEqual(res, 0)
            self.assertIn("Sin archivo VERSION", err.getvalue())


if __name__ == "__main__":
    unittest.main()
