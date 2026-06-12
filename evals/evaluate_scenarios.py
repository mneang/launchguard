from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

from src.orchestrator import run_launchguard_flow, run_recovery_sprint_simulation
from src.utils.cockpit import readiness_score, evidence_coverage
from src.utils.scenarios import list_scenarios


EXPECTED_INITIAL_STATUS = {
    "Blocked Launch": "Red",
    "Recoverable Launch": "Amber",
    "Ready With Approval": "Green",
}


def check(condition: bool, name: str, details: str) -> Dict[str, Any]:
    return {
        "check": name,
        "passed": bool(condition),
        "details": details,
    }


def evaluate_scenario(scenario_name: str) -> Dict[str, Any]:
    base = run_launchguard_flow(scenario_name)
    recovery = run_recovery_sprint_simulation(scenario_name)

    verifier = base["verifier_output"]
    recovery_verifier = recovery["verifier_output"]

    initial_status = verifier["team_status"]
    recovery_status = recovery_verifier["team_status"]

    initial_score = readiness_score(verifier["member_risks"])
    recovery_score = readiness_score(recovery_verifier["member_risks"])

    coverage = evidence_coverage(verifier["citations"])

    expected_status = EXPECTED_INITIAL_STATUS[scenario_name]

    checks: List[Dict[str, Any]] = []

    checks.append(check(
        initial_status == expected_status,
        "Initial verdict matches scenario expectation",
        f"Expected {expected_status}, got {initial_status}."
    ))

    checks.append(check(
        initial_score >= 0 and initial_score <= 100,
        "Initial readiness score is valid",
        f"Initial score: {initial_score}/100."
    ))

    checks.append(check(
        recovery_score >= initial_score or scenario_name == "Ready With Approval",
        "Recovery score does not regress for risky scenarios",
        f"Initial score: {initial_score}/100; recovery score: {recovery_score}/100."
    ))

    checks.append(check(
        len(verifier["member_risks"]) >= 3,
        "Role-level risk records are present",
        f"Risk records: {len(verifier['member_risks'])}."
    ))

    checks.append(check(
        coverage["coverage_percent"] >= 75,
        "Evidence coverage is strong",
        f"Coverage: {coverage['coverage_percent']}%."
    ))

    checks.append(check(
        "approve" in verifier["approval_recommendation"].lower(),
        "Approval guidance is present",
        verifier["approval_recommendation"]
    ))

    checks.append(check(
        any("Synthetic data only" in item for item in base["safety_controls"]),
        "Synthetic data safety control is present",
        "; ".join(base["safety_controls"])
    ))

    checks.append(check(
        "auto" in " ".join(base["safety_controls"]).lower()
        or "approval" in " ".join(base["safety_controls"]).lower(),
        "Human oversight / approval control is present",
        "; ".join(base["safety_controls"])
    ))

    passed = sum(1 for item in checks if item["passed"])

    return {
        "scenario": scenario_name,
        "expected_initial_status": expected_status,
        "actual_initial_status": initial_status,
        "actual_recovery_status": recovery_status,
        "initial_score": initial_score,
        "recovery_score": recovery_score,
        "checks_passed": passed,
        "checks_total": len(checks),
        "checks": checks,
    }


def main() -> None:
    results = [evaluate_scenario(name) for name in list_scenarios()]

    total_passed = sum(result["checks_passed"] for result in results)
    total_checks = sum(result["checks_total"] for result in results)

    report = {
        "project": "LaunchGuard",
        "evaluation_type": "Scenario hardening evaluation",
        "checks_passed": total_passed,
        "checks_total": total_checks,
        "scenarios": results,
    }

    json_path = BASE_DIR / "evals" / "scenario_eval_results.json"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    md_lines = [
        "# LaunchGuard Scenario Evaluation Results",
        "",
        "**Evaluation type:** Scenario hardening evaluation",
        f"**Checks passed:** {total_passed}/{total_checks}",
        "",
        "## Scenario Summary",
        "",
        "| Scenario | Expected | Actual | Recovery | Initial Score | Recovery Score | Checks |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]

    for result in results:
        md_lines.append(
            f"| {result['scenario']} "
            f"| {result['expected_initial_status']} "
            f"| {result['actual_initial_status']} "
            f"| {result['actual_recovery_status']} "
            f"| {result['initial_score']}/100 "
            f"| {result['recovery_score']}/100 "
            f"| {result['checks_passed']}/{result['checks_total']} |"
        )

    md_lines.extend([
        "",
        "## Detailed Checks",
        "",
    ])

    for result in results:
        md_lines.append(f"### {result['scenario']}")
        md_lines.append("")
        for item in result["checks"]:
            mark = "✅" if item["passed"] else "❌"
            md_lines.append(f"- {mark} **{item['check']}** — {item['details']}")
        md_lines.append("")

    md_lines.extend([
        "## Interpretation",
        "",
        "LaunchGuard was evaluated across blocked, recoverable, and ready launch scenarios.",
        "The evaluation checks that verdicts match expectations, evidence coverage is present, role-level risk analysis exists, recovery does not regress risky scenarios, and human oversight remains part of the launch decision.",
    ])

    md_path = BASE_DIR / "evals" / "scenario_eval_results.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"Scenario evaluation complete: {total_passed}/{total_checks} checks passed")
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")

    if total_passed != total_checks:
        raise SystemExit("One or more scenario checks failed.")


if __name__ == "__main__":
    main()
