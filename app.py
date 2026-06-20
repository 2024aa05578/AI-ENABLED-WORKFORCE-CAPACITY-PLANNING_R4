
import streamlit as st
import pandas as pd
from workforce_model import calculate_workforce
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
