"""Tests para _continuum.context."""
from __future__ import annotations

import contextlib
import io
import json
import unittest

from .helpers import temp_project
from _continuum import context


class TestContext(unittest.TestCase):
    def test_build_context_base(self):
        with temp_project() as tmp:
            ctx = context.build_context(tmp)
            self.assertIsNone(ctx["task"])
            self.assertGreater(ctx["startup_tokens"], 0)
            categories = [it["category"] for it in ctx["items"]]
            self.assertIn("mandatory", categories)
            self.assertIn("on_demand", categories)

    def test_build_context_with_valid_task(self):
        with temp_project() as tmp:
            task_dir = tmp / ".ai" / "tasks" / "demo-task"
            task_dir.mkdir(parents=True, exist_ok=True)
            (task_dir / "task.md").write_text("# Demo Task", encoding="utf-8")

            ctx = context.build_context(tmp, task_slug="demo-task")
            self.assertEqual(ctx["task"], "demo-task")
            categories = [it["category"] for it in ctx["items"]]
            self.assertIn("recommended", categories)

    def test_build_context_with_invalid_task_raises(self):
        with temp_project() as tmp:
            with self.assertRaises(ValueError):
                context.build_context(tmp, task_slug="no-existe")

    def test_cmd_context_human_and_why(self):
        with temp_project() as tmp:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                res = context.cmd_context(tmp, show_why=True)
            self.assertEqual(res, 0)
            text = out.getvalue()
            self.assertIn("Contexto Sugerido de Continuum", text)
            self.assertIn("Razón:", text)

    def test_cmd_context_json(self):
        with temp_project() as tmp:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                res = context.cmd_context(tmp, json_output=True)
            self.assertEqual(res, 0)
            data = json.loads(out.getvalue())
            self.assertIn("startup_tokens", data)
            self.assertIn("items", data)

    def test_cmd_tokens_human_and_json(self):
        with temp_project() as tmp:
            out_human = io.StringIO()
            with contextlib.redirect_stdout(out_human):
                res1 = context.cmd_tokens(tmp, json_output=False)
            self.assertEqual(res1, 0)
            self.assertIn("Presupuesto de Tokens de Continuum", out_human.getvalue())

            out_json = io.StringIO()
            with contextlib.redirect_stdout(out_json):
                res2 = context.cmd_tokens(tmp, json_output=True)
            self.assertEqual(res2, 0)
            data = json.loads(out_json.getvalue())
            self.assertIn("startup_tokens", data)
            self.assertIn("mandatory_files", data)


if __name__ == "__main__":
    unittest.main()
