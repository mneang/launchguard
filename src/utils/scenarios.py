from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
SCENARIO_DIR = BASE_DIR / "data" / "scenarios"


SCENARIO_FILES = {
    "Blocked Launch": "blocked_launch.json",
    "Recoverable Launch": "recoverable_launch.json",
    "Ready With Approval": "ready_with_approval.json",
}


def list_scenarios() -> List[str]:
    return list(SCENARIO_FILES.keys())


def load_scenario(name: str) -> Dict[str, Any]:
    if name not in SCENARIO_FILES:
        raise ValueError(f"Unknown scenario: {name}")

    path = SCENARIO_DIR / SCENARIO_FILES[name]
    return json.loads(path.read_text(encoding="utf-8"))


def scenario_to_workload_map(scenario: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {
        row["employee_id"]: row
        for row in scenario["workload_signals"]
    }


def scenario_to_workload_df(scenario: Dict[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(scenario["workload_signals"])
