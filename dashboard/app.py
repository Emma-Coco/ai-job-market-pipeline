import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI/Data Job Market Analytics",
    page_icon="",
    layout="wide"
)

# =====================================================
# DESIGN TOKENS
# =====================================================

# Palette
INK        = "#0D1117"   # near-black pour les titres
SLATE      = "#3D4B60"   # corps de texte
STEEL      = "#6B7B8D"   # labels, captions
MIST       = "#EDF1F7"   # fonds de cartes
BORDER     = "#D8E1EC"   # séparateurs
AZURE      = "#2563EB"   # accent principal
AZURE_SOFT = "#DBEAFE"   # accent doux
SKY        = "#60A5FA"   # accent secondaire
CLOUD      = "#93C5FD"   # accent tertiaire

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

.main {{
    background-color: #F4F7FB;
}}

.block-container {{
    padding-top: 4.5rem;
    padding-bottom: 3rem;
    max-width: 1300px;
}}

/* ---- KPI CARDS ---- */
[data-testid="metric-container"] {{
    background: white;
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 20px 24px;
    box-shadow: none;
    transition: box-shadow 0.15s ease;
}}

[data-testid="metric-container"]:hover {{
    box-shadow: 0 4px 16px rgba(37, 99, 235, 0.08);
}}

[data-testid="metric-container"] [data-testid="stMetricLabel"] {{
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: {STEEL};
}}

[data-testid="metric-container"] [data-testid="stMetricValue"] {{
    font-size: 32px;
    font-weight: 700;
    color: {INK};
    font-family: 'DM Mono', monospace;
}}

/* ---- TABS ---- */
.stTabs [data-baseweb="tab-list"] {{
    gap: 4px;
    background: {MIST};
    padding: 4px;
    border-radius: 10px;
    margin-bottom: 28px;
    border-bottom: none;
}}

.stTabs [data-baseweb="tab"] {{
    background: transparent;
    border-radius: 7px;
    border: none;
    padding: 9px 20px;
    font-weight: 500;
    font-size: 14px;
    color: {SLATE};
    box-shadow: none;
}}

.stTabs [data-baseweb="tab"]:hover {{
    background: white;
    color: {INK};
}}

.stTabs [aria-selected="true"] {{
    background: white !important;
    color: {AZURE} !important;
    font-weight: 600 !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08) !important;
}}

.stTabs [data-baseweb="tab-highlight"] {{
    display: none;
}}

/* ---- CONTAINERS / CHARTS ---- */
[data-testid="stVerticalBlockBorderWrapper"] {{
    background: white;
    border: 1px solid {BORDER} !important;
    border-radius: 14px !important;
    padding: 4px !important;
    box-shadow: none;
}}

/* ---- DATAFRAME ---- */
[data-testid="stDataFrame"] {{
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid {BORDER};
}}

/* ---- DIVIDER ---- */
hr {{
    border-color: {BORDER};
    margin: 1.5rem 0;
}}

/* ---- CAPTION ---- */
[data-testid="stCaptionContainer"] {{
    color: {STEEL};
    font-size: 12px;
    font-family: 'DM Mono', monospace;
}}
</style>
""", unsafe_allow_html=True)

# =====================================================
# PLOTLY THEME HELPER
# =====================================================

CHART_LAYOUT = dict(
    font_family="Inter",
    font_color=SLATE,
    title_font_family="Inter",
    title_font_color=INK,
    title_font_size=15,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(t=44, l=0, r=0, b=0),
    showlegend=True,
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        borderwidth=0,
        font_size=12,
    ),
)

AXIS_STYLE = dict(
    showgrid=True,
    gridcolor=MIST,
    gridwidth=1,
    zeroline=False,
    tickfont=dict(size=12, family="DM Mono"),
    tickcolor=BORDER,
    linecolor=BORDER,
)

# Variante sans grille (axes Y des bar charts horizontaux)
AXIS_STYLE_NO_GRID = {**AXIS_STYLE, "showgrid": False}

PIE_COLORS = [AZURE, SKY, CLOUD, "#BFDBFE", "#EFF6FF"]

# =====================================================
# DATABASE CONNECTION
# =====================================================

DB_USER = "admin"
DB_PASSWORD = "admin"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "jobs_db"

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# =====================================================
# LOAD TABLES
# =====================================================

raw_jobs_df = pd.read_sql("SELECT * FROM raw_jobs", engine)

company_df = pd.read_sql(
    "SELECT * FROM company_statistics ORDER BY job_count DESC LIMIT 10",
    engine
)

skills_df = pd.read_sql(
    "SELECT * FROM skills_frequency WHERE occurrences > 0 ORDER BY occurrences DESC",
    engine
)

contract_df = pd.read_sql(
    "SELECT * FROM contract_statistics ORDER BY job_count DESC",
    engine
)

seniority_df = pd.read_sql(
    "SELECT * FROM seniority_statistics ORDER BY job_count DESC",
    engine
)

location_df = pd.read_sql(
    """
    SELECT * FROM location_statistics
    WHERE location <> 'France'
    ORDER BY job_count DESC LIMIT 10
    """,
    engine
)

jobs_day_df = pd.read_sql(
    "SELECT * FROM jobs_by_day ORDER BY job_date",
    engine
)

live_jobs_count_df = pd.read_sql("SELECT COUNT(*) AS total FROM live_jobs", engine)

latest_live_jobs_df = pd.read_sql(
    """
    SELECT title, company, search_role, received_at
    FROM live_jobs ORDER BY received_at DESC LIMIT 10
    """,
    engine
)

# =====================================================
# KPI CALCULATIONS
# =====================================================

total_jobs      = len(raw_jobs_df)
total_companies = raw_jobs_df["company"].nunique()
total_locations = raw_jobs_df["location"].nunique()
total_skills    = len(skills_df[skills_df["occurrences"] > 0])
live_jobs_count = int(live_jobs_count_df["total"].iloc[0])

# =====================================================
# HEADER
# =====================================================

st.markdown(f"""
<div style="margin-bottom: 8px;">
    <p style="
        margin: 0 0 6px 0;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: {AZURE};
        font-family: 'DM Mono', monospace;
    ">ESILV MSc A4 — ETL & Pipeline Orchestration</p>
    <h1 style="
        margin: 0;
        font-size: 36px;
        font-weight: 700;
        color: {INK};
        letter-spacing: -0.5px;
        line-height: 1.1;
    ">AI / Data Job Market</h1>
    <p style="
        margin: 6px 0 0 0;
        font-size: 15px;
        color: {STEEL};
        font-weight: 400;
    ">End-to-end pipeline — PostgreSQL, Kafka & Streamlit</p>
</div>
""", unsafe_allow_html=True)

st.caption(f"Last refresh: {pd.Timestamp.now().strftime('%Y-%m-%d  %H:%M:%S')}")

st.divider()

# =====================================================
# TABS
# =====================================================

tab_batch, tab_kafka = st.tabs([
    "Batch Analytics Pipeline",
    "Kafka Streaming Pipeline"
])

# =====================================================
# TAB 1 — BATCH PIPELINE
# =====================================================

with tab_batch:

    # ---- KPIs ----

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Job Offers",    total_jobs)
    col2.metric("Companies",     total_companies)
    col3.metric("Locations",     total_locations)
    col4.metric("Skills Found",  total_skills)

    st.divider()

    # ---- Section label ----

    st.markdown(f"""
    <p style="
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: {STEEL};
        margin-bottom: 16px;
        font-family: 'DM Mono', monospace;
    ">Market Insights</p>
    """, unsafe_allow_html=True)

    # ---- ROW 1 — Bar charts ----

    left, right = st.columns(2)

    with left:
        with st.container(border=True):
            fig = px.bar(
                company_df,
                x="job_count",
                y="company",
                orientation="h",
                title="Top Recruiting Companies",
                color_discrete_sequence=[AZURE],
            )
            fig.update_layout(**CHART_LAYOUT)
            fig.update_xaxes(**AXIS_STYLE, title=None)
            fig.update_yaxes(
                **AXIS_STYLE_NO_GRID,
                title=None,
                categoryorder="total ascending",
            )
            fig.update_traces(marker_cornerradius=4)
            st.plotly_chart(fig, use_container_width=True)

    with right:
        with st.container(border=True):
            fig = px.bar(
                skills_df,
                x="occurrences",
                y="skill",
                orientation="h",
                title="Most Requested Skills",
                color_discrete_sequence=[SKY],
            )
            fig.update_layout(**CHART_LAYOUT)
            fig.update_xaxes(**AXIS_STYLE, title=None)
            fig.update_yaxes(
                **AXIS_STYLE_NO_GRID,
                title=None,
                categoryorder="total ascending",
            )
            fig.update_traces(marker_cornerradius=4)
            st.plotly_chart(fig, use_container_width=True)

    # ---- ROW 2 — Pie charts ----

    left, right = st.columns(2)

    with left:
        with st.container(border=True):
            fig = px.pie(
                contract_df,
                names="contract_type",
                values="job_count",
                title="Contract Types",
                color_discrete_sequence=PIE_COLORS,
            )
            fig.update_traces(
                textposition="inside",
                textinfo="percent+label",
                textfont_size=12,
                marker=dict(line=dict(color="white", width=2)),
                hovertemplate="%{label}<br>%{value} offers<extra></extra>",
            )
            fig.update_layout(**CHART_LAYOUT)
            st.plotly_chart(fig, use_container_width=True)

    with right:
        with st.container(border=True):
            fig = px.pie(
                seniority_df,
                names="seniority",
                values="job_count",
                hole=0.5,
                title="Seniority Distribution",
                color_discrete_sequence=PIE_COLORS,
            )
            fig.update_traces(
                textposition="inside",
                textinfo="percent+label",
                textfont_size=12,
                marker=dict(line=dict(color="white", width=2)),
                hovertemplate="%{label}<br>%{value} offers<extra></extra>",
            )
            fig.update_layout(**CHART_LAYOUT)
            st.plotly_chart(fig, use_container_width=True)

    # ---- ROW 3 — Location + Time ----

    left, right = st.columns(2)

    with left:
        with st.container(border=True):
            fig = px.bar(
                location_df,
                x="job_count",
                y="location",
                orientation="h",
                title="Top Locations",
                color_discrete_sequence=[AZURE],
            )
            fig.update_layout(**CHART_LAYOUT)
            fig.update_xaxes(**AXIS_STYLE, title=None)
            fig.update_yaxes(
                **AXIS_STYLE_NO_GRID,
                title=None,
                categoryorder="total ascending",
            )
            fig.update_traces(marker_cornerradius=4)
            st.plotly_chart(fig, use_container_width=True)

    with right:
        with st.container(border=True):
            fig = px.area(
                jobs_day_df,
                x="job_date",
                y="job_count",
                title="Job Publications Over Time",
            )
            fig.update_traces(
                line_color=AZURE,
                fillcolor=AZURE_SOFT,
                line_width=2,
                marker=dict(size=5, color=AZURE),
            )
            fig.update_layout(**CHART_LAYOUT)
            fig.update_xaxes(**AXIS_STYLE, title=None)
            fig.update_yaxes(**AXIS_STYLE, title=None)
            st.plotly_chart(fig, use_container_width=True)

# =====================================================
# TAB 2 — KAFKA PIPELINE
# =====================================================

with tab_kafka:

    st.markdown(f"""
    <div style="
        background: white;
        border: 1px solid {BORDER};
        border-left: 4px solid {AZURE};
        border-radius: 12px;
        padding: 24px 28px;
        margin: 16px 0 28px 0;
    ">
        <p style="
            margin: 0 0 4px 0;
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: {AZURE};
            font-family: 'DM Mono', monospace;
        ">Streaming</p>
        <h2 style="margin: 0 0 6px 0; color: {INK}; font-size: 22px;">Kafka Pipeline</h2>
        <p style="margin: 0; color: {STEEL}; font-size: 14px;">
            Near real-time ingestion — Producer → Topic → Consumer → PostgreSQL
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])

    with col1:
        st.metric("Live Jobs Streamed", live_jobs_count)

    with col2:
        st.dataframe(
            latest_live_jobs_df,
            use_container_width=True,
            hide_index=True,
        )

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption("Emma Coco — ESILV MSc A4 — ETL & Pipeline Orchestration Final Project")
