import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

def plot_line(df: pd.DataFrame, x_axis: str, y_axis: str):
    # prepare data for a continuous line
    df_plot = df[[x_axis, y_axis]].dropna()

    # convert x to numeric or datetime if needed
    # try numeric first, if fails try datetime
    try:
        df_plot[x_axis] = pd.to_numeric(df_plot[x_axis], errors='coerce')
    except Exception:
        pass
    if df_plot[x_axis].dtype == 'object':
        df_plot[x_axis] = pd.to_datetime(df_plot[x_axis], errors='coerce')

    # drop any rows with conversion failures and sort by x
    df_plot = df_plot.dropna(subset=[x_axis, y_axis]).sort_values(by=x_axis)

    # if there are multiple y per x, aggregate (mean) so x->single y
    if df_plot[x_axis].duplicated().any():
        df_plot = df_plot.groupby(x_axis, as_index=False)[y_axis].mean()

    # optional: interpolate to get a smoother continuous curve (produces intermediate points)
    df_interp = df_plot.set_index(x_axis).interpolate(method='index').reset_index()

    # build the line figure (spline for smoothing, mode lines only)
    fig = px.line(df_interp, x=x_axis, y=y_axis, line_shape='spline', render_mode='svg')
    fig.update_traces(mode='lines', line=dict(width=2), marker={'size': 0})

    return fig

def select_dataset():
    # uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    data_folder = Path(__file__).parent.parent / "data"
    if not data_folder.exists():
        st.error(f"Data folder '{data_folder}' does not exist. Please create it and add CSV files.")
        st.stop()

    data_files = [f.name for f in data_folder.glob("*.csv")]
    if not data_files:
        st.error(f"No CSV files found in '{data_folder}'. Please add at least one CSV file.")
        st.stop()
    file_selector = st.selectbox("Select Dataset", data_files, key="file_selector")
    st.markdown('<style>div[data-baseweb="select"]:has(div[aria-label="file_selector"]){max-width:300px !important;min-width:200px !important;}</style>', unsafe_allow_html=True)
    uploaded_file = data_folder / st.session_state["file_selector"]
    if not uploaded_file.exists():
        st.error(f"File {uploaded_file} does not exist. Please upload a valid CSV file.")
        st.stop()
    # Read CSV
    df = pd.read_csv(uploaded_file)
    return df