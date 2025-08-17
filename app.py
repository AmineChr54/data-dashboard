import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import src.logic as logic
import src.containers as containers

# ----------------------------
# Title
# ----------------------------
st.set_page_config(page_title="Data Analysis Dashboard", layout="wide")
st.title("📊 Interactive Data Dashboard")

# ----------------------------
# File Upload
# ----------------------------
df = logic.select_dataset()

# Data Configurations 
# ----------------------------
col_data1, col_data2, col_data3 = st.columns([1, 1, 1])
with col_data1:
    st.subheader("🔍 Column Selection")
    selected_columns = st.multiselect(
        "Select columns to include", df.columns.tolist(), default=df.columns.tolist(), key="selected_columns"
    )

with col_data2:
    st.subheader("📊 Data Options")
    dropna_option = st.radio(
        "Drop NA values",
        ["None", "Drop NA (All)", "Drop NA (X-axis)", "Drop NA (Y-axis)"],
        index=0,
        key="dropna_option"
    )
    if st.button("Reset All", key="reset_all"):
        for k in ["selected_columns", "x_axis", "y_axis", "dropna_option", "file_selector"]:
            if k in st.session_state:
                st.session_state.pop(k)

# Apply selected columns first, then apply dropna options to the filtered DataFrame
df_filtered = df[selected_columns]
if dropna_option == "Drop NA (All)":
    df_filtered = df_filtered.dropna()
elif dropna_option == "Drop NA (X-axis)" and "x_axis" in st.session_state:
    df_filtered = df_filtered.dropna(subset=[st.session_state["x_axis"]])
elif dropna_option == "Drop NA (Y-axis)" and "y_axis" in st.session_state:
    df_filtered = df_filtered.dropna(subset=[st.session_state["y_axis"]])

with col_data3:
    st.subheader("📈 Data Summary")
    st.write("Number of rows:", df_filtered.shape[0])
    st.write("Number of columns:", df_filtered.shape[1])

# Use the filtered dataframe for preview and plotting
df = df_filtered
st.subheader("🔎 Dataset Preview")
st.dataframe(df.head())

# ----------------------------
# Select Columns for Plot
# ----------------------------

st.subheader("⚙️ Select Features")
all_columns = df.columns.tolist()

# Custom CSS for small selectboxes and flex layout
st.markdown("""
    <style>
    .flex-row {
        display: flex;
        align-items: flex-start;
        gap: 32px;
    }
    .small-selectbox {
        max-width: 140px !important;
        min-width: 100px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Create selectboxes with small width using st.markdown and st.selectbox
col1, col2 = st.columns([1, 3])
with col1:
    x_axis, y_axis, chart_type = containers.select_features(all_columns)
with col2:
    st.subheader("📈 Visualization")
    if chart_type == "Scatter":
        fig = px.scatter(df, x=x_axis, y=y_axis)
    elif chart_type == "Line":
        fig = logic.plot_line(df, x_axis, y_axis)
    elif chart_type == "Bar":
        fig = px.bar(df, x=x_axis, y=y_axis)
    st.plotly_chart(fig, use_container_width=True)
