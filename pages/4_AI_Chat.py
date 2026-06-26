import html
from datetime import datetime

import pandas as pd
import streamlit as st

from agents.chat_agent import ChatAgent  # noqa: F401 — kept per existing imports; not currently called
from agents.pandas_agent import PandasAgent
from agents.query_agent import QueryAgent
from agents.executor_agent import ExecutorAgent


# ============================================================
# CSS — same design system as app.py, embedded here too since each
# Streamlit page is its own script run and needs its own CSS injection.
# ============================================================

CSS_STYLES = """
:root {
  --bg-base: #0B0E13;
  --bg-panel: #11151C;
  --bg-card: #161B24;
  --bg-card-hover: #1A2029;
  --bg-input: #0F1318;

  --border-subtle: rgba(255, 255, 255, 0.08);
  --border-strong: rgba(255, 255, 255, 0.16);

  --accent: #3B82F6;
  --accent-soft: rgba(59, 130, 246, 0.12);
  --accent-2: #6366F1;

  --success: #22C55E;
  --success-soft: rgba(34, 197, 94, 0.12);
  --warning: #F59E0B;
  --warning-soft: rgba(245, 158, 11, 0.12);
  --danger: #EF4444;
  --danger-soft: rgba(239, 68, 68, 0.12);

  --text-primary: #E7EBF3;
  --text-secondary: #9AA4B2;
  --text-tertiary: #687087;

  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 14px;

  --font-main: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { transition: none !important; animation: none !important; }
}

/* ---------- Base ---------- */

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
  background-color: var(--bg-base) !important;
  font-family: var(--font-main);
  color: var(--text-primary);
}

[data-testid="stHeader"] {
  background: transparent;
}

.block-container {
  padding-top: 1.4rem !important;
  padding-bottom: 2.5rem !important;
  max-width: 1440px;
}

a, a:visited { color: var(--accent); }
a:focus-visible, button:focus-visible, input:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-thumb { background: var(--border-strong); border-radius: 8px; }
::-webkit-scrollbar-track { background: transparent; }

/* ---------- Sidebar ---------- */

/* Hide Streamlit's auto-generated page list — we render our own nav below
   using st.page_link, so the default list would just duplicate it. */
[data-testid="stSidebarNav"] {
  display: none;
}

[data-testid="stSidebar"] {
  background-color: var(--bg-panel) !important;
  border-right: 1px solid var(--border-subtle);
}

[data-testid="stSidebar"] .block-container {
  padding-top: 1.2rem !important;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
}

.sidebar-brand .brand-mark {
  color: var(--accent);
  font-size: 18px;
}

.brand-badge {
  display: inline-block;
  margin-top: 4px;
  font-size: 10px;
  letter-spacing: 0.08em;
  font-weight: 700;
  color: var(--text-tertiary);
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border-subtle);
  border-radius: 4px;
  padding: 2px 6px;
}

.sidebar-divider {
  height: 1px;
  background: var(--border-subtle);
  margin: 14px 0;
}

.nav-section-label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 700;
  color: var(--text-tertiary);
  margin: 4px 0 8px;
}

.sidebar-dataset {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 10px 12px;
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 4px;
}

.sidebar-dataset strong {
  display: block;
  color: var(--text-primary);
  font-size: 12.5px;
  font-weight: 600;
  margin-bottom: 4px;
  word-break: break-word;
}

.status-dot {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--success);
  margin-right: 6px;
}

[data-testid="stPageLink"] a {
  border-radius: var(--radius-sm) !important;
  padding: 6px 10px !important;
  font-size: 13.5px !important;
  font-weight: 500 !important;
  color: var(--text-secondary) !important;
  transition: background-color 0.12s ease, color 0.12s ease;
}

[data-testid="stPageLink"] a:hover {
  background: rgba(255, 255, 255, 0.05) !important;
  color: var(--text-primary) !important;
}

[data-testid="stPageLink"] a[aria-current="page"] {
  background: var(--accent-soft) !important;
  color: var(--accent) !important;
}

/* ---------- Top bar ---------- */

.app-topbar {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 18px;
}

.main-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}

.subtitle {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: 2px;
}

.top-meta {
  font-size: 12px;
  color: var(--text-tertiary);
  font-variant-numeric: tabular-nums;
}

/* ---------- Section headers ---------- */

.section-row {
  margin-top: 30px;
  margin-bottom: 10px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14.5px;
  font-weight: 700;
  color: var(--text-primary);
}

.section-title .icon { font-size: 15px; }

.section-divider {
  height: 1px;
  background: var(--border-subtle);
  margin-bottom: 16px;
}

/* ---------- Generic panel card ---------- */

.panel-card, .chart-card, .data-card, .report-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 14px 16px 6px;
  margin-bottom: 14px;
}

.panel-card-header, .chart-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 4px;
}

.panel-card-title, .chart-card-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
}

/* ---------- Status banners ---------- */

.status-banner {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border-radius: var(--radius-sm);
  font-size: 13px;
  font-weight: 500;
  margin: 8px 0 14px;
}

.status-banner.success { background: var(--success-soft); color: var(--success); border: 1px solid rgba(34,197,94,0.25); }
.status-banner.warning { background: var(--warning-soft); color: var(--warning); border: 1px solid rgba(245,158,11,0.25); }
.status-banner.danger { background: var(--danger-soft); color: var(--danger); border: 1px solid rgba(239,68,68,0.25); }

/* ---------- Empty state ---------- */

.empty-state {
  text-align: center;
  padding: 56px 20px;
  color: var(--text-secondary);
  border: 1px dashed var(--border-subtle);
  border-radius: var(--radius-lg);
  background: var(--bg-panel);
  margin-bottom: 14px;
}

.empty-icon { font-size: 32px; margin-bottom: 10px; }
.empty-title { font-size: 15px; font-weight: 700; color: var(--text-primary); margin-bottom: 6px; }
.empty-text { font-size: 13px; }

/* ---------- Streamlit widget overrides ---------- */

[data-testid="stButton"] button, [data-testid="stDownloadButton"] button {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-subtle) !important;
  color: var(--text-primary) !important;
  border-radius: var(--radius-sm) !important;
  font-weight: 600 !important;
  padding: 0.45rem 1rem !important;
  transition: border-color 0.12s ease, color 0.12s ease, background-color 0.12s ease;
}

[data-testid="stButton"] button:hover, [data-testid="stDownloadButton"] button:hover {
  border-color: var(--accent) !important;
  color: var(--accent) !important;
  background: var(--accent-soft) !important;
}

[data-testid="stButton"] button[kind="primary"],
[data-testid="baseButton-primary"] {
  background: var(--accent) !important;
  border-color: var(--accent) !important;
  color: #FFFFFF !important;
}

[data-testid="stDataFrame"], [data-testid="stTable"] {
  border: 1px solid var(--border-subtle) !important;
  border-radius: var(--radius-md) !important;
  overflow: hidden;
}

[data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea {
  background: var(--bg-input) !important;
  border: 1px solid var(--border-subtle) !important;
  color: var(--text-primary) !important;
  border-radius: var(--radius-sm) !important;
}

/* ---------- Chat ---------- */

[data-testid="stChatMessage"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: var(--radius-md) !important;
}

[data-testid="stChatInput"] textarea {
  background: var(--bg-input) !important;
  border: 1px solid var(--border-subtle) !important;
  color: var(--text-primary) !important;
  border-radius: var(--radius-lg) !important;
}

[data-testid="stChatInput"] {
  border-color: var(--border-subtle) !important;
}

/* ---------- Misc helpers ---------- */

.caption-muted {
  font-size: 12px;
  color: var(--text-tertiary);
  margin-top: -4px;
  margin-bottom: 10px;
}
"""


def load_css():
    st.markdown(f"<style>{CSS_STYLES}</style>", unsafe_allow_html=True)


# ============================================================
# RENDER HELPERS
# (presentation only — the agent call logic lives in run_pipeline below
# and is unchanged from the original page)
# ============================================================

def render_block(kind, payload):
    """Render one piece of an assistant message. 'kind' mirrors exactly how
    the original page decided what to call (st.dataframe / st.json /
    st.success / st.write) for a given result type — only the container
    changed, not the decision logic.
    """
    if kind == "dataframe":
        st.dataframe(payload, width="stretch")
    elif kind == "json":
        st.json(payload)
    elif kind == "success_text":
        st.markdown(
            f"<div class='status-banner success'>✅ {html.escape(str(payload))}</div>",
            unsafe_allow_html=True,
        )
    elif kind == "write":
        st.write(payload)
    elif kind == "error":
        st.markdown(
            f"<div class='status-banner danger'>⛔ {html.escape(str(payload))}</div>",
            unsafe_allow_html=True,
        )
    elif kind == "code_result":
        st.markdown("<div class='caption-muted'>Generated query</div>", unsafe_allow_html=True)
        st.code(payload["query"], language="python")
        st.markdown(
            "<div class='caption-muted' style='margin-top:10px;'>Result</div>",
            unsafe_allow_html=True,
        )
        render_block(payload["inner_kind"], payload["inner_payload"])
    else:
        st.caption("No result was returned for this question.")


def run_pipeline(question, dataframe):
    """Exact same call sequence and type-based branching as the original
    page: try PandasAgent first; if it returns None, fall back to
    QueryAgent + ExecutorAgent. The only addition is a try/except around
    each agent call so a failure shows a styled error bubble instead of
    crashing the whole page.
    """

    try:
        pandas_agent = PandasAgent()
        result = pandas_agent.execute(dataframe, question)
    except Exception as e:
        return {"kind": "error", "payload": f"Pandas agent error: {str(e)}"}

    if result is not None:
        if isinstance(result, list):
            return {"kind": "dataframe", "payload": pd.DataFrame(result)}
        elif isinstance(result, dict):
            return {"kind": "json", "payload": result}
        else:
            return {"kind": "success_text", "payload": result}

    # ---------- Fallback: generate + execute a pandas query ----------
    try:
        query_agent = QueryAgent()
        query = query_agent.generate_query(dataframe.columns.tolist(), question)
    except Exception as e:
        return {"kind": "error", "payload": f"Query agent error: {str(e)}"}

    try:
        executor = ExecutorAgent()
        output = executor.execute(dataframe, query)
    except Exception as e:
        return {
            "kind": "code_result",
            "payload": {"query": query, "inner_kind": "error", "inner_payload": f"Executor error: {str(e)}"},
        }

    if isinstance(output, pd.DataFrame):
        inner_kind, inner_payload = "dataframe", output
    elif isinstance(output, pd.Series):
        inner_kind, inner_payload = "dataframe", output.to_frame()
    elif isinstance(output, dict):
        inner_kind, inner_payload = "json", output
    else:
        inner_kind, inner_payload = "write", output

    return {
        "kind": "code_result",
        "payload": {"query": query, "inner_kind": inner_kind, "inner_payload": inner_payload},
    }


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Chat",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()

# ============================================================
# SIDEBAR (identical to app.py, for a consistent nav everywhere)
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div class='sidebar-brand'><span class='brand-mark'>◆</span> Analytics AI</div>
        <div class='brand-badge'>ENTERPRISE</div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)

    st.page_link("app.py", label="Dashboard", icon="📊")
    st.page_link("pages/1_Insights.py", label="Insights", icon="🧭")
    st.page_link("pages/2_Visualizations.py", label="Visualizations", icon="📈")
    st.page_link("pages/3_Reports.py", label="Reports", icon="📑")
    st.page_link("pages/4_AI_Chat.py", label="AI Chat", icon="💬")
    st.page_link("pages/5_Research.py", label="Research", icon="🔎")
    st.page_link("pages/6_Command_Center.py", label="Command Center", icon="🛰")

    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='nav-section-label'>Workspace</div>", unsafe_allow_html=True)

    cached_result = st.session_state.get("analysis_result")
    if cached_result:
        fname = st.session_state.get("dataset_filename", "Uploaded dataset")
        st.markdown(
            f"""
            <div class='sidebar-dataset'>
                <strong>{html.escape(fname)}</strong>
                <span class='status-dot'></span>Synced · {cached_result.get('rows', 0):,} rows
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<div class='sidebar-dataset'>No dataset loaded yet</div>",
            unsafe_allow_html=True,
        )

# ============================================================
# TOP BAR
# ============================================================

st.markdown(
    f"""
    <div class='app-topbar'>
        <div>
            <div class='main-title'>AI Chat</div>
            <div class='subtitle'>Ask questions about your dataset in plain language</div>
        </div>
        <div class='top-meta'>{datetime.now().strftime('%b %d, %Y · %I:%M %p')}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# BODY
# ============================================================

if "dataframe" not in st.session_state:

    st.markdown(
        """
        <div class='empty-state'>
            <div class='empty-icon'>💬</div>
            <div class='empty-title'>No dataset loaded</div>
            <div class='empty-text'>Upload an Excel file on the Dashboard first, then come back here to ask questions about it.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("app.py", label="Go to Dashboard", icon="📊")

else:

    st.session_state.setdefault("chat_history", [])

    top_l, top_r = st.columns([5, 1])
    with top_l:
        st.caption(f"Dataset in memory · {len(st.session_state['dataframe']):,} rows")
    with top_r:
        if st.button("Clear chat"):
            st.session_state["chat_history"] = []
            st.rerun()

    # ---------- Conversation history ----------
    for turn in st.session_state["chat_history"]:
        if turn["role"] == "user":
            with st.chat_message("user", avatar="🧑"):
                st.markdown(html.escape(turn["content"]))
        else:
            with st.chat_message("assistant", avatar="🤖"):
                render_block(turn["block"]["kind"], turn["block"]["payload"])

    # ---------- New question ----------
    question = st.chat_input("Ask about your data...")

    if question:
        st.session_state["chat_history"].append({"role": "user", "content": question})

        with st.spinner("Thinking..."):
            block = run_pipeline(question, st.session_state["dataframe"])

        st.session_state["chat_history"].append({"role": "assistant", "block": block})
        st.rerun()