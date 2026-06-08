from __future__ import annotations

from typing import Any, Dict

from src.integrations.foundry_config import get_foundry_config


def get_runtime_mode() -> Dict[str, Any]:
    config = get_foundry_config()

    if config.is_configured:
        return {
            "mode": "Foundry-ready",
            "status": "Configured",
            "details": "Azure AI Foundry project endpoint and model deployment are present."
        }

    return {
        "mode": "Local deterministic fallback",
        "status": "Not configured",
        "details": "Foundry environment variables are missing. The app still runs using deterministic local logic."
    }


def generate_manager_memo_fallback(verifier_output: Dict[str, Any]) -> str:
    team_status = verifier_output["team_status"]

    lines = [
        "LaunchGuard Readiness Memo",
        "",
        f"Verdict: {team_status}",
        "",
        verifier_output["executive_summary"],
        "",
        "Recommended Manager Actions:"
    ]

    for action in verifier_output["recommended_actions"]:
        lines.append(f"- {action}")

    lines.extend([
        "",
        "Approval Guidance:",
        verifier_output["approval_recommendation"],
        "",
        "Safety Note:",
        "This memo uses synthetic demo data only and does not approve launch automatically."
    ])

    return "\n".join(lines)
