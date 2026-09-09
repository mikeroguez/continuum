"""Tests para subcomandos de evidencia e informe de métricas (_continuum.metrics)."""
from __future__ import annotations

import contextlib
import io
import json
import unittest

from .helpers import temp_project
from _continuum import metrics


class TestMetricsEvidence(unittest.TestCase):
    def test_metrics_report(self):
        with temp_project() as tmp:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                res = metrics.cmd_report(tmp, json_output=False)
            self.assertEqual(res, 0)
            self.assertIn("Reporte de Métricas e Impacto de Continuum", out.getvalue())

            out_j = io.StringIO()
            with contextlib.redirect_stdout(out_j):
                res_j = metrics.cmd_report(tmp, json_output=True)
            self.assertEqual(res_j, 0)
            data = json.loads(out_j.getvalue())
            self.assertIn("snapshot", data)

    def test_metrics_export_json_and_csv(self):
        with temp_project() as tmp:
            out_json = io.StringIO()
            with contextlib.redirect_stdout(out_json):
                res1 = metrics.cmd_export(tmp, format_type="json", anonymize=False)
            self.assertEqual(res1, 0)
            data = json.loads(out_json.getvalue())
            self.assertIn("startup_tokens", data)

            out_csv = io.StringIO()
            with contextlib.redirect_stdout(out_csv):
                res2 = metrics.cmd_export(tmp, format_type="csv", anonymize=False)
            self.assertEqual(res2, 0)
            self.assertIn("timestamp,commit,branch", out_csv.getvalue())

    def test_metrics_export_anonymize(self):
        with temp_project() as tmp:
            out_anon = io.StringIO()
            with contextlib.redirect_stdout(out_anon):
                res = metrics.cmd_export(tmp, format_type="json", anonymize=True)
            self.assertEqual(res, 0)
            data = json.loads(out_anon.getvalue())
            self.assertTrue(data["anonymized"])
            self.assertEqual(data["git"]["branch"], "anonymized-branch")

    def test_metrics_compare(self):
        with temp_project() as tmp:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                res = metrics.cmd_compare(tmp, json_output=False)
            self.assertEqual(res, 0)
            self.assertIn("Comparación de Métricas vs Baseline", out.getvalue())

            out_j = io.StringIO()
            with contextlib.redirect_stdout(out_j):
                res_j = metrics.cmd_compare(tmp, json_output=True)
            self.assertEqual(res_j, 0)
            data = json.loads(out_j.getvalue())
            self.assertIn("startup_tokens", data)


if __name__ == "__main__":
    unittest.main()
