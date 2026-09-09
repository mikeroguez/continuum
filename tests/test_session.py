"""Tests para _continuum.session y _continuum.handoff (linting)."""
from __future__ import annotations

import contextlib
import io
import json
import unittest

from .helpers import temp_project
from _continuum import handoff, session


class TestSession(unittest.TestCase):
    def test_session_start_basic(self):
        with temp_project() as tmp:
            data = session.build_session_start(tmp)
            self.assertIn("handoff", data)
            self.assertIn("active_tasks", data)
            self.assertIn("suggested_context", data)
            self.assertIn("warnings", data)

            # Test human output
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                res = session.cmd_session_start(tmp, json_output=False)
            self.assertEqual(res, 0)
            self.assertIn("Inicio de Sesión Continuum", out.getvalue())

            # Test JSON output
            out_json = io.StringIO()
            with contextlib.redirect_stdout(out_json):
                res_j = session.cmd_session_start(tmp, json_output=True)
            self.assertEqual(res_j, 0)
            parsed = json.loads(out_json.getvalue())
            self.assertIn("suggested_context", parsed)

    def test_session_end_manual(self):
        with temp_project() as tmp:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                res = session.cmd_session_end(tmp, message="Cierre de sesión de prueba", role="backend")
            self.assertEqual(res, 0)
            handoff_file = tmp / ".ai" / "HANDOFF.md"
            self.assertTrue(handoff_file.exists())
            text = handoff_file.read_text(encoding="utf-8")
            self.assertIn("Cierre de sesión de prueba", text)

    def test_session_end_auto_and_json(self):
        with temp_project() as tmp:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                res = session.cmd_session_end(tmp, auto=True, provider="gemini", role="backend", json_output=True)
            self.assertEqual(res, 0)
            data = json.loads(out.getvalue())
            self.assertEqual(data["status"], "ok")
            self.assertTrue(data["auto"])

    def test_lint_handoff_warnings(self):
        with temp_project() as tmp:
            handoff_path = tmp / ".ai" / "HANDOFF.md"

            # Case 1: missing handoff
            if handoff_path.exists():
                handoff_path.unlink()
            warnings = handoff.lint_handoff(tmp)
            self.assertTrue(any("No existe" in w for w in warnings))

            # Case 2: placeholder present
            handoff_path.write_text("# Handoff\n\n_(completar manualmente)_\n", encoding="utf-8")
            warnings = handoff.lint_handoff(tmp)
            self.assertTrue(any("_(completar manualmente)_" in w for w in warnings))

            # Case 3: excess tokens
            large_text = "# Handoff\n\n" + ("palabras " * 1500)
            handoff_path.write_text(large_text, encoding="utf-8")
            warnings = handoff.lint_handoff(tmp)
            self.assertTrue(any("límite recomendado" in w for w in warnings))


if __name__ == "__main__":
    unittest.main()
