import contextlib
import io
import unittest

from .helpers import commit_all, temp_project

from _continuum import doctor, tasks  # noqa: E402


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

    def test_missing_copilot_instructions_is_critical(self):
        with temp_project() as root:
            (root / ".github" / "copilot-instructions.md").unlink()
            commit_all()
            code, out = run_quiet(root)
            self.assertEqual(code, 1)
            self.assertIn("copilot: falta .github/copilot-instructions.md", out)

    def test_stale_copilot_instructions_are_critical(self):
        with temp_project() as root:
            source = root / "AI_COLLABORATION.md"
            source.write_text(source.read_text() + "\nCambio de protocolo.\n")
            commit_all()
            code, out = run_quiet(root)
            self.assertEqual(code, 1)
            self.assertIn("está desactualizado", out)

    def test_handoff_with_unresolved_conflict_markers_is_critical(self):
        """ADR-012, punto 2: un handoff con marcadores de conflicto de git
        sin resolver no sirve como contrato de continuidad — reemplaza la
        idea descartada de `.gitattributes merge=ours` (ver
        docs/investigacion-2026.md §10)."""
        with temp_project() as root:
            handoff = root / ".ai" / "HANDOFF.md"
            handoff.write_text(
                "# Handoff\n"
                "<<<<<<< HEAD\n"
                "Objetivo de la rama principal.\n"
                "=======\n"
                "Objetivo de la rama entrante.\n"
                ">>>>>>> feature/otra-tarea\n"
            )
            commit_all()
            code, out = run_quiet(root)
            self.assertEqual(code, 1)
            self.assertIn("marcadores de conflicto de git sin", out)

    def test_adr_duplicate_number_is_critical(self):
        with temp_project() as root:
            decision_log = root / "docs" / "decision-log.md"
            decision_log.parent.mkdir(parents=True, exist_ok=True)
            decision_log.write_text(
                "# Bitácora\n\n"
                "## ADR-001 — Primero\n\nContenido.\n\n"
                "## ADR-002 — Segundo\n\nContenido.\n\n"
                "## ADR-001 — Reutilizado por error\n\nContenido.\n"
            )
            commit_all()
            code, out = run_quiet(root)
            self.assertEqual(code, 1)
            self.assertIn("Número(s) de ADR reutilizado(s): ADR-001", out)

    def test_adr_duplicate_number_across_file_convention_is_critical(self):
        """La convención de archivo por ADR (`docs/architecture/ADR-###-*.md`,
        la que recomienda AI_COLLABORATION.md §5 a un proyecto que instala la
        plantilla) también se verifica, no solo el log único de este
        repositorio autoalojado."""
        with temp_project() as root:
            arch_dir = root / "docs" / "architecture"
            arch_dir.mkdir(parents=True, exist_ok=True)
            (arch_dir / "ADR-0001-primero.md").write_text("# ADR-0001: Primero\n")
            (arch_dir / "ADR-0001-reutilizado.md").write_text("# ADR-0001: Reutilizado por error\n")
            commit_all()
            code, out = run_quiet(root)
            self.assertEqual(code, 1)
            self.assertIn("Número(s) de ADR reutilizado(s): ADR-001", out)


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

    def test_duplicate_under_configured_ignore_path_does_not_warn(self):
        """Vendor con nombre no convencional (p. ej. App/Core/ en vez de
        vendor/) genera N CHANGELOG.md de librerías de terceros -- eso es
        esperado, no un riesgo de divergencia. `.ai/config.json` debe poder
        excluirlo sin tocar el código de doctor."""
        with temp_project() as root:
            nested = root / "app" / "Core" / "alguna-lib" / "CHANGELOG.md"
            nested.parent.mkdir(parents=True, exist_ok=True)
            nested.write_text("v1.0.0")
            (root / "CHANGELOG.md").write_text("changelog del proyecto")

            cfg_path = root / ".ai" / "config.json"
            import json
            cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
            cfg["doctor"] = {"ignore_paths": ["app/Core"]}
            cfg_path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")

            commit_all()
            code, out = run_quiet(root)
            self.assertEqual(code, 0)
            self.assertNotIn("CHANGELOG.md aparece", out)

    def test_duplicate_outside_ignore_path_still_warns(self):
        with temp_project() as root:
            nested = root / "app" / "Core" / "alguna-lib" / "CHANGELOG.md"
            nested.parent.mkdir(parents=True, exist_ok=True)
            nested.write_text("v1.0.0")
            (root / "CHANGELOG.md").write_text("changelog del proyecto")

            cfg_path = root / ".ai" / "config.json"
            import json
            cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
            cfg["doctor"] = {"ignore_paths": ["otra/ruta/que/no/aplica"]}
            cfg_path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")

            commit_all()
            code, out = run_quiet(root)
            self.assertEqual(code, 0)
            self.assertIn("CHANGELOG.md aparece 2 veces", out)

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

    def test_multiple_active_tasks_without_worktree_warns(self):
        with temp_project() as root:
            tasks.start(root, "uno", "small", None)
            tasks.start(root, "dos", "small", None)
            commit_all()
            code, out = run_quiet(root)
            self.assertEqual(code, 0)
            self.assertIn("un solo worktree de git", out)

    def test_single_active_task_does_not_warn_about_worktree(self):
        with temp_project() as root:
            tasks.start(root, "uno", "small", None)
            commit_all()
            code, out = run_quiet(root)
            self.assertEqual(code, 0)
            self.assertNotIn("worktree de git", out)

    def test_adr_gap_warns_but_not_critical(self):
        with temp_project() as root:
            decision_log = root / "docs" / "decision-log.md"
            decision_log.parent.mkdir(parents=True, exist_ok=True)
            decision_log.write_text(
                "# Bitácora\n\n"
                "## ADR-001 — Primero\n\nContenido.\n\n"
                "## ADR-003 — Tercero (el 002 se reservó y no se usó)\n\nContenido.\n"
            )
            commit_all()
            code, out = run_quiet(root)
            self.assertEqual(code, 0)
            self.assertIn("Hueco en la numeración de ADRs: falta(n) ADR-002", out)

    def test_adr_consecutive_numbering_does_not_warn(self):
        with temp_project() as root:
            decision_log = root / "docs" / "decision-log.md"
            decision_log.parent.mkdir(parents=True, exist_ok=True)
            decision_log.write_text(
                "# Bitácora\n\n"
                "## ADR-001 — Primero\n\nContenido.\n\n"
                "## ADR-002 — Segundo\n\nContenido.\n"
            )
            commit_all()
            code, out = run_quiet(root)
            self.assertEqual(code, 0)
    def test_topic_over_token_limit_warns(self):
        with temp_project() as root:
            topic = root / ".ai" / "state" / "topics" / "denso.md"
            # Pocas líneas pero muchas palabras (líneas muy largas) para exceder 1500 tokens
            long_line = "palabra " * 1600 + "\n"
            topic.write_text(long_line)
            commit_all()
            code, out = run_quiet(root)
            self.assertEqual(code, 0)
            self.assertIn("son líneas muy largas, no muchas entradas", out)


if __name__ == "__main__":
    unittest.main()
