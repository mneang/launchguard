from __future__ import annotations

from typing import Any, Dict, List


REQUIRED_EVIDENCE_SOURCES = {
    "ai_launch_policy.md",
    "certification_matrix.md",
    "assessment_rubric.md",
    "workload_guidelines.md",
}


def evaluate_grounding_contract(citations: List[Dict[str, Any]]) -> Dict[str, Any]:
    actual_sources = {
        citation.get("source")
        for citation in citations
        if citation.get("source")
    }

    covered_sources = sorted(REQUIRED_EVIDENCE_SOURCES.intersection(actual_sources))
    missing_sources = sorted(REQUIRED_EVIDENCE_SOURCES - actual_sources)

    coverage_percent = round(
        (len(covered_sources) / len(REQUIRED_EVIDENCE_SOURCES)) * 100
    )

    passed = len(missing_sources) == 0

    return {
        "passed": passed,
        "coverage_percent": coverage_percent,
        "covered_sources": covered_sources,
        "missing_sources": missing_sources,
        "required_sources": sorted(REQUIRED_EVIDENCE_SOURCES),
        "summary": (
            "Grounding contract passed. Required readiness claims are backed by the synthetic evidence package."
            if passed
            else "Grounding contract failed. Green readiness should be blocked until missing evidence is restored."
        ),
    }


def enforce_grounding_on_verdict(verdict: str, grounding_result: Dict[str, Any]) -> str:
    """
    Prevent Green readiness if required evidence sources are missing.
    """
    if verdict == "Green" and not grounding_result["passed"]:
        return "Amber"

    return verdict
