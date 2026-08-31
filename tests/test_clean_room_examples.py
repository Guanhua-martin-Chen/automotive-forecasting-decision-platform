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
    def test_matrix_reconciliation_matches_model_plc_and_brand_controls(self):
        reconcile_matrix = load_example("synthetic_reconciliation").reconcile_matrix
        brand_control_total = 100.0
        model_control_totals = [55.0, 45.0]
        plc_control_totals = [35.0, 65.0]
        matrix = reconcile_matrix(
            [[4.0, 1.0], [2.0, 3.0]],
            model_control_totals,
            plc_control_totals,
        )
        for row, target in zip(matrix, model_control_totals):
            self.assertAlmostEqual(sum(row), target, places=8)
        for column, target in enumerate(plc_control_totals):
            self.assertAlmostEqual(sum(row[column] for row in matrix), target, places=8)
        self.assertAlmostEqual(sum(sum(row) for row in matrix), brand_control_total, places=8)

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
