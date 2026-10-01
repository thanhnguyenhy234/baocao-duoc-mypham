"""Trang đăng ký cập nhật kiến thức chuyên môn dược."""
from datetime import date, datetime
from pathlib import Path

import streamlit as st

from utils.discord_webhook import send_registration_notification
from utils.storage import COURSE_NAME, save_registration
from utils.styles import apply_base_styles
from utils.validators import validate_registration

COURSE_TITLE = "Cập nhật kiến thức chuyên môn dược"
COURSE_ORG = "Trường Cao đẳng Y tế Phú Thọ"
BANNER_PATH = Path(__file__).resolve().parent.parent / "assets" / "banner-kien-thuc-chuyen-mon.png"

st.set_page_config(
    page_title="Đăng ký cập nhật kiến thức chuyên môn dược",
    page_icon="📝",
    layout="wide",
)

apply_base_styles(18)

if BANNER_PATH.exists():
    st.image(str(BANNER_PATH), use_container_width=True)

st.subheader("📝 Phiếu đăng ký cập nhật kiến thức chuyên môn dược")
st.caption(f"Khóa học: {COURSE_TITLE} — Đơn vị tổ chức: {COURSE_ORG}")
st.caption("Địa điểm: Hội trường Trường Cao đẳng Y tế Phú Thọ")
st.markdown("---")

with st.form("registration_form", clear_on_submit=True):
    st.subheader("Thông tin người đăng ký")
    col1, col2 = st.columns(2)

    with col1:
        ho_ten = st.text_input("Họ và tên *", placeholder="Nguyễn Văn A")
        so_cccd = st.text_input("Số CCCND/CCCD *", placeholder="9 số (CMND) hoặc 12 số (CCCD)")
        ngay_cap = st.date_input("Ngày cấp *", value=date.today(), format="DD/MM/YYYY")

    with col2:
        noi_cap = st.text_input("Nơi cấp *", placeholder="Cục Cảnh sát quản lý hành chính về trật tự xã hội")
        dia_chi_thuong_tru = st.text_input(
            "Địa chỉ thường trú *",
            placeholder="Xã/phường, huyện/quận, tỉnh/thành phố",
        )
        so_dien_thoai = st.text_input("Số điện thoại *", placeholder="0912345678")

    ghi_chu = st.text_area(
        "Ghi chú / nhu cầu khác",
        placeholder="Ví dụ: cần hỗ trợ tài liệu, có câu hỏi chuyên môn muốn gửi trước...",
    )

    submitted = st.form_submit_button("✅ GỬI ĐĂNG KÝ", type="primary", use_container_width=True)

if submitted:
    registration = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ho_ten": ho_ten.strip(),
        "so_cccd": so_cccd.strip(),
        "ngay_cap": ngay_cap,
        "noi_cap": noi_cap.strip(),
        "dia_chi_thuong_tru": dia_chi_thuong_tru.strip(),
        "so_dien_thoai": so_dien_thoai.strip(),
        "ghi_chu": ghi_chu.strip(),
        "khoa_hoc": COURSE_NAME,
    }

    errors = validate_registration(registration)
    if errors:
        for error in errors:
            st.error(f"❌ {error}")
    else:
        with st.spinner("Đang lưu đăng ký..."):
            save_result = save_registration(registration)
            discord_result = send_registration_notification(registration)

        if save_result["ok"]:
            st.success("✅ Đăng ký thành công!")
            st.info(f"📦 Dữ liệu đã lưu bằng chế độ: **{save_result['mode']}**")
            if discord_result["ok"]:
                st.info("🔔 Đã gửi thông báo về Discord.")
            else:
                st.warning(f"⚠️ Chưa gửi được Discord: {discord_result['message']}")
            st.balloons()
        else:
            st.error(f"❌ Không thể lưu đăng ký: {save_result['message']}")
