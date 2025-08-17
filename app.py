import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import src.logic as logic
import src.containers as containers


# Title
st.set_page_config(page_title="Data Analysis Dashboard", layout="wide")
st.title("📊 Interactive Data Dashboard")

# File Upload
df = logic.select_dataset()

# Data Filtration 
df_filtered = containers.data_filtration(df)

# Use the filtered dataframe for preview and plotting
df = df_filtered
st.subheader("🔎 Dataset Preview")
st.dataframe(df.head())

# Visualization
containers.data_visualization(df)