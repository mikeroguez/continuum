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


if __name__ == "__main__":
    unittest.main()
