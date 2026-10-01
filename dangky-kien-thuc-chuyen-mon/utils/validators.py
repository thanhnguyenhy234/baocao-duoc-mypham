"""Kiểm tra hợp lệ dữ liệu đăng ký cập nhật kiến thức chuyên môn dược.

Mọi hàm trả về danh sách lỗi bằng tiếng Việt; danh sách rỗng nghĩa là hợp lệ.
"""
from __future__ import annotations

from datetime import date, datetime

# Các trường bắt buộc: (key trong dict đăng ký, thông báo lỗi khi để trống)
REQUIRED_FIELDS: list[tuple[str, str]] = [
    ("ho_ten", "Vui lòng nhập họ và tên."),
    ("so_chung_chi", "Vui lòng nhập số Chứng chỉ hành nghề dược."),
    ("ngay_cap", "Vui lòng chọn ngày cấp."),
    ("noi_cap", "Vui lòng nhập nơi cấp."),
    ("dia_chi_thuong_tru", "Vui lòng nhập địa chỉ thường trú."),
    ("so_dien_thoai", "Vui lòng nhập số điện thoại."),
]

NGAY_CAP_FORMAT = "%d/%m/%Y"

# Quy tắc số Chứng chỉ hành nghề dược (CCHND): mã phối hợp chữ + số + dấu ngăn cách.
SO_CHUNG_CHI_MIN_LENGTH = 5
SO_CHUNG_CHI_MAX_LENGTH = 50
SO_CHUNG_CHI_SYMBOLS = frozenset("-/._")


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


def validate_so_chung_chi(value) -> list[str]:
    """Số Chứng chỉ hành nghề dược (CCHND).

    Số Chứng chỉ hành nghề dược là mã phối hợp chữ + số + dấu ngăn cách,
    ví dụ ``12345``, ``12345/PTH-2024``, ``V-PTH-00123`` hay ``PT-CT-4567``.
    Cho phép chữ cái Unicode (kể cả tiếng Việt có dấu), chữ số, khoảng trắng
    và các ký tự ``- / . _``; phải dài từ 5 đến 50 ký tự và có ít nhất 1 chữ số.
    """
    text = " ".join(_to_text(value).split())
    if not text:
        return ["Vui lòng nhập số Chứng chỉ hành nghề dược."]
    if len(text) < SO_CHUNG_CHI_MIN_LENGTH or len(text) > SO_CHUNG_CHI_MAX_LENGTH:
        return [
            "Số Chứng chỉ hành nghề dược phải gồm từ "
            f"{SO_CHUNG_CHI_MIN_LENGTH} đến {SO_CHUNG_CHI_MAX_LENGTH} ký tự."
        ]
    if any(
        not (ch.isalpha() or ch.isdigit() or ch.isspace() or ch in SO_CHUNG_CHI_SYMBOLS)
        for ch in text
    ):
        return [
            "Số Chứng chỉ hành nghề dược chỉ được chứa chữ cái, chữ số, khoảng trắng "
            "và các ký tự - / . _ (ví dụ: 12345/PTH-2024)."
        ]
    if not any(ch.isdigit() for ch in text):
        return ["Số Chứng chỉ hành nghề dược phải chứa ít nhất một chữ số."]
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

    errors.extend(validate_so_chung_chi(registration.get("so_chung_chi")))
    errors.extend(validate_so_dien_thoai(registration.get("so_dien_thoai")))
    if _to_text(registration.get("ngay_cap")) != "":
        errors.extend(validate_ngay_cap(registration.get("ngay_cap"), today))

    # Loại bỏ thông báo trùng nhau nhưng giữ nguyên thứ tự xuất hiện
    unique_errors: list[str] = []
    for error in errors:
        if error not in unique_errors:
            unique_errors.append(error)
    return unique_errors
