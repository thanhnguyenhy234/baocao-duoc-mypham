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
    /* Form chia khối: tiêu đề khối nổi bật + đường phân cách rõ ranh giới */
    [data-testid="stForm"] h3 {{
        margin-top: 0.25rem !important;
        margin-bottom: 0.25rem !important;
    }}
    [data-testid="stForm"] hr {{
        margin-top: 0.75rem !important;
        margin-bottom: 0.75rem !important;
        border: none !important;
        border-top: 1px solid rgba(0, 128, 128, 0.35) !important;
    }}
</style>
""",
        unsafe_allow_html=True,
    )
