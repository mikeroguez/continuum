"""Tests para _continuum.tasks (subcomandos guided: task current y task resume)."""
from __future__ import annotations

import contextlib
import io
import json
import unittest

from .helpers import temp_project
from _continuum import tasks


class TestTasksGuided(unittest.TestCase):
    def test_task_current_no_tasks(self):
        with temp_project() as tmp:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                res = tasks.current(tmp, json_output=False)
            self.assertEqual(res, 0)
            self.assertIn("No hay tareas activas", out.getvalue())

            out_json = io.StringIO()
            with contextlib.redirect_stdout(out_json):
                res_j = tasks.current(tmp, json_output=True)
            self.assertEqual(res_j, 0)
            data = json.loads(out_json.getvalue())
            self.assertEqual(data["active_count"], 0)
            self.assertIsNone(data["current_task"])

    def test_task_current_single_and_multiple_tasks(self):
        with temp_project() as tmp:
            tasks.start(tmp, "tarea-1", "small", owner="alice")

            out_single = io.StringIO()
            with contextlib.redirect_stdout(out_single):
                res1 = tasks.current(tmp, json_output=False)
            self.assertEqual(res1, 0)
            self.assertIn("Tarea Actual", out_single.getvalue())
            self.assertIn("tarea-1", out_single.getvalue())

            tasks.start(tmp, "tarea-2", "small", owner="bob")

            out_multi = io.StringIO()
            with contextlib.redirect_stdout(out_multi):
                res2 = tasks.current(tmp, json_output=False)
            self.assertEqual(res2, 0)
            self.assertIn("Tareas Activas (2)", out_multi.getvalue())

            out_multi_json = io.StringIO()
            with contextlib.redirect_stdout(out_multi_json):
                res3 = tasks.current(tmp, json_output=True)
            self.assertEqual(res3, 0)
            data_m = json.loads(out_multi_json.getvalue())
            self.assertEqual(data_m["active_count"], 2)
            self.assertIsNone(data_m["current_task"])

    def test_task_resume(self):
        with temp_project() as tmp:
            tasks.start(tmp, "mi-tarea", "medium", owner="alice")

            # 1. Resume con auto-detección (solo 1 tarea activa)
            out_auto = io.StringIO()
            with contextlib.redirect_stdout(out_auto):
                res_auto = tasks.resume(tmp, json_output=False)
            self.assertEqual(res_auto, 0)
            self.assertIn("Retomando Tarea: mi-tarea", out_auto.getvalue())

            # 2. Resume explícito con JSON
            out_json = io.StringIO()
            with contextlib.redirect_stdout(out_json):
                res_j = tasks.resume(tmp, slug="mi-tarea", json_output=True)
            self.assertEqual(res_j, 0)
            data = json.loads(out_json.getvalue())
            self.assertEqual(data["slug"], "mi-tarea")
            self.assertIn("suggested_context", data)

            # 3. Resume de tarea inexistente
            out_err = io.StringIO()
            with contextlib.redirect_stderr(out_err):
                res_err = tasks.resume(tmp, slug="no-existe")
            self.assertEqual(res_err, 1)


if __name__ == "__main__":
    unittest.main()
