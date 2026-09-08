import json
import os
import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="MarketMind AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PATH CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #f7f8fc;
    }

    .hero {
        padding: 2rem;
        border-radius: 15px;
        background: linear-gradient(135deg, #1f3c88, #4a69bd);
        color: white;
        margin-bottom: 2rem;
    }

    .hero h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }

    .hero p {
        font-size: 1.2rem;
        opacity: 0.9;
    }

    .metric-card {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
    }

    .pipeline-step {
        padding: 10px;
        border-radius: 8px;
        background-color: white;
        margin-bottom: 8px;
        border-left: 4px solid #4a69bd;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("⚙️ Configuration")

    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        help="Enter your OpenAI API key to run MarketMind AI.",
    )

    st.divider()

    st.subheader("Research Pipeline")

    pipeline_steps = [
        "1. Request Analysis",
        "2. Research Planning",
        "3. Research Execution",
        "4. Evidence Analysis",
        "5. Comparison",
        "6. Synthesis",
        "7. Quality Control",
        "8. Report Generation",
    ]

    for step in pipeline_steps:
        st.markdown(
            f"""
            <div class="pipeline-step">
                {step}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    st.caption(
        "MarketMind AI • Multi-Agent Market Research System"
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">
        <h1>📊 MarketMind AI</h1>
        <p>
            AI-Powered Multi-Agent Market Research and
            Competitive Intelligence Platform
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FEATURES
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "AI Agents",
        "8",
        "Specialized Agents",
    )

with col2:
    st.metric(
        "Research Pipeline",
        "8 Steps",
        "Automated",
    )

with col3:
    st.metric(
        "Evidence Analysis",
        "AI Powered",
        "Structured",
    )

with col4:
    st.metric(
        "Output",
        "Market Report",
        "Professional",
    )


st.divider()


# ============================================================
# RESEARCH REQUEST SECTION
# ============================================================

st.subheader("🔍 Start Market Research")

st.write(
    "Describe the market, companies, industry, or competitive "
    "landscape you want MarketMind AI to analyse."
)


user_request = st.text_area(
    "Market Research Request",
    placeholder=(
        "Example: Analyse the global AI customer support market, "
        "identify major competitors, market trends, opportunities, "
        "and potential challenges."
    ),
    height=180,
)


# ============================================================
# RUN BUTTON
# ============================================================

run_research = st.button(
    "🚀 Run Market Research",
    use_container_width=True,
)


# ============================================================
# MAIN RESEARCH FUNCTION
# ============================================================

if run_research:

    if not api_key:

        st.error(
            "Please enter your OpenAI API key in the sidebar."
        )

        st.stop()

    if not user_request.strip():

        st.error(
            "Please enter a market research request."
        )

        st.stop()

    try:

        # Temporarily configure API key
        os.environ["OPENAI_API_KEY"] = api_key

        from src.main import MarketMindOrchestrator

        orchestrator = MarketMindOrchestrator()

        st.divider()

        st.subheader("🤖 AI Research Pipeline")

        progress_bar = st.progress(0)

        status = st.empty()

        pipeline_progress = [
            "Analysing research request...",
            "Creating research plan...",
            "Conducting research...",
            "Analysing evidence...",
            "Comparing entities...",
            "Generating insights...",
            "Performing quality control...",
            "Generating final report...",
        ]

        for index, message in enumerate(pipeline_progress):

            status.info(
                f"Step {index + 1}/8: {message}"
            )

            progress_bar.progress(
                (index + 1) / len(pipeline_progress)
            )

        # Run orchestrator
        result = orchestrator.run(
            user_request
        )

        status.success(
            "Market research completed successfully!"
        )

        st.session_state["research_result"] = result

    except Exception as error:

        st.error(
            f"Research pipeline error: {str(error)}"
        )


# ============================================================
# DISPLAY RESULTS
# ============================================================

if "research_result" in st.session_state:

    result = st.session_state["research_result"]

    st.divider()

    st.header("📑 Market Research Results")

    # --------------------------------------------------------
    # QUALITY CONTROL
    # --------------------------------------------------------

    quality_control = result.get(
        "quality_control",
        {},
    )

    if quality_control:

        st.subheader("✅ Research Quality")

        quality_score = quality_control.get(
            "quality_score",
            "N/A",
        )

        qc_col1, qc_col2 = st.columns(2)

        with qc_col1:

            st.metric(
                "Quality Score",
                quality_score,
            )

        with qc_col2:

            passed = quality_control.get(
                "passed",
                False,
            )

            if passed:

                st.success("Quality Review Passed")

            else:

                st.warning("Quality Review Requires Attention")

    # --------------------------------------------------------
    # FINAL REPORT
    # --------------------------------------------------------

    final_report = result.get(
        "final_report",
        {},
    )

    if final_report:

        st.divider()

        st.header(
            final_report.get(
                "title",
                "Market Research Report",
            )
        )

        sections = [
            (
                "Executive Summary",
                "executive_summary",
            ),
            (
                "Research Objective",
                "research_objective",
            ),
            (
                "Market Overview",
                "market_overview",
            ),
            (
                "Competitive Analysis",
                "competitive_analysis",
            ),
            (
                "Conclusion",
                "conclusion",
            ),
        ]

        for title, key in sections:

            content = final_report.get(key)

            if content:

                st.subheader(title)

                st.write(content)

        # Key Findings

        findings = final_report.get(
            "key_findings",
            [],
        )

        if findings:

            st.subheader("Key Findings")

            for finding in findings:

                st.markdown(
                    f"- {finding}"
                )

        # Market Trends

        trends = final_report.get(
            "market_trends",
            [],
        )

        if trends:

            st.subheader("Market Trends")

            for trend in trends:

                st.markdown(
                    f"- {trend}"
                )

        # Risks

        risks = final_report.get(
            "risks_and_challenges",
            [],
        )

        if risks:

            st.subheader(
                "Risks and Challenges"
            )

            for risk in risks:

                st.markdown(
                    f"- {risk}"
                )

        # Limitations

        limitations = final_report.get(
            "research_limitations",
            [],
        )

        if limitations:

            st.subheader(
                "Research Limitations"
            )

            for limitation in limitations:

                st.markdown(
                    f"- {limitation}"
                )

    # --------------------------------------------------------
    # DETAILED PIPELINE DATA
    # --------------------------------------------------------

    st.divider()

    with st.expander(
        "🔬 View Complete Research Pipeline Data"
    ):

        st.json(result)

    # --------------------------------------------------------
    # DOWNLOAD
    # --------------------------------------------------------

    st.divider()

    json_result = json.dumps(
        result,
        indent=4,
        default=str,
    )

    st.download_button(
        label="⬇️ Download Complete Research Report (JSON)",
        data=json_result,
        file_name="marketmind_research_report.json",
        mime="application/json",
        use_container_width=True,
    )