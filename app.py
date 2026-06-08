import pandas as pd
import streamlit as st

from src.orchestrator import run_launchguard_flow
from src.integrations.ai_client import get_runtime_mode, generate_manager_memo_fallback


st.set_page_config(
    page_title="LaunchGuard",
    page_icon="🚀",
    layout="wide"
)

runtime = get_runtime_mode()

with st.sidebar:
    st.title("🚀 LaunchGuard")
    st.markdown("### Runtime")
    if runtime["status"] == "Configured":
        st.success(runtime["mode"])
    else:
        st.warning(runtime["mode"])

    st.caption(runtime["details"])

    st.divider()

    st.markdown("### Judging Alignment")
    st.markdown("""
    - **Accuracy/Relevance:** enterprise certification readiness
    - **Reasoning:** 3-agent workflow
    - **Reliability:** safety gates + evals
    - **UX:** one clear manager decision
    """)

    st.divider()

    st.markdown("### Microsoft Stack")
    st.markdown("""
    - Microsoft Foundry-ready
    - Foundry IQ grounding planned
    - Microsoft Agent Framework path
    - Synthetic data only
    """)

st.title("🚀 LaunchGuard")
st.caption("A multi-agent reasoning system for internal AI launch certification readiness")

st.markdown("""
## Manager-grade readiness, not a generic study planner

**Question:** Is this internal AI feature team actually certification-ready to launch — and if not, what must be fixed first?

LaunchGuard turns certification progress, workload pressure, and policy evidence into a safe launch-readiness decision.
""")

result = run_launchguard_flow()

launch_request = result["launch_request"]
team_roster = result["team_roster"]
workload_df = result["workload_df"]

top_a, top_b, top_c = st.columns(3)

with top_a:
    st.metric("Initiative", launch_request["initiative"])

with top_b:
    st.metric("Launch Target", launch_request["launch_target_date"])

with top_c:
    st.metric("Synthetic Team Size", len(team_roster))

st.divider()

left, right = st.columns([1, 1])

with left:
    st.subheader("🎯 Launch Request")
    st.json(launch_request)

with right:
    st.subheader("👥 Synthetic Team Roster")
    st.dataframe(pd.DataFrame(team_roster), use_container_width=True)

st.subheader("📅 Synthetic Workload Signals")
st.dataframe(workload_df, use_container_width=True)

st.divider()

st.subheader("⚽ LaunchGuard Agent Flow")

agent_col_1, agent_col_2, agent_col_3 = st.columns(3)

with agent_col_1:
    st.markdown("### 1️⃣ Requirement Curator")
    st.write("Extracts certification and launch-readiness requirements from approved guidance.")

with agent_col_2:
    st.markdown("### 2️⃣ Capacity Planner")
    st.write("Builds a readiness sprint using workload, focus capacity, and practice score signals.")

with agent_col_3:
    st.markdown("### 3️⃣ Readiness Verifier")
    st.write("Checks risk, generates grounded drill questions, and produces a manager-safe verdict.")

st.divider()

if st.button("Run LaunchGuard Readiness Review", type="primary"):
    requirement_output = result["requirement_output"]
    capacity_output = result["capacity_output"]
    verifier_output = result["verifier_output"]

    status = verifier_output["team_status"]

    st.markdown("## Final Readiness Verdict")

    if status == "Green":
        st.success(f"🟢 {status}: Ready only after manager evidence review")
    elif status == "Amber":
        st.warning(f"🟠 {status}: Recoverable, but not launch-ready yet")
    else:
        st.error(f"🔴 {status}: Launch blocked until risks are fixed")

    st.markdown("## 🧠 Agent 1: Requirement Curator Output")
    st.write(requirement_output["purpose"])
    st.dataframe(
        pd.DataFrame(requirement_output["role_requirements"]),
        use_container_width=True
    )

    st.markdown("## 📆 Agent 2: Capacity Planner Output")
    st.write(capacity_output["purpose"])
    st.dataframe(
        pd.DataFrame(capacity_output["readiness_plan"]),
        use_container_width=True
    )

    st.markdown("## 🛡️ Agent 3: Readiness Verifier Output")
    st.write(verifier_output["executive_summary"])
    st.dataframe(
        pd.DataFrame(verifier_output["member_risks"]),
        use_container_width=True
    )

    st.markdown("### Recommended Manager Actions")
    for action in verifier_output["recommended_actions"]:
        st.markdown(f"- {action}")

    st.markdown("## 📝 Manager Readiness Memo")
    memo = generate_manager_memo_fallback(verifier_output)
    st.text_area("Generated memo", memo, height=280)

    st.markdown("### Grounded Drill Questions")
    for item in verifier_output["sample_grounded_drill_questions"]:
        with st.expander(item["question"]):
            st.write(item["expected_answer"])

    st.markdown("## 🧾 Evidence / Citation Panel")
    st.caption("Local synthetic citations now. Next pass: connect these documents through Foundry IQ.")
    for citation in verifier_output["citations"]:
        st.markdown(f"- **{citation['source']}** — {citation['claim']}")

    st.markdown("## ✅ Human Approval Gate")
    st.warning(verifier_output["approval_recommendation"])
    approval = st.checkbox("Manager has reviewed the cited evidence and accepts the readiness recommendation.")
    if approval:
        st.success("Approval recorded for demo purposes. No automatic launch action is performed.")

    st.markdown("## 🔐 Safety Controls")
    for control in result["safety_controls"]:
        st.markdown(f"- {control}")

st.divider()

st.markdown("""
## Judge-facing build notes

| Criterion | LaunchGuard proof |
|---|---|
| **Accuracy & Relevance** | Aligned to enterprise certification readiness and internal team learning |
| **Reasoning** | Three specialized agents pass evidence and context forward |
| **Reliability & Safety** | Synthetic data, citations, human approval, conservative launch blocking |
| **UX & Presentation** | One manager question, one verdict, one memo |
| **Creativity** | Reframes learning agents as AI launch-readiness command systems |
""")
