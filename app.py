import pandas as pd
import streamlit as st

from src.orchestrator import run_launchguard_flow, run_recovery_sprint_simulation
from src.utils.ui_copy import decision_copy, status_label, confidence_label, recovery_summary, render_recommendation_box, next_actions_for_status, render_recommendation_box, next_actions_for_status
from src.utils.scenarios import list_scenarios
from src.integrations.ai_client import get_runtime_mode, generate_manager_memo_fallback
from src.utils.cockpit import (
    readiness_score,
    risk_distribution,
    top_blockers,
    evidence_coverage,
    build_agent_timeline,
)


st.set_page_config(
    page_title="LaunchGuard",
    page_icon="🚀",
    layout="wide"
)

st.markdown(
    """
    <style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    .hero-card {
        padding: 1.25rem 1.5rem;
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 18px;
        background: rgba(255,255,255,0.035);
        margin-bottom: 1rem;
    }

    .decision-red {
        padding: 1rem 1.25rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 90, 90, 0.45);
        background: rgba(255, 60, 60, 0.10);
    }

    .decision-amber {
        padding: 1rem 1.25rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 190, 60, 0.45);
        background: rgba(255, 190, 60, 0.10);
    }

    .decision-green {
        padding: 1rem 1.25rem;
        border-radius: 16px;
        border: 1px solid rgba(80, 220, 130, 0.45);
        background: rgba(80, 220, 130, 0.10);
    }

    .mini-card {
        padding: 1rem;
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 16px;
        background: rgba(255,255,255,0.03);
        height: 100%;
    }

    .muted {
        opacity: 0.72;
        font-size: 0.95rem;
    }

    .big-status {
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 0.25rem;
    }

    .small-label {
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-size: 0.78rem;
        opacity: 0.70;
        font-weight: 700;
    }

    div[data-testid="stMetric"] {
        padding: 0.7rem 0.8rem;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        background: rgba(255,255,255,0.025);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

runtime = get_runtime_mode()

if "foundry_memo" not in st.session_state:
    st.session_state.foundry_memo = None

if "foundry_error" not in st.session_state:
    st.session_state.foundry_error = None


# -----------------------------
# Scenario selector
# -----------------------------
scenario_options = list_scenarios()

with st.sidebar:
    st.markdown("### Scenario")
    selected_scenario = st.selectbox(
        "Launch scenario",
        scenario_options,
        index=0,
        help="Switch between risk states to test how LaunchGuard responds."
    )

    scenario_takeaways = {
        "Blocked Launch": "High-risk launch request. The system should block approval and explain the blockers.",
        "Recoverable Launch": "Moderate-risk launch request. The system should show a focused recovery path.",
        "Ready With Approval": "Ready launch request. The system should still require manager evidence review."
    }

    st.caption(scenario_takeaways.get(selected_scenario, "Scenario selected."))

# -----------------------------
# Load reasoning flows
# -----------------------------
base = run_launchguard_flow(selected_scenario)
recovery = run_recovery_sprint_simulation(selected_scenario)

launch_request = base["launch_request"]
team_roster = base["team_roster"]
workload_df = base["workload_df"]

base_verifier = base["verifier_output"]
recovery_verifier = recovery["verifier_output"]

base_status = base_verifier["team_status"]
recovery_status = recovery_verifier["team_status"]

base_score = readiness_score(base_verifier["member_risks"])
recovery_score = readiness_score(recovery_verifier["member_risks"])

base_dist = risk_distribution(base_verifier["member_risks"])
recovery_dist = risk_distribution(recovery_verifier["member_risks"])

base_coverage = evidence_coverage(base_verifier["citations"])


def status_class(status: str) -> str:
    if status == "Green":
        return "decision-green"
    if status == "Amber":
        return "decision-amber"
    return "decision-red"


def status_icon(status: str) -> str:
    if status == "Green":
        return "🟢"
    if status == "Amber":
        return "🟠"
    return "🔴"


# -----------------------------
# Sidebar: system status only
# -----------------------------
with st.sidebar:
    st.title("🚀 LaunchGuard")
    st.caption("Manager launch-readiness cockpit")

    st.markdown("### System Status")
    if runtime["status"] == "Configured":
        st.success("Foundry-ready")
    else:
        st.warning("Local fallback mode")
    st.caption(runtime["details"])

    st.divider()

    st.markdown("### Evidence Grounding")
    st.markdown("""
    - `kb_docs/` synthetic policy set
    - Local citation mapping
    - Evidence coverage check
    - Human approval gate
    """)

    with st.expander("Cost-control note"):
        st.write(
            "Live Foundry IQ provisioning was not enabled because the available resource tiers "
            "required a billable Azure AI Search-backed plan. LaunchGuard preserves the grounding "
            "pattern locally with synthetic documents and citation mapping."
        )

    with st.expander("Quality gate"):
        st.write(
            "LaunchGuard includes local and scenario evaluations covering verdict accuracy, "
            "evidence coverage, role-level risk analysis, recovery behavior, and safety controls."
        )
        st.code("./scripts/quality_gate.sh")

    st.divider()

    st.markdown("### Foundry Adapter")
    if runtime["status"] == "Configured":
        if st.button("Prepare grounded memo"):
            from src.integrations.foundry_memo import generate_manager_memo_foundry_safe

            memo_result = generate_manager_memo_foundry_safe(base_verifier)
            st.session_state.foundry_memo = memo_result["memo"]
            st.session_state.foundry_error = memo_result["error"]
    else:
        st.info("Foundry not configured.")

    if st.session_state.foundry_memo:
        st.success("Memo prepared.")
        with st.expander("View memo"):
            st.text_area("Foundry-safe memo", st.session_state.foundry_memo, height=260)

    if st.session_state.foundry_error:
        with st.expander("Technical adapter note"):
            st.code(st.session_state.foundry_error)


# -----------------------------
# Hero
# -----------------------------
st.title("🚀 LaunchGuard")
st.caption("AI launch-readiness cockpit for managers")

st.markdown(
    """
    <div class="hero-card">
        <div class="small-label">Decision question</div>
        <h2 style="margin-bottom:0.35rem;">Should this AI feature team be cleared for launch?</h2>
        <p class="muted">
            LaunchGuard evaluates certification evidence, role readiness, workload pressure, and policy guardrails.
            It gives managers a conservative launch decision, the reason behind it, and the safest next action.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Top decision board
# -----------------------------
left_decision, right_decision = st.columns([1, 1])

with left_decision:
    st.markdown(
        f"""
        <div class="{status_class(base_status)}">
            <div class="small-label">Current launch decision</div>
            <div class="big-status">{status_icon(base_status)} {base_status}</div>
            <p><b>{decision_copy(base_status)["headline"]}</b> {decision_copy(base_status)["body"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right_decision:
    st.markdown(
        f"""
        <div class="{status_class(recovery_status)}">
            <div class="small-label">After recommended actions</div>
            <div class="big-status">{status_icon(recovery_status)} {recovery_status}</div>
            <p><b>{decision_copy(recovery_status)["headline"]}</b> {decision_copy(recovery_status)["body"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("### Launch review summary")

summary_a, summary_b, summary_c = st.columns([1, 1, 1])

with summary_a:
    st.markdown(
        f"""
        <div class="mini-card">
            <div class="small-label">Selected scenario</div>
            <h3>{selected_scenario}</h3>
            <p class="muted">{launch_request["initiative"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with summary_b:
    st.markdown(
        f"""
        <div class="mini-card">
            <div class="small-label">Manager action</div>
            <h3>{decision_copy(base_status)["headline"]}</h3>
            <p class="muted">{decision_copy(base_status)["primary_action"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with summary_c:
    st.markdown(
        f"""
        <div class="mini-card">
            <div class="small-label">Recovery movement</div>
            <h3>{base_status} → {recovery_status}</h3>
            <p class="muted">{recovery_summary(base_status, recovery_status, base_score, recovery_score)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("### Readiness movement")
score_a, score_b, score_c, score_d = st.columns(4)

with score_a:
    st.metric("Initial Score", f"{base_score}/100")

with score_b:
    st.metric("After Actions Score", f"{recovery_score}/100", delta=f"{recovery_score - base_score}")

with score_c:
    st.metric("Red Roles Removed", base_dist["Red"] - recovery_dist["Red"])

with score_d:
    st.metric("Evidence Coverage", f"{base_coverage['coverage_percent']}%")

progress_left, progress_right = st.columns([1, 1])

with progress_left:
    st.caption("Initial readiness score")
    st.progress(base_score / 100)

with progress_right:
    st.caption("After-action readiness score")
    st.progress(recovery_score / 100)

st.markdown("## 🎬 Judge Tour")

tour_1, tour_2, tour_3, tour_4 = st.columns(4)

with tour_1:
    st.markdown("""
    <div class="mini-card">
        <div class="small-label">Step 1</div>
        <b>Choose scenario</b>
        <p class="muted">Blocked, recoverable, or ready launch.</p>
    </div>
    """, unsafe_allow_html=True)

with tour_2:
    st.markdown("""
    <div class="mini-card">
        <div class="small-label">Step 2</div>
        <b>Read verdict</b>
        <p class="muted">Red, Amber, or Green with score.</p>
    </div>
    """, unsafe_allow_html=True)

with tour_3:
    st.markdown("""
    <div class="mini-card">
        <div class="small-label">Step 3</div>
        <b>Inspect recovery</b>
        <p class="muted">See the shortest safe path forward.</p>
    </div>
    """, unsafe_allow_html=True)

with tour_4:
    st.markdown("""
    <div class="mini-card">
        <div class="small-label">Step 4</div>
        <b>Check evidence</b>
        <p class="muted">Citations, guardrails, approval gate.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()


# -----------------------------
# Main command tabs
# -----------------------------
command_tab, agent_tab, evidence_tab, memo_tab, input_tab = st.tabs([
    "🏆 Decision",
    "⚽ Reasoning",
    "🛡️ Evidence",
    "📝 Memo",
    "📦 Data"
])


with command_tab:
    st.markdown("## Launch Decision")

    c1, c2 = st.columns([1, 1])

    with c1:
        st.markdown("### Why this decision was made")
        for blocker in top_blockers(base_verifier["member_risks"]):
            st.markdown(f"- {blocker}")

        st.markdown("### Current recommendation")
        render_recommendation_box(st, base_status, base_verifier["approval_recommendation"])

    with c2:
        st.markdown("### Recommended next actions")
        for action in next_actions_for_status(base_status, recovery["changed_actions"]):
            st.markdown(f"- {action}")

        st.markdown("### After-action recommendation")
        render_recommendation_box(st, recovery_status, recovery_verifier["approval_recommendation"])

    st.markdown("### Role readiness comparison")

    before_df = pd.DataFrame(base_verifier["member_risks"])
    before_df.insert(0, "scenario", "Initial")

    after_df = pd.DataFrame(recovery_verifier["member_risks"])
    after_df.insert(0, "scenario", "After Sprint")

    combined_df = pd.concat([before_df, after_df], ignore_index=True)
    st.dataframe(combined_df, use_container_width=True, hide_index=True)

    st.markdown("### Approval control")
    approval = st.checkbox("I reviewed the evidence and accept this recommendation.")
    if approval:
        st.success("Approval recorded for review only. LaunchGuard does not automatically approve or trigger launch.")


with agent_tab:
    st.markdown("## Agent Trace")
    st.caption("Three specialized agents pass evidence forward. The recovery simulator shows reassessment after targeted actions.")

    st.dataframe(pd.DataFrame(build_agent_timeline()), use_container_width=True, hide_index=True)

    a1, a2, a3 = st.tabs([
        "Requirement Curator",
        "Capacity Planner",
        "Readiness Verifier"
    ])

    with a1:
        req = base["requirement_output"]
        st.write(req["purpose"])
        st.dataframe(pd.DataFrame(req["role_requirements"]), use_container_width=True, hide_index=True)

    with a2:
        cap = base["capacity_output"]
        st.write(cap["purpose"])
        st.dataframe(pd.DataFrame(cap["readiness_plan"]), use_container_width=True, hide_index=True)

    with a3:
        st.write(base_verifier["purpose"])
        st.markdown("### Manager actions")
        for action in base_verifier["recommended_actions"]:
            st.markdown(f"- {action}")

        st.markdown("### Grounded drill questions")
        for item in base_verifier["sample_grounded_drill_questions"]:
            with st.expander(item["question"]):
                st.write(item["expected_answer"])


with evidence_tab:
    st.markdown("## Evidence & Safety")

    e1, e2 = st.columns([1, 1])

    with e1:
        st.markdown("### Evidence coverage")
        st.metric(
            "Required sources covered",
            f"{base_coverage['covered_count']}/{base_coverage['expected_count']}"
        )
        st.progress(base_coverage["coverage_percent"] / 100)

        for source in base_coverage["covered_sources"]:
            st.markdown(f"- ✅ `{source}`")

        for source in base_coverage["missing_sources"]:
            st.markdown(f"- ⚠️ `{source}`")

    with e2:
        st.markdown("### Safety controls")
        for control in base["safety_controls"]:
            st.markdown(f"- {control}")

    st.markdown("### Citation panel")
    for citation in base_verifier["citations"]:
        st.markdown(f"- **{citation['source']}** — {citation['claim']}")


with memo_tab:
    st.markdown("## Manager Memos")

    m1, m2 = st.columns([1, 1])

    with m1:
        st.markdown("### Initial memo")
        memo = generate_manager_memo_fallback(base_verifier)
        st.text_area("Initial readiness memo", memo, height=300)

    with m2:
        st.markdown("### After-action memo")
        recovery_memo = generate_manager_memo_fallback(recovery_verifier)
        st.text_area("After-action memo", recovery_memo, height=300)


with input_tab:
    st.markdown("## Synthetic Inputs")

    st.info("All data is synthetic. No real employee, customer, or confidential company information is used.")

    i1, i2 = st.columns([1, 1])

    with i1:
        st.markdown("### Launch request")
        st.json(launch_request)

    with i2:
        st.markdown("### Team roster")
        st.dataframe(pd.DataFrame(team_roster), use_container_width=True, hide_index=True)

    st.markdown("### Workload signals")
    st.dataframe(workload_df, use_container_width=True, hide_index=True)
