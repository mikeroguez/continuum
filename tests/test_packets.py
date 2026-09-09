import unittest
from pathlib import Path

from .helpers import temp_project

from _continuum import packets  # noqa: E402


class TestPacketize(unittest.TestCase):
    def test_small_file_is_left_alone(self):
        with temp_project() as root:
            target = root / "chico.txt"
            target.write_text("\n".join(f"linea {i}" for i in range(10)) + "\n")
            code = packets.packetize(root, target, None, chunk_lines=200)
            self.assertEqual(code, 0)
            self.assertFalse((root / ".ai" / "state" / "packets").exists())

    def test_large_file_relative_path_is_resolved(self):
        """Regresión: packetize fallaba con ValueError si se le pasaba una
        ruta relativa (como la arma argparse desde la CLI) en vez de
        absoluta, porque comparaba contra `root` sin resolver primero."""
        with temp_project() as root:
            target = root / "grande.txt"
            target.write_text("\n".join(f"linea {i}" for i in range(500)) + "\n")

            relative = Path("grande.txt")  # cwd ya es root, ver temp_project
            code = packets.packetize(root, relative, None, chunk_lines=200)

            self.assertEqual(code, 0)
            out_dir = root / ".ai" / "state" / "packets"
            chunks = sorted(out_dir.glob("grande.txt__chunk-*.md"))
            self.assertEqual(len(chunks), 3)  # 500 líneas / 200 = 3 fragmentos
            self.assertTrue((out_dir / "grande.txt__index.md").exists())

    def test_packets_with_slug_go_under_task_dir(self):
        with temp_project() as root:
            (root / ".ai" / "tasks" / "mi-tarea").mkdir(parents=True)
            target = root / "grande.txt"
            target.write_text("\n".join(f"linea {i}" for i in range(500)) + "\n")
            packets.packetize(root, target, "mi-tarea", chunk_lines=200)
            out_dir = root / ".ai" / "tasks" / "mi-tarea" / "packets"
            self.assertTrue(out_dir.exists())
            self.assertEqual(len(list(out_dir.glob("*.md"))), 4)  # 3 chunks + índice

    def test_chunk_header_marks_source_and_range(self):
        with temp_project() as root:
            target = root / "grande.txt"
            target.write_text("\n".join(f"linea {i}" for i in range(500)) + "\n")
            packets.packetize(root, target, None, chunk_lines=200)
            first_chunk = root / ".ai" / "state" / "packets" / "grande.txt__chunk-001-of-003.md"
            header = first_chunk.read_text().splitlines()[0]
            self.assertIn("grande.txt", header)
            self.assertIn("líneas 1-200", header)


if __name__ == "__main__":
    unittest.main()
