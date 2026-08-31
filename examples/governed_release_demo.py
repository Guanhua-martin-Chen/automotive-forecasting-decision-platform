"""Clean-room Approved Run state transition using fabricated run labels."""

from dataclasses import dataclass


@dataclass(frozen=True)
class DraftRun:
    label: str
    qa_passed: bool


class ReleaseGate:
    def __init__(self, approved_label: str):
        self.approved_label = approved_label

    def approve(self, draft: DraftRun, *, explicit_approval: bool) -> bool:
        """Promote only a passing draft with an explicit approval action."""
        if not draft.qa_passed or not explicit_approval:
            return False
        self.approved_label = draft.label
        return True


if __name__ == "__main__":
    gate = ReleaseGate("synthetic-approved-v1")
    print(gate.approve(DraftRun("synthetic-draft-v2", qa_passed=True), explicit_approval=True))
