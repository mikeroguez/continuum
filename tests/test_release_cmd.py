"""Tests para _continuum.release."""
from __future__ import annotations

import contextlib
import io
import json
import unittest

from .helpers import temp_project
from _continuum import release


class TestReleaseCmd(unittest.TestCase):
    def test_export_status(self):
        with temp_project() as tmp:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                res = release.cmd_export_status(tmp, json_output=False)
            self.assertEqual(res, 1)  # export branch doesn't exist in temp_project
            self.assertIn("Estado de Rama Export", out.getvalue())

            out_j = io.StringIO()
            with contextlib.redirect_stdout(out_j):
                res_j = release.cmd_export_status(tmp, json_output=True)
            self.assertEqual(res_j, 1)
            data = json.loads(out_j.getvalue())
            self.assertFalse(data["export_branch_exists"])

    def test_export_refresh_dry_run(self):
        with temp_project() as tmp:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                res = release.cmd_export_refresh(tmp, dry_run=True)
            self.assertEqual(res, 0)
            self.assertIn("Plan de Actualización de Rama Export", out.getvalue())

    def test_release_validation_and_dry_run(self):
        with temp_project() as tmp:
            # Invalid SemVer
            out_err = io.StringIO()
            with contextlib.redirect_stdout(out_err):
                res_bad = release.cmd_release(tmp, version="bad-ver", dry_run=True)
            self.assertEqual(res_bad, 1)
            self.assertIn("INVÁLIDO", out_err.getvalue())

            # Valid SemVer via JSON
            (tmp / "CHANGELOG.md").write_text("# Changelog\n\n## v1.0.0\n", encoding="utf-8")
            out_json = io.StringIO()
            with contextlib.redirect_stdout(out_json):
                res_j = release.cmd_release(tmp, version="v1.0.0", dry_run=True, json_output=True)
            self.assertEqual(res_j, 0)
            data = json.loads(out_json.getvalue())
            self.assertTrue(data["valid_semver"])
            self.assertEqual(data["version"], "v1.0.0")

    def test_write_version_updates_root_always(self):
        with temp_project() as tmp:
            release._write_version(tmp, "2.0.0")
            self.assertEqual((tmp / "VERSION").read_text(encoding="utf-8"), "2.0.0\n")

    def test_write_version_skips_template_when_absent(self):
        """Un proyecto consumidor de Continuum no tiene su propia carpeta
        `template/` — `_write_version` no debe crearla."""
        with temp_project() as tmp:
            self.assertFalse((tmp / "template").exists())
            release._write_version(tmp, "2.0.0")
            self.assertFalse((tmp / "template").exists())

    def test_write_version_updates_template_when_present(self):
        with temp_project() as tmp:
            (tmp / "template").mkdir()
            release._write_version(tmp, "2.0.0")
            self.assertEqual(
                (tmp / "template" / "VERSION").read_text(encoding="utf-8"), "2.0.0\n"
            )



if __name__ == "__main__":
    unittest.main()
