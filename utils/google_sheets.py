"""
Google Sheets utility functions for the reporting system.
"""
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime


# Google Sheets scopes
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


def get_google_client():
    """Get authenticated Google Sheets client."""
    try:
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=SCOPES
        )
        client = gspread.authorize(credentials)
        return client
    except Exception as e:
        st.error(f"Lỗi kết nối Google Sheets: {e}")
        return None


def get_spreadsheet():
    """Get the main spreadsheet."""
    client = get_google_client()
    if client:
        try:
            spreadsheet = client.open_by_key(st.secrets["spreadsheet_id"])
            return spreadsheet
        except Exception as e:
            st.error(f"Lỗi mở spreadsheet: {e}")
    return None


def get_or_create_worksheet(spreadsheet, sheet_name, headers=None):
    """Get worksheet by name, create if not exists."""
    try:
        worksheet = spreadsheet.worksheet(sheet_name)
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=30)
        if headers:
            worksheet.append_row(headers)
    return worksheet


def save_facility_info(data: dict):
    """Save facility information to Google Sheets."""
    spreadsheet = get_spreadsheet()
    if not spreadsheet:
        return False
    
    headers = [
        "Thời gian nộp", "Tên cơ sở", "Địa chỉ", "Điện thoại", 
        "Email", "Loại cơ sở", "Người đại diện"
    ]
    
    worksheet = get_or_create_worksheet(spreadsheet, "Danh sách cơ sở", headers)
    
    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        data.get("ten_co_so", ""),
        data.get("dia_chi", ""),
        data.get("dien_thoai", ""),
        data.get("email", ""),
        data.get("loai_co_so", ""),
        data.get("nguoi_dai_dien", "")
    ]
    
    worksheet.append_row(row)
    return True


def save_form_01(facility_name: str, data: dict):
    """Save Form 01 - Nhân lực dược lâm sàng."""
    spreadsheet = get_spreadsheet()
    if not spreadsheet:
        return False
    
    headers = [
        "Thời gian nộp", "Tên cơ sở", "Tổng số", "Sau ĐH dược", 
        "ĐH dược", "Khác", "Số kiêm nhiệm", "Số có CCHN"
    ]
    
    worksheet = get_or_create_worksheet(spreadsheet, "Biểu mẫu 01 - Nhân lực DLS", headers)
    
    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        facility_name,
        data.get("tong_so", 0),
        data.get("sau_dh", 0),
        data.get("dh", 0),
        data.get("khac", 0),
        data.get("kiem_nhiem", 0),
        data.get("co_cchn", 0)
    ]
    
    worksheet.append_row(row)
    return True


def save_form_02(facility_name: str, data: dict):
    """Save Form 02 - Giá trị thuốc sử dụng."""
    spreadsheet = get_spreadsheet()
    if not spreadsheet:
        return False
    
    headers = [
        "Thời gian nộp", "Tên cơ sở", "Tổng giá trị", "Biệt dược gốc",
        "Generic", "Dược liệu", "Kháng sinh", "Vắc xin", 
        "Sinh phẩm", "Phóng xạ", "BHYT", "Viện trợ"
    ]
    
    worksheet = get_or_create_worksheet(spreadsheet, "Biểu mẫu 02 - Giá trị thuốc", headers)
    
    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        facility_name,
        data.get("tong_gia_tri", 0),
        data.get("biet_duoc_goc", 0),
        data.get("generic", 0),
        data.get("duoc_lieu", 0),
        data.get("khang_sinh", 0),
        data.get("vac_xin", 0),
        data.get("sinh_pham", 0),
        data.get("phong_xa", 0),
        data.get("bhyt", 0),
        data.get("vien_tro", 0)
    ]
    
    worksheet.append_row(row)
    return True


def save_form_03(facility_name: str, data: dict):
    """Save Form 03 - Thuốc sản xuất trong nước."""
    spreadsheet = get_spreadsheet()
    if not spreadsheet:
        return False
    
    headers = [
        "Thời gian nộp", "Tên cơ sở", "SL thuốc trúng thầu", 
        "SL thuốc SX trong nước", "Tỷ lệ SL (%)", 
        "Tổng giá trị", "Giá trị thuốc SX trong nước", "Tỷ lệ GT (%)"
    ]
    
    worksheet = get_or_create_worksheet(spreadsheet, "Biểu mẫu 03 - Thuốc trong nước", headers)
    
    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        facility_name,
        data.get("sl_trung_thau", 0),
        data.get("sl_trong_nuoc", 0),
        data.get("ty_le_sl", 0),
        data.get("tong_gia_tri", 0),
        data.get("gt_trong_nuoc", 0),
        data.get("ty_le_gt", 0)
    ]
    
    worksheet.append_row(row)
    return True


def save_form_04(facility_name: str, data: dict):
    """Save Form 04 - Chất lượng thuốc."""
    spreadsheet = get_spreadsheet()
    if not spreadsheet:
        return False
    
    headers = [
        "Thời gian nộp", "Tên cơ sở", "Số mẫu kiểm tra", 
        "Số mẫu không đạt", "Mức độ 1", "Mức độ 2", "Mức độ 3",
        "Tỷ lệ không đạt (%)", "Số lô thuốc giả", "Tỷ lệ thuốc giả (%)"
    ]
    
    worksheet = get_or_create_worksheet(spreadsheet, "Biểu mẫu 04 - Chất lượng thuốc", headers)
    
    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        facility_name,
        data.get("so_mau_kiem_tra", 0),
        data.get("so_mau_khong_dat", 0),
        data.get("muc_do_1", 0),
        data.get("muc_do_2", 0),
        data.get("muc_do_3", 0),
        data.get("ty_le_khong_dat", 0),
        data.get("so_lo_gia", 0),
        data.get("ty_le_gia", 0)
    ]
    
    worksheet.append_row(row)
    return True


def save_form_05(facility_name: str, data: dict):
    """Save Form 05 - Hệ thống cung ứng thuốc."""
    spreadsheet = get_spreadsheet()
    if not spreadsheet:
        return False
    
    headers = [
        "Thời gian nộp", "Tên cơ sở", "CS bán buôn", "Tổng CS bán lẻ",
        "Nhà thuốc", "Quầy thuốc", "Tủ thuốc TYT",
        "TS/DSCKII", "ThS/DSCKI", "DSĐH", "DSCĐ/TH", "Dược tá"
    ]
    
    worksheet = get_or_create_worksheet(spreadsheet, "Biểu mẫu 05 - Cung ứng thuốc", headers)
    
    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        facility_name,
        data.get("cs_ban_buon", 0),
        data.get("tong_cs_ban_le", 0),
        data.get("nha_thuoc", 0),
        data.get("quay_thuoc", 0),
        data.get("tu_thuoc_tyt", 0),
        data.get("ts_dsckii", 0),
        data.get("ths_dscki", 0),
        data.get("dsdh", 0),
        data.get("dscd_th", 0),
        data.get("duoc_ta", 0)
    ]
    
    worksheet.append_row(row)
    return True


def save_form_06(facility_name: str, data: dict):
    """Save Form 06 - Sản xuất mỹ phẩm."""
    spreadsheet = get_spreadsheet()
    if not spreadsheet:
        return False
    
    headers = [
        "Thời gian nộp", "Tên cơ sở", "Giá trị nhập khẩu",
        "Giá trị sản xuất", "Số phiếu công bố"
    ]
    
    worksheet = get_or_create_worksheet(spreadsheet, "Biểu mẫu 06 - Mỹ phẩm", headers)
    
    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        facility_name,
        data.get("gia_tri_nhap_khau", 0),
        data.get("gia_tri_san_xuat", 0),
        data.get("so_phieu_cong_bo", 0)
    ]
    
    worksheet.append_row(row)
    return True


def save_form_07(facility_name: str, data: dict):
    """Save Form 07 - Phụ lục VII: Giá trị SX, nhập khẩu mỹ phẩm."""
    spreadsheet = get_spreadsheet()
    if not spreadsheet:
        return False
    
    headers = [
        "Thời gian nộp", "Tên cơ sở", "Giá trị nhập khẩu",
        "Giá trị sản xuất", "Số phiếu công bố"
    ]
    
    worksheet = get_or_create_worksheet(spreadsheet, "Phụ lục VII - Mỹ phẩm", headers)
    
    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        facility_name,
        data.get("gia_tri_nhap_khau", 0),
        data.get("gia_tri_san_xuat", 0),
        data.get("so_phieu_cong_bo", 0)
    ]
    
    worksheet.append_row(row)
    return True


def save_pdf_link(facility_name: str, pdf_link: str):
    """Save PDF file link."""
    spreadsheet = get_spreadsheet()
    if not spreadsheet:
        return False
    
    headers = ["Thời gian nộp", "Tên cơ sở", "Link file PDF"]
    
    worksheet = get_or_create_worksheet(spreadsheet, "File PDF", headers)
    
    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        facility_name,
        pdf_link
    ]
    
    worksheet.append_row(row)
    return True


def save_pdf_info(facility_name: str, filename: str, filesize: int):
    """Save PDF file info (không upload, chỉ lưu thông tin)."""
    spreadsheet = get_spreadsheet()
    if not spreadsheet:
        return False
    
    headers = ["Thời gian nộp", "Tên cơ sở", "Tên file", "Kích thước (KB)", "Ghi chú"]
    
    worksheet = get_or_create_worksheet(spreadsheet, "File PDF", headers)
    
    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        facility_name,
        filename,
        round(filesize / 1024, 2),
        "Đã upload - cần gửi file qua email"
    ]
    
    worksheet.append_row(row)
    return True


def get_all_facilities():
    """Get all facilities data."""
    spreadsheet = get_spreadsheet()
    if not spreadsheet:
        return pd.DataFrame()
    
    try:
        worksheet = spreadsheet.worksheet("Danh sách cơ sở")
        data = worksheet.get_all_records()
        return pd.DataFrame(data)
    except:
        return pd.DataFrame()


def get_form_data(sheet_name: str):
    """Get data from a specific form sheet."""
    spreadsheet = get_spreadsheet()
    if not spreadsheet:
        return pd.DataFrame()
    
    try:
        worksheet = spreadsheet.worksheet(sheet_name)
        data = worksheet.get_all_records()
        return pd.DataFrame(data)
    except:
        return pd.DataFrame()


def get_statistics():
    """Get statistics for dashboard."""
    facilities = get_all_facilities()
    
    if facilities.empty:
        return {
            "total": 0,
            "kcb": 0,
            "kiem_nghiem": 0,
            "sx_kd_duoc": 0,
            "sx_kd_my_pham": 0
        }
    
    stats = {
        "total": len(facilities),
        "kcb": len(facilities[facilities["Loại cơ sở"] == "Cơ sở khám bệnh, chữa bệnh"]),
        "kiem_nghiem": len(facilities[facilities["Loại cơ sở"] == "Trung tâm Kiểm nghiệm"]),
        "sx_kd_duoc": len(facilities[facilities["Loại cơ sở"] == "Cơ sở SX-KD dược"]),
        "sx_kd_my_pham": len(facilities[facilities["Loại cơ sở"] == "Cơ sở SX-KD mỹ phẩm"])
    }
    
    return stats
