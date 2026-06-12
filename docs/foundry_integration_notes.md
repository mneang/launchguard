# LaunchGuard Foundry Integration Notes

LaunchGuard is designed for the Microsoft Agents League Reasoning Agents track.

## Current Foundry Status

- Azure AI Foundry project endpoint is configured through `.env`.
- Model deployment name is configured through `.env`.
- The app detects Foundry configuration and displays Foundry-ready mode.
- The deterministic local flow remains the reliable demo fallback.

## Why a Fallback Exists

The installed `agent-framework` package in the Codespaces environment exposes `DurableAIAgentClient` under `agent_framework.azure`, while some quickstart examples reference a different client import path.

LaunchGuard keeps the demo stable by avoiding hard failure when preview SDK import paths differ.

## Planned IQ Grounding

LaunchGuard uses synthetic knowledge documents in `kb_docs/` as the basis for Foundry IQ grounding:

- `ai_launch_policy.md`
- `certification_matrix.md`
- `study_guidance.md`
- `assessment_rubric.md`
- `workload_guidelines.md`
- `manager_memo_template.md`

These documents support grounded readiness claims, role-certification requirements, workload constraints, and manager memo generation.

## Safety Position

LaunchGuard does not auto-approve launch readiness. It requires manager review and uses synthetic data only.
