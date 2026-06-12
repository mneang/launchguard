# LaunchGuard Scenario Evaluation Results

**Evaluation type:** Scenario hardening evaluation
**Checks passed:** 24/24

## Scenario Summary

| Scenario | Expected | Actual | Recovery | Initial Score | Recovery Score | Checks |
|---|---:|---:|---:|---:|---:|---:|
| Blocked Launch | Red | Red | Amber | 65/100 | 77/100 | 8/8 |
| Recoverable Launch | Amber | Amber | Amber | 88/100 | 88/100 | 8/8 |
| Ready With Approval | Green | Green | Green | 100/100 | 100/100 | 8/8 |

## Detailed Checks

### Blocked Launch

- ✅ **Initial verdict matches scenario expectation** — Expected Red, got Red.
- ✅ **Initial readiness score is valid** — Initial score: 65/100.
- ✅ **Recovery score does not regress for risky scenarios** — Initial score: 65/100; recovery score: 77/100.
- ✅ **Role-level risk records are present** — Risk records: 3.
- ✅ **Evidence coverage is strong** — Coverage: 100%.
- ✅ **Approval guidance is present** — Do not approve launch. Escalate blockers and protect learning capacity first.
- ✅ **Synthetic data safety control is present** — Synthetic data only; No real employee names, emails, customer records, credentials, or confidential information; Citations required for requirement and readiness claims; Human approval required before any launch readiness decision; Low-confidence or missing-evidence situations should block Green readiness
- ✅ **Human oversight / approval control is present** — Synthetic data only; No real employee names, emails, customer records, credentials, or confidential information; Citations required for requirement and readiness claims; Human approval required before any launch readiness decision; Low-confidence or missing-evidence situations should block Green readiness

### Recoverable Launch

- ✅ **Initial verdict matches scenario expectation** — Expected Amber, got Amber.
- ✅ **Initial readiness score is valid** — Initial score: 88/100.
- ✅ **Recovery score does not regress for risky scenarios** — Initial score: 88/100; recovery score: 88/100.
- ✅ **Role-level risk records are present** — Risk records: 3.
- ✅ **Evidence coverage is strong** — Coverage: 100%.
- ✅ **Approval guidance is present** — Do not approve final launch yet. Run the recommended readiness sprint and reassess.
- ✅ **Synthetic data safety control is present** — Synthetic data only; No real employee names, emails, customer records, credentials, or confidential information; Citations required for requirement and readiness claims; Human approval required before any launch readiness decision; Low-confidence or missing-evidence situations should block Green readiness
- ✅ **Human oversight / approval control is present** — Synthetic data only; No real employee names, emails, customer records, credentials, or confidential information; Citations required for requirement and readiness claims; Human approval required before any launch readiness decision; Low-confidence or missing-evidence situations should block Green readiness

### Ready With Approval

- ✅ **Initial verdict matches scenario expectation** — Expected Green, got Green.
- ✅ **Initial readiness score is valid** — Initial score: 100/100.
- ✅ **Recovery score does not regress for risky scenarios** — Initial score: 100/100; recovery score: 100/100.
- ✅ **Role-level risk records are present** — Risk records: 3.
- ✅ **Evidence coverage is strong** — Coverage: 100%.
- ✅ **Approval guidance is present** — Approve only after manager reviews the cited evidence and confirms launch controls.
- ✅ **Synthetic data safety control is present** — Synthetic data only; No real employee names, emails, customer records, credentials, or confidential information; Citations required for requirement and readiness claims; Human approval required before any launch readiness decision; Low-confidence or missing-evidence situations should block Green readiness
- ✅ **Human oversight / approval control is present** — Synthetic data only; No real employee names, emails, customer records, credentials, or confidential information; Citations required for requirement and readiness claims; Human approval required before any launch readiness decision; Low-confidence or missing-evidence situations should block Green readiness

## Interpretation

LaunchGuard was evaluated across blocked, recoverable, and ready launch scenarios.
The evaluation checks that verdicts match expectations, evidence coverage is present, role-level risk analysis exists, recovery does not regress risky scenarios, and human oversight remains part of the launch decision.