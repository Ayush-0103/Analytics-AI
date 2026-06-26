import html
from datetime import datetime
from urllib.parse import urlparse

import streamlit as st

from agents.research_agent import ResearchAgent


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
  max-width: 1280px;
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

/* ---------- Search panel ---------- */

.search-panel {
  background: linear-gradient(135deg, rgba(59,130,246,0.10), rgba(99,102,241,0.05));
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 20px 22px 8px;
  margin-bottom: 18px;
}

.search-eyebrow {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-weight: 700;
  color: var(--accent);
  margin-bottom: 10px;
}

[data-testid="stTextInput"] input {
  background: var(--bg-input) !important;
  border: 1px solid var(--border-subtle) !important;
  color: var(--text-primary) !important;
  border-radius: var(--radius-sm) !important;
  font-size: 14px !important;
  padding: 10px 12px !important;
}

/* ---------- Result cards ---------- */

.result-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 16px 18px;
  margin-bottom: 12px;
  transition: border-color 0.12s ease, background-color 0.12s ease;
}

.result-card:hover {
  border-color: var(--border-strong);
  background: var(--bg-card-hover);
}

.result-card-top {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.result-index {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: var(--accent-soft);
  color: var(--accent);
  font-size: 11px;
  font-weight: 700;
  flex-shrink: 0;
}

.result-domain {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 11.5px;
  font-weight: 600;
  color: var(--text-tertiary);
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--border-subtle);
  border-radius: 20px;
  padding: 2px 10px;
}

.result-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 8px;
  line-height: 1.4;
}

.result-title a {
  color: var(--text-primary);
  text-decoration: none;
}

.result-title a:hover {
  color: var(--accent);
}

.result-content {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.65;
  margin-bottom: 4px;
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

[data-testid="stButton"] button, [data-testid="stDownloadButton"] button, [data-testid="stLinkButton"] a {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-subtle) !important;
  color: var(--text-primary) !important;
  border-radius: var(--radius-sm) !important;
  font-weight: 600 !important;
  padding: 0.4rem 0.9rem !important;
  font-size: 12.5px !important;
  transition: border-color 0.12s ease, color 0.12s ease, background-color 0.12s ease;
}

[data-testid="stButton"] button:hover, [data-testid="stDownloadButton"] button:hover, [data-testid="stLinkButton"] a:hover {
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
# HELPERS
# ============================================================

def get_domain(url):
    try:
        netloc = urlparse(url).netloc
        return netloc.replace("www.", "") if netloc else "source"
    except Exception:
        return "source"


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


def render_stat_strip(results):
    domains = {get_domain(r.get("url", "")) for r in results if r.get("url")}
    st.markdown(
        f"""
        <div class='stat-strip'>
            <div class='stat-pill'><span class='dot' style='background:var(--accent)'></span>
                <span class='num'>{len(results)}</span><span class='lbl'>results found</span></div>
            <div class='stat-pill'><span class='dot' style='background:var(--success)'></span>
                <span class='num'>{len(domains)}</span><span class='lbl'>unique sources</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_result_card(index, item):
    title = item.get("title") or "Untitled result"
    content = item.get("content") or "No summary available for this result."
    url = item.get("url") or ""
    domain = get_domain(url) if url else None

    domain_html = (
        f"<span class='result-domain'>🌐 {html.escape(domain)}</span>" if domain else ""
    )
    title_html = (
        f"<a href='{html.escape(url)}' target='_blank' rel='noopener noreferrer'>{html.escape(title)}</a>"
        if url else html.escape(title)
    )

    st.markdown(
        f"""
        <div class='result-card'>
            <div class='result-card-top'>
                <span class='result-index'>{index}</span>
                {domain_html}
            </div>
            <div class='result-title'>{title_html}</div>
            <div class='result-content'>{html.escape(content)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if url:
        st.link_button("Visit source ↗", url)


def log_search(query, result_count):
    st.session_state.setdefault("research_history", [])
    history = st.session_state["research_history"]
    history = [h for h in history if h["query"] != query]
    history.append(
        {"query": query, "count": result_count, "timestamp": datetime.now().strftime("%I:%M %p")}
    )
    st.session_state["research_history"] = history[-8:]


def run_research(query):
    try:
        agent = ResearchAgent()
        results = agent.research(query)
        return {"ok": True, "data": results}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Research",
    page_icon="🔎",
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

    history = st.session_state.get("research_history", [])
    if history:
        st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)
        st.markdown("<div class='nav-section-label'>Recent searches</div>", unsafe_allow_html=True)
        for h in reversed(history):
            st.markdown("<div class='history-chip-btn'>", unsafe_allow_html=True)
            if st.button(f"🔎 {h['query']}", key=f"hist_{h['query']}", help=f"{h['count']} results · {h['timestamp']}"):
                st.session_state["pending_query"] = h["query"]
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# TOP BAR
# ============================================================

st.markdown(
    f"""
    <div class='app-topbar'>
        <div>
            <div class='main-title'>Industry Research</div>
            <div class='subtitle'>AI-powered web research, summarized and sourced</div>
        </div>
        <div class='top-meta'>{datetime.now().strftime('%b %d, %Y · %I:%M %p')}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SEARCH PANEL
# ============================================================

st.markdown("<div class='search-panel'>", unsafe_allow_html=True)
st.markdown("<div class='search-eyebrow'>🔎 Research a topic</div>", unsafe_allow_html=True)

default_query = st.session_state.pop("pending_query", "")

with st.form("research_form", clear_on_submit=False):
    c1, c2 = st.columns([5, 1])
    with c1:
        query = st.text_input(
            "Research Topic",
            value=default_query,
            placeholder="e.g. competitive landscape for AI analytics tools",
            label_visibility="collapsed",
        )
    with c2:
        submitted = st.form_submit_button("Research", type="primary", width="stretch")

st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# RESULTS
# ============================================================

if submitted:
    if not query or not query.strip():
        status_banner("warning", "Enter a topic to research before searching.")
    else:
        with st.spinner(f"Researching \u201c{query}\u201d..."):
            outcome = run_research(query.strip())

        if not outcome["ok"]:
            status_banner("danger", f"Research failed: {outcome['error']}")
            st.session_state["last_research"] = None
        else:
            results_list = (outcome["data"] or {}).get("results", [])
            st.session_state["last_research"] = {"query": query.strip(), "results": results_list}
            log_search(query.strip(), len(results_list))

# ---------- Render last results (persists across reruns / nav) ----------
last = st.session_state.get("last_research")

if last:
    results_list = last["results"]

    if not results_list:
        status_banner("warning", f"No results were found for \u201c{last['query']}\u201d.")
    else:
        section_header("📄", f"Results for \u201c{last['query']}\u201d")
        render_stat_strip(results_list)
        st.write("")
        for i, item in enumerate(results_list, start=1):
            render_result_card(i, item)

elif not submitted:
    st.markdown(
        """
        <div class='empty-state'>
            <div class='empty-icon'>🔎</div>
            <div class='empty-title'>Start your research</div>
            <div class='empty-text'>Enter a topic above — competitors, market trends, industry benchmarks — and AI will pull together sourced summaries.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )