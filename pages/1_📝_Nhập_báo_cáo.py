"""
Trang nhập báo cáo - Form nhập liệu cho các cơ sở
Theo Thông tư số 25/2021/TT-BYT
"""
import streamlit as st
import sys
sys.path.insert(0, '..')

from utils.google_sheets import (
    save_facility_info, save_form_01, save_form_02, save_form_03,
    save_form_04, save_form_05, save_form_06, save_form_07, save_pdf_info
)
from utils.discord_webhook import upload_pdf_to_discord

st.set_page_config(
    page_title="Nhập báo cáo | Sở Y tế Phú Thọ",
    page_icon="📝",
    layout="wide"
)

st.title("📝 Nhập báo cáo thống kê dược - mỹ phẩm")

st.markdown("""
<style>
    .stApp, .main, .block-container {
        font-size: 16px !important;
    }
    .stMarkdown p, .stMarkdown li, .stMarkdown span,
    .element-container p, .element-container li,
    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stMarkdownContainer"] li {
        font-size: 16px !important;
        line-height: 1.6 !important;
    }
    label, .stSelectbox label, .stTextInput label, .stNumberInput label {
        font-size: 16px !important;
    }
    .stTextInput input, .stNumberInput input, .stSelectbox > div > div {
        font-size: 16px !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("---")

# Initialize session state
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# ============================================================================
# PHẦN 1: THÔNG TIN CƠ SỞ
# ============================================================================
st.header("📌 Thông tin cơ sở")

col1, col2 = st.columns(2)

with col1:
    ten_co_so = st.text_input("Tên cơ sở *", placeholder="Nhập tên cơ sở")
    dia_chi = st.text_input("Địa chỉ *", placeholder="Nhập địa chỉ")
    nguoi_dai_dien = st.text_input("Người đại diện", placeholder="Họ và tên người đại diện")

with col2:
    dien_thoai = st.text_input("Số điện thoại", placeholder="0xxx.xxx.xxx")
    email = st.text_input("Email", placeholder="example@email.com")
    loai_co_so = st.selectbox(
        "Loại cơ sở *",
        options=[
            "-- Chọn loại cơ sở --",
            "UBND xã, phường",
            "Đơn vị y tế trực thuộc Sở Y tế / Bệnh viện",
            "Trung tâm Kiểm nghiệm tỉnh Phú Thọ",
            "Cơ sở bán buôn thuốc",
            "Cơ sở sản xuất, kinh doanh mỹ phẩm"
        ]
    )

st.markdown("---")

# ============================================================================
# PHẦN 2: CÁC BIỂU MẪU THEO LOẠI CƠ SỞ
# ============================================================================

# Initialize form data
form_01_data = {}
form_02_data = {}
form_03_data = {}
form_04_data = {}
form_05_data = {}
form_06_data = {}
form_07_data = {}


def render_form_01():
    """Phụ lục I: Tình hình nhân lực làm công tác dược lâm sàng"""
    st.header("📋 Phụ lục I: Tình hình nhân lực làm công tác dược lâm sàng")
    st.caption("Số có mặt đến 31/12/2025")

    col1, col2, col3 = st.columns(3)

    with col1:
        form_01_data["tong_so"] = st.number_input("Tổng số nhân lực", min_value=0, value=0, key="f01_tong")
        form_01_data["sau_dh"] = st.number_input("Sau đại học dược", min_value=0, value=0, key="f01_sau_dh")

    with col2:
        form_01_data["dh"] = st.number_input("Đại học dược", min_value=0, value=0, key="f01_dh")
        form_01_data["khac"] = st.number_input("Khác", min_value=0, value=0, key="f01_khac")

    with col3:
        form_01_data["kiem_nhiem"] = st.number_input("Số kiêm nhiệm", min_value=0, value=0, key="f01_kn")
        form_01_data["co_cchn"] = st.number_input("Số có CCHN về DLS", min_value=0, value=0, key="f01_cchn")

    return form_01_data


def render_form_02():
    """Phụ lục II: Giá trị thuốc đã sử dụng trong cơ sở y tế"""
    st.header("📋 Phụ lục II: Giá trị thuốc đã sử dụng trong cơ sở y tế")
    st.caption("Đơn vị: Triệu đồng | Báo cáo năm 2025")

    col1, col2, col3 = st.columns(3)

    with col1:
        form_02_data["tong_gia_tri"] = st.number_input("Tổng giá trị sử dụng thuốc", min_value=0.0, value=0.0, format="%.2f", key="f02_tong")
        form_02_data["biet_duoc_goc"] = st.number_input("Thuốc biệt dược gốc", min_value=0.0, value=0.0, format="%.2f", key="f02_bdg")
        form_02_data["generic"] = st.number_input("Thuốc generic", min_value=0.0, value=0.0, format="%.2f", key="f02_gen")
        form_02_data["duoc_lieu"] = st.number_input("Thuốc dược liệu", min_value=0.0, value=0.0, format="%.2f", key="f02_dl")

    with col2:
        form_02_data["khang_sinh"] = st.number_input("Kháng sinh", min_value=0.0, value=0.0, format="%.2f", key="f02_ks")
        form_02_data["vac_xin"] = st.number_input("Vắc xin", min_value=0.0, value=0.0, format="%.2f", key="f02_vx")
        form_02_data["sinh_pham"] = st.number_input("Sinh phẩm", min_value=0.0, value=0.0, format="%.2f", key="f02_sp")
        form_02_data["phong_xa"] = st.number_input("Thuốc phóng xạ", min_value=0.0, value=0.0, format="%.2f", key="f02_px")

    with col3:
        form_02_data["bhyt"] = st.number_input("Giá trị thuốc BHYT", min_value=0.0, value=0.0, format="%.2f", key="f02_bhyt")
        form_02_data["vien_tro"] = st.number_input("Thuốc viện trợ", min_value=0.0, value=0.0, format="%.2f", key="f02_vt")

    return form_02_data


def render_form_03():
    """Phụ lục III: Tình hình sử dụng thuốc sản xuất trong nước"""
    st.header("📋 Phụ lục III: Tình hình sử dụng thuốc sản xuất trong nước")
    st.caption("Báo cáo năm 2025")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Tính theo số lượng mặt hàng")
        form_03_data["sl_trung_thau"] = st.number_input("Số lượng thuốc trúng thầu", min_value=0, value=0, key="f03_sl_tt")
        form_03_data["sl_trong_nuoc"] = st.number_input("Số lượng thuốc SX trong nước trúng thầu", min_value=0, value=0, key="f03_sl_tn")
        if form_03_data["sl_trung_thau"] > 0:
            form_03_data["ty_le_sl"] = round(form_03_data["sl_trong_nuoc"] / form_03_data["sl_trung_thau"] * 100, 2)
        else:
            form_03_data["ty_le_sl"] = 0
        st.metric("Tỷ lệ (%)", f"{form_03_data['ty_le_sl']}%")

    with col2:
        st.subheader("Tính theo giá trị (triệu đồng)")
        form_03_data["tong_gia_tri"] = st.number_input("Tổng số tiền thuốc sử dụng", min_value=0.0, value=0.0, format="%.2f", key="f03_gt_tong")
        form_03_data["gt_trong_nuoc"] = st.number_input("Tổng số tiền thuốc SX trong nước", min_value=0.0, value=0.0, format="%.2f", key="f03_gt_tn")
        if form_03_data["tong_gia_tri"] > 0:
            form_03_data["ty_le_gt"] = round(form_03_data["gt_trong_nuoc"] / form_03_data["tong_gia_tri"] * 100, 2)
        else:
            form_03_data["ty_le_gt"] = 0
        st.metric("Tỷ lệ (%)", f"{form_03_data['ty_le_gt']}%")

    return form_03_data


def render_form_04():
    """Phụ lục IV: Tình hình chất lượng thuốc, nguyên liệu làm thuốc lưu hành"""
    st.header("📋 Phụ lục IV: Tình hình chất lượng thuốc, nguyên liệu làm thuốc lưu hành")
    st.caption("Báo cáo năm 2025")

    col1, col2, col3 = st.columns(3)

    with col1:
        form_04_data["so_mau_kiem_tra"] = st.number_input("Số mẫu lấy kiểm tra chất lượng", min_value=0, value=0, key="f04_mau_kt")
        form_04_data["so_mau_khong_dat"] = st.number_input("Số mẫu không đạt tiêu chuẩn", min_value=0, value=0, key="f04_mau_kd")

    with col2:
        st.markdown("**Phân loại mức độ vi phạm:**")
        form_04_data["muc_do_1"] = st.number_input("Vi phạm mức độ 1", min_value=0, value=0, key="f04_md1")
        form_04_data["muc_do_2"] = st.number_input("Vi phạm mức độ 2", min_value=0, value=0, key="f04_md2")
        form_04_data["muc_do_3"] = st.number_input("Vi phạm mức độ 3", min_value=0, value=0, key="f04_md3")

    with col3:
        if form_04_data["so_mau_kiem_tra"] > 0:
            form_04_data["ty_le_khong_dat"] = round(form_04_data["so_mau_khong_dat"] / form_04_data["so_mau_kiem_tra"] * 100, 2)
        else:
            form_04_data["ty_le_khong_dat"] = 0
        st.metric("Tỷ lệ không đạt (%)", f"{form_04_data['ty_le_khong_dat']}%")

        form_04_data["so_lo_gia"] = st.number_input("Số lô thuốc giả phát hiện", min_value=0, value=0, key="f04_lo_gia")
        form_04_data["ty_le_gia"] = st.number_input("Tỷ lệ thuốc giả (%)", min_value=0.0, value=0.0, format="%.2f", key="f04_tl_gia")

    return form_04_data


def render_form_05():
    """Phụ lục V: Nhân lực dược (dùng cho cơ sở bán buôn thuốc)"""
    st.header("📋 Phụ lục V: Nhân lực dược")
    st.caption("Số liệu tính đến 31/12/2025")

    col1, col2 = st.columns(2)

    with col1:
        form_05_data["ts_dsckii"] = st.number_input("Tiến sỹ Dược / DSCK II", min_value=0, value=0, key="f05_ts")
        form_05_data["ths_dscki"] = st.number_input("Thạc sỹ Dược / DSCK I", min_value=0, value=0, key="f05_ths")
        form_05_data["dsdh"] = st.number_input("Dược sỹ Đại học", min_value=0, value=0, key="f05_dh")

    with col2:
        form_05_data["dscd_th"] = st.number_input("Dược sĩ CĐ, TH & KTV TH Dược", min_value=0, value=0, key="f05_cd")
        form_05_data["duoc_ta"] = st.number_input("Dược tá", min_value=0, value=0, key="f05_dt")

    return form_05_data


def render_form_06():
    """Phụ lục VI: Hệ thống cung ứng thuốc (dùng cho UBND xã, phường)"""
    st.header("📋 Phụ lục VI: Hệ thống cung ứng thuốc")
    st.caption("Số liệu tính đến 31/12/2025")

    col1, col2 = st.columns(2)

    with col1:
        form_06_data["tong_cs_ban_le"] = st.number_input("Tổng số cơ sở bán lẻ", min_value=0, value=0, key="f06_bl_tong")
        form_06_data["nha_thuoc"] = st.number_input("Số nhà thuốc", min_value=0, value=0, key="f06_nt")

    with col2:
        form_06_data["quay_thuoc"] = st.number_input("Số quầy thuốc", min_value=0, value=0, key="f06_qt")
        form_06_data["tu_thuoc_tyt"] = st.number_input("Số tủ thuốc Trạm Y tế", min_value=0, value=0, key="f06_tyt")

    return form_06_data


def render_form_07():
    """Phụ lục VII: Giá trị sản xuất, nhập khẩu mỹ phẩm"""
    st.header("📋 Phụ lục VII: Giá trị sản xuất, nhập khẩu mỹ phẩm")
    st.caption("Số liệu tính đến 31/12/2025 | Đơn vị: Triệu đồng")

    col1, col2 = st.columns(2)

    with col1:
        form_07_data["gia_tri_nhap_khau"] = st.number_input("Giá trị mỹ phẩm nhập khẩu", min_value=0, value=0, key="f07_nk")
        form_07_data["gia_tri_san_xuat"] = st.number_input("Giá trị mỹ phẩm sản xuất trong nước", min_value=0, value=0, key="f07_sx")

    with col2:
        form_07_data["so_phieu_cong_bo"] = st.number_input("Số phiếu công bố sản phẩm đã được cấp số tiếp nhận", min_value=0, value=0, key="f07_cb")

    return form_07_data


# ============================================================================
# HIỂN THỊ FORM THEO LOẠI CƠ SỞ
# ============================================================================

if loai_co_so == "UBND xã, phường":
    st.info("📋 UBND xã, phường báo cáo: Phụ lục I, II, III, V, VI")

    form_01_data = render_form_01()
    st.markdown("---")
    form_02_data = render_form_02()
    st.markdown("---")
    form_03_data = render_form_03()
    st.markdown("---")
    form_05_data = render_form_05()
    st.markdown("---")
    form_06_data = render_form_06()

elif loai_co_so == "Đơn vị y tế trực thuộc Sở Y tế / Bệnh viện":
    st.info("📋 Đơn vị y tế/Bệnh viện báo cáo: Phụ lục I, II, III")

    form_01_data = render_form_01()
    st.markdown("---")
    form_02_data = render_form_02()
    st.markdown("---")
    form_03_data = render_form_03()

elif loai_co_so == "Trung tâm Kiểm nghiệm tỉnh Phú Thọ":
    st.info("📋 Trung tâm Kiểm nghiệm báo cáo: Phụ lục IV")

    form_04_data = render_form_04()

elif loai_co_so == "Cơ sở bán buôn thuốc":
    st.info("📋 Cơ sở bán buôn thuốc báo cáo: Phụ lục V (chỉ nhân lực bán buôn, không bao gồm bán lẻ)")

    form_05_data = render_form_05()

elif loai_co_so == "Cơ sở sản xuất, kinh doanh mỹ phẩm":
    st.info("📋 Cơ sở SX-KD mỹ phẩm báo cáo: Phụ lục VII")

    form_07_data = render_form_07()

else:
    st.info("👆 Vui lòng chọn loại cơ sở để hiển thị các biểu mẫu tương ứng.")

st.markdown("---")

# ============================================================================
# PHẦN 3: UPLOAD FILE PDF
# ============================================================================
st.header("📎 Upload file PDF (Văn bản ký số/scan)")

uploaded_file = st.file_uploader(
    "Chọn file PDF báo cáo có chữ ký và đóng dấu",
    type=["pdf"],
    help="File PDF tối đa 10MB (giới hạn Discord)"
)

if uploaded_file:
    file_size_mb = uploaded_file.size / (1024 * 1024)
    if file_size_mb > 10:
        st.error(f"❌ File quá lớn: {file_size_mb:.2f} MB. Giới hạn tối đa 10MB.")
    else:
        st.success(f"✅ Đã chọn file: {uploaded_file.name} ({file_size_mb:.2f} MB)")

st.markdown("---")

# ============================================================================
# PHẦN 4: GỬI BÁO CÁO
# ============================================================================
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    submit_button = st.button("✅ GỬI BÁO CÁO", type="primary", use_container_width=True)

if submit_button:
    # Validation
    errors = []

    if not ten_co_so:
        errors.append("Vui lòng nhập tên cơ sở")
    if not dia_chi:
        errors.append("Vui lòng nhập địa chỉ")
    if loai_co_so == "-- Chọn loại cơ sở --":
        errors.append("Vui lòng chọn loại cơ sở")
    if not uploaded_file:
        errors.append("Vui lòng đính kèm file PDF báo cáo có chữ ký và đóng dấu")

    if errors:
        for error in errors:
            st.error(f"❌ {error}")
    else:
        with st.spinner("Đang gửi báo cáo..."):
            try:
                # Save facility info
                facility_data = {
                    "ten_co_so": ten_co_so,
                    "dia_chi": dia_chi,
                    "dien_thoai": dien_thoai,
                    "email": email,
                    "loai_co_so": loai_co_so,
                    "nguoi_dai_dien": nguoi_dai_dien
                }
                save_facility_info(facility_data)

                # Save form data based on facility type
                if loai_co_so == "UBND xã, phường":
                    save_form_01(ten_co_so, form_01_data)
                    save_form_02(ten_co_so, form_02_data)
                    save_form_03(ten_co_so, form_03_data)
                    save_form_05(ten_co_so, form_05_data)
                    save_form_06(ten_co_so, form_06_data)
                elif loai_co_so == "Đơn vị y tế trực thuộc Sở Y tế / Bệnh viện":
                    save_form_01(ten_co_so, form_01_data)
                    save_form_02(ten_co_so, form_02_data)
                    save_form_03(ten_co_so, form_03_data)
                elif loai_co_so == "Trung tâm Kiểm nghiệm tỉnh Phú Thọ":
                    save_form_04(ten_co_so, form_04_data)
                elif loai_co_so == "Cơ sở bán buôn thuốc":
                    save_form_05(ten_co_so, form_05_data)
                elif loai_co_so == "Cơ sở sản xuất, kinh doanh mỹ phẩm":
                    save_form_07(ten_co_so, form_07_data)

                # Save PDF info and upload to Discord if provided
                if uploaded_file:
                    file_size_mb = uploaded_file.size / (1024 * 1024)
                    if file_size_mb <= 10:
                        # Upload to Discord
                        discord_result = upload_pdf_to_discord(
                            uploaded_file.getvalue(),
                            uploaded_file.name,
                            ten_co_so,
                            loai_co_so
                        )
                        if discord_result:
                            save_pdf_info(ten_co_so, uploaded_file.name, uploaded_file.size)
                            st.info("📤 File PDF đã được gửi qua Discord!")
                    else:
                        st.warning(f"⚠️ File quá lớn ({file_size_mb:.2f} MB), không thể gửi qua Discord.")

                st.success("✅ Đã gửi báo cáo thành công!")
                st.balloons()
                st.session_state.submitted = True

            except Exception as e:
                st.error(f"❌ Lỗi khi gửi báo cáo: {e}")

# Show success message if submitted
if st.session_state.submitted:
    st.info("📝 Bạn có thể xem báo cáo đã nộp tại trang Dashboard.")
