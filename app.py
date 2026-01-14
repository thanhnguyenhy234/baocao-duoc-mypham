"""
Entry point - redirect to Giới thiệu page
"""
import streamlit as st

st.set_page_config(
    page_title="Báo cáo Dược - Mỹ phẩm | Sở Y tế Phú Thọ",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Redirect to main page
exec(open("0_🏠_Giới_thiệu.py", encoding="utf-8").read())
