"""Reusable CSS styles for the Streamlit app."""

import streamlit as st


def apply_base_styles(font_size_px: int = 18) -> None:
    st.markdown(
        f"""
<style>
    .stApp, .main, .block-container {{
        font-size: {font_size_px}px !important;
    }}
    html, body, [class*="css"] {{
        font-size: {font_size_px}px !important;
    }}
    .stMarkdown p, .stMarkdown li, .stMarkdown span,
    .element-container p, .element-container li,
    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stMarkdownContainer"] li,
    div[data-testid="stCaptionContainer"],
    div[data-testid="stCaptionContainer"] p,
    .stCaption,
    label, .stSelectbox label, .stTextInput label, .stNumberInput label,
    .stTextInput input, .stNumberInput input, .stSelectbox > div > div,
    .stTextArea textarea,
    .stButton button,
    .stAlert,
    .stRadio label,
    .stCheckbox label,
    [data-testid="stSidebar"] *,
    [data-testid="stForm"] * {{
        font-size: {font_size_px}px !important;
        line-height: 1.5 !important;
    }}
    .stButton button {{
        padding-top: 0.6rem !important;
        padding-bottom: 0.6rem !important;
    }}
</style>
""",
        unsafe_allow_html=True,
    )
