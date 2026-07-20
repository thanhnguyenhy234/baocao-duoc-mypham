"""
Hệ thống Thu thập Báo cáo Thống kê Dược - Mỹ phẩm
Sở Y tế tỉnh Phú Thọ - BÁO CÁO 6 THÁNG ĐẦU NĂM 2026

Theo Thông tư số 25/2021/TT-BYT ngày 13/12/2021 của Bộ Y tế
Kỳ báo cáo: 6 tháng đầu năm 2026 (01/01/2026 → 30/06/2026)
Hạn nộp: 31/07/2026

3 phụ lục theo cv_bao_cao_thong_ke_duoc_my_pham.tex:
  - Phụ lục I  : Giá trị thuốc đã sử dụng            (Đơn vị y tế / Bệnh viện)
  - Phụ lục II : Tình hình sử dụng thuốc SX trong nước (Đơn vị y tế / Bệnh viện)
  - Phụ lục III: Tình hình CL thuốc, NL làm thuốc     (Trung tâm Kiểm nghiệm tỉnh Phú Thọ)

Single-page app: Giới thiệu + Nhập báo cáo + Admin Dashboard (cuối trang).
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.google_sheets import (
    save_facility_info,
    save_phuluc_01, save_phuluc_02, save_phuluc_03,
    save_pdf_info,
    get_statistics, get_all_facilities, get_form_data
)
from utils.discord_webhook import upload_pdf_to_discord

# Page config
st.set_page_config(
    page_title="Báo cáo 6 tháng | Dược - Mỹ phẩm | Sở Y tế Phú Thọ",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stApp, .main, .block-container {
        font-size: 20px !important;
    }
    .stMarkdown p, .stMarkdown li, .stMarkdown span,
    .element-container p, .element-container li,
    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stMarkdownContainer"] li {
        font-size: 20px !important;
        line-height: 1.6 !important;
    }
    label, .stSelectbox label, .stTextInput label, .stNumberInput label {
        font-size: 20px !important;
    }
    .stTextInput input, .stNumberInput input, .stSelectbox > div > div {
        font-size: 20px !important;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6B7280;
        text-align: center;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #F0F9FF;
        border-left: 4px solid #0EA5E9;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #FEF3C7;
        border-left: 4px solid #F59E0B;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# ============================================================================
# PHẦN 1: GIỚI THIỆU
# ============================================================================
st.markdown('<p class="main-header">🏥 HỆ THỐNG BÁO CÁO THỐNG KÊ DƯỢC - MỸ PHẨM</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Sở Y tế tỉnh Phú Thọ — Báo cáo 6 tháng đầu năm 2026</p>', unsafe_allow_html=True)

st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📋 Giới thiệu")
    st.markdown("""
    Căn cứ **Thông tư số 25/2021/TT-BYT** ngày 13/12/2021 của Bộ trưởng Bộ Y tế
    (kỳ báo cáo thống kê 6 tháng đầu năm: từ ngày 01/01 đến hết ngày 30/06),
    Sở Y tế yêu cầu các đơn vị thuộc đối tượng báo cáo thực hiện báo cáo
    **6 tháng đầu năm 2026**, cụ thể:
    """)

    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("""
    **📌 Đối tượng báo cáo:**
    - **Đơn vị y tế trực thuộc Sở Y tế; bệnh viện thuộc Bộ, ngành; bệnh viện tư nhân:** Phụ lục I, II
    - **Trung tâm Kiểm nghiệm tỉnh Phú Thọ:** Phụ lục III
    """)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("### 📅 Thời hạn báo cáo")
    st.markdown('<div class="warning-box">', unsafe_allow_html=True)
    st.markdown("""
    **Báo cáo 6 tháng đầu năm 2026:**

    ⏰ Hạn nộp: **31/07/2026**

    📆 Kỳ báo cáo: 01/01/2026 → 30/06/2026
    """)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# Forms overview
st.markdown("### 📑 Các biểu mẫu báo cáo (kỳ 6 tháng đầu năm 2026)")
st.markdown("""
<style>
    small { font-size: 0.85rem !important; }
</style>
""", unsafe_allow_html=True)

forms_data = [
    ("I", "Giá trị thuốc đã sử dụng trong cơ sở y tế", "Đơn vị y tế, Bệnh viện"),
    ("II", "Tình hình sử dụng thuốc sản xuất trong nước", "Đơn vị y tế, Bệnh viện"),
    ("III", "Tình hình CL thuốc, nguyên liệu làm thuốc lưu hành", "Trung tâm Kiểm nghiệm tỉnh Phú Thọ"),
]

cols = st.columns(3)
for i, (num, name, target) in enumerate(forms_data):
    with cols[i]:
        st.markdown(f"""
        <div style="background-color: #FFFFFF; border: 2px solid #3B82F6; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; min-height: 160px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <strong style="color: #1E40AF; font-size: 1.1rem;">Phụ lục {num}</strong><br>
            <span style="font-size: 0.9rem; color: #1F2937;">{name}</span><br>
            <span style="font-size: 0.8rem; color: #059669; font-weight: 500;">📌 {target}</span>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ============================================================================
# PHẦN 2: NHẬP BÁO CÁO
# ============================================================================
st.title("📝 Nhập báo cáo thống kê dược - mỹ phẩm (6 tháng đầu năm 2026)")

# ---------- Thông tin cơ sở ----------
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
            "Đơn vị y tế trực thuộc Sở Y tế / Bệnh viện",
            "Trung tâm Kiểm nghiệm tỉnh Phú Thọ"
        ]
    )

st.markdown("---")

# ---------- Dữ liệu form ----------
form_01_data = {}
form_02_data = {}
form_03_data = {}


def render_phuluc_01():
    """Phụ lục I: Giá trị thuốc đã sử dụng (Biểu 4/BCT - 06 tháng)."""
    st.header("📋 Phụ lục I: Giá trị thuốc đã sử dụng trong cơ sở y tế")
    st.caption("6 tháng đầu năm 2026 (01/01 → 30/06/2026) | Đơn vị tính: Triệu đồng")

    col1, col2, col3 = st.columns(3)

    with col1:
        form_01_data["tong_gia_tri"] = st.number_input("Tổng giá trị sử dụng thuốc", min_value=0.0, value=0.0, format="%.2f", key="f01_tong")
        form_01_data["biet_duoc_goc"] = st.number_input("Thuốc biệt dược gốc", min_value=0.0, value=0.0, format="%.2f", key="f01_bdg")
        form_01_data["generic"] = st.number_input("Thuốc generic", min_value=0.0, value=0.0, format="%.2f", key="f01_gen")
        form_01_data["duoc_lieu"] = st.number_input("Thuốc dược liệu", min_value=0.0, value=0.0, format="%.2f", key="f01_dl")

    with col2:
        form_01_data["khang_sinh"] = st.number_input("Kháng sinh", min_value=0.0, value=0.0, format="%.2f", key="f01_ks")
        form_01_data["vac_xin"] = st.number_input("Vắc xin", min_value=0.0, value=0.0, format="%.2f", key="f01_vx")
        form_01_data["sinh_pham"] = st.number_input("Sinh phẩm", min_value=0.0, value=0.0, format="%.2f", key="f01_sp")
        form_01_data["phong_xa"] = st.number_input("Thuốc phóng xạ", min_value=0.0, value=0.0, format="%.2f", key="f01_px")

    with col3:
        form_01_data["bhyt"] = st.number_input("Giá trị thuốc BHYT", min_value=0.0, value=0.0, format="%.2f", key="f01_bhyt")
        form_01_data["vien_tro"] = st.number_input("Thuốc viện trợ", min_value=0.0, value=0.0, format="%.2f", key="f01_vt")

    return form_01_data


def render_phuluc_02():
    """Phụ lục II: Tình hình sử dụng thuốc SX trong nước (Biểu 5/BCT - 06 tháng)."""
    st.header("📋 Phụ lục II: Tình hình sử dụng thuốc sản xuất trong nước")
    st.caption("6 tháng đầu năm 2026 (01/01 → 30/06/2026)")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Tính theo số lượng mặt hàng")
        form_02_data["sl_trung_thau"] = st.number_input("Số lượng thuốc trúng thầu", min_value=0, value=0, key="f02_sl_tt")
        form_02_data["sl_trong_nuoc"] = st.number_input("Số lượng thuốc SX trong nước trúng thầu", min_value=0, value=0, key="f02_sl_tn")
        if form_02_data["sl_trung_thau"] > 0:
            form_02_data["ty_le_sl"] = round(form_02_data["sl_trong_nuoc"] / form_02_data["sl_trung_thau"] * 100, 2)
        else:
            form_02_data["ty_le_sl"] = 0
        st.metric("Tỷ lệ (%)", f"{form_02_data['ty_le_sl']}%")

    with col2:
        st.subheader("Tính theo giá trị (triệu đồng)")
        form_02_data["tong_gia_tri"] = st.number_input("Tổng số tiền thuốc sử dụng", min_value=0.0, value=0.0, format="%.2f", key="f02_gt_tong")
        form_02_data["gt_trong_nuoc"] = st.number_input("Tổng số tiền thuốc SX trong nước", min_value=0.0, value=0.0, format="%.2f", key="f02_gt_tn")
        if form_02_data["tong_gia_tri"] > 0:
            form_02_data["ty_le_gt"] = round(form_02_data["gt_trong_nuoc"] / form_02_data["tong_gia_tri"] * 100, 2)
        else:
            form_02_data["ty_le_gt"] = 0
        st.metric("Tỷ lệ (%)", f"{form_02_data['ty_le_gt']}%")

    return form_02_data


def render_phuluc_03():
    """Phụ lục III: Tình hình CL thuốc, NL làm thuốc (Biểu 3/BCT - 06 tháng).

    Bao gồm 4 phân loại thuốc giả theo tex.
    """
    st.header("📋 Phụ lục III: Tình hình CL thuốc, nguyên liệu làm thuốc lưu hành")
    st.caption("6 tháng đầu năm 2026 (01/01 → 30/06/2026)")

    # Block 1: mẫu kiểm tra + không đạt + phân loại vi phạm
    st.subheader("🔍 Số mẫu lấy kiểm tra chất lượng")
    col1, col2, col3 = st.columns(3)

    with col1:
        form_03_data["so_mau_kiem_tra"] = st.number_input("Số mẫu lấy kiểm tra chất lượng", min_value=0, value=0, key="f03_mau_kt")
        form_03_data["so_mau_khong_dat"] = st.number_input("Số mẫu không đạt tiêu chuẩn CL", min_value=0, value=0, key="f03_mau_kd")
        if form_03_data["so_mau_kiem_tra"] > 0:
            form_03_data["ty_le_khong_dat"] = round(form_03_data["so_mau_khong_dat"] / form_03_data["so_mau_kiem_tra"] * 100, 2)
        else:
            form_03_data["ty_le_khong_dat"] = 0
        st.metric("Tỷ lệ mẫu không đạt CL (%)", f"{form_03_data['ty_le_khong_dat']}%")

    with col2:
        st.markdown("**Thuốc không đạt CL vi phạm mức độ:**")
        form_03_data["muc_do_1"] = st.number_input("Vi phạm mức độ 1", min_value=0, value=0, key="f03_md1")
        form_03_data["muc_do_2"] = st.number_input("Vi phạm mức độ 2", min_value=0, value=0, key="f03_md2")
        form_03_data["muc_do_3"] = st.number_input("Vi phạm mức độ 3", min_value=0, value=0, key="f03_md3")

    with col3:
        form_03_data["so_lo_gia"] = st.number_input("Số lô thuốc giả phát hiện được", min_value=0, value=0, key="f03_lo_gia")

    st.markdown("---")
    st.subheader("⚠️ Tỷ lệ thuốc giả (%) — phân loại theo nguồn gốc/đặc điểm")
    st.caption("Tổng tỷ lệ thuốc giả + 4 phân loại thành phần (đơn vị: %)")

    form_03_data["ty_le_gia"] = st.number_input("Tỷ lệ thuốc giả (%) - tổng", min_value=0.0, value=0.0, format="%.2f", key="f03_tl_gia")

    col1, col2 = st.columns(2)
    with col1:
        form_03_data["gia_tn"] = st.number_input("Thuốc giả SP cơ sở SX trong nước (%)", min_value=0.0, value=0.0, format="%.2f", key="f03_gia_tn")
        form_03_data["gia_nn"] = st.number_input("Thuốc giả SP cơ sở SX nước ngoài (%)", min_value=0.0, value=0.0, format="%.2f", key="f03_gia_nn")
    with col2:
        form_03_data["gia_khong_hoat_chat"] = st.number_input("Thuốc giả không chứa hoạt chất (%)", min_value=0.0, value=0.0, format="%.2f", key="f03_gia_khc")
        form_03_data["gia_bao_bi"] = st.number_input("Thuốc giả bao bì nhãn mác (%)", min_value=0.0, value=0.0, format="%.2f", key="f03_gia_bb")

    return form_03_data


# ---------- Hiển thị form theo loại cơ sở ----------
if loai_co_so == "Đơn vị y tế trực thuộc Sở Y tế / Bệnh viện":
    st.info("📋 Đơn vị y tế / Bệnh viện báo cáo: Phụ lục I, II")
    form_01_data = render_phuluc_01()
    st.markdown("---")
    form_02_data = render_phuluc_02()

elif loai_co_so == "Trung tâm Kiểm nghiệm tỉnh Phú Thọ":
    st.info("📋 Trung tâm Kiểm nghiệm tỉnh Phú Thọ báo cáo: Phụ lục III")
    form_03_data = render_phuluc_03()

else:
    st.info("👆 Vui lòng chọn loại cơ sở để hiển thị các biểu mẫu tương ứng.")

st.markdown("---")

# ---------- Upload PDF ----------
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

# ---------- Nút Gửi ----------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    submit_button = st.button("✅ GỬI BÁO CÁO", type="primary", use_container_width=True)

if submit_button:
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
                facility_data = {
                    "ten_co_so": ten_co_so,
                    "dia_chi": dia_chi,
                    "dien_thoai": dien_thoai,
                    "email": email,
                    "loai_co_so": loai_co_so,
                    "nguoi_dai_dien": nguoi_dai_dien
                }
                save_facility_info(facility_data)

                if loai_co_so == "Đơn vị y tế trực thuộc Sở Y tế / Bệnh viện":
                    save_phuluc_01(ten_co_so, form_01_data)
                    save_phuluc_02(ten_co_so, form_02_data)
                elif loai_co_so == "Trung tâm Kiểm nghiệm tỉnh Phú Thọ":
                    save_phuluc_03(ten_co_so, form_03_data)

                if uploaded_file:
                    file_size_mb = uploaded_file.size / (1024 * 1024)
                    if file_size_mb <= 10:
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

# ============================================================================
# PHẦN 3: ADMIN DASHBOARD (cuối trang, có xác thực mật khẩu)
# ============================================================================
st.markdown("---")
st.markdown("---")


def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets.get("admin_password", "admin123"):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.title("🔐 Đăng nhập Dashboard")
        st.markdown("---")
        st.warning("⚠️ Phần này chỉ dành cho quản trị viên Sở Y tế.")
        st.text_input("Nhập mật khẩu:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.title("🔐 Đăng nhập Dashboard")
        st.markdown("---")
        st.warning("⚠️ Phần này chỉ dành cho quản trị viên Sở Y tế.")
        st.text_input("Nhập mật khẩu:", type="password", on_change=password_entered, key="password")
        st.error("❌ Mật khẩu không đúng!")
        return False
    return True


if not check_password():
    st.stop()

st.title("📊 Dashboard tổng hợp báo cáo — 6 tháng đầu năm 2026")
st.markdown("---")

# ---------- Thống kê tổng quan ----------
st.header("📈 Thống kê tổng quan")

try:
    stats = get_statistics()
except Exception:
    stats = {"total": 0, "yte": 0, "kiem_nghiem": 0}

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Tổng số cơ sở đã nộp", value=stats["total"], delta=None)
with col2:
    st.metric(label="Đơn vị y tế / Bệnh viện", value=stats["yte"], delta=None)
with col3:
    st.metric(label="Trung tâm Kiểm nghiệm", value=stats["kiem_nghiem"], delta=None)

st.markdown("---")

# ---------- Biểu đồ ----------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Phân bố theo loại cơ sở")
    if stats["total"] > 0:
        chart_data = {
            "Loại cơ sở": ["Đơn vị y tế / Bệnh viện", "Trung tâm Kiểm nghiệm"],
            "Số lượng": [stats["yte"], stats["kiem_nghiem"]]
        }
        fig = px.pie(
            chart_data,
            values="Số lượng",
            names="Loại cơ sở",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_traces(textposition='inside', textinfo='percent+value')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Chưa có dữ liệu để hiển thị biểu đồ")

with col2:
    st.subheader("📈 Tiến độ nộp báo cáo")
    total_expected = 50
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=stats["total"],
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Số cơ sở đã nộp"},
        delta={'reference': total_expected, 'relative': False},
        gauge={
            'axis': {'range': [None, total_expected], 'tickwidth': 1},
            'bar': {'color': "#0EA5E9"},
            'steps': [
                {'range': [0, total_expected * 0.5], 'color': "#FEE2E2"},
                {'range': [total_expected * 0.5, total_expected * 0.8], 'color': "#FEF3C7"},
                {'range': [total_expected * 0.8, total_expected], 'color': "#D1FAE5"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': total_expected
            }
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ---------- Danh sách cơ sở đã nộp ----------
st.header("📋 Danh sách cơ sở đã nộp báo cáo")

try:
    facilities_df = get_all_facilities()
except Exception:
    facilities_df = pd.DataFrame()

if not facilities_df.empty:
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        search_term = st.text_input("🔍 Tìm kiếm theo tên cơ sở", "", key="adm_search")
    with col2:
        filter_type = st.selectbox(
            "Lọc theo loại cơ sở",
            ["Tất cả", "Đơn vị y tế trực thuộc Sở Y tế / Bệnh viện", "Trung tâm Kiểm nghiệm tỉnh Phú Thọ"],
            key="adm_filter"
        )
    with col3:
        st.write("")
        st.write("")
        refresh_btn = st.button("🔄 Làm mới", key="adm_refresh")

    filtered_df = facilities_df.copy()
    if search_term:
        filtered_df = filtered_df[filtered_df["Tên cơ sở"].str.contains(search_term, case=False, na=False)]
    if filter_type != "Tất cả":
        filtered_df = filtered_df[filtered_df["Loại cơ sở"] == filter_type]

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Thời gian nộp": st.column_config.DatetimeColumn("Thời gian nộp", format="DD/MM/YYYY HH:mm")
        }
    )
    st.caption(f"Hiển thị {len(filtered_df)} / {len(facilities_df)} cơ sở")
else:
    st.info("📭 Chưa có cơ sở nào nộp báo cáo")

st.markdown("---")

# ---------- Xem chi tiết ----------
st.header("👁️ Xem chi tiết báo cáo")

if not facilities_df.empty:
    selected_facility = st.selectbox(
        "Chọn cơ sở để xem chi tiết",
        options=["-- Chọn cơ sở --"] + facilities_df["Tên cơ sở"].tolist(),
        key="adm_select_facility"
    )

    if selected_facility != "-- Chọn cơ sở --":
        facility_info = facilities_df[facilities_df["Tên cơ sở"] == selected_facility].iloc[0]
        st.subheader(f"🏥 {selected_facility}")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            **Địa chỉ:** {facility_info.get('Địa chỉ', 'N/A')}

            **Điện thoại:** {facility_info.get('Điện thoại', 'N/A')}

            **Email:** {facility_info.get('Email', 'N/A')}
            """)
        with col2:
            st.markdown(f"""
            **Loại cơ sở:** {facility_info.get('Loại cơ sở', 'N/A')}

            **Người đại diện:** {facility_info.get('Người đại diện', 'N/A')}

            **Thời gian nộp:** {facility_info.get('Thời gian nộp', 'N/A')}
            """)

        st.markdown("---")

        for sheet_name, title in [
            ("6T2026 - Phụ lục I - Giá trị thuốc", "Phụ lục I: Giá trị thuốc đã sử dụng"),
            ("6T2026 - Phụ lục II - Thuốc trong nước", "Phụ lục II: Thuốc sản xuất trong nước"),
            ("6T2026 - Phụ lục III - CL thuốc", "Phụ lục III: Tình hình CL thuốc")
        ]:
            try:
                df = get_form_data(sheet_name)
                data = df[df["Tên cơ sở"] == selected_facility]
                if not data.empty:
                    st.subheader(f"📋 {title}")
                    st.dataframe(data, use_container_width=True, hide_index=True)
            except Exception:
                pass
else:
    st.info("Chưa có dữ liệu để hiển thị")

# ---------- Xuất báo cáo ----------
st.markdown("---")
st.header("📥 Xuất báo cáo tổng hợp")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📥 Xuất danh sách cơ sở (Excel)", use_container_width=True, key="adm_export_list"):
        if not facilities_df.empty:
            import io
            buffer = io.BytesIO()
            facilities_df.to_excel(buffer, index=False, engine='openpyxl')
            buffer.seek(0)
            st.download_button(
                label="💾 Tải file Excel",
                data=buffer,
                file_name="6T2026_danh_sach_co_so_bao_cao.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("Không có dữ liệu để xuất")

with col2:
    if st.button("📥 Xuất Phụ lục I (Excel)", use_container_width=True, key="adm_export_pl1"):
        try:
            df = get_form_data("6T2026 - Phụ lục I - Giá trị thuốc")
            if not df.empty:
                import io
                buffer = io.BytesIO()
                df.to_excel(buffer, index=False, engine='openpyxl')
                buffer.seek(0)
                st.download_button(
                    label="💾 Tải file Excel",
                    data=buffer,
                    file_name="6T2026_phu_luc_I_gia_tri_thuoc.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.warning("Không có dữ liệu để xuất")
        except Exception:
            st.warning("Không có dữ liệu để xuất")

with col3:
    if st.button("📥 Xuất Phụ lục III (Excel)", use_container_width=True, key="adm_export_pl3"):
        try:
            df = get_form_data("6T2026 - Phụ lục III - CL thuốc")
            if not df.empty:
                import io
                buffer = io.BytesIO()
                df.to_excel(buffer, index=False, engine='openpyxl')
                buffer.seek(0)
                st.download_button(
                    label="💾 Tải file Excel",
                    data=buffer,
                    file_name="6T2026_phu_luc_III_CL_thuoc.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.warning("Không có dữ liệu để xuất")
        except Exception:
            st.warning("Không có dữ liệu để xuất")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #9CA3AF; font-size: 0.8rem;">
    © 2026 Sở Y tế tỉnh Phú Thọ | Hệ thống báo cáo thống kê dược - mỹ phẩm (Kỳ 6 tháng đầu năm 2026)
</div>
""", unsafe_allow_html=True)
