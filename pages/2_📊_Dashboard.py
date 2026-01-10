"""
Dashboard - Tổng hợp và xem chi tiết báo cáo
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
sys.path.insert(0, '..')

from utils.google_sheets import (
    get_statistics, get_all_facilities, get_form_data
)

st.set_page_config(
    page_title="Dashboard | Sở Y tế Phú Thọ",
    page_icon="📊",
    layout="wide"
)

# ============================================================================
# XÁC THỰC ADMIN
# ============================================================================
def check_password():
    """Kiểm tra mật khẩu để vào Dashboard."""
    
    def password_entered():
        """Kiểm tra mật khẩu đã nhập."""
        if st.session_state["password"] == st.secrets.get("admin_password", "admin123"):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Xóa mật khẩu khỏi session
        else:
            st.session_state["password_correct"] = False

    # Nếu chưa kiểm tra mật khẩu
    if "password_correct" not in st.session_state:
        st.title("🔐 Đăng nhập Dashboard")
        st.markdown("---")
        st.warning("⚠️ Trang này chỉ dành cho quản trị viên Sở Y tế.")
        st.text_input(
            "Nhập mật khẩu:", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        return False
    
    # Nếu mật khẩu sai
    elif not st.session_state["password_correct"]:
        st.title("🔐 Đăng nhập Dashboard")
        st.markdown("---")
        st.warning("⚠️ Trang này chỉ dành cho quản trị viên Sở Y tế.")
        st.text_input(
            "Nhập mật khẩu:", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        st.error("❌ Mật khẩu không đúng!")
        return False
    
    # Mật khẩu đúng
    return True

# Kiểm tra mật khẩu trước khi hiển thị Dashboard
if not check_password():
    st.stop()

st.title("📊 Dashboard tổng hợp báo cáo")
st.markdown("---")

# ============================================================================
# PHẦN 1: THỐNG KÊ TỔNG QUAN
# ============================================================================
st.header("📈 Thống kê tổng quan")

# Get statistics
try:
    stats = get_statistics()
except:
    # Demo data if Google Sheets not connected
    stats = {
        "total": 0,
        "kcb": 0,
        "kiem_nghiem": 0,
        "sx_kd_duoc": 0,
        "sx_kd_my_pham": 0
    }

# Display metrics
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="Tổng số cơ sở đã nộp",
        value=stats["total"],
        delta=None
    )

with col2:
    st.metric(
        label="Cơ sở KCB",
        value=stats["kcb"],
        delta=None
    )

with col3:
    st.metric(
        label="TT Kiểm nghiệm",
        value=stats["kiem_nghiem"],
        delta=None
    )

with col4:
    st.metric(
        label="SX-KD Dược",
        value=stats["sx_kd_duoc"],
        delta=None
    )

with col5:
    st.metric(
        label="SX-KD Mỹ phẩm",
        value=stats["sx_kd_my_pham"],
        delta=None
    )

st.markdown("---")

# ============================================================================
# PHẦN 2: BIỂU ĐỒ
# ============================================================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Phân bố theo loại cơ sở")
    
    if stats["total"] > 0:
        chart_data = {
            "Loại cơ sở": ["Cơ sở KCB", "TT Kiểm nghiệm", "SX-KD Dược", "SX-KD Mỹ phẩm"],
            "Số lượng": [stats["kcb"], stats["kiem_nghiem"], stats["sx_kd_duoc"], stats["sx_kd_my_pham"]]
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
    
    # Giả sử có 100 cơ sở cần nộp
    total_expected = 100
    progress = stats["total"] / total_expected if total_expected > 0 else 0
    
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

# ============================================================================
# PHẦN 3: DANH SÁCH CƠ SỞ ĐÃ NỘP
# ============================================================================
st.header("📋 Danh sách cơ sở đã nộp báo cáo")

# Get facilities data
try:
    facilities_df = get_all_facilities()
except:
    facilities_df = pd.DataFrame()

if not facilities_df.empty:
    # Filter options
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        search_term = st.text_input("🔍 Tìm kiếm theo tên cơ sở", "")
    
    with col2:
        filter_type = st.selectbox(
            "Lọc theo loại cơ sở",
            ["Tất cả", "Cơ sở khám bệnh, chữa bệnh", "Trung tâm Kiểm nghiệm", 
             "Cơ sở SX-KD dược", "Cơ sở SX-KD mỹ phẩm"]
        )
    
    with col3:
        st.write("")
        st.write("")
        refresh_btn = st.button("🔄 Làm mới")
    
    # Apply filters
    filtered_df = facilities_df.copy()
    
    if search_term:
        filtered_df = filtered_df[
            filtered_df["Tên cơ sở"].str.contains(search_term, case=False, na=False)
        ]
    
    if filter_type != "Tất cả":
        filtered_df = filtered_df[filtered_df["Loại cơ sở"] == filter_type]
    
    # Display table
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Thời gian nộp": st.column_config.DatetimeColumn(
                "Thời gian nộp",
                format="DD/MM/YYYY HH:mm"
            )
        }
    )
    
    st.caption(f"Hiển thị {len(filtered_df)} / {len(facilities_df)} cơ sở")
else:
    st.info("📭 Chưa có cơ sở nào nộp báo cáo")

st.markdown("---")

# ============================================================================
# PHẦN 4: XEM CHI TIẾT TỪNG CƠ SỞ
# ============================================================================
st.header("👁️ Xem chi tiết báo cáo")

if not facilities_df.empty:
    selected_facility = st.selectbox(
        "Chọn cơ sở để xem chi tiết",
        options=["-- Chọn cơ sở --"] + facilities_df["Tên cơ sở"].tolist()
    )
    
    if selected_facility != "-- Chọn cơ sở --":
        facility_info = facilities_df[facilities_df["Tên cơ sở"] == selected_facility].iloc[0]
        
        # Display facility info
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
        
        # Display form data based on facility type
        facility_type = facility_info.get('Loại cơ sở', '')
        
        if facility_type == "Cơ sở khám bệnh, chữa bệnh":
            # Form 01
            try:
                form_01_df = get_form_data("Biểu mẫu 01 - Nhân lực DLS")
                form_01_data = form_01_df[form_01_df["Tên cơ sở"] == selected_facility]
                
                if not form_01_data.empty:
                    st.subheader("📋 Biểu mẫu 01: Nhân lực dược lâm sàng")
                    st.dataframe(form_01_data, use_container_width=True, hide_index=True)
            except:
                pass
            
            # Form 02
            try:
                form_02_df = get_form_data("Biểu mẫu 02 - Giá trị thuốc")
                form_02_data = form_02_df[form_02_df["Tên cơ sở"] == selected_facility]
                
                if not form_02_data.empty:
                    st.subheader("📋 Biểu mẫu 02: Giá trị thuốc sử dụng")
                    st.dataframe(form_02_data, use_container_width=True, hide_index=True)
            except:
                pass
            
            # Form 03
            try:
                form_03_df = get_form_data("Biểu mẫu 03 - Thuốc trong nước")
                form_03_data = form_03_df[form_03_df["Tên cơ sở"] == selected_facility]
                
                if not form_03_data.empty:
                    st.subheader("📋 Biểu mẫu 03: Thuốc sản xuất trong nước")
                    st.dataframe(form_03_data, use_container_width=True, hide_index=True)
            except:
                pass
        
        elif facility_type == "Trung tâm Kiểm nghiệm":
            try:
                form_04_df = get_form_data("Biểu mẫu 04 - Chất lượng thuốc")
                form_04_data = form_04_df[form_04_df["Tên cơ sở"] == selected_facility]
                
                if not form_04_data.empty:
                    st.subheader("📋 Biểu mẫu 04: Chất lượng thuốc")
                    st.dataframe(form_04_data, use_container_width=True, hide_index=True)
            except:
                pass
        
        elif facility_type == "Cơ sở SX-KD dược":
            try:
                form_05_df = get_form_data("Biểu mẫu 05 - Cung ứng thuốc")
                form_05_data = form_05_df[form_05_df["Tên cơ sở"] == selected_facility]
                
                if not form_05_data.empty:
                    st.subheader("📋 Biểu mẫu 05: Hệ thống cung ứng thuốc")
                    st.dataframe(form_05_data, use_container_width=True, hide_index=True)
            except:
                pass
        
        elif facility_type == "Cơ sở SX-KD mỹ phẩm":
            try:
                form_06_df = get_form_data("Biểu mẫu 06 - Mỹ phẩm")
                form_06_data = form_06_df[form_06_df["Tên cơ sở"] == selected_facility]
                
                if not form_06_data.empty:
                    st.subheader("📋 Biểu mẫu 06: Sản xuất mỹ phẩm")
                    st.dataframe(form_06_data, use_container_width=True, hide_index=True)
            except:
                pass
        
        # PDF link
        try:
            pdf_df = get_form_data("File PDF")
            pdf_data = pdf_df[pdf_df["Tên cơ sở"] == selected_facility]
            
            if not pdf_data.empty:
                st.subheader("📄 File PDF đã upload")
                for _, row in pdf_data.iterrows():
                    st.markdown(f"🔗 [Xem file PDF]({row['Link file PDF']})")
        except:
            pass

else:
    st.info("Chưa có dữ liệu để hiển thị")

# ============================================================================
# PHẦN 5: XUẤT BÁO CÁO
# ============================================================================
st.markdown("---")
st.header("📥 Xuất báo cáo tổng hợp")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📥 Xuất danh sách cơ sở (Excel)", use_container_width=True):
        if not facilities_df.empty:
            # Convert to Excel
            import io
            buffer = io.BytesIO()
            facilities_df.to_excel(buffer, index=False, engine='openpyxl')
            buffer.seek(0)
            
            st.download_button(
                label="💾 Tải file Excel",
                data=buffer,
                file_name="danh_sach_co_so_bao_cao.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("Không có dữ liệu để xuất")

with col2:
    if st.button("📥 Xuất biểu mẫu 01 (Excel)", use_container_width=True):
        try:
            form_01_df = get_form_data("Biểu mẫu 01 - Nhân lực DLS")
            if not form_01_df.empty:
                import io
                buffer = io.BytesIO()
                form_01_df.to_excel(buffer, index=False, engine='openpyxl')
                buffer.seek(0)
                
                st.download_button(
                    label="💾 Tải file Excel",
                    data=buffer,
                    file_name="bieu_mau_01_nhan_luc_dls.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.warning("Không có dữ liệu để xuất")
        except:
            st.warning("Không có dữ liệu để xuất")

with col3:
    if st.button("📥 Xuất biểu mẫu 02 (Excel)", use_container_width=True):
        try:
            form_02_df = get_form_data("Biểu mẫu 02 - Giá trị thuốc")
            if not form_02_df.empty:
                import io
                buffer = io.BytesIO()
                form_02_df.to_excel(buffer, index=False, engine='openpyxl')
                buffer.seek(0)
                
                st.download_button(
                    label="💾 Tải file Excel",
                    data=buffer,
                    file_name="bieu_mau_02_gia_tri_thuoc.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.warning("Không có dữ liệu để xuất")
        except:
            st.warning("Không có dữ liệu để xuất")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #9CA3AF; font-size: 0.8rem;">
    © 2026 Sở Y tế tỉnh Phú Thọ | Dashboard báo cáo thống kê dược - mỹ phẩm
</div>
""", unsafe_allow_html=True)
