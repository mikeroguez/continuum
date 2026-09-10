import importlib.util
import tempfile
import unittest
from pathlib import Path


PILOT = Path(__file__).resolve().parents[1] / "evaluation" / "pilot"


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, PILOT / filename)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


prepare_trial = load_module("prepare_trial", "prepare_trial.py")
verify_trial = load_module("verify_trial", "verify_trial.py")


class EvaluationPilotTests(unittest.TestCase):
    def test_conditions_share_partial_state_and_expose_only_expected_context(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            trials = {
                condition: prepare_trial.prepare(condition, f"pilot-{condition.lower()}-001", root / condition)
                for condition in "ABC"
            }

            self.assertEqual({trial["partial_tree_sha256"] for trial in trials.values()}, {trials["A"]["partial_tree_sha256"]})
            self.assertFalse((root / "A" / "AGENT_GUIDE.md").exists())
            self.assertTrue((root / "B" / "AGENT_GUIDE.md").is_file())
            self.assertFalse((root / "B" / ".ai").exists())
            self.assertTrue((root / "C" / "AI_COLLABORATION.md").is_file())
            self.assertTrue((root / "C" / ".ai" / "HANDOFF.md").is_file())

    def test_acceptance_fails_for_the_frozen_partial_state(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "trial"
            prepare_trial.prepare("A", "pilot-a-002", destination)
            return_code, _duration = verify_trial.run_acceptance(destination, capture_output=True)
            self.assertEqual(return_code, 1)

    def test_acceptance_passes_for_a_valid_solution(self):
        solution = '''def render_report(entries: list[dict[str, object]]) -> str:
    validated = []
    for entry in entries:
        name = entry.get("name")
        amount = entry.get("amount")
        if not isinstance(name, str) or not name or not isinstance(amount, int):
            raise ValueError("entries need a non-empty name and integer amount")
        validated.append((name, amount))
    lines = [f"{name}: {amount}" for name, amount in sorted(validated)]
    lines.append(f"TOTAL: {sum(amount for _name, amount in validated)}")
    return "\\n".join(lines)
'''
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "trial"
            prepare_trial.prepare("C", "pilot-c-003", destination)
            (destination / "reporting.py").write_text(solution)
            return_code, _duration = verify_trial.run_acceptance(destination, capture_output=True)
            self.assertEqual(return_code, 0)


if __name__ == "__main__":
    unittest.main()
