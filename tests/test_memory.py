import unittest

from .helpers import temp_project

from _continuum import memory  # noqa: E402


LEGACY_ESTADO_DEV = """# Estado de desarrollo — legado

## CAMBIO RECIENTE (2026-08-20): CIERRE — Sprint X
### Cambios
- feature vieja

## 1. Resumen ejecutivo
Proyecto legado de prueba.

## 2. Stack
- PHP, Laravel

## 3. Pendientes
- cosa A
"""


class TestCompact(unittest.TestCase):
    def _topic_with_entries(self, root, n):
        path = root / ".ai" / "state" / "topics" / "pendientes.md"
        entries = "\n\n".join(
            f"## CAMBIO ({2026 - i}-01-{(i % 27) + 1:02d}): cierre {i}\n- item {i}"
            for i in range(n)
        )
        path.write_text(f"# Pendientes\n\n{entries}\n\n## Mayores\n-\n")
        return path

    def test_below_threshold_is_noop(self):
        with temp_project() as root:
            path = self._topic_with_entries(root, 2)
            before = path.read_text()
            code = memory.compact(root, topic="pendientes", keep_last=5)
            self.assertEqual(code, 0)
            self.assertEqual(path.read_text(), before)

    def test_archives_old_entries_keeping_last_n(self):
        with temp_project() as root:
            path = self._topic_with_entries(root, 4)
            code = memory.compact(root, topic="pendientes", keep_last=1)
            self.assertEqual(code, 0)
            content = path.read_text()
            self.assertIn("Historial archivado", content)
            self.assertIn("cierre 0", content)  # el más reciente, se conserva
            self.assertNotIn("cierre 1", content)  # archivado
            archive_dir = root / ".ai" / "state" / "archive"
            archived_files = list(archive_dir.glob("pendientes-*.md"))
            self.assertGreater(len(archived_files), 0)


class TestSplitLegacy(unittest.TestCase):
    def _write_legacy(self, root):
        (root / ".ai" / "state" / "estado-dev.md").write_text(LEGACY_ESTADO_DEV)

    def test_splits_sections_into_topics_and_rewrites_index(self):
        with temp_project() as root:
            self._write_legacy(root)
            code = memory.split_legacy(root)
            self.assertEqual(code, 0)
            topics_dir = root / ".ai" / "state" / "topics"
            self.assertTrue((topics_dir / "stack.md").exists())
            self.assertIn("PHP, Laravel", (topics_dir / "stack.md").read_text())
            index = (root / ".ai" / "state" / "estado-dev.md").read_text()
            self.assertIn("stack.md", index)
            archive = list((root / ".ai" / "state" / "archive").glob("historial-*.md"))
            self.assertEqual(len(archive), 1)

    def test_does_not_overwrite_existing_topic_with_content(self):
        """Regresión: memory-split-legacy pisaba en silencio un tema que ya
        existía con contenido real (p. ej. pendientes.md por defecto de la
        plantilla) en vez de fusionar. Ver docs/decision-log.md ADR-004."""
        with temp_project() as root:
            existing = root / ".ai" / "state" / "topics" / "pendientes.md"
            existing.write_text("# Pendientes (con contenido real ya existente)\n"
                                 "## Mayores\n- cosa importante ya documentada\n")
            self._write_legacy(root)

            code = memory.split_legacy(root)
            self.assertEqual(code, 0)

            merged = existing.read_text()
            self.assertIn("cosa importante ya documentada", merged)
            self.assertIn("cosa A", merged)  # el contenido legado también quedó


if __name__ == "__main__":
    unittest.main()
