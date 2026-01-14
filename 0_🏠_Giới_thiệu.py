"""
Hệ thống Thu thập Báo cáo Thống kê Dược - Mỹ phẩm
Sở Y tế tỉnh Phú Thọ

Theo Thông tư số 25/2021/TT-BYT ngày 13/12/2021 của Bộ Y tế
"""
import streamlit as st

# Page config
st.set_page_config(
    page_title="Báo cáo Dược - Mỹ phẩm | Sở Y tế Phú Thọ",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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

# Header
st.markdown('<p class="main-header">🏥 HỆ THỐNG BÁO CÁO THỐNG KÊ DƯỢC - MỸ PHẨM</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Sở Y tế tỉnh Phú Thọ</p>', unsafe_allow_html=True)

st.divider()

# Introduction
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📋 Giới thiệu")
    st.markdown("""
    Hệ thống thu thập báo cáo thống kê lĩnh vực dược - mỹ phẩm theo quy định tại 
    **Thông tư số 25/2021/TT-BYT** ngày 13/12/2021 của Bộ trưởng Bộ Y tế.
    
    Các cơ sở trên địa bàn tỉnh Phú Thọ thực hiện báo cáo trực tuyến qua hệ thống này.
    """)
    
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("""
    **📌 Đối tượng báo cáo:**
    - Các cơ sở khám bệnh, chữa bệnh (bệnh viện, TTYT, phòng khám tư nhân)
    - Trung tâm Kiểm nghiệm thuốc, mỹ phẩm, thực phẩm
    - Các cơ sở sản xuất, kinh doanh dược
    - Các cơ sở sản xuất, kinh doanh mỹ phẩm
    """)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("### 📅 Thời hạn báo cáo")
    st.markdown('<div class="warning-box">', unsafe_allow_html=True)
    st.markdown("""
    **Báo cáo năm 2025:**
    
    ⏰ Hạn nộp: **17/01/2026**
    
    Số liệu tính đến: 31/12/2025
    """)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# Instructions
st.markdown("### 📝 Hướng dẫn sử dụng")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **Bước 1: Nhập báo cáo**
    
    👉 Chọn menu **"📝 Nhập báo cáo"** ở thanh bên trái
    
    - Điền thông tin cơ sở
    - Chọn loại cơ sở
    - Điền các biểu mẫu tương ứng
    - Upload file PDF ký số/scan
    """)

with col2:
    st.markdown("""
    **Bước 2: Xác nhận và gửi**
    
    👉 Kiểm tra lại thông tin
    
    - Đảm bảo số liệu chính xác
    - File PDF đầy đủ chữ ký
    - Nhấn nút **"Gửi báo cáo"**
    """)

with col3:
    st.markdown("""
    **Bước 3: Theo dõi**
    
    👉 Xem **"📊 Dashboard"** để theo dõi
    
    - Danh sách cơ sở đã nộp
    - Thống kê tổng hợp
    - Xem chi tiết từng cơ sở
    """)

st.divider()

# Forms overview
st.markdown("### 📑 Các biểu mẫu báo cáo")

forms_data = [
    ("I", "Tình hình nhân lực làm công tác dược lâm sàng", "Đơn vị y tế, UBND xã/phường"),
    ("II", "Giá trị thuốc đã sử dụng trong cơ sở y tế", "Đơn vị y tế, UBND xã/phường"),
    ("III", "Tình hình sử dụng thuốc sản xuất trong nước", "Đơn vị y tế, UBND xã/phường"),
    ("IV", "Tình hình chất lượng thuốc, nguyên liệu làm thuốc", "TT Kiểm nghiệm"),
    ("V", "Nhân lực dược", "Cơ sở bán buôn thuốc, UBND xã/phường"),
    ("VI", "Hệ thống cung ứng thuốc", "UBND xã/phường"),
    ("VII", "Giá trị sản xuất, nhập khẩu mỹ phẩm", "Cơ sở SX-KD mỹ phẩm"),
]

cols = st.columns(3)
for i, (num, name, target) in enumerate(forms_data):
    with cols[i % 3]:
        st.markdown(f"""
        <div style="background-color: #FFFFFF; border: 2px solid #3B82F6; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; min-height: 120px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <strong style="color: #1E40AF; font-size: 1.1rem;">Phụ lục {num}</strong><br>
            <span style="font-size: 0.9rem; color: #1F2937;">{name}</span><br>
            <span style="font-size: 0.8rem; color: #059669; font-weight: 500;">📌 {target}</span>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# Contact
st.markdown("### 📞 Liên hệ hỗ trợ")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Phòng Nghiệp vụ Dược - Sở Y tế tỉnh Phú Thọ**
    
    📍 Địa chỉ: Đường Trần Phú, TP. Việt Trì, tỉnh Phú Thọ
    
    📧 Email: nghiepvuduocpt@gmail.com
    """)

with col2:
    st.markdown("""
    **Hỗ trợ kỹ thuật:**
    
    📱 Điện thoại: 0989.836.165
    
    ⏰ Thời gian: 8:00 - 17:00 (Thứ 2 - Thứ 6)
    """)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #9CA3AF; font-size: 0.8rem;">
    © 2026 Sở Y tế tỉnh Phú Thọ | Hệ thống báo cáo thống kê dược - mỹ phẩm
</div>
""", unsafe_allow_html=True)
