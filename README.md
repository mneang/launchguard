# LaunchGuard

**A multi-agent AI launch-readiness cockpit for managers.**

LaunchGuard helps managers answer one high-stakes question:

> Should this internal AI feature team be cleared for launch, or should approval be blocked until readiness risks are fixed?

Instead of acting like a generic certification planner, LaunchGuard evaluates certification evidence, role readiness, workload pressure, policy grounding, and human approval controls. It returns a conservative **Red / Amber / Green** readiness decision, explains the reason, and recommends the safest next action.

---

## Why It Matters

Internal AI teams are moving fast, but launch readiness can become a loose checklist:

- Did the team complete the right certifications?
- Are practice scores strong enough?
- Does the team have enough focus capacity to recover before launch?
- Is the approval decision grounded in policy evidence?
- Is a human still accountable for the final launch call?

LaunchGuard turns those questions into an auditable manager workflow.

**Goal:** move fast without rubber-stamping unsafe AI launches.

---

## What LaunchGuard Does

- Shows a manager-facing launch-readiness cockpit
- Supports dynamic **Red, Amber, and Green** scenarios
- Runs a multi-agent workflow across requirements, workload, and readiness verification
- Identifies role-level blockers
- Simulates a recovery path and reassesses readiness
- Enforces a grounding contract with synthetic evidence citations
- Keeps launch approval human-controlled
- Exports manager decision memos
- Includes scenario evaluations and a one-command quality gate

---

## System Architecture

<img width="1536" height="1024" alt="System Architecture" src="https://github.com/user-attachments/assets/068dcb26-640e-4328-955d-c6e1404b0e45" />

LaunchGuard routes a manager’s launch request through a cockpit, multi-agent orchestrator, synthetic data, Foundry IQ-ready knowledge package, grounding contract, memo export, and human approval gate.

---

## Demo Scenarios

| Scenario | Verdict | What It Demonstrates |
|---|---:|---|
| Blocked Launch | Red | Blocks unsafe launch when readiness risks are critical |
| Recoverable Launch | Amber | Finds a focused recovery path before final approval |
| Ready With Approval | Green | Recognizes readiness while still requiring manager review |

Even when readiness reaches Green, LaunchGuard does **not** automatically approve launch.

---

## Multi-Agent Workflow

<img width="1536" height="1024" alt="Agent Reasoning Flow" src="https://github.com/user-attachments/assets/d7da9f2e-f182-4f52-b988-f4eb9fd4d183" />

| Agent | Responsibility |
|---|---|
| Requirement Curator Agent | Maps role requirements, certifications, and readiness evidence to each team member |
| Capacity Planner Agent | Uses workload and focus-capacity signals to recommend a realistic readiness plan |
| Readiness Verifier Agent | Classifies the launch as Red, Amber, or Green and explains the blockers |
| Recovery Sprint Simulator | Applies a manager-approved recovery plan and reassesses readiness |

This keeps the system easier to audit than one generic chatbot.

---

## Microsoft Foundry and IQ Strategy

LaunchGuard is built as a **Microsoft Foundry-ready** project.

The app detects Azure AI Foundry configuration through environment variables and includes a Foundry-safe memo adapter path. The repository also includes a **Foundry IQ-ready** synthetic knowledge package in `kb_docs/`.

The knowledge package includes:

- AI launch readiness policy
- Certification matrix
- Study guidance
- Assessment rubric
- Workload guidelines
- Manager memo guidance

In this cost-controlled demo environment, live Foundry IQ provisioning was not enabled because the available resource tiers required a billable Azure AI Search-backed plan. LaunchGuard preserves the grounding pattern locally through synthetic documents, citation mapping, evidence coverage checks, and a grounding contract.

---

## Grounding Contract

LaunchGuard enforces a local grounding contract:

- Required readiness evidence sources must be present
- Evidence coverage is checked
- Readiness claims are tied to synthetic citations
- Green readiness is blocked if required evidence is missing
- Human approval remains required before launch decisions

This makes the system conservative by design.

<img width="1536" height="1024" alt="Grounding Contract and Safety" src="https://github.com/user-attachments/assets/efced2d6-f195-490d-9518-e3021687df12" />

---

## Safety Controls

- Synthetic data only
- No real employee, customer, or confidential data
- No credentials committed to the repo
- Human approval required
- No automatic launch action
- Conservative readiness classification
- Grounding contract enforcement

---

## Evaluation and Quality Gate

Run:

```bash
./scripts/quality_gate.sh
```

The quality gate checks:

- Python compilation
- Local readiness evaluation
- Scenario verdict accuracy
- Role-level risk records
- Evidence coverage
- Grounding contract enforcement
- Human approval guidance
- Synthetic-data safety controls

Evaluation outputs are written to:

```text
evals/scenario_eval_results.json
evals/scenario_eval_results.md
```

---

## How to Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Run the quality gate:

```bash
./scripts/quality_gate.sh
```

---

## Environment Variables

Create a `.env` file from `.env.example`.

```text
AZURE_AI_PROJECT_ENDPOINT=your_foundry_project_endpoint
AZURE_AI_MODEL_DEPLOYMENT=your_model_deployment_name
```

The app remains demoable with deterministic local fallback behavior if live Foundry calls are unavailable.

---

## Repository Map

```text
launchguard/
├── app.py
├── data/
│   └── scenarios/
├── docs/
├── evals/
├── kb_docs/
├── scripts/
└── src/
    ├── orchestrator.py
    ├── integrations/
    └── utils/
```

| Folder | Purpose |
|---|---|
| `src/` | Multi-agent orchestration, scoring, grounding, and integrations |
| `data/` | Synthetic launch scenarios and workload signals |
| `kb_docs/` | Foundry IQ-ready synthetic knowledge package |
| `evals/` | Evaluation scripts and generated reports |
| `docs/` | Architecture, Foundry notes, and repo documentation |
| `scripts/` | Quality gate and diagnostics |

---

## Positioning

LaunchGuard is not a study planner.

It is a launch-readiness command system for internal AI teams.

It helps managers:

1. See whether an AI feature team is launch-ready
2. Understand the exact blockers
3. Review grounded evidence
4. Protect learning and focus capacity
5. Export a decision memo
6. Keep final approval human-controlled

> **Move fast without approving unsafe AI launches.**
