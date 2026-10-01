"""Lưu dữ liệu đăng ký vào Google Sheets hoặc CSV cục bộ."""
from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

import pandas as pd
import streamlit as st

try:
    import gspread
    from google.oauth2.service_account import Credentials
except Exception:  # pragma: no cover
    gspread = None
    Credentials = None

CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "registrations.csv"
SHEET_NAME = "Đăng ký cập nhật KKT chuyên môn dược"
COURSE_NAME = "Cập nhật kiến thức chuyên môn dược"
HEADERS = [
    "Thời gian đăng ký",
    "Họ và tên",
    "Số CCCND",
    "Ngày cấp",
    "Nơi cấp",
    "Địa chỉ thường trú",
    "Số điện thoại",
    "Ghi chú",
    "Khóa học",
]
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def format_ngay_cap(value) -> str:
    """Chuẩn hóa ngày cấp về chuỗi dd/mm/yyyy để lưu và gửi thông báo."""
    if isinstance(value, datetime):
        value = value.date()
    if isinstance(value, date):
        return value.strftime("%d/%m/%Y")
    return str(value or "").strip()


def _row_from_registration(registration: dict) -> list[str]:
    return [
        registration.get("timestamp", ""),
        registration.get("ho_ten", ""),
        registration.get("so_cccd", ""),
        format_ngay_cap(registration.get("ngay_cap", "")),
        registration.get("noi_cap", ""),
        registration.get("dia_chi_thuong_tru", ""),
        registration.get("so_dien_thoai", ""),
        registration.get("ghi_chu", ""),
        registration.get("khoa_hoc", COURSE_NAME),
    ]


def _google_ready() -> bool:
    try:
        return bool(gspread and Credentials and st.secrets.get("spreadsheet_id") and st.secrets.get("gcp_service_account"))
    except Exception:
        return False


def _get_google_sheet():
    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES,
    )
    client = gspread.authorize(credentials)
    return client.open_by_key(st.secrets["spreadsheet_id"])


def _get_or_create_worksheet(spreadsheet):
    try:
        worksheet = spreadsheet.worksheet(SHEET_NAME)
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title=SHEET_NAME, rows=1000, cols=len(HEADERS) + 2)
        worksheet.append_row(HEADERS)
    return worksheet


def _save_to_google(registration: dict) -> dict:
    spreadsheet = _get_google_sheet()
    worksheet = _get_or_create_worksheet(spreadsheet)
    worksheet.append_row(_row_from_registration(registration))
    return {"ok": True, "mode": "Google Sheets", "message": ""}


def _save_to_csv(registration: dict) -> dict:
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    values = _row_from_registration(registration)
    row_df = pd.DataFrame([dict(zip(HEADERS, values))])

    if CSV_PATH.exists():
        # Đọc dạng chuỗi để không mất số 0 đầu của số điện thoại/số CCCND khi ghi nối tiếp
        current_df = pd.read_csv(CSV_PATH, dtype=str, keep_default_na=False)
        row_df = pd.concat([current_df, row_df], ignore_index=True)

    row_df.to_csv(CSV_PATH, index=False)
    return {"ok": True, "mode": "CSV cục bộ", "message": ""}


def save_registration(registration: dict) -> dict:
    try:
        if _google_ready():
            return _save_to_google(registration)
        return _save_to_csv(registration)
    except Exception as exc:
        return {"ok": False, "mode": "Lỗi", "message": str(exc)}


def get_registrations_df() -> pd.DataFrame:
    if _google_ready():
        try:
            worksheet = _get_or_create_worksheet(_get_google_sheet())
            records = worksheet.get_all_records()
            return pd.DataFrame(records)
        except Exception:
            pass

    if CSV_PATH.exists():
        return pd.read_csv(CSV_PATH, dtype=str, keep_default_na=False)

    return pd.DataFrame(columns=HEADERS)
