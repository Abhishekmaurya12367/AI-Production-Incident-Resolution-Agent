from typing import TypedDict, List


class IncidentState(TypedDict, total=False):
    incident: str

    supervisor_plan: str

    evidence: List[str]

    root_cause: str

    proposed_fix: str

    review_result: str

    final_report: str
