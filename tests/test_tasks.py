import unittest

from .helpers import temp_project

from _continuum import tasks  # noqa: E402


class TestTaskLifecycle(unittest.TestCase):
    def test_start_creates_expected_files(self):
        with temp_project() as root:
            code = tasks.start(root, "demo", "medium", "ana")
            self.assertEqual(code, 0)
            task_dir = root / ".ai" / "tasks" / "demo"
            self.assertTrue((task_dir / "task.md").exists())
            self.assertTrue((task_dir / "notes.md").exists())
            self.assertTrue((task_dir / "execution-plan.md").exists())
            self.assertIn("ana", (task_dir / "task.md").read_text())

    def test_start_large_creates_packets_dir(self):
        with temp_project() as root:
            tasks.start(root, "grande", "large", None)
            self.assertTrue((root / ".ai" / "tasks" / "grande" / "packets").is_dir())

    def test_start_twice_fails(self):
        with temp_project() as root:
            tasks.start(root, "demo", "small", None)
            code = tasks.start(root, "demo", "small", None)
            self.assertEqual(code, 1)

    def test_claim_sets_owner(self):
        with temp_project() as root:
            tasks.start(root, "demo", "small", None)
            tasks.claim(root, "demo", "beto")
            content = (root / ".ai" / "tasks" / "demo" / "task.md").read_text()
            self.assertIn("**Owner:** beto", content)

    def test_close_without_handoff_generates_placeholder_and_fails(self):
        with temp_project() as root:
            tasks.start(root, "demo", "small", None)
            code = tasks.close(root, "demo")
            self.assertEqual(code, 1)
            handoff = root / ".ai" / "tasks" / "demo" / "handoff.md"
            self.assertTrue(handoff.exists())
            self.assertIn("{{", handoff.read_text())

    def test_close_with_force_moves_task_despite_placeholder(self):
        with temp_project() as root:
            tasks.start(root, "demo", "small", None)
            code = tasks.close(root, "demo", force=True)
            self.assertEqual(code, 0)
            self.assertFalse((root / ".ai" / "tasks" / "demo").exists())
            self.assertTrue((root / ".ai" / "tasks" / "_closed" / "demo").exists())

    def test_close_with_real_handoff_succeeds(self):
        with temp_project() as root:
            tasks.start(root, "demo", "small", None)
            handoff = root / ".ai" / "tasks" / "demo" / "handoff.md"
            handoff.write_text(
                "Objetivo: probar el cierre.\nDecision: funciona.\n"
                "Siguiente paso: ninguno, es una prueba automatizada.\n"
            )
            code = tasks.close(root, "demo")
            self.assertEqual(code, 0)
            self.assertTrue((root / ".ai" / "tasks" / "_closed" / "demo").exists())

    def test_close_nonexistent_task_fails(self):
        with temp_project() as root:
            self.assertEqual(tasks.close(root, "no-existe"), 1)

    def test_list_reports_active_and_closed(self):
        with temp_project() as root:
            tasks.start(root, "activa", "small", None)
            tasks.start(root, "para-cerrar", "small", None)
            tasks.close(root, "para-cerrar", force=True)
            # list_tasks solo imprime; que no reviente es la validación
            code = tasks.list_tasks(root)
            self.assertEqual(code, 0)
            active = [p.name for p in (root / ".ai" / "tasks").iterdir() if p.is_dir() and p.name != "_closed"]
            self.assertEqual(active, ["activa"])
            closed = [p.name for p in (root / ".ai" / "tasks" / "_closed").iterdir()]
            self.assertEqual(closed, ["para-cerrar"])


if __name__ == "__main__":
    unittest.main()
