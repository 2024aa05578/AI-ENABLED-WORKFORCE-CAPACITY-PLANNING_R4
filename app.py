import streamlit as st
import pandas as pd
from workforce_model import calculate_workforce

# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="AI Enabled Workforce & Capacity Planning",
    page_icon="🚀",
    layout="wide"
)

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

st.sidebar.header("Growth Parameters")

bau_growth = st.sidebar.slider(
    "BAU Growth %",
    0,
    100,
    20
)

dc_growth = st.sidebar.slider(
    "Data Center Surge %",
    0,
    100,
    35
)

attrition = st.sidebar.slider(
    "Attrition %",
    0,
    30,
    8
)

# -------------------------------------------------
# MAIN SCREEN
# -------------------------------------------------

st.title("🚀 AI Enabled Workforce & Capacity Planning")

uploaded_file = st.file_uploader(
    "Upload Workforce Input CSV",
    type=["csv"]
)

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

    st.subheader("📊 Workforce Planning Results")
    st.dataframe(result, use_container_width=True)

    # KPI Metrics
    total_current = df["Current_SE"].sum()

    total_available = round(
        total_current * (1 - attrition / 100),
        1
    )

    total_required = round(
        result["Required Engineers"].sum(),
        1
    )

    total_hiring = result["Additional Required"].sum()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Current Engineers", total_current)
    c2.metric("Available After Attrition", total_available)
    c3.metric("Required Engineers", total_required)
    c4.metric("Hiring Gap", total_hiring)

    # Product Summary
    st.subheader("📦 Hiring by Product")

    product_summary = (
        result.groupby("Product")
        ["Additional Required"]
        .sum()
    )

    st.bar_chart(product_summary)

    # Region Summary
    st.subheader("🌍 Hiring by Region")

    region_summary = (
        result.groupby("Region")
        ["Additional Required"]
        .sum()
    )

    st.bar_chart(region_summary)

    # Product vs Region Matrix
    st.subheader("📈 Product vs Region Matrix")

    pivot = result.pivot_table(
        values="Additional Required",
        index="Product",
        columns="Region",
        aggfunc="sum",
        fill_value=0
    )

    st.dataframe(pivot)

    # Download
    csv = result.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇ Download Results",
        data=csv,
        file_name="workforce_forecast.csv",
        mime="text/csv"
    )

else:

    st.info(
        "Upload a workforce_input.csv file to begin analysis."
    )
