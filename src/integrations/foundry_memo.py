from __future__ import annotations

from typing import Any, Dict

from src.integrations.ai_client import generate_manager_memo_fallback
from src.integrations.foundry_config import get_foundry_config


def generate_manager_memo_foundry_safe(verifier_output: Dict[str, Any]) -> Dict[str, Any]:
    """
    Safe Foundry memo adapter.

    The demo must never break because of SDK import drift, Azure CLI login,
    region quota, or preview-package changes.
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
        import agent_framework.azure as azure_agent_framework  # type: ignore

        available_names = dir(azure_agent_framework)
        likely_clients = [
            name for name in available_names
            if "Client" in name or "Foundry" in name or "Chat" in name or "Agent" in name
        ]

        note = (
            "\n\nMicrosoft Foundry readiness note:\n"
            "- Azure AI Foundry project endpoint and deployment are configured.\n"
            "- The app keeps a safe deterministic memo path for reliable demo execution.\n"
            "- Live preview SDK wiring remains optional and isolated from the core workflow."
        )

        return {
            "ok": False,
            "mode": "Foundry configured with safe fallback",
            "memo": fallback_memo + note,
            "error": (
                "Live SDK adapter not invoked. "
                f"Detected Azure Agent Framework exports: {likely_clients[:20]}"
            )
        }

    except Exception as exc:
        return {
            "ok": False,
            "mode": "Deterministic fallback after SDK check",
            "memo": fallback_memo,
            "error": str(exc)
        }


def generate_manager_memo_foundry(verifier_output: Dict[str, Any]) -> str:
    result = generate_manager_memo_foundry_safe(verifier_output)
    return result["memo"]
