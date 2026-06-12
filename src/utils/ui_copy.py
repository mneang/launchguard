from __future__ import annotations

from typing import Dict


def decision_copy(status: str) -> Dict[str, str]:
    if status == "Green":
        return {
            "headline": "Ready for approval review.",
            "body": "Readiness evidence is strong, but human approval is still required.",
            "primary_action": "Review evidence and approve only if launch controls are confirmed.",
            "tone": "success",
        }

    if status == "Amber":
        return {
            "headline": "Hold launch for recovery.",
            "body": "The team can recover, but readiness is not fully proven.",
            "primary_action": "Run the recommended readiness actions and reassess before final approval.",
            "tone": "warning",
        }

    return {
        "headline": "Do not approve launch.",
        "body": "Critical readiness evidence is missing or unsafe.",
        "primary_action": "Escalate blockers, protect focus capacity, and reassess after remediation.",
        "tone": "error",
    }


def status_label(status: str) -> str:
    if status == "Green":
        return "Clear for approval review"
    if status == "Amber":
        return "Recovery required"
    return "Blocked"


def confidence_label(score: int) -> str:
    if score >= 85:
        return "High"
    if score >= 65:
        return "Medium"
    return "Low"


def recovery_summary(initial_status: str, recovery_status: str, initial_score: int, recovery_score: int) -> str:
    if initial_status == "Green":
        return "The team starts in a strong readiness state. LaunchGuard still keeps approval human-controlled."

    if recovery_score > initial_score:
        return (
            f"Recommended actions improve readiness from {initial_status} to {recovery_status} "
            f"and raise the score from {initial_score}/100 to {recovery_score}/100."
        )

    return "Recommended actions preserve readiness without bypassing approval controls."

def render_recommendation_box(st, status: str, message: str) -> None:
    """Render status-aware recommendation guidance."""
    if status == "Green":
        st.success(message)
    elif status == "Amber":
        st.warning(message)
    else:
        st.error(message)


def next_actions_for_status(status: str, recovery_actions: list[str]) -> list[str]:
    """Return manager-native next actions for the selected status."""
    if status == "Green":
        return [
            "Review cited readiness evidence before approval.",
            "Confirm launch controls and rollback ownership.",
            "Record manager approval decision.",
            "Schedule post-launch readiness check-in.",
        ]

    if status == "Amber":
        return [
            "Run the focused readiness sprint before final approval.",
            "Close remaining certification or assessment gaps.",
            "Protect study/focus time for constrained roles.",
            "Reassess readiness after evidence improves.",
        ]

    return recovery_actions

