import streamlit as st
import pandas as pd
from workforce_model import calculate_workforce

# --------------------------------------------------
# PAGE SETUP
# --------------------------------------------------

st.set_page_config(
    page_title="AI Enabled Workforce & Capacity Planning",
    page_icon="🚀",
    layout="wide"
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("BU Wise Planning Parameters")

bus = [
    "UPS",
    "Cooling",
    "Power Products",
    "Power System",
    "Industrial Automation"
]

bu_parameters = {}

for bu in bus:

    st.sidebar.subheader(bu)

    bau = st.sidebar.slider(
        f"{bu} BAU Growth %",
        0,
        100,
        20,
        key=f"bau_{bu}"
    )

    dc = st.sidebar.slider(
        f"{bu} Data Center Surge %",
        0,
        100,
        20,
        key=f"dc_{bu}"
    )

    attr = st.sidebar.slider(
        f"{bu} Attrition %",
        0,
        30,
        8,
        key=f"attr_{bu}"
    )

    bu_parameters[bu] = {
        "BAU": bau,
        "DC": dc,
        "Attrition": attr
    }

# --------------------------------------------------
# MAIN
# --------------------------------------------------

st.title("🚀 AI Enabled Workforce & Capacity Planning")

st.markdown("""
Forecast workforce requirement based on:

- Breakdown Maintenance
- Preventive Maintenance
- Startup & Commissioning
- BAU Growth
- Data Center Surge
- Attrition Impact
""")

uploaded_file = st.file_uploader(
    "Upload workforce_input.csv",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("Input Data")

    st.dataframe(
        df,
        use_container_width=True
    )

    result = calculate_workforce(
        df,
        bu_parameters
    )

    st.subheader("Workforce Planning Results")

    st.dataframe(
        result,
        use_container_width=True
    )

    # KPI SECTION

    total_current = df["Current_SE"].sum()

    total_available = round(
        result["Available Engineers"].sum(),
        1
    )

    total_required = round(
        result["Required Engineers"].sum(),
        1
    )

    total_hiring = int(
        result["Additional Required"].sum()
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Current Engineers",
        total_current
    )

    c2.metric(
        "Available After Attrition",
        total_available
    )

    c3.metric(
        "Required Engineers",
        total_required
    )

    c4.metric(
        "Additional Hiring Required",
        total_hiring
    )

    # PRODUCT SUMMARY

    st.subheader("📦 Hiring Requirement by BU")

    product_summary = (
        result.groupby("Product")
        ["Additional Required"]
        .sum()
    )

    st.bar_chart(product_summary)

    # REGION SUMMARY

    st.subheader("🌍 Hiring Requirement by Region")

    region_summary = (
        result.groupby("Region")
        ["Additional Required"]
        .sum()
    )

    st.bar_chart(region_summary)

    # MATRIX

    st.subheader("📊 Product vs Region Hiring Matrix")

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

    # DOWNLOAD

    csv = result.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "⬇ Download Results",
        csv,
        "workforce_forecast.csv",
        "text/csv"
    )

else:

    st.info(
        "Upload workforce_input.csv to start analysis."
    )
