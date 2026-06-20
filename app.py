import streamlit as st
import pandas as pd

from workforce_model import calculate_workforce

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="AI Enabled Workforce & Capacity Planning",
    page_icon="🚀",
    layout="wide"
)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("Growth Parameters")

bau_growth = st.sidebar.slider(
    "BAU Growth %",
    min_value=0,
    max_value=100,
    value=20
)

dc_growth = st.sidebar.slider(
    "Data Center Surge %",
    min_value=0,
    max_value=100,
    value=35
)

attrition = st.sidebar.slider(
    "Attrition %",
    min_value=0,
    max_value=30,
    value=8
)

# -----------------------------
# TITLE
# -----------------------------
st.title("🚀 AI Enabled Workforce & Capacity Planning")

st.markdown(
    """
    Forecast Service Engineer requirements based on:
    - Business As Usual (BAU) Growth
    - Data Center Surge Growth
    - Attrition Impact
    - Product-wise Demand
    - Region-wise Demand
    """
)

# -----------------------------
# FILE UPLOAD
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload Workforce Input CSV",
    type=["csv"]
)

# -----------------------------
# PROCESS FILE
# -----------------------------
if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.subheader("📋 Input Data")

    st.dataframe(df, use_container_width=True)

    result = calculate_workforce(
        df,
        bau_growth,
        dc_growth,
        attrition
    )

    # -----------------------------
    # KPI SECTION
    # -----------------------------
    total_current_se = df["Current_SE"].sum()

    available_after_attrition = (
        total_current_se *
        (1 - attrition / 100)
    )

    total_required = result["Required Engineers"].sum()

    total_hiring_gap = result["Additional Required"].sum()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Current Engineers",
            round(total_current_se)
        )

    with col2:
        st.metric(
            "Available After Attrition",
            round(available_after_attrition)
        )

    with col3:
        st.metric(
            "Required Engineers",
            round(total_required)
        )

    with col4:
        st.metric(
            "Additional Hiring Required",
            round(total_hiring_gap)
        )

    # -----------------------------
    # RESULTS
    # -----------------------------
    st.subheader(
        "📊 Region-wise & Product-wise Workforce Requirement"
    )

    st.dataframe(
        result,
        use_container_width=True
    )

    # -----------------------------
    # PRODUCT SUMMARY
    # -----------------------------
    st.subheader(
        "📦 Hiring Requirement by Product"
    )

    product_summary = result.groupby(
        "Product"
    )["Additional Required"].sum()

    st.bar_chart(product_summary)

    # -----------------------------
    # REGION SUMMARY
    # -----------------------------
    st.subheader(
        "🌍 Hiring Requirement by Region"
    )

    region_summary = result.groupby(
        "Region"
    )["Additional Required"].sum()

    st.bar_chart(region_summary)

    # -----------------------------
    # PIVOT TABLE
    # -----------------------------
    st.subheader(
        "📈 Product vs Region Hiring Matrix"
    )

    pivot = result.pivot_table(
        values="Additional Required",
        index="Product",
        columns="Region",
        aggfunc="sum",
        fill_value=0
    )

    st.dataframe(
        pivot,
        use_container_width=True
    )

    # -----------------------------
    # DOWNLOAD RESULTS
    # -----------------------------
    csv = result.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇ Download Results",
        data=csv,
        file_name="workforce_forecast_output.csv",
        mime="text/csv"
    )

else:
    st.info(
        "Please upload Workforce Input CSV file to begin analysis."
    )
