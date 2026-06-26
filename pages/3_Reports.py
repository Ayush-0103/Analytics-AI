import html
import os
from datetime import datetime

import streamlit as st

from agents.html_report_agent import HTMLReportAgent


# ============================================================
# CSS — same design system as app.py / 4_AI_Chat.py, embedded
# here too since each Streamlit page is its own script run.
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

/* ---------- Generic panel / report cards ---------- */

.panel-card, .report-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 16px 18px;
  margin-bottom: 14px;
}

.panel-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 4px;
}

.panel-card-title {
  font-size: 13.5px;
  font-weight: 700;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 8px;
}

.panel-card-desc {
  font-size: 12.5px;
  color: var(--text-secondary);
  margin: 4px 0 14px;
  line-height: 1.5;
}

.format-badge {
  display: inline-block;
  font-size: 10.5px;
  font-weight: 700;
  letter-spacing: 0.04em;
  padding: 2px 8px;
  border-radius: 20px;
  background: var(--accent-soft);
  color: var(--accent);
}

/* ---------- History list ---------- */

.history-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  background: rgba(255, 255, 255, 0.02);
  margin-bottom: 8px;
  font-size: 12.5px;
}

.history-row .h-name {
  color: var(--text-primary);
  font-weight: 600;
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
# SMALL PRESENTATION HELPERS
# ============================================================

def section_header(icon, title):
    st.markdown(
        f"""
        <div class='section-row'>
            <div class='section-title'><span class='icon'>{icon}</span>{html.escape(title)}</div>
        </div>
        <div class='section-divider'></div>
        """,
        unsafe_allow_html=True,
    )


def status_banner(kind, message):
    icons = {"success": "✅", "warning": "⚠️", "danger": "⛔"}
    st.markdown(
        f"<div class='status-banner {kind}'>{icons.get(kind, 'ℹ️')} {html.escape(message)}</div>",
        unsafe_allow_html=True,
    )


def render_history():
    history = st.session_state.get("report_history", [])
    if not history:
        st.caption("No reports generated yet this session.")
        return
    for item in reversed(history):
        st.markdown(
            f"""
            <div class='history-row'>
                <div>
                    <div class='h-name'>{html.escape(item['name'])}</div>
                    <div class='h-meta'>{item['timestamp']}</div>
                </div>
                <span class='format-badge'>{item['format']}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def log_report(name, fmt):
    st.session_state.setdefault("report_history", [])
    st.session_state["report_history"].append(
        {
            "name": name,
            "format": fmt,
            "timestamp": datetime.now().strftime("%b %d, %Y · %I:%M %p"),
        }
    )


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Reports",
    page_icon="📑",
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
            <div class='main-title'>Reports</div>
            <div class='subtitle'>Export and download your analytics deliverables</div>
        </div>
        <div class='top-meta'>{datetime.now().strftime('%b %d, %Y · %I:%M %p')}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# BODY
# ============================================================

if "analysis_result" not in st.session_state:

    st.markdown(
        """
        <div class='empty-state'>
            <div class='empty-icon'>📑</div>
            <div class='empty-title'>No dataset loaded</div>
            <div class='empty-text'>Upload an Excel file on the Dashboard first, then come back here to export reports.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("app.py", label="Go to Dashboard", icon="📊")

else:

    section_header("📦", "Export Center")

    col1, col2 = st.columns(2)

    # ---------- PowerPoint export ----------
    with col1:
        st.markdown("<div class='report-card'>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class='panel-card-header'>
                <span class='panel-card-title'>🖥 PowerPoint Deck</span>
                <span class='format-badge'>PPTX</span>
            </div>
            <div class='panel-card-desc'>
                Slide deck built from the dashboard's KPIs, AI insights and charts.
            </div>
            """,
            unsafe_allow_html=True,
        )

        ppt_path = st.session_state.get("ppt_path")
        if ppt_path and os.path.exists(ppt_path):
            with open(ppt_path, "rb") as file:
                st.download_button(
                    "📥 Download PPT",
                    file,
                    "Analytics_Report.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    width="stretch",
                )
        else:
            st.caption("No PPT generated yet. Generate one from the Dashboard's Reports section.")

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------- HTML report export ----------
    with col2:
        st.markdown("<div class='report-card'>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class='panel-card-header'>
                <span class='panel-card-title'>🌐 HTML Report</span>
                <span class='format-badge'>HTML</span>
            </div>
            <div class='panel-card-desc'>
                Self-contained, shareable report combining analysis results and AI-generated insights.
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Generate HTML Report", type="primary", width="stretch"):
            try:
                with st.spinner("Building HTML report..."):
                    agent = HTMLReportAgent()
                    html_path = agent.generate_report(
                        st.session_state["analysis_result"],
                        st.session_state.get("insights", ""),
                    )
                st.session_state["html_report_path"] = html_path
                log_report("Analytics_Report.html", "HTML")
                status_banner("success", "HTML report generated successfully")
            except Exception as e:
                status_banner("danger", f"HTML report error: {str(e)}")

        html_path = st.session_state.get("html_report_path")
        if html_path and os.path.exists(html_path):
            with open(html_path, "rb") as file:
                st.download_button(
                    "📥 Download HTML",
                    file,
                    "Analytics_Report.html",
                    mime="text/html",
                    width="stretch",
                )

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------- Report history ----------
    section_header("🕓", "Report History")
    st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
    render_history()
    st.markdown("</div>", unsafe_allow_html=True)