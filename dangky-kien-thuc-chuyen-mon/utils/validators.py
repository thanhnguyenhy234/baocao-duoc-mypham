"""Kiểm tra hợp lệ dữ liệu đăng ký cập nhật kiến thức chuyên môn dược.

Mọi hàm trả về danh sách lỗi bằng tiếng Việt; danh sách rỗng nghĩa là hợp lệ.
"""
from __future__ import annotations

from datetime import date, datetime

# Các trường bắt buộc: (key trong dict đăng ký, thông báo lỗi khi để trống)
REQUIRED_FIELDS: list[tuple[str, str]] = [
    ("ho_ten", "Vui lòng nhập họ và tên."),
    ("so_cccd", "Vui lòng nhập số CCCND/CCCD."),
    ("ngay_cap", "Vui lòng chọn ngày cấp."),
    ("noi_cap", "Vui lòng nhập nơi cấp."),
    ("dia_chi_thuong_tru", "Vui lòng nhập địa chỉ thường trú."),
    ("so_dien_thoai", "Vui lòng nhập số điện thoại."),
]

NGAY_CAP_FORMAT = "%d/%m/%Y"


def _to_text(value) -> str:
    """Chuẩn hóa giá trị về chuỗi đã cắt khoảng trắng."""
    if value is None:
        return ""
    return str(value).strip()


def _parse_ngay_cap(value) -> date | None:
    """Đọc ngày cấp từ date/datetime hoặc chuỗi dd/mm/yyyy."""
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value

    text = _to_text(value)
    if not text:
        return None
    for fmt in (NGAY_CAP_FORMAT, "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def validate_so_cccd(value) -> list[str]:
    """Số CCCND/CCCD: chỉ chữ số, gồm 9 số (CMND) hoặc 12 số (CCCD)."""
    text = _to_text(value)
    if not text:
        return ["Vui lòng nhập số CCCND/CCCD."]
    if not (text.isascii() and text.isdigit()):
        return ["Số CCCND/CCCD chỉ được chứa chữ số."]
    if len(text) not in (9, 12):
        return ["Số CCCND/CCCD phải gồm 9 số (CMND) hoặc 12 số (CCCD)."]
    return []


def validate_ngay_cap(value, today: date | None = None) -> list[str]:
    """Ngày cấp không được sau ngày hôm nay."""
    if value is None or _to_text(value) == "":
        return ["Vui lòng chọn ngày cấp."]

    parsed = _parse_ngay_cap(value)
    if parsed is None:
        return [f"Ngày cấp không hợp lệ (định dạng {NGAY_CAP_FORMAT})."]
    if parsed > (today or date.today()):
        return ["Ngày cấp không được sau ngày hôm nay."]
    return []


def validate_so_dien_thoai(value) -> list[str]:
    """Số điện thoại: gồm 10 số và bắt đầu bằng số 0."""
    text = _to_text(value)
    if not text:
        return ["Vui lòng nhập số điện thoại."]
    if not (text.isascii() and text.isdigit()):
        return ["Số điện thoại chỉ được chứa chữ số."]
    if len(text) != 10 or not text.startswith("0"):
        return ["Số điện thoại phải gồm 10 số và bắt đầu bằng số 0 (ví dụ: 0912345678)."]
    return []


def validate_registration(registration: dict, today: date | None = None) -> list[str]:
    """Kiểm tra toàn bộ phiếu đăng ký, trả về danh sách lỗi (rỗng là hợp lệ)."""
    if not isinstance(registration, dict):
        return ["Dữ liệu đăng ký không hợp lệ."]

    errors: list[str] = []
    for key, message in REQUIRED_FIELDS:
        if _to_text(registration.get(key)) == "":
            errors.append(message)

    errors.extend(validate_so_cccd(registration.get("so_cccd")))
    errors.extend(validate_so_dien_thoai(registration.get("so_dien_thoai")))
    if _to_text(registration.get("ngay_cap")) != "":
        errors.extend(validate_ngay_cap(registration.get("ngay_cap"), today))

    # Loại bỏ thông báo trùng nhau nhưng giữ nguyên thứ tự xuất hiện
    unique_errors: list[str] = []
    for error in errors:
        if error not in unique_errors:
            unique_errors.append(error)
    return unique_errors
