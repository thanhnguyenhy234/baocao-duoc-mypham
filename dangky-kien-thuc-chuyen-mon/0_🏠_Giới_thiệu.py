"""Trang giới thiệu khóa cập nhật kiến thức chuyên môn dược."""
from pathlib import Path

import streamlit as st

from utils.styles import apply_base_styles

COURSE_TITLE = "Cập nhật kiến thức chuyên môn dược"
COURSE_ORG = "Trường Cao đẳng Y tế Phú Thọ"
COURSE_LOCATION = "Hội trường Trường Cao đẳng Y tế Phú Thọ"
LOGO_PATH = Path(__file__).resolve().parent / "logo.jpg"
BANNER_PATH = Path(__file__).resolve().parent / "assets" / "banner-kien-thuc-chuyen-mon.png"

st.set_page_config(
    page_title="Đăng ký cập nhật kiến thức chuyên môn dược",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_base_styles(18)

st.markdown(
    """
<style>
    .info-box {background: #F0FDFA; border-left: 5px solid #0F766E; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;}
    .note-box {background: #F0FDF4; border-left: 5px solid #16A34A; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;}
    .banner-wrap img {border-radius: 18px; box-shadow: 0 10px 30px rgba(0,0,0,0.08);}
</style>
""",
    unsafe_allow_html=True,
)

if LOGO_PATH.exists():
    st.image(str(LOGO_PATH), width=140)

if BANNER_PATH.exists():
    st.markdown('<div class="banner-wrap">', unsafe_allow_html=True)
    st.image(str(BANNER_PATH), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📋 Thông tin khóa học")
    st.markdown(
        f"""
**Tên khóa học:** {COURSE_TITLE}

**Đơn vị tổ chức:** {COURSE_ORG}

**Nội dung chính**
- Cập nhật kiến thức chuyên môn dược mới nhất
- Hướng dẫn thực hành dược lâm sàng, sử dụng thuốc an toàn, hợp lý
- Giải đáp vướng mắc và trao đổi kinh nghiệm giữa các cơ sở y tế
"""
    )
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown(
        f"""
**📍 Địa điểm:** {COURSE_LOCATION}

**👥 Đối tượng:** dược sĩ, cán bộ y tế đang công tác tại các cơ sở y tế, nhà thuốc trên địa bàn tỉnh Phú Thọ.
"""
    )
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("### ✅ Hướng dẫn nhanh")
    st.markdown('<div class="note-box">', unsafe_allow_html=True)
    st.markdown(
        """
1. Vào menu **📝 Đăng ký**
2. Điền 6 thông tin bắt buộc
3. Kiểm tra lại số CCCND/CCCD và số điện thoại
4. Nhấn **Gửi đăng ký**

Thông tin đăng ký sẽ được lưu và gửi thông báo về Discord.
"""
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

st.markdown("### 📌 Thông tin cần chuẩn bị")
st.markdown(
    """
- Họ và tên (ghi đúng như trên giấy tờ tùy thân)
- Số CCCND (9 số) hoặc số CCCD (12 số)
- Ngày cấp và nơi cấp
- Địa chỉ thường trú
- Số điện thoại liên hệ (10 số, bắt đầu bằng số 0)
"""
)

st.divider()
st.info("👉 Chọn **📝 Đăng ký** ở thanh bên trái để gửi phiếu đăng ký của bạn.")
