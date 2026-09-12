"""Tests para _continuum.adr — ADR-012, punto 3 (extensión opcional sobre
la verificación de numeración de doctor)."""
from __future__ import annotations

import unittest
from unittest.mock import patch

from .helpers import commit_all, temp_project

from _continuum import adr


class TestAdrNewFileConvention(unittest.TestCase):
    """Sin docs/decision-log.md ni docs/architecture/ previos, `adr new` usa
    la convención de archivo por ADR (AI_COLLABORATION.md §5) — la que
    recomienda la plantilla a un proyecto que la instala por primera vez."""

    def test_first_adr_gets_number_one(self):
        with temp_project() as root:
            code = adr.new(root, "No usar orquestación entre agentes")
            self.assertEqual(code, 0)
            fpath = root / "docs" / "architecture" / "ADR-0001-no-usar-orquestacion-entre-agentes.md"
            self.assertTrue(fpath.exists())
            text = fpath.read_text(encoding="utf-8")
            self.assertIn("# ADR-0001: No usar orquestación entre agentes", text)
            self.assertIn("## Contexto", text)

    def test_explicit_slug_is_respected(self):
        with temp_project() as root:
            code = adr.new(root, "Segunda decisión de prueba", slug="decision-custom")
            self.assertEqual(code, 0)
            self.assertTrue((root / "docs" / "architecture" / "ADR-0001-decision-custom.md").exists())

    def test_second_adr_increments_from_existing_files(self):
        with temp_project() as root:
            adr.new(root, "Primero")
            code = adr.new(root, "Segundo")
            self.assertEqual(code, 0)
            self.assertTrue(any(
                p.name.startswith("ADR-0002-")
                for p in (root / "docs" / "architecture").glob("*.md")
            ))

    def test_refuses_to_overwrite_existing_file(self):
        """La numeración automática siempre incrementa, así que este choque
        no ocurre en uso secuencial normal — el guard protege una carrera
        real (dos `adr new` casi simultáneos) o un archivo puesto a mano con
        un número que el próximo cálculo todavía no ve. Se fuerza el
        escenario fijando `next_number` para poder probarlo igual."""
        with temp_project() as root:
            arch_dir = root / "docs" / "architecture"
            arch_dir.mkdir(parents=True, exist_ok=True)
            (arch_dir / "ADR-0001-mismo-slug.md").write_text("ya existe")

            with patch.object(adr, "next_number", return_value=1):
                code = adr.new(root, "Choca con el existente", slug="mismo-slug")
            self.assertEqual(code, 1)

    def test_empty_title_is_rejected(self):
        with temp_project() as root:
            code = adr.new(root, "   ")
            self.assertEqual(code, 1)


class TestAdrNewDecisionLogConvention(unittest.TestCase):
    """Con docs/decision-log.md presente (la convención de este mismo
    repositorio autoalojado), `adr new` agrega una sección ahí en vez de
    crear un archivo nuevo."""

    def test_appends_section_with_next_number(self):
        with temp_project() as root:
            decision_log = root / "docs" / "decision-log.md"
            decision_log.parent.mkdir(parents=True, exist_ok=True)
            decision_log.write_text(
                "# Bitácora\n\n## ADR-001 — Primero\n\n**Decisión.** X.\n"
            )
            commit_all()

            code = adr.new(root, "Segunda decisión real")
            self.assertEqual(code, 0)
            text = decision_log.read_text(encoding="utf-8")
            self.assertIn("## ADR-002 — Segunda decisión real", text)
            # No debe haber creado también un archivo bajo la otra convención
            # (el directorio placeholder de la plantilla, con su .gitkeep,
            # puede existir de todas formas).
            arch_dir = root / "docs" / "architecture"
            self.assertEqual(list(arch_dir.glob("ADR-*.md")), [])

    def test_never_reuses_a_number_even_if_referenced_elsewhere(self):
        with temp_project() as root:
            decision_log = root / "docs" / "decision-log.md"
            decision_log.parent.mkdir(parents=True, exist_ok=True)
            decision_log.write_text(
                "# Bitácora\n\n"
                "## ADR-001 — Primero\n\nContenido.\n\n"
                "## ADR-005 — Con huecos antes (002-004 nunca se usaron)\n\nContenido.\n"
            )
            commit_all()

            code = adr.new(root, "Siguiente decisión")
            self.assertEqual(code, 0)
            text = decision_log.read_text(encoding="utf-8")
            self.assertIn("## ADR-006 — Siguiente decisión", text)


class TestAdrNextNumber(unittest.TestCase):
    def test_next_number_combines_both_conventions(self):
        """Si por algún motivo conviven ambas convenciones (p. ej. a medio
        migrar), el siguiente número no repite ninguno de los dos lados —
        mismo criterio que `common.collect_adr_numbers` usa en `doctor`."""
        with temp_project() as root:
            decision_log = root / "docs" / "decision-log.md"
            decision_log.parent.mkdir(parents=True, exist_ok=True)
            decision_log.write_text("# Bitácora\n\n## ADR-001 — Primero\n\nX.\n")

            arch_dir = root / "docs" / "architecture"
            arch_dir.mkdir(parents=True, exist_ok=True)
            (arch_dir / "ADR-0005-suelto.md").write_text("# ADR-0005: Suelto\n")

            self.assertEqual(adr.next_number(root), 6)


if __name__ == "__main__":
    unittest.main()
