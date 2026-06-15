import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI/Data Job Market Analytics",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# COLORS
# =====================================================

PRIMARY_COLOR = "#4F8EF7"
SECONDARY_COLOR = "#6FA8FF"
BACKGROUND_COLOR = "#F7FAFF"

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.main {
    background-color: #F7FAFF;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

[data-testid="metric-container"] {
    background-color: white;
    border-top: 5px solid #4F8EF7;
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0px 2px 12px rgba(0,0,0,0.06);
}

/* Tabs */

.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    margin-bottom: 25px;
}

.stTabs [data-baseweb="tab"] {
    background: white;
    border-radius: 14px;
    border: 1px solid #E6EEF9;
    padding: 12px 24px;
    font-weight: 600;
    color: #4F8EF7;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.04);
}

.stTabs [data-baseweb="tab"]:hover {
    background: #EEF5FF;
}

.stTabs [aria-selected="true"] {
    background-color: #4F8EF7 !important;
    color: white !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    display: none;
}

</style>
""", unsafe_allow_html=True)

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

raw_jobs_df = pd.read_sql(
    """
    SELECT *
    FROM raw_jobs
    """,
    engine
)

company_df = pd.read_sql(
    """
    SELECT *
    FROM company_statistics
    ORDER BY job_count DESC
    LIMIT 10
    """,
    engine
)

skills_df = pd.read_sql(
    """
    SELECT *
    FROM skills_frequency
    WHERE occurrences > 0
    ORDER BY occurrences DESC
    """,
    engine
)

contract_df = pd.read_sql(
    """
    SELECT *
    FROM contract_statistics
    ORDER BY job_count DESC
    """,
    engine
)

seniority_df = pd.read_sql(
    """
    SELECT *
    FROM seniority_statistics
    ORDER BY job_count DESC
    """,
    engine
)

location_df = pd.read_sql(
    """
    SELECT *
    FROM location_statistics
    WHERE location <> 'France'
    ORDER BY job_count DESC
    LIMIT 10
    """,
    engine
)

jobs_day_df = pd.read_sql(
    """
    SELECT *
    FROM jobs_by_day
    ORDER BY job_date
    """,
    engine
)

# =====================================================
# KAFKA STREAMING TABLES
# =====================================================

live_jobs_count_df = pd.read_sql(
    """
    SELECT COUNT(*) AS total
    FROM live_jobs
    """,
    engine
)

latest_live_jobs_df = pd.read_sql(
    """
    SELECT
        title,
        company,
        search_role,
        received_at
    FROM live_jobs
    ORDER BY received_at DESC
    LIMIT 10
    """,
    engine
)

# =====================================================
# KPI CALCULATIONS
# =====================================================

total_jobs = len(raw_jobs_df)

total_companies = raw_jobs_df["company"].nunique()

total_locations = raw_jobs_df["location"].nunique()

total_skills = len(
    skills_df[skills_df["occurrences"] > 0]
)

live_jobs_count = int(
    live_jobs_count_df["total"].iloc[0]
)

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<h1 style='text-align:center;
           font-size:42px;
           margin-bottom:0;'>
AI/Data Job Market Analytics
</h1>

<p style='text-align:center;
          color:gray;
          font-size:18px;'>
End-to-End ETL, ELT, PostgreSQL, Kafka & Streamlit Pipeline
</p>
""", unsafe_allow_html=True)

st.caption(
    f"Last refresh: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}"
)

st.divider()

# =====================================================
# TABS
# =====================================================

tab_batch, tab_kafka = st.tabs(
    [
        "Batch Analytics Pipeline",
        "Kafka Streaming Pipeline"
    ]
)

# =====================================================
# TAB 1 - BATCH PIPELINE
# =====================================================

with tab_batch:

    # =====================================================
    # KPI SECTION
    # =====================================================

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Job Offers",
        total_jobs
    )

    col2.metric(
        "Companies",
        total_companies
    )

    col3.metric(
        "Locations",
        total_locations
    )

    col4.metric(
        "Skills Found",
        total_skills
    )

    st.divider()

    st.markdown("## Market Insights")

    # =====================================================
    # ROW 1
    # =====================================================

    left, right = st.columns(2)

    with left:

        with st.container(border=True):

            fig_companies = px.bar(
                company_df,
                x="job_count",
                y="company",
                orientation="h",
                title="Top Recruiting Companies",
                color_discrete_sequence=[PRIMARY_COLOR]
            )

            fig_companies.update_layout(
                yaxis={'categoryorder': 'total ascending'}
            )

            st.plotly_chart(
                fig_companies,
                use_container_width=True
            )

    with right:

        with st.container(border=True):

            fig_skills = px.bar(
                skills_df,
                x="occurrences",
                y="skill",
                orientation="h",
                title="Most Requested Skills",
                color_discrete_sequence=[PRIMARY_COLOR]
            )

            fig_skills.update_layout(
                yaxis={'categoryorder': 'total ascending'}
            )

            st.plotly_chart(
                fig_skills,
                use_container_width=True
            )

    # =====================================================
    # ROW 2
    # =====================================================

    left, right = st.columns(2)

    with left:

        with st.container(border=True):

            fig_contract = px.pie(
                contract_df,
                names="contract_type",
                values="job_count",
                title="Contract Types",
                color_discrete_sequence=[
                    PRIMARY_COLOR,
                    "#8AB8FF",
                    "#C7DDFF"
                ]
            )

            st.plotly_chart(
                fig_contract,
                use_container_width=True
            )

    with right:

        with st.container(border=True):

            fig_seniority = px.pie(
                seniority_df,
                names="seniority",
                values="job_count",
                hole=0.45,
                title="Seniority Distribution",
                color_discrete_sequence=[
                    PRIMARY_COLOR,
                    "#8AB8FF",
                    "#C7DDFF",
                    "#E6F0FF"
                ]
            )

            st.plotly_chart(
                fig_seniority,
                use_container_width=True
            )

    # =====================================================
    # ROW 3
    # =====================================================

    left, right = st.columns(2)

    with left:

        with st.container(border=True):

            fig_location = px.bar(
                location_df,
                x="job_count",
                y="location",
                orientation="h",
                title="Top Locations",
                color_discrete_sequence=[PRIMARY_COLOR]
            )

            fig_location.update_layout(
                yaxis={'categoryorder': 'total ascending'}
            )

            st.plotly_chart(
                fig_location,
                use_container_width=True
            )

    with right:

        with st.container(border=True):

            fig_time = px.line(
                jobs_day_df,
                x="job_date",
                y="job_count",
                markers=True,
                title="Job Publications Over Time"
            )

            fig_time.update_traces(
                line_color=PRIMARY_COLOR
            )

            st.plotly_chart(
                fig_time,
                use_container_width=True
            )

# =====================================================
# TAB 2 - KAFKA PIPELINE
# =====================================================

with tab_kafka:

    st.markdown(
        """
        <div style="
            background-color:white;
            padding:25px;
            border-radius:18px;
            border-left:6px solid #4F8EF7;
            box-shadow:0px 2px 12px rgba(0,0,0,0.06);
            margin-top:25px;
            margin-bottom:25px;
        ">
            <h2 style="margin-bottom:5px;">
                Kafka Streaming Pipeline
            </h2>
            <p style="color:gray;margin-top:0;">
                Near real-time job offers received through Kafka Producer → Topic → Consumer → PostgreSQL
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col_stream_1, col_stream_2 = st.columns([1, 3])

    with col_stream_1:
        st.metric(
            "Live Jobs Streamed",
            live_jobs_count
        )

    with col_stream_2:
        st.dataframe(
            latest_live_jobs_df,
            use_container_width=True,
            hide_index=True
        )

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "ESILV MSc A4 • ETL & Pipeline Orchestration Final Project • Emma Coco"
)