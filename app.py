import html
import os
import re
from datetime import datetime

import pandas as pd
import streamlit as st

from agents.analysis_agent import AnalysisAgent
from agents.insight_agent import InsightAgent
from agents.visualization_agent import VisualizationAgent
from agents.ppt_agent import PPTAgent


# ============================================================
# CSS — embedded directly so this file has no external dependency.
# Internal-tool design system: dense, fast, quiet, high-contrast dark theme.
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

/* ---------- KPI cards ---------- */

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: 12px;
}

.kpi-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 14px 16px;
  transition: border-color 0.12s ease, background-color 0.12s ease;
}

.kpi-card:hover {
  border-color: var(--border-strong);
  background: var(--bg-card-hover);
}

.kpi-icon-wrap {
  width: 30px;
  height: 30px;
  border-radius: 8px;
  background: var(--accent-soft);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 15px;
  margin-bottom: 10px;
}

.kpi-label {
  font-size: 10.5px;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  font-weight: 700;
  color: var(--text-secondary);
  margin-bottom: 4px;
}

.kpi-value {
  font-size: 22px;
  font-weight: 700;
  color: var(--text-primary);
  font-variant-numeric: tabular-nums;
  line-height: 1.15;
}

.kpi-trend {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  font-weight: 600;
  margin-top: 8px;
  padding: 2px 7px;
  border-radius: 20px;
}

.kpi-trend.up { background: var(--success-soft); color: var(--success); }
.kpi-trend.down { background: var(--danger-soft); color: var(--danger); }
.kpi-trend.neutral { background: rgba(255,255,255,0.06); color: var(--text-tertiary); }

/* ---------- Generic panel card (charts / data / reports) ---------- */

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

/* ---------- Insight cards ---------- */

.insight-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 12px;
}

.insight-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-left: 3px solid var(--accent);
  border-radius: var(--radius-md);
  padding: 14px 16px;
}

.insight-card h4 {
  margin: 0 0 8px;
  font-size: 13px;
  font-weight: 700;
  color: var(--text-primary);
}

.insight-card p, .insight-card li {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0 0 4px;
}

.insight-card ul { margin: 0; padding-left: 18px; }

/* ---------- Recommendation cards ---------- */

.rec-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
  gap: 12px;
}

.rec-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 14px 16px;
  position: relative;
}

.rec-rank {
  position: absolute;
  top: 12px;
  right: 14px;
  font-size: 11px;
  font-weight: 700;
  color: var(--text-tertiary);
}

.rec-badge {
  display: inline-block;
  font-size: 10.5px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 20px;
  margin-bottom: 8px;
}

.rec-badge.high { background: var(--danger-soft); color: var(--danger); }
.rec-badge.medium { background: var(--warning-soft); color: var(--warning); }
.rec-badge.low { background: var(--success-soft); color: var(--success); }

.rec-text {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.55;
}

/* ---------- Status banners (replace default st.success/st.error) ---------- */

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
}

.empty-icon { font-size: 32px; margin-bottom: 10px; }
.empty-title { font-size: 15px; font-weight: 700; color: var(--text-primary); margin-bottom: 6px; }
.empty-text { font-size: 13px; }

/* ---------- Streamlit widget overrides ---------- */

[data-testid="stFileUploaderDropzone"] {
  background: var(--bg-panel) !important;
  border: 1.5px dashed var(--border-strong) !important;
  border-radius: var(--radius-md) !important;
}

[data-testid="stFileUploaderDropzone"]:hover {
  border-color: var(--accent) !important;
}

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

[data-testid="stExpander"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: var(--radius-md) !important;
}

[data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea {
  background: var(--bg-input) !important;
  border: 1px solid var(--border-subtle) !important;
  color: var(--text-primary) !important;
  border-radius: var(--radius-sm) !important;
}

[data-testid="stMultiSelect"] > div {
  background: var(--bg-input) !important;
  border-color: var(--border-subtle) !important;
}

[data-testid="stMetric"] {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 12px 14px;
}

/* ---------- Chat bubbles (used on AI Chat page) ---------- */

[data-testid="stChatMessage"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: var(--radius-md) !important;
}

/* ---------- Misc helpers ---------- */

.caption-muted {
  font-size: 12px;
  color: var(--text-tertiary);
  margin-top: -4px;
  margin-bottom: 10px;
}

.chip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 11.5px;
  font-weight: 600;
  padding: 3px 9px;
  border-radius: 20px;
  background: rgba(255,255,255,0.05);
  color: var(--text-secondary);
  margin: 0 6px 6px 0;
  border: 1px solid var(--border-subtle);
}
"""


def load_css():
    st.markdown(f"<style>{CSS_STYLES}</style>", unsafe_allow_html=True)


# ============================================================
# SMALL PRESENTATION HELPERS
# (none of these touch agent logic — formatting / parsing only)
# ============================================================

def format_value(value):
    """Format a raw numeric/string value for display. Presentation only."""
    try:
        if isinstance(value, bool):
            return str(value)
        if isinstance(value, int):
            return f"{value:,}"
        if isinstance(value, float):
            if value.is_integer():
                return f"{int(value):,}"
            return f"{value:,.2f}"
        return str(value)
    except Exception:
        return str(value)


def find_kpi(result, keywords, stat="mean"):
    """Look for a column in result['kpis'] whose name matches one of the
    given keywords (e.g. 'rating', 'price', 'review') and return the
    requested stat, formatted. Returns None if nothing matches.
    Pure read of the existing AnalysisAgent output — no new computation.
    """
    kpis = result.get("kpis", {}) or {}
    for col, stats in kpis.items():
        col_lower = str(col).lower()
        if any(k in col_lower for k in keywords):
            val = stats.get(stat)
            if val is not None:
                return format_value(val)
    return None


INSIGHT_HEADINGS = ["Executive Summary", "Key Insights", "Business Recommendations"]


def parse_insights(text):
    """Split the InsightAgent's single returned string into labeled
    sections, if it contains the expected headings. Falls back to putting
    the entire text under 'Executive Summary' if parsing doesn't match —
    so nothing is ever lost or hidden.
    """
    if not text:
        return {}

    pattern = r"(?im)^\s*(?:#{1,4}\s*|\*\*)?(" + "|".join(INSIGHT_HEADINGS) + r")\b\s*:?\**\s*$"
    matches = list(re.finditer(pattern, text))

    if not matches:
        return {"Executive Summary": text.strip()}

    sections = {}
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        key = m.group(1)
        for heading in INSIGHT_HEADINGS:
            if heading.lower() == key.lower():
                key = heading
                break
        sections[key] = text[start:end].strip(" \n:-*")

    return sections


def extract_bullets(text):
    """Turn a block of text into a list of bullet-like items."""
    if not text:
        return []
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    bullets = []
    for line in lines:
        cleaned = re.sub(r"^[\-\*\u2022]\s*|^\d+[\.\)]\s*", "", line).strip()
        if cleaned:
            bullets.append(cleaned)
    return bullets


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


def render_kpi_grid(cards):
    parts = ["<div class='kpi-grid'>"]
    for c in cards:
        trend_html = ""
        if c.get("trend"):
            direction = c["trend"].get("direction", "neutral")
            arrow = {"up": "▲", "down": "▼", "neutral": "●"}.get(direction, "●")
            trend_html = (
                f"<div class='kpi-trend {direction}'>{arrow} "
                f"{html.escape(str(c['trend'].get('text', '')))}</div>"
            )
        parts.append(
            f"""
            <div class='kpi-card'>
                <div class='kpi-icon-wrap'>{c['icon']}</div>
                <div class='kpi-label'>{html.escape(c['label'])}</div>
                <div class='kpi-value'>{html.escape(str(c['value']))}</div>
                {trend_html}
            </div>
            """
        )
    parts.append("</div>")
    st.markdown("".join(parts), unsafe_allow_html=True)


def render_insight_cards(sections, keys, icons):
    parts = ["<div class='insight-grid'>"]
    rendered_any = False
    for key in keys:
        content = sections.get(key, "").strip()
        if not content:
            continue
        rendered_any = True
        bullets = extract_bullets(content)
        icon = icons.get(key, "📌")
        if len(bullets) > 1:
            items = "".join(f"<li>{html.escape(b)}</li>" for b in bullets)
            body = f"<ul>{items}</ul>"
        else:
            body = f"<p>{html.escape(content)}</p>"
        parts.append(f"<div class='insight-card'><h4>{icon} {html.escape(key)}</h4>{body}</div>")
    parts.append("</div>")
    if rendered_any:
        st.markdown("".join(parts), unsafe_allow_html=True)
    return rendered_any


def render_recommendations(bullets):
    n = len(bullets)
    parts = ["<div class='rec-grid'>"]
    for i, b in enumerate(bullets):
        if i < max(1, n // 3):
            tier, label = "high", "Priority"
        elif i < max(2, (2 * n) // 3):
            tier, label = "medium", "Consider"
        else:
            tier, label = "low", "Optional"
        parts.append(
            f"""
            <div class='rec-card'>
                <span class='rec-rank'>#{i + 1}</span>
                <span class='rec-badge {tier}'>{label}</span>
                <div class='rec-text'>{html.escape(b)}</div>
            </div>
            """
        )
    parts.append("</div>")
    st.markdown("".join(parts), unsafe_allow_html=True)


def status_banner(kind, message):
    icons = {"success": "✅", "warning": "⚠️", "danger": "⛔"}
    st.markdown(
        f"<div class='status-banner {kind}'>{icons.get(kind, 'ℹ️')} {html.escape(message)}</div>",
        unsafe_allow_html=True,
    )


def theme_chart(fig):
    """Cosmetic re-theming only — same figure object, same data."""
    try:
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", color="#9AA4B2", size=12),
            title_font=dict(color="#E7EBF3", size=14),
            legend=dict(bgcolor="rgba(0,0,0,0)"),
            margin=dict(l=10, r=10, t=40, b=10),
            colorway=["#3B82F6", "#6366F1", "#22C55E", "#F59E0B", "#EC4899", "#14B8A6"],
        )
        fig.update_xaxes(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.06)")
        fig.update_yaxes(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.06)")
    except Exception:
        pass
    return fig


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Analytics AI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()

# ============================================================
# SIDEBAR
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
            <div class='main-title'>Analytics AI Dashboard</div>
            <div class='subtitle'>Excel intelligence, insights &amp; reporting</div>
        </div>
        <div class='top-meta'>Last refreshed {datetime.now().strftime('%b %d, %Y · %I:%M %p')}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# UPLOAD
# ============================================================

section_header("📂", "Dataset Upload")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"], label_visibility="collapsed")

result = None
insights = ""
insights_failed = False
charts = []

if uploaded_file:

    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{uploaded_file.name}"

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.session_state["dataset_filename"] = uploaded_file.name

    # ---------- ANALYSIS AGENT ----------
    with st.spinner("Analyzing dataset..."):
        analysis_agent = AnalysisAgent()
        result = analysis_agent.analyze(file_path)

    # ---------- INSIGHT AGENT ----------
    try:
        insight_agent = InsightAgent()
        insights = insight_agent.generate_insights(result)
    except Exception as e:
        insights_failed = True
        insights = f"Insight generation failed: {str(e)}"

    # ---------- VISUALIZATION AGENT ----------
    with st.spinner("Building charts..."):
        viz_agent = VisualizationAgent()
        charts = viz_agent.create_charts(result["dataframe"])

    # ---------- SESSION STATE (preserved keys) ----------
    st.session_state["analysis_result"] = result
    st.session_state["dataframe"] = result["dataframe"]
    st.session_state["insights"] = insights
    st.session_state["charts"] = charts

    if "ppt_path" not in st.session_state:
        st.session_state["ppt_path"] = None

elif st.session_state.get("analysis_result") is not None:
    # No new upload this run (e.g. returning from another page) — redraw
    # the dashboard from the existing session state instead of losing it.
    # No agent is called here; this only reads what was already computed.
    result = st.session_state["analysis_result"]
    insights = st.session_state.get("insights", "")
    charts = st.session_state.get("charts", [])

# ============================================================
# DASHBOARD
# ============================================================

if result is not None:

    # ---------- SECTION 1: EXECUTIVE KPI CARDS ----------
    section_header("📊", "Executive Overview")

    kpi_cards = [
        {"icon": "📦", "label": "Total Records", "value": format_value(result.get("rows", 0))},
        {"icon": "📐", "label": "Total Columns", "value": format_value(result.get("columns", 0))},
        {"icon": "⭐", "label": "Avg Rating", "value": find_kpi(result, ["rating"], "mean") or "—"},
        {"icon": "💬", "label": "Total Reviews", "value": find_kpi(result, ["review"], "sum") or "—"},
        {"icon": "💰", "label": "Avg Price", "value": find_kpi(result, ["price"], "mean") or "—"},
    ]
    render_kpi_grid(kpi_cards)

    # ---------- DATASET PROFILE (collapsed — keeps daily view lean) ----------
    with st.expander("📋 Dataset profile & data quality", expanded=False):

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown("**Sheets Detected**")
            st.write(result.get("sheet_names", []))

        with c2:
            num_cols = result.get("numeric_columns", [])
            st.markdown(f"**Numeric Columns ({len(num_cols)})**")
            st.write(num_cols)

        with c3:
            cat_cols = result.get("categorical_columns", [])
            st.markdown(f"**Categorical Columns ({len(cat_cols)})**")
            st.write(cat_cols)

        st.markdown("**Column Statistics**")
        kpis_dict = result.get("kpis", {}) or {}
        if kpis_dict:
            kpi_df = pd.DataFrame(kpis_dict).T.reset_index().rename(columns={"index": "Column"})
            st.dataframe(kpi_df, width="stretch", hide_index=True)
        else:
            st.caption("No numeric columns available for statistics.")

        st.markdown("**Missing Values**")
        missing = {k: v for k, v in result.get("missing_values", {}).items() if v > 0}
        if missing:
            status_banner("warning", f"Missing values detected in {len(missing)} column(s)")
            st.write(missing)
        else:
            status_banner("success", "No missing values found")

    # ---------- SECTION 2: AI EXECUTIVE SUMMARY ----------
    section_header("🧭", "AI Executive Summary")

    if insights_failed:
        status_banner("danger", insights)
    else:
        sections = parse_insights(insights)
        render_insight_cards(
            sections,
            keys=["Executive Summary", "Key Insights"],
            icons={"Executive Summary": "🧭", "Key Insights": "💡"},
        )

    # ---------- SECTION 3: INTERACTIVE ANALYTICS ----------
    section_header("📈", "Interactive Analytics")

    os.makedirs("graphs", exist_ok=True)
    chart_paths = []

    if charts:
        cols = st.columns(2)
        for i, chart in enumerate(charts):
            chart = theme_chart(chart)

            try:
                chart_title = chart.layout.title.text
            except Exception:
                chart_title = None
            title = chart_title or f"Chart {i + 1}"

            target = cols[i % 2]
            with target:
                st.markdown(
                    f"""
                    <div class='chart-card'>
                        <div class='chart-card-header'>
                            <span class='chart-card-title'>📊 {html.escape(title)}</span>
                        </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.plotly_chart(chart, width="stretch", key=f"chart_{i}")
                st.markdown("</div>", unsafe_allow_html=True)

            chart_path = f"graphs/chart_{i}.png"
            chart.write_image(chart_path)
            chart_paths.append(chart_path)
    else:
        st.caption("No charts were generated for this dataset.")

    st.session_state["charts"] = charts
    st.session_state["chart_paths"] = chart_paths

    # ---------- SECTION 4: AI RECOMMENDATIONS ----------
    section_header("✅", "AI Recommendations")

    if insights_failed:
        st.caption("Recommendations unavailable — insight generation failed above.")
    else:
        rec_text = parse_insights(insights).get("Business Recommendations", "")
        rec_bullets = extract_bullets(rec_text)
        if rec_bullets:
            render_recommendations(rec_bullets)
        else:
            st.caption("No specific recommendations were returned for this dataset.")

    # ---------- SECTION 5: DATASET EXPLORER ----------
    section_header("🔍", "Dataset Explorer")

    preview_df = pd.DataFrame(result.get("preview", []))

    t1, t2 = st.columns([2, 1])
    with t1:
        search_term = st.text_input(
            "Search dataset",
            placeholder="Search across all columns...",
            label_visibility="collapsed",
        )
    with t2:
        selected_cols = st.multiselect(
            "Columns",
            options=list(preview_df.columns),
            default=list(preview_df.columns),
            label_visibility="collapsed",
        )

    display_df = preview_df
    if search_term:
        mask = display_df.astype(str).apply(
            lambda col: col.str.contains(search_term, case=False, na=False)
        ).any(axis=1)
        display_df = display_df[mask]
    if selected_cols:
        display_df = display_df[selected_cols]

    st.markdown("<div class='data-card'>", unsafe_allow_html=True)
    st.dataframe(display_df, width="stretch", height=420, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='caption-muted'>Showing {len(display_df):,} of {len(preview_df):,} preview rows</div>",
        unsafe_allow_html=True,
    )

    # ---------- SECTION 6: REPORTS ----------
    section_header("📑", "Reports")

    st.markdown("<div class='report-card'>", unsafe_allow_html=True)
    st.markdown("<span class='panel-card-title'>🖥 PowerPoint Export</span>", unsafe_allow_html=True)
    st.caption("Generates a slide deck from this dataset's analysis, insights and charts.")

    if st.button("Generate PPT", type="primary"):
        try:
            ppt_agent = PPTAgent()
            ppt_path = ppt_agent.generate_ppt(result, insights, chart_paths)
            st.session_state["ppt_path"] = ppt_path

            with open(ppt_path, "rb") as file:
                st.download_button(
                    label="📥 Download PPT",
                    data=file,
                    file_name="Analytics_Report.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                )

            status_banner("success", "PPT generated successfully")

        except Exception as e:
            status_banner("danger", f"PPT generation error: {str(e)}")

    st.markdown("</div>", unsafe_allow_html=True)

    st.page_link(
        "pages/3_Reports.py",
        label="Open the full Report Center for HTML export & report history",
        icon="📑",
    )

else:
    st.markdown(
        """
        <div class='empty-state'>
            <div class='empty-icon'>📂</div>
            <div class='empty-title'>No dataset loaded</div>
            <div class='empty-text'>Upload an Excel file above to generate your executive dashboard.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )