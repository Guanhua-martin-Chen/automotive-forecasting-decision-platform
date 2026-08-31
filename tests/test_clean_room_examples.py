"""Standard-library tests for the public clean-room conceptual examples."""

import importlib.util
from pathlib import Path
import sys
import unittest


EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


def load_example(name: str):
    spec = importlib.util.spec_from_file_location(name, EXAMPLES / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class CleanRoomExampleTests(unittest.TestCase):
    def test_reconciled_detail_equals_control_total(self):
        reconcile = load_example("synthetic_reconciliation").reconcile
        detail = reconcile(101, {"Brand A / Model": 5, "Brand A / PLC": 3, "Brand B / PLC": 2})
        self.assertEqual(sum(detail.values()), 101)

    def test_rolling_origin_training_never_uses_future_observations(self):
        rolling_origins = load_example("rolling_origin_backtest").rolling_origins
        for train, test in rolling_origins(length=8, minimum_history=3, horizon=1):
            self.assertLess(train.stop - 1, test.start)
            self.assertEqual(test.stop - test.start, 1)

    def test_failed_or_unapproved_draft_cannot_replace_approved_run(self):
        release = load_example("governed_release_demo")
        gate = release.ReleaseGate("synthetic-approved-v1")
        self.assertFalse(gate.approve(release.DraftRun("failed-draft", qa_passed=False), explicit_approval=True))
        self.assertFalse(gate.approve(release.DraftRun("unapproved-draft", qa_passed=True), explicit_approval=False))
        self.assertEqual(gate.approved_label, "synthetic-approved-v1")

    def test_explicit_approval_promotes_passing_draft(self):
        release = load_example("governed_release_demo")
        gate = release.ReleaseGate("synthetic-approved-v1")
        self.assertTrue(gate.approve(release.DraftRun("passing-draft", qa_passed=True), explicit_approval=True))
        self.assertEqual(gate.approved_label, "passing-draft")


if __name__ == "__main__":
    unittest.main()
