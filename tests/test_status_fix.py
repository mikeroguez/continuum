"""Tests para _continuum.status y _continuum.doctor --fix."""
from __future__ import annotations

import contextlib
import io
import json
import unittest

from .helpers import temp_project
from _continuum import doctor, status


class TestStatusFix(unittest.TestCase):
    def test_cmd_status_human_and_json(self):
        with temp_project() as tmp:
            out_h = io.StringIO()
            with contextlib.redirect_stdout(out_h):
                res1 = status.cmd_status(tmp, json_output=False)
            self.assertEqual(res1, 0)
            self.assertIn("Estado de Continuum", out_h.getvalue())

            out_j = io.StringIO()
            with contextlib.redirect_stdout(out_j):
                res2 = status.cmd_status(tmp, json_output=True)
            self.assertEqual(res2, 0)
            data = json.loads(out_j.getvalue())
            self.assertIn("ready", data)
            self.assertIn("next_action", data)

    def test_doctor_fix_dry_run(self):
        with temp_project() as tmp:
            topics = tmp / ".ai" / "state" / "topics"
            if topics.exists():
                for f in topics.glob("*.md"):
                    f.unlink()
                topics.rmdir()

            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                res = doctor.run_fix(tmp, dry_run=True)
            self.assertEqual(res, 0)
            self.assertIn("Plan de Auto-Reparación Segura", out.getvalue())
            self.assertFalse(topics.exists())

    def test_doctor_fix_no_dry_run_and_idempotency(self):
        with temp_project() as tmp:
            topics = tmp / ".ai" / "state" / "topics"
            if topics.exists():
                for f in topics.glob("*.md"):
                    f.unlink()
                topics.rmdir()

            out1 = io.StringIO()
            with contextlib.redirect_stdout(out1):
                res1 = doctor.run_fix(tmp, dry_run=False)
            self.assertEqual(res1, 0)
            self.assertTrue(topics.exists())

            # Second execution: idempotency check
            out2 = io.StringIO()
            with contextlib.redirect_stdout(out2):
                res2 = doctor.run_fix(tmp, dry_run=False)
            self.assertEqual(res2, 0)
            self.assertIn("No se requieren auto-reparaciones seguras", out2.getvalue())


if __name__ == "__main__":
    unittest.main()
