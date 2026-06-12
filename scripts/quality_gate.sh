#!/usr/bin/env bash
set -e

echo "Running LaunchGuard quality gate..."

python -m compileall src app.py evals/evaluate_local.py evals/evaluate_scenarios.py
python evals/evaluate_local.py
python evals/evaluate_scenarios.py

echo "LaunchGuard quality gate passed."
