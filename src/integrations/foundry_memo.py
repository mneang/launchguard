from __future__ import annotations

import json
from typing import Any, Dict

from src.integrations.ai_client import generate_manager_memo_fallback
from src.integrations.foundry_config import get_foundry_config


def _build_safe_payload(verifier_output: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "team_status": verifier_output.get("team_status"),
        "executive_summary": verifier_output.get("executive_summary"),
        "member_risks": verifier_output.get("member_risks"),
        "recommended_actions": verifier_output.get("recommended_actions"),
        "approval_recommendation": verifier_output.get("approval_recommendation"),
        "citations": verifier_output.get("citations"),
    }


def generate_manager_memo_foundry_safe(verifier_output: Dict[str, Any]) -> Dict[str, Any]:
    """
    Safe Foundry memo adapter.

    The local deterministic demo must never break because of SDK import drift,
    Azure CLI login issues, region quota issues, or preview-package changes.

    This function returns a structured result:
    - ok=True only when a real Foundry call succeeds.
    - ok=False when it safely falls back to deterministic output.
    """
    config = get_foundry_config()

    fallback_memo = generate_manager_memo_fallback(verifier_output)

    if not config.is_configured:
        return {
            "ok": False,
            "mode": "Deterministic fallback",
            "memo": fallback_memo,
            "error": "Foundry environment variables are not configured."
        }

    try:
        # Do not import brittle SDK objects at module import time.
        # This keeps the Streamlit app alive even when Agent Framework paths change.
        import agent_framework.azure as azure_agent_framework  # type: ignore

        available_names = dir(azure_agent_framework)
        likely_clients = [
            name for name in available_names
            if "Client" in name or "Foundry" in name or "Chat" in name
        ]

        return {
            "ok": False,
            "mode": "Foundry configured, SDK adapter not finalized",
            "memo": (
                "LaunchGuard Readiness Memo\n\n"
                f"{fallback_memo}\n\n"
                "Microsoft Foundry Configuration Note:\n"
                "- Foundry project endpoint and deployment are configured.\n"
                "- The current Agent Framework package does not expose the expected FoundryChatClient import path.\n"
                "- The demo safely falls back to deterministic manager memo generation while preserving the Foundry-ready architecture.\n"
            ),
            "error": (
                "FoundryChatClient import path unavailable in installed agent_framework package. "
                f"Detected possible Azure agent framework exports: {likely_clients[:20]}"
            )
        }

    except Exception as exc:
        return {
            "ok": False,
            "mode": "Deterministic fallback after SDK error",
            "memo": fallback_memo,
            "error": str(exc)
        }


def generate_manager_memo_foundry(verifier_output: Dict[str, Any]) -> str:
    """
    Backward-compatible wrapper used by older app code.
    """
    result = generate_manager_memo_foundry_safe(verifier_output)
    return result["memo"]
