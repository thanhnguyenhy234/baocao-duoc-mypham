"""Entry point cho ứng dụng đăng ký cập nhật kiến thức chuyên môn dược."""
import streamlit as st

st.set_page_config(
    page_title="Đăng ký cập nhật kiến thức chuyên môn dược | Trường Cao đẳng Y tế Phú Thọ",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

exec(open("0_🏠_Giới_thiệu.py", encoding="utf-8").read())
