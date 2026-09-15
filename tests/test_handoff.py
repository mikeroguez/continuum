import unittest

from .helpers import commit_all, temp_project

from _continuum import handoff  # noqa: E402


class TestHandoffManual(unittest.TestCase):
    def test_write_manual_includes_message(self):
        with temp_project() as root:
            code = handoff.write_manual(root, "Mensaje de prueba.")
            self.assertEqual(code, 0)
            content = (root / ".ai" / "HANDOFF.md").read_text()
            self.assertIn("Mensaje de prueba.", content)
            self.assertNotIn("{{MESSAGE}}", content)

    def test_write_manual_records_role(self):
        with temp_project() as root:
            handoff.write_manual(root, "msg", role="backend")
            content = (root / ".ai" / "HANDOFF.md").read_text()
            self.assertIn("**Rol:** backend", content)

    def test_write_manual_without_role_uses_placeholder(self):
        with temp_project() as root:
            handoff.write_manual(root, "msg")
            content = (root / ".ai" / "HANDOFF.md").read_text()
            self.assertIn("(sin asignar)", content)

    def test_second_call_archives_previous(self):
        with temp_project() as root:
            # La plantilla ya trae un .ai/HANDOFF.md con contenido por
            # defecto — se quita para probar limpiamente el caso "primera
            # vez, nada que archivar todavía".
            (root / ".ai" / "HANDOFF.md").unlink()
            archive_dir = root / ".ai" / "state" / "archive" / "handoffs"

            handoff.write_manual(root, "Primero")
            self.assertFalse(archive_dir.exists())

            handoff.write_manual(root, "Segundo")
            self.assertTrue(archive_dir.exists())
            archived = list(archive_dir.glob("*.md"))
            self.assertEqual(len(archived), 1)
            self.assertIn("Primero", archived[0].read_text())


class TestHandoffAuto(unittest.TestCase):
    def test_auto_reports_uncommitted_changes(self):
        with temp_project() as root:
            (root / "AI_COLLABORATION.md").write_text("cambio de prueba\n", encoding="utf-8")
            code = handoff.write_auto(root, "claude")
            self.assertEqual(code, 0)
            content = (root / ".ai" / "HANDOFF.md").read_text()
            self.assertIn("Proveedor:** claude", content)
            self.assertIn("AI_COLLABORATION.md", content)

    def test_auto_records_role(self):
        with temp_project() as root:
            code = handoff.write_auto(root, "claude", role="qa")
            self.assertEqual(code, 0)
            content = (root / ".ai" / "HANDOFF.md").read_text()
            self.assertIn("Rol:** qa", content)

    def test_auto_records_copilot_provider(self):
        with temp_project() as root:
            code = handoff.write_auto(root, "copilot")
            self.assertEqual(code, 0)
            content = (root / ".ai" / "HANDOFF.md").read_text()
            self.assertIn("Proveedor:** copilot", content)

    def test_auto_on_clean_tree_says_no_changes(self):
        with temp_project() as root:
            # Si se deja el .ai/HANDOFF.md por defecto, write_auto lo
            # archiva antes de leer el status — y ese archivo nuevo hace
            # que el árbol ya no esté "limpio". Se quita y se commitea la
            # baja para probar el caso realmente limpio.
            (root / ".ai" / "HANDOFF.md").unlink()
            commit_all("quita el handoff por defecto")
            handoff.write_auto(root, None)
            content = (root / ".ai" / "HANDOFF.md").read_text()
            self.assertIn("working tree limpio", content)

    def test_auto_carries_forward_objetivo_and_siguiente_paso(self):
        """Si la sesión anterior dejó un handoff manual con Objetivo/
        Siguiente paso reales (la plantilla completada, no el placeholder),
        write_auto no debe reemplazarlos por '(completar manualmente)' —
        debe heredarlos con una nota de que vienen del handoff anterior."""
        with temp_project() as root:
            handoff_path = root / ".ai" / "HANDOFF.md"
            handoff_path.write_text(
                "# Handoff: (general)\n\n"
                "**Fecha:** 2026-09-14 · **Rol:** backend\n\n"
                "## Objetivo\n"
                "Implementar validación de cédula.\n\n"
                "## Archivos modificados\n"
                "- CapturarCedula.tsx\n\n"
                "## Siguiente paso recomendado\n"
                "Probar el flujo con un alumno de prueba y cerrar la tarea.\n",
                encoding="utf-8",
            )
            code = handoff.write_auto(root, "claude")
            self.assertEqual(code, 0)
            new_content = handoff_path.read_text()
            self.assertIn("Implementar validación de cédula.", new_content)
            self.assertIn(
                "Probar el flujo con un alumno de prueba y cerrar la tarea.",
                new_content,
            )
            self.assertIn("Heredado del handoff anterior", new_content)
            self.assertNotIn("_(completar manualmente)_", new_content)

    def test_auto_keeps_placeholder_when_previous_objetivo_was_unfilled(self):
        """Si el handoff anterior nunca se completó (placeholder de la
        plantilla), no hay nada real que heredar — debe seguir pidiendo
        completarlo a mano, no arrastrar el placeholder como si fuera
        contenido real."""
        with temp_project() as root:
            # La plantilla por defecto de temp_project() no trae siquiera
            # un encabezado "## Objetivo" (ver template/.ai/HANDOFF.md) —
            # caso realista de un proyecto recién inicializado.
            handoff.write_auto(root, "claude")
            content = (root / ".ai" / "HANDOFF.md").read_text()
            self.assertIn("_(completar manualmente)_", content)
            self.assertNotIn("Heredado del handoff anterior", content)

    def test_auto_after_auto_does_not_duplicate_carried_note(self):
        """Dos hooks seguidos (p. ej. PreCompact y luego SessionEnd) sin
        edición manual entre medio no deben ir acumulando notas de
        'heredado' en cadena — el segundo write_auto hereda del primero
        tal cual, no envuelve la nota anterior otra vez."""
        with temp_project() as root:
            handoff_path = root / ".ai" / "HANDOFF.md"
            handoff_path.write_text(
                "# Handoff: (general)\n\n"
                "## Objetivo\n"
                "Objetivo real de la tarea.\n\n"
                "## Siguiente paso recomendado\n"
                "Cerrar la tarea.\n",
                encoding="utf-8",
            )
            handoff.write_auto(root, "claude")
            content_after_first = handoff_path.read_text()
            notes_after_first = content_after_first.count("Heredado del handoff anterior")
            self.assertGreater(notes_after_first, 0)

            # Un segundo hook corriendo sin edición manual entre medio debe
            # heredar la MISMA cantidad de notas, no acumularlas.
            handoff.write_auto(root, "claude")
            content_after_second = handoff_path.read_text()
            self.assertEqual(
                content_after_second.count("Heredado del handoff anterior"),
                notes_after_first,
            )
            self.assertIn("Objetivo real de la tarea.", content_after_second)
            self.assertIn("Cerrar la tarea.", content_after_second)


if __name__ == "__main__":
    unittest.main()
