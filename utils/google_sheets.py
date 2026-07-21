"""
Google Sheets utility functions - Báo cáo 6 tháng đầu năm 2026.

Schema áp dụng cho 3 phụ lục theo cv_bao_cao_thong_ke_duoc_my_pham.tex:
  - Phụ lục I  : Giá trị thuốc đã sử dụng            (đơn vị y tế / bệnh viện)
  - Phụ lục II : Tình hình sử dụng thuốc SX trong nước (đơn vị y tế / bệnh viện)
  - Phụ lục III: Tình hình CL thuốc, NL làm thuốc     (Trung tâm Kiểm nghiệm)

Sheet name có prefix "6T2026 -" để không trộn với dữ liệu báo cáo năm
(tách biệt cả trong cùng 1 spreadsheet).
"""
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


def get_google_client():
    try:
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=SCOPES
        )
        return gspread.authorize(credentials)
    except Exception as e:
        st.error(f"Lỗi kết nối Google Sheets: {e}")
        return None


def get_spreadsheet():
    client = get_google_client()
    if client:
        try:
            return client.open_by_key(st.secrets["spreadsheet_id"])
        except Exception as e:
            st.error(f"Lỗi mở spreadsheet: {e}")
    return None


def get_or_create_worksheet(spreadsheet, sheet_name, headers=None):
    try:
        worksheet = spreadsheet.worksheet(sheet_name)
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=30)
        if headers:
            worksheet.append_row(headers)
    return worksheet


def save_facility_info(data: dict):
    spreadsheet = get_spreadsheet()
    if not spreadsheet:
        return False

    headers = [
        "Thời gian nộp", "Tên cơ sở", "Địa chỉ", "Điện thoại",
        "Email", "Loại cơ sở", "Người đại diện"
    ]
    worksheet = get_or_create_worksheet(spreadsheet, "6T2026 - Danh sách cơ sở", headers)

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


def save_phuluc_01(facility_name: str, data: dict):
    """Phụ lục I: Giá trị thuốc đã sử dụng (Biểu 4/BCT - 06 tháng)."""
    spreadsheet = get_spreadsheet()
    if not spreadsheet:
        return False

    headers = [
        "Thời gian nộp", "Tên cơ sở", "Tổng giá trị sử dụng thuốc",
        "Thuốc biệt dược gốc", "Thuốc generic", "Thuốc dược liệu",
        "Kháng sinh", "Vắc xin", "Sinh phẩm", "Thuốc phóng xạ",
        "Giá trị thuốc BHYT", "Thuốc viện trợ"
    ]
    worksheet = get_or_create_worksheet(spreadsheet, "6T2026 - Phụ lục I - Giá trị thuốc", headers)

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


def save_phuluc_02(facility_name: str, data: dict):
    """Phụ lục II: Tình hình sử dụng thuốc SX trong nước (Biểu 5/BCT - 06 tháng)."""
    spreadsheet = get_spreadsheet()
    if not spreadsheet:
        return False

    headers = [
        "Thời gian nộp", "Tên cơ sở",
        "SL thuốc trúng thầu", "SL thuốc SX trong nước trúng thầu", "Tỷ lệ SL (%)",
        "Tổng số tiền thuốc sử dụng", "Tổng số tiền thuốc SX trong nước", "Tỷ lệ GT (%)"
    ]
    worksheet = get_or_create_worksheet(spreadsheet, "6T2026 - Phụ lục II - Thuốc trong nước", headers)

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


def save_phuluc_03(facility_name: str, data: dict):
    """Phụ lục III: Tình hình CL thuốc, NL làm thuốc (Biểu 3/BCT - 06 tháng).

    Bao gồm 4 phân loại thuốc giả theo tex:
      - SP cơ sở SX trong nước
      - SP cơ sở SX nước ngoài
      - Không chứa hoạt chất
      - Bao bì nhãn mác
    """
    spreadsheet = get_spreadsheet()
    if not spreadsheet:
        return False

    headers = [
        "Thời gian nộp", "Tên cơ sở",
        "Số mẫu lấy kiểm tra CL",
        "Số mẫu không đạt tiêu chuẩn CL",
        "Vi phạm mức độ 1", "Vi phạm mức độ 2", "Vi phạm mức độ 3",
        "Tỷ lệ mẫu thuốc không đạt CL (%)",
        "Số lô thuốc giả phát hiện được",
        "Tỷ lệ thuốc giả (%)",
        "Giả - SP cơ sở SX trong nước (%)",
        "Giả - SP cơ sở SX nước ngoài (%)",
        "Giả - Không chứa hoạt chất (%)",
        "Giả - Bao bì nhãn mác (%)"
    ]
    worksheet = get_or_create_worksheet(spreadsheet, "6T2026 - Phụ lục III - CL thuốc", headers)

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
        data.get("ty_le_gia", 0),
        data.get("gia_nn", 0),
        data.get("gia_tn", 0),
        data.get("gia_khong_hoat_chat", 0),
        data.get("gia_bao_bi", 0)
    ]
    worksheet.append_row(row)
    return True


def save_pdf_info(facility_name: str, filename: str, filesize: int,
                  drive_link: str = "", drive_id: str = ""):
    spreadsheet = get_spreadsheet()
    if not spreadsheet:
        return False

    # Schema có 2 cột mới ở cuối (Link Drive, Drive File ID) dùng cho Dashboard đối chiếu PDF.
    headers = ["Thời gian nộp", "Tên cơ sở", "Tên file", "Kích thước (KB)",
               "Ghi chú", "Link Drive", "Drive File ID"]
    worksheet = get_or_create_worksheet(spreadsheet, "6T2026 - File PDF", headers)

    ghi_chu = "Đã upload lên Drive" if drive_link else "Chỉ gửi Discord - chưa có link Drive"
    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        facility_name,
        filename,
        round(filesize / 1024, 2),
        ghi_chu,
        drive_link,
        drive_id
    ]
    worksheet.append_row(row)
    return True


def get_pdf_link(facility_name: str):
    """Trả về (drive_link, drive_id) mới nhất của cơ sở trong sheet 'File PDF'.

    Returns:
        tuple(str, str): (link, id); ("", "") nếu không có hoặc thiếu cấu hình.
    """
    spreadsheet = get_spreadsheet()
    if not spreadsheet:
        return "", ""
    try:
        worksheet = spreadsheet.worksheet("6T2026 - File PDF")
        data = worksheet.get_all_records()
    except Exception:
        return "", ""
    if not data:
        return "", ""
    df = pd.DataFrame(data)
    df = df[df["Tên cơ sở"] == facility_name]
    if df.empty:
        return "", ""
    # Lấy bản mới nhất (dòng cuối cùng theo thời gian nộp)
    last = df.iloc[-1]
    link = str(last.get("Link Drive", "") or "")
    file_id = str(last.get("Drive File ID", "") or "")
    if not link:
        return "", ""
    # Nếu có link nhưng thiếu id (do link cũ), cố suy id từ webViewLink
    if not file_id and "file/d/" in link:
        try:
            file_id = link.split("file/d/")[1].split("/")[0]
        except Exception:
            file_id = ""
    return link, file_id


def get_all_facilities():
    spreadsheet = get_spreadsheet()
    if not spreadsheet:
        return pd.DataFrame()
    try:
        worksheet = spreadsheet.worksheet("6T2026 - Danh sách cơ sở")
        data = worksheet.get_all_records()
        return pd.DataFrame(data)
    except Exception:
        return pd.DataFrame()


def get_form_data(sheet_name: str):
    spreadsheet = get_spreadsheet()
    if not spreadsheet:
        return pd.DataFrame()
    try:
        worksheet = spreadsheet.worksheet(sheet_name)
        data = worksheet.get_all_records()
        return pd.DataFrame(data)
    except Exception:
        return pd.DataFrame()


def get_statistics():
    """Thống kê cho dashboard 6 tháng - chỉ 2 loại cơ sở."""
    facilities = get_all_facilities()
    if facilities.empty:
        return {"total": 0, "yte": 0, "kiem_nghiem": 0}

    return {
        "total": len(facilities),
        "yte": len(facilities[facilities["Loại cơ sở"] == "Đơn vị y tế trực thuộc Sở Y tế / Bệnh viện"]),
        "kiem_nghiem": len(facilities[facilities["Loại cơ sở"] == "Trung tâm Kiểm nghiệm tỉnh Phú Thọ"])
    }
