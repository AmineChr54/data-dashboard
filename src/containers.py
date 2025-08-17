import streamlit as st
import pandas as pd


def select_features(all_columns):
    """Render selectboxes and radio for feature selection and return (x_axis, y_axis, chart_type)."""
    x_axis = st.selectbox("Select X-axis", all_columns, key="x_axis")
    st.markdown(
        '<style>div[data-baseweb="select"]:has(div[aria-label="x_axis"]){max-width:140px !important;min-width:100px !important;}</style>',
        unsafe_allow_html=True,
    )
    st.button("Reset", key="reset_x_axis", on_click=lambda: st.session_state.pop("x_axis", None))

    y_axis = st.selectbox("Select Y-axis", all_columns, key="y_axis")
    st.markdown(
        '<style>div[data-baseweb="select"]:has(div[aria-label="y_axis"]){max-width:140px !important;min-width:100px !important;}</style>',
        unsafe_allow_html=True,
    )
    st.button("Reset", key="reset_y_axis", on_click=lambda: st.session_state.pop("y_axis", None))

    chart_type = st.radio("Select Chart Type", ["Scatter", "Line", "Bar"])

    return x_axis, y_axis, chart_type

