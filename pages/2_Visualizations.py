import html
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# CSS — same design system as app.py / other pages, embedded
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

.section-sub {
  font-size: 12px;
  color: var(--text-tertiary);
  margin: -4px 0 12px;
}

.section-divider {
  height: 1px;
  background: var(--border-subtle);
  margin-bottom: 16px;
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

/* ---------- Chart cards ---------- */

.chart-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 14px 16px 4px;
  margin-bottom: 14px;
  transition: border-color 0.12s ease;
}

.chart-card:hover {
  border-color: var(--border-strong);
}

.chart-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2px;
}

.chart-card-title {
  font-size: 13px;
  font-weight: 700;
  color: var(--text-primary);
}

.chart-card-tag {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--text-tertiary);
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--border-subtle);
  border-radius: 4px;
  padding: 2px 6px;
}

/* ---------- Mini stat cards (distribution summary) ---------- */

.mini-stat {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 10px 14px;
  margin-bottom: 8px;
  font-size: 12.5px;
}

.mini-stat-label {
  color: var(--text-tertiary);
  font-weight: 600;
}

.mini-stat-value {
  color: var(--text-primary);
  font-weight: 700;
  font-variant-numeric: tabular-nums;
}

/* ---------- Empty / info states ---------- */

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

.inline-note {
  font-size: 12.5px;
  color: var(--text-tertiary);
  background: var(--bg-panel);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 10px 14px;
  margin-bottom: 12px;
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

/* ---------- Streamlit widget overrides ---------- */

[data-testid="stButton"] button, [data-testid="stDownloadButton"] button {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-subtle) !important;
  color: var(--text-primary) !important;
  border-radius: var(--radius-sm) !important;
  font-weight: 600 !important;
  padding: 0.4rem 0.9rem !important;
  font-size: 12.5px !important;
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

[data-testid="stSelectbox"] > div, [data-testid="stMultiSelect"] > div {
  background: var(--bg-input) !important;
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
# DATA HELPERS
# ============================================================

def get_column_types(df, result):
    """Prefer the AnalysisAgent's own classification (if available in
    session state) and fall back to dtype inference — no recomputation
    of the agent's logic, just a safe default when it's missing."""
    numeric_cols = (result or {}).get("numeric_columns") or df.select_dtypes(include="number").columns.tolist()
    categorical_cols = (result or {}).get("categorical_columns") or df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()
    datetime_cols = df.select_dtypes(include=["datetime64[ns]", "datetimetz"]).columns.tolist()

    numeric_cols = [c for c in numeric_cols if c in df.columns]
    categorical_cols = [c for c in categorical_cols if c in df.columns and c not in datetime_cols]

    return numeric_cols, categorical_cols, datetime_cols


def format_value(value):
    try:
        if isinstance(value, bool):
            return str(value)
        if pd.isna(value):
            return "—"
        if isinstance(value, int):
            return f"{value:,}"
        if isinstance(value, float):
            return f"{int(value):,}" if value.is_integer() else f"{value:,.2f}"
        return str(value)
    except Exception:
        return str(value)


# ============================================================
# PRESENTATION HELPERS
# ============================================================

def section_header(icon, title, sub=None):
    sub_html = f"<div class='section-sub'>{html.escape(sub)}</div>" if sub else ""
    st.markdown(
        f"""
        <div class='section-row'>
            <div class='section-title'><span class='icon'>{icon}</span>{html.escape(title)}</div>
            {sub_html}
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


def theme_chart(fig, title=None, height=420):
    """Apply the same dark, professional theme to every chart on this
    page — consistent fonts, gridlines, colorway and hover styling."""
    if title:
        fig.update_layout(title=dict(text=title, x=0.0, xanchor="left"))
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#9AA4B2", size=12),
        title_font=dict(color="#E7EBF3", size=14),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11), orientation="h", y=-0.18),
        margin=dict(l=10, r=10, t=46, b=10),
        height=height,
        colorway=["#3B82F6", "#6366F1", "#22C55E", "#F59E0B", "#EC4899", "#14B8A6", "#F472B6", "#A78BFA"],
        hoverlabel=dict(bgcolor="#161B24", font_size=12, font_family="Inter, sans-serif", bordercolor="rgba(255,255,255,0.12)"),
    )
    fig.update_xaxes(
        gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.08)",
        title_font=dict(size=12), tickfont=dict(size=11),
    )
    fig.update_yaxes(
        gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.08)",
        title_font=dict(size=12), tickfont=dict(size=11),
    )
    return fig


def render_chart_card(fig, title, icon="📊", key=None, height=420, tag=None):
    """Wrap any plotly figure in the same chart-card shell used on the
    Dashboard, with a title bar and an optional PNG export."""
    fig = theme_chart(fig, height=height)
    tag_html = f"<span class='chart-card-tag'>{html.escape(tag)}</span>" if tag else ""
    st.markdown(
        f"""
        <div class='chart-card'>
            <div class='chart-card-header'>
                <span class='chart-card-title'>{icon} {html.escape(title)}</span>
                {tag_html}
            </div>
        """,
        unsafe_allow_html=True,
    )
    st.plotly_chart(fig, width="stretch", key=key)

    try:
        img_bytes = fig.to_image(format="png", scale=2)
        st.download_button(
            "⬇ Download PNG", img_bytes, file_name=f"{key or 'chart'}.png",
            mime="image/png", key=f"dl_{key}",
        )
    except Exception:
        pass

    st.markdown("</div>", unsafe_allow_html=True)


def render_stat_strip(numeric_cols, categorical_cols, datetime_cols, chart_count):
    st.markdown(
        f"""
        <div class='stat-strip'>
            <div class='stat-pill'><span class='dot' style='background:var(--accent)'></span>
                <span class='num'>{chart_count}</span><span class='lbl'>AI-generated charts</span></div>
            <div class='stat-pill'><span class='dot' style='background:var(--success)'></span>
                <span class='num'>{len(numeric_cols)}</span><span class='lbl'>numeric columns</span></div>
            <div class='stat-pill'><span class='dot' style='background:var(--warning)'></span>
                <span class='num'>{len(categorical_cols)}</span><span class='lbl'>categorical columns</span></div>
            <div class='stat-pill'><span class='dot' style='background:var(--text-tertiary)'></span>
                <span class='num'>{len(datetime_cols)}</span><span class='lbl'>date columns</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_mini_stats(series):
    stats = [
        ("Mean", series.mean()), ("Median", series.median()), ("Std Dev", series.std()),
        ("Min", series.min()), ("Max", series.max()), ("Count", series.count()),
    ]
    parts = []
    for label, val in stats:
        parts.append(
            f"<div class='mini-stat'><span class='mini-stat-label'>{label}</span>"
            f"<span class='mini-stat-value'>{format_value(val)}</span></div>"
        )
    st.markdown("".join(parts), unsafe_allow_html=True)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Visualizations",
    page_icon="📈",
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
            <div class='main-title'>Visualizations</div>
            <div class='subtitle'>Interactive, presentation-ready charts built from your dataset</div>
        </div>
        <div class='top-meta'>{datetime.now().strftime('%b %d, %Y · %I:%M %p')}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# BODY
# ============================================================

df = st.session_state.get("dataframe")
charts = st.session_state.get("charts", [])

if df is None:

    st.markdown(
        """
        <div class='empty-state'>
            <div class='empty-icon'>📈</div>
            <div class='empty-title'>No dataset loaded</div>
            <div class='empty-text'>Upload an Excel file on the Dashboard first, then come back here to explore your data visually.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("app.py", label="Go to Dashboard", icon="📊")

else:

    result = st.session_state.get("analysis_result", {})
    numeric_cols, categorical_cols, datetime_cols = get_column_types(df, result)

    render_stat_strip(numeric_cols, categorical_cols, datetime_cols, len(charts))

    # ---------- SECTION 1: AI-Generated Charts ----------
    if charts:
        section_header("🤖", "AI-Generated Charts", sub="Produced automatically by the Visualization Agent")
        cols = st.columns(2)
        for i, chart in enumerate(charts):
            try:
                chart_title = chart.layout.title.text
            except Exception:
                chart_title = None
            title = chart_title or f"Chart {i + 1}"
            with cols[i % 2]:
                render_chart_card(chart, title, icon="📊", key=f"agent_chart_{i}", tag="AUTO")

    # ---------- SECTION 2: Explore Your Data ----------
    section_header("🔍", "Explore Your Data", sub="Build your own views — pick columns, the chart updates instantly")

    tab_dist, tab_comp, tab_compose, tab_rel, tab_trend = st.tabs(
        ["📊 Distributions", "📐 Comparisons", "🥧 Composition", "🔗 Relationships", "📈 Trends"]
    )

    # ---- Distributions ----
    with tab_dist:
        if not numeric_cols:
            st.caption("No numeric columns available for distribution analysis.")
        else:
            col = st.selectbox("Numeric column", numeric_cols, key="dist_col")
            c1, c2 = st.columns([3, 1])
            with c1:
                fig = px.histogram(
                    df, x=col, nbins=30, marginal="box", opacity=0.88,
                    color_discrete_sequence=["#3B82F6"],
                    labels={col: col.replace("_", " ").title()},
                )
                fig.update_traces(marker_line_width=0)
                render_chart_card(fig, f"Distribution of {col}", icon="📊", key=f"hist_{col}", tag="HISTOGRAM")
            with c2:
                st.markdown("<div class='caption-muted'>Summary statistics</div>", unsafe_allow_html=True)
                render_mini_stats(df[col].dropna())

    # ---- Comparisons ----
    with tab_comp:
        if not categorical_cols or not numeric_cols:
            st.caption("Need at least one categorical and one numeric column for comparisons.")
        else:
            c1, c2, c3 = st.columns(3)
            with c1:
                cat_col = st.selectbox("Category", categorical_cols, key="comp_cat")
            with c2:
                num_col = st.selectbox("Metric", numeric_cols, key="comp_num")
            with c3:
                agg = st.selectbox("Aggregation", ["mean", "sum", "median", "count"], key="comp_agg")

            grouped = (
                df.groupby(cat_col)[num_col]
                .agg(agg)
                .reset_index()
                .sort_values(num_col, ascending=False)
                .head(15)
            )
            fig = px.bar(
                grouped, x=cat_col, y=num_col, color=num_col,
                color_continuous_scale=["#1e3a8a", "#3B82F6", "#818CF8"],
                text_auto=".2s",
                labels={cat_col: cat_col.replace("_", " ").title(), num_col: num_col.replace("_", " ").title()},
            )
            fig.update_layout(coloraxis_showscale=False)
            fig.update_traces(textfont_size=11, textposition="outside")
            render_chart_card(
                fig, f"{agg.title()} {num_col} by {cat_col} (top 15)", icon="📐",
                key=f"bar_{cat_col}_{num_col}_{agg}", tag="BAR",
            )

    # ---- Composition ----
    with tab_compose:
        if not categorical_cols:
            st.caption("No categorical columns available for composition analysis.")
        else:
            cat_col = st.selectbox("Category", categorical_cols, key="pie_cat")
            counts = df[cat_col].value_counts()
            top = counts.head(8)
            other_sum = counts.iloc[8:].sum()
            if other_sum > 0:
                top = pd.concat([top, pd.Series({"Other": other_sum})])

            fig = px.pie(
                values=top.values, names=top.index.astype(str), hole=0.55,
            )
            fig.update_traces(
                textinfo="percent+label", textfont_size=11,
                pull=[0.03] * len(top), marker=dict(line=dict(color="#0B0E13", width=2)),
            )
            render_chart_card(fig, f"Composition of {cat_col} (top 8)", icon="🥧", key=f"pie_{cat_col}", tag="DONUT")

    # ---- Relationships ----
    with tab_rel:
        if len(numeric_cols) < 2:
            st.caption("Need at least two numeric columns for relationship analysis.")
        else:
            c1, c2, c3 = st.columns(3)
            with c1:
                x_col = st.selectbox("X axis", numeric_cols, index=0, key="scat_x")
            with c2:
                y_idx = 1 if len(numeric_cols) > 1 else 0
                y_col = st.selectbox("Y axis", numeric_cols, index=y_idx, key="scat_y")
            with c3:
                color_choice = st.selectbox("Color by", ["None"] + categorical_cols, key="scat_color")
            color_arg = None if color_choice == "None" else color_choice

            try:
                fig = px.scatter(
                    df, x=x_col, y=y_col, color=color_arg, opacity=0.75, trendline="ols",
                    labels={x_col: x_col.replace("_", " ").title(), y_col: y_col.replace("_", " ").title()},
                )
            except Exception:
                fig = px.scatter(
                    df, x=x_col, y=y_col, color=color_arg, opacity=0.75,
                    labels={x_col: x_col.replace("_", " ").title(), y_col: y_col.replace("_", " ").title()},
                )
            render_chart_card(fig, f"{y_col} vs {x_col}", icon="🔗", key=f"scatter_{x_col}_{y_col}", tag="SCATTER")

            if len(numeric_cols) >= 3:
                corr = df[numeric_cols].corr().round(2)
                fig2 = go.Figure(
                    data=go.Heatmap(
                        z=corr.values, x=corr.columns, y=corr.columns,
                        colorscale=[[0, "#EF4444"], [0.5, "#161B24"], [1, "#22C55E"]],
                        zmid=0, text=corr.values, texttemplate="%{text}",
                        hovertemplate="%{x} × %{y}: %{z}<extra></extra>",
                    )
                )
                render_chart_card(fig2, "Correlation Matrix", icon="🧮", key="corr_heatmap", height=480, tag="HEATMAP")

    # ---- Trends ----
    with tab_trend:
        if not datetime_cols or not numeric_cols:
            st.markdown(
                "<div class='inline-note'>No date/time column was detected in this dataset, "
                "so a time-trend view isn't available here.</div>",
                unsafe_allow_html=True,
            )
        else:
            c1, c2 = st.columns(2)
            with c1:
                dt_col = st.selectbox("Date column", datetime_cols, key="trend_dt")
            with c2:
                num_col = st.selectbox("Metric", numeric_cols, key="trend_num")

            ts = df[[dt_col, num_col]].dropna().sort_values(dt_col)
            fig = px.line(
                ts, x=dt_col, y=num_col, markers=True,
                labels={dt_col: "Date", num_col: num_col.replace("_", " ").title()},
            )
            fig.update_traces(line=dict(width=2.5))
            render_chart_card(fig, f"{num_col} over time", icon="📈", key=f"line_{dt_col}_{num_col}", tag="TIME SERIES")