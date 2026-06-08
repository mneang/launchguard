from __future__ import annotations

from typing import Dict, List, Any


READY_SCORE_TARGET = 75
RED_SCORE_THRESHOLD = 70
MIN_FOCUS_HOURS = 10
HEALTHY_FOCUS_HOURS = 15
HIGH_MEETING_LOAD = 20


def get_missing_certs(member: Dict[str, Any]) -> List[str]:
    current = set(member.get("current_certs", []))
    required = set(member.get("required_certs", []))
    return sorted(list(required - current))


def classify_member_risk(member: Dict[str, Any], workload: Dict[str, Any]) -> Dict[str, Any]:
    missing_certs = get_missing_certs(member)
    practice_score = int(member.get("practice_score_avg", 0))
    meeting_hours = int(workload.get("meeting_hours_per_week", 0))
    focus_hours = int(workload.get("focus_hours_per_week", 0))

    risk_reasons = []

    if missing_certs:
        risk_reasons.append(f"Missing required certification(s): {', '.join(missing_certs)}")

    if practice_score < RED_SCORE_THRESHOLD:
        risk_reasons.append(f"Practice score {practice_score}% is below the red-risk threshold of {RED_SCORE_THRESHOLD}%")
    elif practice_score < READY_SCORE_TARGET:
        risk_reasons.append(f"Practice score {practice_score}% is below the readiness target of {READY_SCORE_TARGET}%")

    if meeting_hours > HIGH_MEETING_LOAD:
        risk_reasons.append(f"Meeting load is high at {meeting_hours} hours/week")

    if focus_hours < MIN_FOCUS_HOURS:
        risk_reasons.append(f"Focus capacity is low at {focus_hours} hours/week")
    elif focus_hours < HEALTHY_FOCUS_HOURS:
        risk_reasons.append(f"Focus capacity is constrained at {focus_hours} hours/week")

    if practice_score < RED_SCORE_THRESHOLD or focus_hours < MIN_FOCUS_HOURS:
        status = "Red"
    elif missing_certs or practice_score < READY_SCORE_TARGET or focus_hours < HEALTHY_FOCUS_HOURS:
        status = "Amber"
    else:
        status = "Green"

    return {
        "employee_id": member["employee_id"],
        "role": member["role"],
        "status": status,
        "practice_score": practice_score,
        "meeting_hours_per_week": meeting_hours,
        "focus_hours_per_week": focus_hours,
        "missing_certs": missing_certs,
        "risk_reasons": risk_reasons or ["No major readiness blockers detected."]
    }


def classify_team_status(member_risks: List[Dict[str, Any]]) -> str:
    statuses = [risk["status"] for risk in member_risks]

    if "Red" in statuses:
        return "Red"
    if "Amber" in statuses:
        return "Amber"
    return "Green"


def make_recommended_actions(member_risks: List[Dict[str, Any]]) -> List[str]:
    actions = []

    for risk in member_risks:
        employee_id = risk["employee_id"]
        role = risk["role"]

        if risk["status"] == "Red":
            actions.append(
                f"{employee_id} ({role}): protect focus time immediately and run a targeted certification recovery sprint before launch approval."
            )
        elif risk["status"] == "Amber":
            actions.append(
                f"{employee_id} ({role}): complete remaining certification gaps and reassess practice score before final launch review."
            )
        else:
            actions.append(
                f"{employee_id} ({role}): maintain readiness and support team review checkpoints."
            )

    return actions
