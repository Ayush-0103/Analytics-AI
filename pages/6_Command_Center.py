import html
import time
from datetime import datetime

import pandas as pd
import streamlit as st

from workflow.router_graph import graph


# ============================================================
# CSS — same design system as the rest of the app, embedded here
# too since each Streamlit page is its own script run.
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
  --purple: #A78BFA;
  --purple-soft: rgba(167, 139, 250, 0.12);
  --teal: #14B8A6;
  --teal-soft: rgba(20, 184, 166, 0.12);

  --text-primary: #E7EBF3;
  --text-secondary: #9AA4B2;
  --text-tertiary: #687087;

  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 14px;

  --font-main: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-mono: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
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

.history-chip-btn button {
  width: 100% !important;
  text-align: left !important;
  justify-content: flex-start !important;
  font-size: 12px !important;
  padding: 6px 10px !important;
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

/* ---------- Command panel ---------- */

.command-panel {
  background: linear-gradient(135deg, rgba(59,130,246,0.10), rgba(99,102,241,0.05));
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 20px 22px;
  margin-bottom: 18px;
}

.command-eyebrow {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-weight: 700;
  color: var(--accent);
  margin-bottom: 10px;
}

.command-eyebrow .pulse {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--success);
  box-shadow: 0 0 0 0 rgba(34,197,94,0.6);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(34,197,94,0.5); }
  70% { box-shadow: 0 0 0 7px rgba(34,197,94,0); }
  100% { box-shadow: 0 0 0 0 rgba(34,197,94,0); }
}

[data-testid="stTextInput"] input {
  background: var(--bg-input) !important;
  border: 1px solid var(--border-subtle) !important;
  color: var(--text-primary) !important;
  border-radius: var(--radius-sm) !important;
  font-size: 14px !important;
  padding: 10px 12px !important;
}

/* ---------- Suggestion chips ---------- */

.chip-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 10px;
}

[data-testid="column"] .chip-btn button {
  font-size: 11.5px !important;
  padding: 4px 10px !important;
  border-radius: 20px !important;
  background: rgba(255,255,255,0.04) !important;
}

/* ---------- Route badge ---------- */

.route-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 10px;
  padding: 12px 16px;
  border-radius: var(--radius-md);
  margin: 4px 0 14px;
  border: 1px solid var(--border-subtle);
  background: var(--bg-card);
}

.route-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.route-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 11.5px;
  font-weight: 700;
  letter-spacing: 0.03em;
  text-transform: uppercase;
  padding: 4px 11px;
  border-radius: 20px;
}

.route-query {
  font-size: 12.5px;
  color: var(--text-secondary);
  font-family: var(--font-mono);
}

.route-time {
  font-size: 11.5px;
  color: var(--text-tertiary);
  font-variant-numeric: tabular-nums;
}

/* ---------- Output card ---------- */

.output-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 16px 18px;
  margin-bottom: 14px;
}

.output-card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12.5px;
  font-weight: 700;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 12px;
}

/* ---------- History ---------- */

.history-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 10px 14px;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  background: rgba(255, 255, 255, 0.02);
  margin-bottom: 8px;
  font-size: 12.5px;
}

.history-row .h-query {
  color: var(--text-primary);
  font-weight: 600;
  font-family: var(--font-mono);
  font-size: 12px;
}

.history-row .h-meta {
  color: var(--text-tertiary);
  font-size: 11.5px;
  margin-top: 2px;
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

[data-testid="stButton"] button[kind="primary"]:hover {
  background: #2563EB !important;
}

[data-testid="stDataFrame"], [data-testid="stTable"] {
  border: 1px solid var(--border-subtle) !important;
  border-radius: var(--radius-md) !important;
  overflow: hidden;
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
# ROUTE STYLING
# ============================================================

ROUTE_STYLES = {
    "pandas": {"icon": "🐼", "color": "var(--accent)", "soft": "var(--accent-soft)"},
    "query": {"icon": "🧮", "color": "var(--purple)", "soft": "var(--purple-soft)"},
    "chat": {"icon": "💬", "color": "var(--teal)", "soft": "var(--teal-soft)"},
    "analysis": {"icon": "📊", "color": "var(--success)", "soft": "var(--success-soft)"},
    "insight": {"icon": "🧭", "color": "var(--warning)", "soft": "var(--warning-soft)"},
    "report": {"icon": "📑", "color": "var(--accent-2)", "soft": "rgba(99,102,241,0.12)"},
    "research": {"icon": "🔎", "color": "var(--teal)", "soft": "var(--teal-soft)"},
}

DEFAULT_ROUTE_STYLE = {"icon": "🛰", "color": "var(--text-secondary)", "soft": "rgba(255,255,255,0.06)"}

SUGGESTED_QUERIES = [
    "Summarize key trends in this dataset",
    "What are the top 5 records by value?",
    "Generate a report-ready insight",
]


def get_route_style(route):
    key = str(route).lower().strip()
    for name, style in ROUTE_STYLES.items():
        if name in key:
            return style
    return DEFAULT_ROUTE_STYLE


# ============================================================
# PRESENTATION HELPERS
# ============================================================

def section_header(icon, title, sub=None):
    sub_html = f"<div class='caption-muted'>{html.escape(sub)}</div>" if sub else ""
    st.markdown(
        f"""
        <div class='section-row'>
            <div class='section-title'><span class='icon'>{icon}</span>{html.escape(title)}</div>
        </div>
        <div class='section-divider'></div>
        {sub_html}
        """,
        unsafe_allow_html=True,
    )


def status_banner(kind, message):
    icons = {"success": "✅", "warning": "⚠️", "danger": "⛔"}
    st.markdown(
        f"<div class='status-banner {kind}'>{icons.get(kind, 'ℹ️')} {html.escape(message)}</div>",
        unsafe_allow_html=True,
    )


def render_route_banner(route, query, elapsed):
    style = get_route_style(route)
    st.markdown(
        f"""
        <div class='route-banner'>
            <div class='route-left'>
                <span class='route-badge' style='background:{style["soft"]}; color:{style["color"]};'>
                    {style["icon"]} {html.escape(str(route))}
                </span>
                <span class='route-query'>"{html.escape(query)}"</span>
            </div>
            <span class='route-time'>⏱ {elapsed:.2f}s</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_output(output):
    """Identical type-based branching to the original page — only the
    container changed, not the decision logic. Each branch is wrapped
    in the same styled output-card shell."""
    st.markdown("<div class='output-card'>", unsafe_allow_html=True)

    if isinstance(output, pd.DataFrame):
        st.markdown(
            f"<div class='output-card-header'>📋 Result · {len(output):,} rows</div>",
            unsafe_allow_html=True,
        )
        st.dataframe(output, width="stretch")

    elif isinstance(output, dict):
        st.markdown("<div class='output-card-header'>🗂 Result (structured)</div>", unsafe_allow_html=True)
        st.json(output)

    elif isinstance(output, list):
        try:
            df_out = pd.DataFrame(output)
            st.markdown(
                f"<div class='output-card-header'>📋 Result · {len(df_out):,} rows</div>",
                unsafe_allow_html=True,
            )
            st.dataframe(df_out, width="stretch")
        except Exception:
            st.markdown("<div class='output-card-header'>📄 Result</div>", unsafe_allow_html=True)
            st.write(output)

    elif output is None:
        st.caption("No result was returned for this query.")

    else:
        st.markdown("<div class='output-card-header'>📄 Result</div>", unsafe_allow_html=True)
        st.write(output)

    st.markdown("</div>", unsafe_allow_html=True)


def log_execution(query, route, elapsed, ok):
    st.session_state.setdefault("command_history", [])
    st.session_state["command_history"].append(
        {
            "query": query,
            "route": route,
            "elapsed": elapsed,
            "ok": ok,
            "timestamp": datetime.now().strftime("%I:%M %p"),
        }
    )
    st.session_state["command_history"] = st.session_state["command_history"][-10:]


def render_history():
    history = st.session_state.get("command_history", [])
    if not history:
        st.caption("No commands executed yet this session.")
        return
    for item in reversed(history):
        style = get_route_style(item["route"]) if item["ok"] else DEFAULT_ROUTE_STYLE
        status_icon = "✅" if item["ok"] else "⛔"
        st.markdown(
            f"""
            <div class='history-row'>
                <div>
                    <div class='h-query'>{status_icon} {html.escape(item['query'])}</div>
                    <div class='h-meta'>{item['timestamp']} · {item['elapsed']:.2f}s</div>
                </div>
                <span class='route-badge' style='background:{style["soft"]}; color:{style["color"]};'>
                    {style["icon"]} {html.escape(str(item['route']))}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def run_command(query, dataframe):
    start = time.time()
    try:
        result = graph.invoke({"query": query, "dataframe": dataframe})
        elapsed = time.time() - start
        return {"ok": True, "route": result.get("route", "unknown"), "output": result.get("result"), "elapsed": elapsed}
    except Exception as e:
        elapsed = time.time() - start
        return {"ok": False, "error": str(e), "elapsed": elapsed}


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Command Center",
    page_icon="🛰",
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
            <div class='main-title'>Executive Command Center</div>
            <div class='subtitle'>Ask anything — the router picks the right agent automatically</div>
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
            <div class='empty-icon'>🛰</div>
            <div class='empty-title'>No dataset loaded</div>
            <div class='empty-text'>Upload an Excel file on the Dashboard first, then come back here to run commands against it.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("app.py", label="Go to Dashboard", icon="📊")

else:

    default_query = st.session_state.pop("pending_command", "")

    # ---------- Command panel ----------
    st.markdown("<div class='command-panel'>", unsafe_allow_html=True)
    st.markdown(
        "<div class='command-eyebrow'><span class='pulse'></span>Router online — ask anything about your dataset</div>",
        unsafe_allow_html=True,
    )

    with st.form("command_form", clear_on_submit=False):
        c1, c2 = st.columns([5, 1])
        with c1:
            query = st.text_input(
                "Ask anything...",
                value=default_query,
                placeholder="e.g. show me revenue trends by region",
                label_visibility="collapsed",
            )
        with c2:
            submitted = st.form_submit_button("Execute", type="primary", width="stretch")

    st.markdown("<div class='chip-row'>", unsafe_allow_html=True)
    chip_cols = st.columns(len(SUGGESTED_QUERIES))
    for i, suggestion in enumerate(SUGGESTED_QUERIES):
        with chip_cols[i]:
            st.markdown("<div class='chip-btn'>", unsafe_allow_html=True)
            if st.button(suggestion, key=f"chip_{i}"):
                st.session_state["pending_command"] = suggestion
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- Execute ----------
    if submitted:
        if not query or not query.strip():
            status_banner("warning", "Enter a command or question before executing.")
        else:
            with st.spinner("Routing and executing..."):
                outcome = run_command(query.strip(), st.session_state["dataframe"])

            if outcome["ok"]:
                st.session_state["last_command"] = {
                    "query": query.strip(),
                    "route": outcome["route"],
                    "output": outcome["output"],
                    "elapsed": outcome["elapsed"],
                }
                log_execution(query.strip(), outcome["route"], outcome["elapsed"], ok=True)
            else:
                st.session_state["last_command"] = None
                log_execution(query.strip(), "error", outcome["elapsed"], ok=False)
                status_banner("danger", f"Execution failed: {outcome['error']}")

    # ---------- Render last result (persists across reruns) ----------
    last = st.session_state.get("last_command")
    if last:
        section_header("⚡", "Execution Result")
        render_route_banner(last["route"], last["query"], last["elapsed"])
        render_output(last["output"])

    # ---------- History ----------
    if st.session_state.get("command_history"):
        section_header("🕓", "Recent Commands")
        render_history()