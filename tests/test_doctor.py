import contextlib
import io
import unittest

from .helpers import commit_all, temp_project

from _continuum import doctor  # noqa: E402


def run_quiet(root):
    """doctor.ok()/info() van a stdout; doctor.warn()/err() van a stderr
    (ver tools/_continuum/common.py) — hay que capturar ambos para poder
    revisar el mensaje completo en las pruebas."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = doctor.run(root, quiet=True)
    return code, out.getvalue() + err.getvalue()


class TestDoctorHappyPath(unittest.TestCase):
    def test_fresh_project_has_zero_problems(self):
        with temp_project() as root:
            code, _ = run_quiet(root)
            self.assertEqual(code, 0)


class TestDoctorCriticalProblems(unittest.TestCase):
    def test_missing_canonical_file_is_critical(self):
        with temp_project() as root:
            (root / "AI_COLLABORATION.md").unlink()
            code, out = run_quiet(root)
            self.assertEqual(code, 1)
            self.assertIn("Falta AI_COLLABORATION.md", out)

    def test_untracked_entrypoint_is_critical(self):
        # Antes del primer commit, nada está trackeado — es exactamente lo
        # que se vio la primera vez que corrió `continuum doctor` sobre
        # este mismo repositorio (ver .ai/state/archive/handoffs/).
        with temp_project(git_init=True, commit=False) as root:
            code, out = run_quiet(root)
            self.assertEqual(code, 1)
            self.assertIn("no está trackeado en git", out)

    def test_entrypoint_not_referencing_canonical_is_critical(self):
        with temp_project() as root:
            (root / "CLAUDE.md").write_text("Reglas propias, sin relación con nada más.\n")
            commit_all()
            code, out = run_quiet(root)
            self.assertEqual(code, 1)
            self.assertIn("no referencia AI_COLLABORATION.md", out)


class TestDoctorWarnings(unittest.TestCase):
    def test_duplicate_files_warn_but_not_critical(self):
        with temp_project() as root:
            nested = root / "docs" / "estado-dev.md"
            nested.parent.mkdir(parents=True, exist_ok=True)
            nested.write_text("copia vieja")
            commit_all()
            code, out = run_quiet(root)
            self.assertEqual(code, 0)
            self.assertIn("aparece 2 veces", out)

    def test_oversized_index_warns(self):
        with temp_project() as root:
            estado = root / ".ai" / "state" / "estado-dev.md"
            estado.write_text("\n".join(f"línea {i}" for i in range(200)))
            commit_all()
            code, out = run_quiet(root)
            self.assertEqual(code, 0)
            self.assertIn("un índice debería ser corto", out)

    def test_stale_task_without_handoff_warns(self):
        import os
        import time

        with temp_project() as root:
            task_dir = root / ".ai" / "tasks" / "vieja"
            task_dir.mkdir(parents=True)
            task_md = task_dir / "task.md"
            task_md.write_text("# vieja")
            old = time.time() - 20 * 86400
            os.utime(task_md, (old, old))
            commit_all()
            code, out = run_quiet(root)
            self.assertEqual(code, 0)
            self.assertIn("abandonada", out)


if __name__ == "__main__":
    unittest.main()
