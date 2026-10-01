"""Trang đăng ký cập nhật kiến thức chuyên môn dược (trang duy nhất của app)."""
from datetime import datetime

import streamlit as st

from utils.discord_webhook import send_registration_notification
from utils.storage import COURSE_NAME, save_registration
from utils.styles import apply_base_styles
from utils.validators import validate_registration

COURSE_ORG = "Trường Cao đẳng Y tế Phú Thọ"
COURSE_LOCATION = "Hội trường"

st.set_page_config(
    page_title="Đăng ký cập nhật kiến thức chuyên môn dược",
    page_icon="📝",
    layout="wide",
)

apply_base_styles(18)

# Header giới thiệu rút gọn: mở URL là thấy ngay form, không cần trang giới thiệu riêng.
st.title("Đăng ký cập nhật kiến thức chuyên môn dược")
st.caption(f"{COURSE_ORG} — {COURSE_LOCATION}")
st.info("Vui lòng điền đầy đủ thông tin bên dưới. Thông tin dùng để lập danh sách học viên.")
st.markdown("---")

# clear_on_submit=False: cố ý KHÔNG xoá form sau khi bấm Gửi, kể cả khi validate_registration()
# báo lỗi — giữ nguyên 12 trường đã nhập để người dùng chỉ sửa ô sai thay vì gõ lại từ đầu.
with st.form("registration_form", clear_on_submit=False):
    # Bố cục 2 khối: (1) giấy chứng chỉ hành nghề dược gồm số + ngày cấp + nơi cấp,
    # (2) thông tin người đăng ký. Khối 1 đặt trước để nhóm CCHND liền mạch,
    # không bị xen kẽ bởi các ô thông tin cá nhân.

    # --- Khối 1: Thông tin chứng chỉ hành nghề dược ---
    st.subheader("Thông tin chứng chỉ hành nghề dược")
    col1, col2 = st.columns(2)

    with col1:
        so_chung_chi = st.text_input(
            "Số Chứng chỉ hành nghề dược *",
            placeholder="Ví dụ: 12345/PTH-2024 hoặc 12345",
        )

    with col2:
        # Ngày cấp: ô nhập tự do, KHÔNG bắt buộc và KHÔNG kiểm tra định dạng.
        # Bỏ calendar vì người đăng ký thường tra cứu nhanh từ chứng chỉ đã in,
        # gõ "22/02/2024" nhanh hơn việc bấm lịch.
        ngay_cap = st.text_input(
            "Ngày cấp",
            placeholder="Ví dụ: 22/02/2024 (không bắt buộc)",
        )

    # Nơi cấp là cơ quan cấp Chứng chỉ hành nghề dược (Sở Y tế tỉnh), không phải
    # cơ quan cấp CCCD/cư trú. Vẫn để text_input để người dùng tự gõ tên Sở của
    # tỉnh mình (không selectbox, không validate cứng danh sách tỉnh).
    noi_cap = st.text_input(
        "Nơi cấp *", placeholder="Ví dụ: Sở Y tế tỉnh Vĩnh Phúc"
    )

    # Lĩnh vực hành nghề dược + văn bằng chuyên môn (2 trường mới theo phiếu gốc):
    # đặt cạnh nhau, đều KHÔNG bắt buộc và KHÔNG kiểm tra định dạng.
    col5, col6 = st.columns(2)

    with col5:
        linh_vuc_nghe_duoc = st.text_input(
            "Lĩnh vực hành nghề dược",
            placeholder="Ví dụ: Bán lẻ thuốc, Bán buôn thuốc",
        )

    with col6:
        van_bang_chuyen_mon = st.text_input(
            "Văn bằng chuyên môn",
            placeholder="Ví dụ: Dược sĩ, Thạc sĩ Dược",
        )

    st.divider()

    # --- Khối 2: Thông tin người đăng ký ---
    st.subheader("Thông tin người đăng ký")
    col3, col4 = st.columns(2)

    with col3:
        ho_ten = st.text_input("Họ và tên *", placeholder="Nguyễn Văn A")

    with col4:
        ngay_sinh = st.text_input(
            "Ngày, tháng, năm sinh", placeholder="Ví dụ: 01/02/1990"
        )

    col7, col8 = st.columns(2)

    with col7:
        so_dien_thoai = st.text_input("Số điện thoại *", placeholder="0912345678")

    with col8:
        email = st.text_input(
            "Email", placeholder="Ví dụ: nguoiban@example.com"
        )

    # Chỗ ở hiện nay đặt ngay trước địa chỉ thường trú (cùng nhóm thông tin nơi ở),
    # mỗi trường 1 dòng cho dễ gõ địa chỉ dài.
    cho_o_hien_nay = st.text_input(
        "Chỗ ở hiện nay",
        placeholder="Địa chỉ nơi ở hiện nay",
    )

    dia_chi_thuong_tru = st.text_input(
        "Địa chỉ thường trú *",
        placeholder="Xã/phường, huyện/quận, tỉnh/thành phố",
    )

    noi_cong_tac = st.text_input(
        "Nơi công tác",
        placeholder="Tên cơ quan, đơn vị",
    )

    submitted = st.form_submit_button("✅ GỬI ĐĂNG KÝ", type="primary", use_container_width=True)

if submitted:
    registration = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ho_ten": (ho_ten or "").strip(),
        "ngay_sinh": (ngay_sinh or "").strip(),
        "cho_o_hien_nay": (cho_o_hien_nay or "").strip(),
        "so_chung_chi": (so_chung_chi or "").strip(),
        "ngay_cap": (ngay_cap or "").strip(),
        "noi_cap": (noi_cap or "").strip(),
        "linh_vuc_nghe_duoc": (linh_vuc_nghe_duoc or "").strip(),
        "van_bang_chuyen_mon": (van_bang_chuyen_mon or "").strip(),
        "noi_cong_tac": (noi_cong_tac or "").strip(),
        "dia_chi_thuong_tru": (dia_chi_thuong_tru or "").strip(),
        "email": (email or "").strip(),
        "so_dien_thoai": (so_dien_thoai or "").strip(),
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
            st.info(
                "📌 Form vẫn giữ nguyên dữ liệu vừa gửi để bạn kiểm tra — chỉ bấm GỬI ĐĂNG KÝ "
                "lần nữa nếu muốn tạo thêm một bản ghi mới."
            )
            st.balloons()
        else:
            st.error(f"❌ Không thể lưu đăng ký: {save_result['message']}")
