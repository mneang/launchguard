# Foundry IQ Cost-Control Decision

LaunchGuard is structured to integrate with Foundry IQ through a synthetic knowledge base in `kb_docs/`.

## Knowledge Base Package

The project includes synthetic documents for:

- AI launch readiness policy
- Certification matrix
- Study guidance
- Readiness assessment rubric
- Workload and learning capacity guidelines
- Manager readiness memo template

## Cost-Control Decision

During setup, the available Foundry IQ resource tiers required a billable Azure AI Search-backed resource. Because this hackathon demo is designed to avoid accidental cloud spend, the live Foundry IQ resource was not provisioned in this environment.

## Why This Is Safe

LaunchGuard keeps the same grounding pattern locally:

- Synthetic documents only
- Evidence/citation panel
- Conservative Green/Amber/Red readiness rules
- Human approval gate
- Evaluation checks for reliability and safety

## Production Path

In a production or approved Azure environment, the `kb_docs/` folder can be uploaded as a Foundry IQ knowledge base and attached to the Requirement Curator and Readiness Verifier agents.
