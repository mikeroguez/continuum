import hashlib
import json
import unittest
from pathlib import Path

from .helpers import REPO_ROOT


class TestCopilotIntegrationArtifacts(unittest.TestCase):
    def test_root_and_template_have_required_copilot_artifacts(self):
        for base in (REPO_ROOT, REPO_ROOT / "template"):
            self.assertTrue((base / ".github" / "copilot-instructions.md").exists())
            instructions = base / ".github" / "instructions"
            self.assertEqual(
                sorted(path.name for path in instructions.glob("*.instructions.md")),
                [
                    "continuum-memory.instructions.md",
                    "documentation.instructions.md",
                    "python.instructions.md",
                ],
            )
            self.assertTrue((base / ".github" / "agents").is_dir())

    def test_copilot_instruction_has_current_protocol_fingerprint(self):
        for base in (REPO_ROOT, REPO_ROOT / "template"):
            source = base / "AI_COLLABORATION.md"
            instructions = (base / ".github" / "copilot-instructions.md").read_text()
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            self.assertIn(f"sha256:{digest}", instructions)

    def test_generated_agent_count_matches_active_packs(self):
        for base in (REPO_ROOT, REPO_ROOT / "template"):
            cfg = json.loads((base / ".ai" / "config.json").read_text())
            expected = sum(
                len(list((base / ".ai" / "roles" / pack).glob("*.md")))
                for pack in cfg["roles"]["packs"]
            )
            generated = list((base / ".github" / "agents").glob("*.agent.md"))
            self.assertEqual(len(generated), expected)


if __name__ == "__main__":
    unittest.main()
