import streamlit as st
import pandas as pd

from workforce_model import calculate_workforce

st.set_page_config(
    page_title="AI Workforce Planning",
    layout="wide"
)

st.title("🚀 AI Enabled Workforce & Capacity Planning")

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

uploaded_file = st.file_uploader(
    "Upload Workforce Input File",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("Input Data")

    st.dataframe(df)

    result = calculate_workforce(
        df,
        bau_growth,
        dc_growth
    )

    st.subheader(
        "Region Wise & Product Wise Workforce Requirement"
    )

    st.dataframe(result)

    st.subheader(
        "Additional Engineers Required"
    )

    st.bar_chart(
        result.set_index("Product")
        ["Additional Required"]
    )

    st.subheader(
        "Regional Hiring Requirement"
    )

    region_summary = result.groupby(
        "Region"
    )["Additional Required"].sum()

    st.bar_chart(region_summary)

    st.subheader("Management Summary")

    total_required = result[
        "Additional Required"
    ].sum()

    st.metric(
        "Total Additional Engineers Required",
        total_required
    )
