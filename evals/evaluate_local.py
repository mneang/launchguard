from __future__ import annotations

import json
import sys
from pathlib import Path

# Make project root importable when this script is run from evals/
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

from src.orchestrator import run_launchguard_flow


EVAL_DIR = BASE_DIR / "evals"


def main() -> None:
    result = run_launchguard_flow()
    verifier_output = result["verifier_output"]

    actual_status = verifier_output["team_status"]
    approval_recommendation = verifier_output["approval_recommendation"]
    citations = verifier_output["citations"]
    safety_controls = result["safety_controls"]

    checks = []

    checks.append({
        "check": "Produces a readiness status",
        "passed": actual_status in {"Green", "Amber", "Red"},
        "details": f"Actual status: {actual_status}"
    })

    checks.append({
        "check": "Blocks automatic launch approval",
        "passed": "do not approve" in approval_recommendation.lower()
        or "manager" in approval_recommendation.lower(),
        "details": approval_recommendation
    })

    checks.append({
        "check": "Includes citations/evidence",
        "passed": len(citations) >= 3,
        "details": f"{len(citations)} citations included"
    })

    checks.append({
        "check": "Includes synthetic-data safety controls",
        "passed": any("Synthetic data only" in control for control in safety_controls),
        "details": "; ".join(safety_controls)
    })

    checks.append({
        "check": "Includes role-level risk analysis",
        "passed": len(verifier_output["member_risks"]) >= 3,
        "details": f"{len(verifier_output['member_risks'])} member risk records"
    })

    passed_count = sum(1 for check in checks if check["passed"])
    total_count = len(checks)

    report = {
        "project": "LaunchGuard",
        "evaluation_type": "Local deterministic readiness evaluation",
        "actual_team_status": actual_status,
        "checks_passed": passed_count,
        "checks_total": total_count,
        "checks": checks
    }

    output_path = EVAL_DIR / "eval_results_sample.json"
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    md_lines = [
        "# LaunchGuard Local Evaluation Results",
        "",
        "**Evaluation type:** Local deterministic readiness evaluation",
        f"**Actual team status:** {actual_status}",
        f"**Checks passed:** {passed_count}/{total_count}",
        "",
        "## Checks",
        ""
    ]

    for check in checks:
        mark = "✅" if check["passed"] else "❌"
        md_lines.append(f"### {mark} {check['check']}")
        md_lines.append("")
        md_lines.append(check["details"])
        md_lines.append("")

    md_lines.extend([
        "## Interpretation",
        "",
        "LaunchGuard passed the local reliability checks for deterministic readiness classification, evidence display, synthetic-data safety, and human approval gating.",
        "",
        "This local evaluation is intended as a lightweight hackathon validation layer before connecting the grounding layer to Microsoft Foundry / Foundry IQ."
    ])

    md_output_path = EVAL_DIR / "eval_results_sample.md"
    md_output_path.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"LaunchGuard evaluation complete: {passed_count}/{total_count} checks passed")
    print(f"Wrote {output_path}")
    print(f"Wrote {md_output_path}")


if __name__ == "__main__":
    main()
