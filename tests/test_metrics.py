"""Tests para _continuum.metrics."""
from __future__ import annotations

import contextlib
import io
import json
import unittest

from .helpers import temp_project
from _continuum import metrics


class TestMetrics(unittest.TestCase):
    def test_build_snapshot_basic(self):
        with temp_project() as tmp:
            snap = metrics.build_snapshot(tmp)
            self.assertIn("timestamp", snap)
            self.assertIn("git", snap)
            self.assertIn("startup_tokens", snap)
            self.assertIn("memory", snap)
            self.assertIn("tasks", snap)
            self.assertIn("handoff", snap)
            self.assertIn("hooks", snap)
            self.assertGreater(snap["startup_tokens"], 0)
            self.assertIsInstance(snap["memory"]["index_lines"], int)
            self.assertIsInstance(snap["tasks"]["active"], int)

    def test_cmd_snapshot_dry_run_human(self):
        with temp_project() as tmp:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                res = metrics.cmd_snapshot(tmp, dry_run=True, json_output=False)
            self.assertEqual(res, 0)
            text = out.getvalue()
            self.assertIn("Snapshot de métricas locales de Continuum", text)
            self.assertIn("Modo --dry-run", text)

    def test_cmd_snapshot_dry_run_json(self):
        with temp_project() as tmp:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                res = metrics.cmd_snapshot(tmp, dry_run=True, json_output=True)
            self.assertEqual(res, 0)
            data = json.loads(out.getvalue())
            self.assertIn("startup_tokens", data)
            self.assertIn("memory", data)

    def test_cmd_snapshot_no_dry_run(self):
        with temp_project() as tmp:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                res = metrics.cmd_snapshot(tmp, dry_run=False, json_output=False)
            self.assertEqual(res, 0)
            snapshots_dir = tmp / ".ai" / "metrics" / "snapshots"
    def test_topics_over_limit_in_snapshot_and_report(self):
        with temp_project() as tmp:
            topic = tmp / ".ai" / "state" / "topics" / "pesado.md"
            topic.write_text("dato " * 1600 + "\n")
            snap = metrics.build_snapshot(tmp)
            self.assertEqual(len(snap["memory"]["topics_over_limit"]), 1)
            self.assertEqual(snap["memory"]["topics_over_limit"][0]["path"], ".ai/state/topics/pesado.md")

            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                res = metrics.cmd_report(tmp, json_output=False)
            self.assertEqual(res, 0)
            text = out.getvalue()
            self.assertIn("HAY TEMAS SOBRE EL LÍMITE", text)
            self.assertIn(".ai/state/topics/pesado.md", text)
            self.assertIn("continuum compact --topic pesado", text)


if __name__ == "__main__":
    unittest.main()
