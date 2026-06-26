import html
import re
from datetime import datetime

import streamlit as st


# ============================================================
# CSS — same design system as app.py / 4_AI_Chat.py / 3_Reports.py,
# embedded here too since each Streamlit page is its own script run.
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

/* ---------- Hero summary card ---------- */

.hero-card {
  background: linear-gradient(135deg, rgba(59,130,246,0.10), rgba(99,102,241,0.05));
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 22px 24px;
  margin-bottom: 6px;
}

.hero-eyebrow {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-weight: 700;
  color: var(--accent);
  margin-bottom: 8px;
}

.hero-text {
  font-size: 14.5px;
  line-height: 1.7;
  color: var(--text-primary);
}

/* ---------- Insight cards ---------- */

.insight-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 12px;
}

.insight-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-left: 3px solid var(--accent);
  border-radius: var(--radius-md);
  padding: 16px 18px;
  transition: border-color 0.12s ease, background-color 0.12s ease;
}

.insight-card:hover {
  background: var(--bg-card-hover);
  border-left-color: var(--accent-2);
}

.insight-card h4 {
  margin: 0 0 10px;
  font-size: 13.5px;
  font-weight: 700;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 8px;
}

.insight-card p, .insight-card li {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.65;
  margin: 0 0 6px;
}

.insight-card ul { margin: 0; padding-left: 18px; }
.insight-card li::marker { color: var(--accent); }

/* ---------- Recommendation cards ---------- */

.rec-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 12px;
}

.rec-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 16px 18px;
  position: relative;
  transition: border-color 0.12s ease, background-color 0.12s ease;
}

.rec-card:hover {
  background: var(--bg-card-hover);
  border-color: var(--border-strong);
}

.rec-rank {
  position: absolute;
  top: 14px;
  right: 16px;
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
  margin-bottom: 10px;
}

.rec-badge.high { background: var(--danger-soft); color: var(--danger); }
.rec-badge.medium { background: var(--warning-soft); color: var(--warning); }
.rec-badge.low { background: var(--success-soft); color: var(--success); }

.rec-text {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
}

/* ---------- Stat strip ---------- */

.stat-strip {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 4px;
}

.stat-pill {
  display: flex;
  align-items: center;
  gap: 8px;
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: 20px;
  padding: 6px 14px 6px 10px;
  font-size: 12px;
}

.stat-pill .dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
}

.stat-pill .num {
  font-weight: 700;
  color: var(--text-primary);
  font-variant-numeric: tabular-nums;
}

.stat-pill .lbl {
  color: var(--text-tertiary);
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

[data-testid="stTabs"] [data-baseweb="tab-list"] {
  gap: 4px;
  border-bottom: 1px solid var(--border-subtle);
}

[data-testid="stTabs"] [data-baseweb="tab"] {
  background: transparent;
  color: var(--text-secondary);
  font-weight: 600;
  font-size: 13px;
  padding: 8px 14px;
  border-radius: var(--radius-sm) var(--radius-sm) 0 0;
}

[data-testid="stTabs"] [aria-selected="true"] {
  color: var(--accent) !important;
  background: var(--accent-soft) !important;
}

[data-testid="stExpander"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: var(--radius-md) !important;
}

[data-testid="stTextInput"] input {
  background: var(--bg-input) !important;
  border: 1px solid var(--border-subtle) !important;
  color: var(--text-primary) !important;
  border-radius: var(--radius-sm) !important;
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
# PARSING HELPERS
# (mirrors the exact logic used on the Dashboard so insights
# render identically everywhere — no new interpretation added)
# ============================================================

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


def status_banner(kind, message):
    icons = {"success": "✅", "warning": "⚠️", "danger": "⛔"}
    st.markdown(
        f"<div class='status-banner {kind}'>{icons.get(kind, 'ℹ️')} {html.escape(message)}</div>",
        unsafe_allow_html=True,
    )


def render_hero(summary_text):
    """Top hero card pulling the Executive Summary forward, since that's
    the single most-read piece of an insights page."""
    preview = summary_text.strip()
    st.markdown(
        f"""
        <div class='hero-card'>
            <div class='hero-eyebrow'>🧭 Executive Summary</div>
            <div class='hero-text'>{html.escape(preview)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


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


def render_stat_strip(sections):
    key_count = len(extract_bullets(sections.get("Key Insights", "")))
    rec_count = len(extract_bullets(sections.get("Business Recommendations", "")))
    words = sum(len(s.split()) for s in sections.values())
    st.markdown(
        f"""
        <div class='stat-strip'>
            <div class='stat-pill'><span class='dot' style='background:var(--accent)'></span>
                <span class='num'>{key_count}</span><span class='lbl'>key insights</span></div>
            <div class='stat-pill'><span class='dot' style='background:var(--success)'></span>
                <span class='num'>{rec_count}</span><span class='lbl'>recommendations</span></div>
            <div class='stat-pill'><span class='dot' style='background:var(--text-tertiary)'></span>
                <span class='num'>{words}</span><span class='lbl'>words analyzed</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Insights",
    page_icon="🧭",
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
            <div class='main-title'>AI Insights</div>
            <div class='subtitle'>Narrative analysis generated from your dataset</div>
        </div>
        <div class='top-meta'>{datetime.now().strftime('%b %d, %Y · %I:%M %p')}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# BODY
# ============================================================

raw_insights = st.session_state.get("insights")

if not raw_insights:

    st.markdown(
        """
        <div class='empty-state'>
            <div class='empty-icon'>🧭</div>
            <div class='empty-title'>No insights yet</div>
            <div class='empty-text'>Upload an Excel file on the Dashboard first — AI Insights are generated automatically once a dataset is analyzed.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("app.py", label="Go to Dashboard", icon="📊")

else:

    sections = parse_insights(raw_insights)

    # ---------- Hero: Executive Summary ----------
    summary = sections.get("Executive Summary", "").strip()
    if summary:
        render_hero(summary)

    render_stat_strip(sections)

    # ---------- Tabs: Key Insights / Recommendations / Raw ----------
    tab_labels = ["💡 Key Insights", "✅ Recommendations", "📄 Full Report"]
    tab1, tab2, tab3 = st.tabs(tab_labels)

    with tab1:
        ki_content = sections.get("Key Insights", "")
        ki_rendered = render_insight_cards(
            sections,
            keys=["Key Insights"],
            icons={"Key Insights": "💡"},
        )
        if not ki_rendered:
            st.caption("No key insights were returned for this dataset.")

    with tab2:
        rec_text = sections.get("Business Recommendations", "")
        rec_bullets = extract_bullets(rec_text)
        if rec_bullets:
            render_recommendations(rec_bullets)
        else:
            st.caption("No specific recommendations were returned for this dataset.")

    with tab3:
        search_term = st.text_input(
            "Search insights",
            placeholder="Search the full report...",
            label_visibility="collapsed",
        )

        display_text = raw_insights
        if search_term:
            lines = raw_insights.split("\n")
            matched = [l for l in lines if search_term.lower() in l.lower()]
            if matched:
                display_text = "\n".join(matched)
                status_banner("success", f"{len(matched)} matching line(s) found")
            else:
                display_text = ""
                status_banner("warning", "No matches found")

        if display_text:
            with st.expander("📄 Raw AI-generated report", expanded=True):
                st.markdown(display_text)