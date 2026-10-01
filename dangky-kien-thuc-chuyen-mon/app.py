"""Entry point cho ứng dụng đăng ký cập nhật kiến thức chuyên môn dược.

App một trang: mở URL là vào thẳng form đăng ký, không có trang giới thiệu riêng.

Lưu ý kỹ thuật: khi thư mục `pages/` tồn tại, Streamlit chạy file entry point này
làm trang mặc định ở đường dẫn "/" (xem `_mpa_v1` trong streamlit/runtime/scriptrunner).
Vì vậy nếu app.py chỉ có `st.set_page_config` thì người dùng mở URL sẽ thấy trang trắng.
`st.navigation(...)` bên dưới đăng ký trang đăng ký duy nhất làm trang mặc định,
để URL gốc render thẳng form.
"""
import streamlit as st

st.set_page_config(
    page_title="Đăng ký cập nhật kiến thức chuyên môn dược | Trường Cao đẳng Y tế Phú Thọ",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.navigation(
    [
        st.Page(
            "pages/1_📝_Đăng_ký.py",
            title="📝 Đăng ký",
            default=True,
        )
    ]
).run()
