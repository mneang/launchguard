from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Any

import pandas as pd

from src.utils.scoring import (
    classify_member_risk,
    classify_team_status,
    make_recommended_actions,
)
from src.utils.scenarios import (
    load_scenario,
    scenario_to_workload_df,
    scenario_to_workload_map,
)


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"


SYNTHETIC_CITATIONS = [
    {
        "source": "ai_launch_policy.md",
        "claim": "Launch approval should not be granted when required roles are missing certifications, practice scores are below threshold, focus capacity is insufficient, or evidence is not grounded."
    },
    {
        "source": "certification_matrix.md",
        "claim": "AI Engineer requires AI-102 and Responsible AI Foundations; Platform Engineer requires AZ-204 and Responsible AI Foundations; Product Lead requires Responsible AI Foundations."
    },
    {
        "source": "assessment_rubric.md",
        "claim": "Green, Amber, and Red readiness are determined by certification completion, practice scores, focus capacity, and completeness of evidence."
    },
    {
        "source": "workload_guidelines.md",
        "claim": "More than 20 meeting hours per week indicates high workload; fewer than 10 focus hours per week indicates capacity risk."
    }
]


def load_inputs(scenario_name: str | None = None) -> Dict[str, Any]:
    if scenario_name:
        scenario = load_scenario(scenario_name)
        return {
            "scenario_name": scenario["scenario_name"],
            "launch_request": scenario["launch_request"],
            "team_roster": scenario["team_roster"],
            "workload_by_employee": scenario_to_workload_map(scenario),
            "workload_df": scenario_to_workload_df(scenario),
        }

    with open(DATA_DIR / "launch_request.json", "r", encoding="utf-8") as f:
        launch_request = json.load(f)

    with open(DATA_DIR / "team_roster.json", "r", encoding="utf-8") as f:
        team_roster = json.load(f)

    workload_df = pd.read_csv(DATA_DIR / "workload_signals.csv")
    workload_by_employee = {
        row["employee_id"]: row.to_dict()
        for _, row in workload_df.iterrows()
    }

    return {
        "scenario_name": "Blocked Launch",
        "launch_request": launch_request,
        "team_roster": team_roster,
        "workload_by_employee": workload_by_employee,
        "workload_df": workload_df,
    }


def requirement_curator_agent(launch_request: Dict[str, Any], team_roster: List[Dict[str, Any]]) -> Dict[str, Any]:
    role_requirements = []

    for member in team_roster:
        role_requirements.append({
            "employee_id": member["employee_id"],
            "role": member["role"],
            "required_certs": member.get("required_certs", []),
            "current_certs": member.get("current_certs", []),
            "practice_score_avg": member.get("practice_score_avg"),
            "last_assessment_date": member.get("last_assessment_date"),
        })

    return {
        "agent": "Requirement Curator Agent",
        "purpose": "Extract role-based certification and launch-readiness requirements.",
        "launch_request_id": launch_request["launch_request_id"],
        "initiative": launch_request["initiative"],
        "role_requirements": role_requirements,
        "grounding_status": "Local synthetic policy citations now; Foundry IQ-ready knowledge package is included in kb_docs.",
        "citations": SYNTHETIC_CITATIONS[:3]
    }


def capacity_planner_agent(
    requirement_output: Dict[str, Any],
    workload_by_employee: Dict[str, Any],
) -> Dict[str, Any]:
    readiness_plan = []

    for member in requirement_output["role_requirements"]:
        workload = workload_by_employee.get(member["employee_id"], {})
        focus_hours = int(workload.get("focus_hours_per_week", 0))
        meeting_hours = int(workload.get("meeting_hours_per_week", 0))
        preferred_slot = workload.get("preferred_learning_slot", "Unknown")

        if focus_hours < 10:
            plan = "Create 30-45 minute protected study blocks four times per week and reduce meeting load before launch review."
            intensity = "Recovery"
        elif focus_hours < 15:
            plan = "Create 60 minute protected study blocks three times per week and reassess at the end of Week 1."
            intensity = "Targeted"
        else:
            plan = "Create 60-90 minute study blocks two to three times per week and maintain readiness."
            intensity = "Maintenance"

        readiness_plan.append({
            "employee_id": member["employee_id"],
            "role": member["role"],
            "meeting_hours_per_week": meeting_hours,
            "focus_hours_per_week": focus_hours,
            "preferred_learning_slot": preferred_slot,
            "plan_intensity": intensity,
            "recommended_plan": plan
        })

    return {
        "agent": "Capacity Planner Agent",
        "purpose": "Build a realistic readiness sprint using workload and focus-capacity signals.",
        "readiness_plan": readiness_plan,
        "citations": [SYNTHETIC_CITATIONS[3]]
    }


def readiness_verifier_agent(
    requirement_output: Dict[str, Any],
    capacity_output: Dict[str, Any],
    workload_by_employee: Dict[str, Any],
) -> Dict[str, Any]:
    member_risks = []

    for member in requirement_output["role_requirements"]:
        workload = workload_by_employee.get(member["employee_id"], {})
        risk = classify_member_risk(member, workload)
        member_risks.append(risk)

    team_status = classify_team_status(member_risks)
    recommended_actions = make_recommended_actions(member_risks)

    if team_status == "Green":
        executive_summary = "LaunchGuard classifies the team as Green. Readiness evidence is strong, but manager approval is still required before launch."
        approval_recommendation = "Approve only after manager reviews the cited evidence and confirms launch controls."
    elif team_status == "Amber":
        executive_summary = "LaunchGuard classifies the team as Amber. The team can recover before launch, but readiness is not yet fully proven."
        approval_recommendation = "Do not approve final launch yet. Run the recommended readiness sprint and reassess."
    else:
        executive_summary = "LaunchGuard classifies the team as Red. Launch readiness is blocked by certification, score, or capacity risks."
        approval_recommendation = "Do not approve launch. Escalate blockers and protect learning capacity first."

    return {
        "agent": "Readiness Verifier Agent",
        "purpose": "Verify certification readiness, classify launch risk, and produce a manager-safe verdict.",
        "team_status": team_status,
        "executive_summary": executive_summary,
        "member_risks": member_risks,
        "recommended_actions": recommended_actions,
        "approval_recommendation": approval_recommendation,
        "sample_grounded_drill_questions": [
            {
                "question": "Which required role is currently most at risk for launch readiness?",
                "expected_answer": "The highest-risk role is determined by missing certifications, low practice scores, high meeting load, and low focus capacity."
            },
            {
                "question": "Why should LaunchGuard avoid declaring Green readiness too early?",
                "expected_answer": "Because the readiness rubric requires sufficient certification evidence, practice scores, focus capacity, and manager review before launch approval."
            }
        ],
        "citations": SYNTHETIC_CITATIONS
    }


def run_launchguard_flow(scenario_name: str | None = None) -> Dict[str, Any]:
    inputs = load_inputs(scenario_name=scenario_name)

    requirement_output = requirement_curator_agent(
        launch_request=inputs["launch_request"],
        team_roster=inputs["team_roster"],
    )

    capacity_output = capacity_planner_agent(
        requirement_output=requirement_output,
        workload_by_employee=inputs["workload_by_employee"],
    )

    verifier_output = readiness_verifier_agent(
        requirement_output=requirement_output,
        capacity_output=capacity_output,
        workload_by_employee=inputs["workload_by_employee"],
    )

    return {
        "scenario_name": inputs["scenario_name"],
        "launch_request": inputs["launch_request"],
        "team_roster": inputs["team_roster"],
        "workload_df": inputs["workload_df"],
        "requirement_output": requirement_output,
        "capacity_output": capacity_output,
        "verifier_output": verifier_output,
        "safety_controls": [
            "Synthetic data only",
            "No real employee names, emails, customer records, credentials, or confidential information",
            "Citations required for requirement and readiness claims",
            "Human approval required before any launch readiness decision",
            "Low-confidence or missing-evidence situations should block Green readiness"
        ]
    }


def run_recovery_sprint_simulation(scenario_name: str | None = None) -> Dict[str, Any]:
    inputs = load_inputs(scenario_name=scenario_name)

    improved_team_roster = []
    for member in inputs["team_roster"]:
        updated = dict(member)

        current_certs = set(updated.get("current_certs", []))
        required_certs = set(updated.get("required_certs", []))
        missing_certs = required_certs - current_certs

        if updated.get("practice_score_avg", 0) < 75:
            updated["practice_score_avg"] = min(78, int(updated.get("practice_score_avg", 0)) + 10)

        if updated.get("hours_studied", 0) < 20:
            updated["hours_studied"] = 20

        if "RAI-FOUNDATIONS" in missing_certs:
            current_certs.add("RAI-FOUNDATIONS")

        updated["current_certs"] = sorted(current_certs)
        improved_team_roster.append(updated)

    improved_workload_by_employee = {}
    for employee_id, workload in inputs["workload_by_employee"].items():
        updated_workload = dict(workload)

        if int(updated_workload.get("meeting_hours_per_week", 0)) > 20:
            updated_workload["meeting_hours_per_week"] = 18

        if int(updated_workload.get("focus_hours_per_week", 0)) < 12:
            updated_workload["focus_hours_per_week"] = 12

        improved_workload_by_employee[employee_id] = updated_workload

    requirement_output = requirement_curator_agent(
        launch_request=inputs["launch_request"],
        team_roster=improved_team_roster,
    )

    capacity_output = capacity_planner_agent(
        requirement_output=requirement_output,
        workload_by_employee=improved_workload_by_employee,
    )

    verifier_output = readiness_verifier_agent(
        requirement_output=requirement_output,
        capacity_output=capacity_output,
        workload_by_employee=improved_workload_by_employee,
    )

    return {
        "scenario": "After manager-approved 14-day recovery sprint",
        "changed_actions": [
            "Protected focus time for overloaded team members",
            "Reduced meeting load for high-risk roles",
            "Raised practice scores through targeted certification drills",
            "Completed Responsible AI Foundations where missing",
            "Reassessed launch readiness after recovery actions"
        ],
        "team_roster": improved_team_roster,
        "workload_by_employee": improved_workload_by_employee,
        "requirement_output": requirement_output,
        "capacity_output": capacity_output,
        "verifier_output": verifier_output
    }
