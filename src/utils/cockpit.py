from __future__ import annotations

from typing import Any, Dict, List


STATUS_POINTS = {
    "Green": 100,
    "Amber": 65,
    "Red": 30,
}


def readiness_score(member_risks: List[Dict[str, Any]]) -> int:
    if not member_risks:
        return 0

    points = [STATUS_POINTS.get(item.get("status", "Red"), 30) for item in member_risks]
    return round(sum(points) / len(points))


def risk_distribution(member_risks: List[Dict[str, Any]]) -> Dict[str, int]:
    dist = {"Green": 0, "Amber": 0, "Red": 0}
    for item in member_risks:
        status = item.get("status", "Red")
        if status in dist:
            dist[status] += 1
    return dist


def top_blockers(member_risks: List[Dict[str, Any]], limit: int = 5) -> List[str]:
    blockers: List[str] = []

    priority = {"Red": 0, "Amber": 1, "Green": 2}
    sorted_risks = sorted(member_risks, key=lambda x: priority.get(x.get("status", "Red"), 0))

    for risk in sorted_risks:
        if risk.get("status") == "Green":
            continue

        employee_id = risk.get("employee_id", "Unknown")
        role = risk.get("role", "Unknown role")

        for reason in risk.get("risk_reasons", []):
            blockers.append(f"{employee_id} ({role}): {reason}")

    return blockers[:limit]


def evidence_coverage(citations: List[Dict[str, Any]]) -> Dict[str, Any]:
    expected_sources = {
        "ai_launch_policy.md",
        "certification_matrix.md",
        "assessment_rubric.md",
        "workload_guidelines.md",
    }

    actual_sources = {item.get("source") for item in citations}
    covered = sorted(list(expected_sources.intersection(actual_sources)))
    missing = sorted(list(expected_sources - actual_sources))

    return {
        "covered_count": len(covered),
        "expected_count": len(expected_sources),
        "covered_sources": covered,
        "missing_sources": missing,
        "coverage_percent": round((len(covered) / len(expected_sources)) * 100)
    }


def build_agent_timeline() -> List[Dict[str, str]]:
    return [
        {
            "step": "1",
            "agent": "Requirement Curator",
            "action": "Maps launch policy and role requirements to each team member.",
            "judge_value": "Accuracy & relevance"
        },
        {
            "step": "2",
            "agent": "Capacity Planner",
            "action": "Uses workload and focus-time signals to build a realistic readiness sprint.",
            "judge_value": "Reasoning & multi-step thinking"
        },
        {
            "step": "3",
            "agent": "Readiness Verifier",
            "action": "Classifies launch status, identifies blockers, and prevents unsafe auto-approval.",
            "judge_value": "Reliability & safety"
        },
        {
            "step": "4",
            "agent": "Recovery Simulator",
            "action": "Shows how targeted actions change readiness without bypassing manager review.",
            "judge_value": "UX, creativity, and safety"
        }
    ]
