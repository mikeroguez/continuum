import json
import unittest

from .helpers import temp_project

from _continuum import roles  # noqa: E402


def _activate_packs(root, packs):
    cfg_path = root / ".ai" / "config.json"
    data = json.loads(cfg_path.read_text())
    data["roles"]["packs"] = packs
    cfg_path.write_text(json.dumps(data))


class TestDiscoverRoles(unittest.TestCase):
    def test_default_pack_is_comun_only(self):
        with temp_project() as root:
            found = roles.discover_roles(root)
            packs = {r["pack"] for r in found}
            self.assertEqual(packs, {"comun"})
            self.assertEqual(len(found), 9)

    def test_activating_a_domain_pack_adds_its_roles(self):
        with temp_project() as root:
            _activate_packs(root, ["comun", "software"])
            found = roles.discover_roles(root)
            slugs = {r["slug"] for r in found}
            self.assertIn("frontend", slugs)
            self.assertIn("orquestador", slugs)

    def test_inactive_pack_roles_are_not_discovered(self):
        with temp_project() as root:
            found = roles.discover_roles(root)  # solo "comun" por defecto
            slugs = {r["slug"] for r in found}
            self.assertNotIn("pedagogo", slugs)  # vive en contenido-educativo

    def test_mandato_is_captured_as_full_paragraph(self):
        with temp_project() as root:
            role = roles.find_role(root, "orquestador")
            self.assertIsNotNone(role)
            self.assertGreater(len(role["mandato"]), 40)
            self.assertNotIn("\n", role["mandato"])


class TestFindRole(unittest.TestCase):
    def test_find_existing_role(self):
        with temp_project() as root:
            role = roles.find_role(root, "legal")
            self.assertEqual(role["pack"], "comun")
            self.assertEqual(role["title"], "Legal")

    def test_find_missing_role_returns_none(self):
        with temp_project() as root:
            self.assertIsNone(roles.find_role(root, "no-existe"))


class TestSync(unittest.TestCase):
    def test_sync_generates_one_subagent_per_active_role(self):
        with temp_project() as root:
            code = roles.sync(root, provider="claude")
            self.assertEqual(code, 0)
            agents_dir = root / ".claude" / "agents"
            generated = sorted(p.stem for p in agents_dir.glob("*.md"))
            expected = sorted(r["slug"] for r in roles.discover_roles(root))
            self.assertEqual(generated, expected)

    def test_generated_subagent_has_valid_frontmatter(self):
        with temp_project() as root:
            roles.sync(root, provider="claude")
            content = (root / ".claude" / "agents" / "qa.md").read_text()
            self.assertTrue(content.startswith("---\nname: qa\n"))
            self.assertIn("description:", content)
            self.assertIn('Eres el rol "QA', content)

    def test_sync_generates_copilot_agents(self):
        with temp_project() as root:
            code = roles.sync(root, provider="copilot")
            self.assertEqual(code, 0)
            agents_dir = root / ".github" / "agents"
            generated = sorted(p.name for p in agents_dir.glob("*.agent.md"))
            expected = sorted(f"{r['slug']}.agent.md" for r in roles.discover_roles(root))
            self.assertEqual(generated, expected)

    def test_generated_copilot_agent_has_valid_frontmatter(self):
        with temp_project() as root:
            roles.sync(root, provider="copilot")
            content = (root / ".github" / "agents" / "qa.agent.md").read_text()
            self.assertTrue(content.startswith("---\nname: qa\n"))
            self.assertIn("description:", content)
            self.assertIn('Eres el rol "QA', content)

    def test_copilot_sync_is_deterministic(self):
        with temp_project() as root:
            roles.sync(root, provider="copilot")
            first = {
                path.name: path.read_text()
                for path in (root / ".github" / "agents").glob("*.agent.md")
            }
            roles.sync(root, provider="copilot")
            second = {
                path.name: path.read_text()
                for path in (root / ".github" / "agents").glob("*.agent.md")
            }
            self.assertEqual(first, second)
    def test_sync_generates_gemini_skills(self):
        with temp_project() as root:
            code = roles.sync(root, provider="gemini")
            self.assertEqual(code, 0)
            skills_dir = root / ".gemini" / "skills"
            generated = sorted(p.name for p in skills_dir.iterdir() if p.is_dir())
            expected = sorted(r["slug"] for r in roles.discover_roles(root))
            self.assertEqual(generated, expected)
            qa_skill = skills_dir / "qa" / "SKILL.md"
            self.assertTrue(qa_skill.exists())
            content = qa_skill.read_text()
            self.assertTrue(content.startswith("---\nname: qa\n"))
            self.assertIn('Eres el rol "QA', content)

    def test_unsupported_provider_fails_cleanly(self):
        with temp_project() as root:
            code = roles.sync(root, provider="desconocido")
            self.assertEqual(code, 1)
            self.assertFalse((root / ".claude" / "agents").exists())


if __name__ == "__main__":
    unittest.main()
