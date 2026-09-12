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

    def test_canonical_and_memory_files_are_inlined(self):
        """AI_COLLABORATION.md, estado-dev.md y HANDOFF.md se vuelcan
        completos porque ningún cliente los carga de forma nativa (ADR-012,
        punto 1)."""
        with temp_project() as tmp:
            ctx = context.build_context(tmp)
            by_path = {it["path"]: it for it in ctx["items"]}

            canonical = by_path["AI_COLLABORATION.md"]
            self.assertTrue(canonical["inline"])
            self.assertIn("Protocolo de colaboración", canonical["content"])

            estado = by_path[".ai/state/estado-dev.md"]
            self.assertTrue(estado["inline"])
            self.assertIn("content", estado)

            handoff = by_path[".ai/HANDOFF.md"]
            self.assertTrue(handoff["inline"])
            self.assertIn("content", handoff)

    def test_provider_entrypoints_are_not_inlined(self):
        """CLAUDE.md/AGENTS.md/GEMINI.md/copilot-instructions.md no se
        duplican: el cliente correspondiente ya los descubre nativamente."""
        with temp_project() as tmp:
            ctx = context.build_context(tmp)
            provider_items = [
                it for it in ctx["items"]
                if it["path"] in ("CLAUDE.md", "AGENTS.md", "GEMINI.md", ".github/copilot-instructions.md")
            ]
            self.assertGreater(len(provider_items), 0)
            for it in provider_items:
                self.assertFalse(it["inline"])
                self.assertNotIn("content", it)

    def test_format_human_context_inlines_canonical_content(self):
        with temp_project() as tmp:
            ctx = context.build_context(tmp)
            text = context.format_human_context(ctx)
            self.assertIn("--- AI_COLLABORATION.md (contenido completo) ---", text)
            self.assertIn("--- fin AI_COLLABORATION.md ---", text)
            self.assertIn("Protocolo de colaboración", text)

    def test_format_human_context_marks_provider_files_as_native(self):
        with temp_project() as tmp:
            ctx = context.build_context(tmp)
            text = context.format_human_context(ctx)
            self.assertIn("CLAUDE.md (~", text)
            self.assertIn("cargado nativamente por el cliente", text)
            # Los temas "bajo demanda" no llevan esa nota: nunca la tuvieron.
            on_demand_lines = [
                line for line in text.splitlines()
                if ".ai/state/topics/" in line
            ]
            self.assertTrue(on_demand_lines)
            for line in on_demand_lines:
                self.assertNotIn("cargado nativamente", line)

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
