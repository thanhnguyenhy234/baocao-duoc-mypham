"""Kiểm tra hợp lệ dữ liệu đăng ký cập nhật kiến thức chuyên môn dược.

Mọi hàm trả về danh sách lỗi bằng tiếng Việt; danh sách rỗng nghĩa là hợp lệ.
"""
from __future__ import annotations

# Các trường bắt buộc: (key trong dict đăng ký, thông báo lỗi khi để trống)
# Lưu ý: "ngay_cap" KHÔNG nằm trong danh sách này — ngày cấp CCHND là trường
# không bắt buộc, người đăng ký được phép để trống.
REQUIRED_FIELDS: list[tuple[str, str]] = [
    ("ho_ten", "Vui lòng nhập họ và tên."),
    ("so_chung_chi", "Vui lòng nhập số Chứng chỉ hành nghề dược."),
    ("noi_cap", "Vui lòng nhập nơi cấp."),
    ("dia_chi_thuong_tru", "Vui lòng nhập địa chỉ thường trú."),
    ("so_dien_thoai", "Vui lòng nhập số điện thoại."),
]


def _to_text(value) -> str:
    """Chuẩn hóa giá trị về chuỗi đã cắt khoảng trắng."""
    if value is None:
        return ""
    return str(value).strip()


def validate_so_chung_chi(value) -> list[str]:
    """Số Chứng chỉ hành nghề dược (CCHND): chỉ bắt buộc không để trống.

    Số CCHND là chuỗi tự do do người dùng nhập theo đúng chứng chỉ thật của họ
    (ví dụ ``12345``, ``12345/PTH-2024``, ``V-PTH-00123`` hay chuỗi có ký tự đặc biệt);
    không kiểm tra định dạng, độ dài hay thành phần ký tự.
    Chỉ trả về lỗi khi giá trị rỗng hoặc chỉ gồm khoảng trắng.
    """
    if not _to_text(value):
        return ["Vui lòng nhập số Chứng chỉ hành nghề dược."]
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


def validate_email(value) -> list[str]:
    """Email: KHÔNG bắt buộc, chỉ kiểm tra nhẹ.

    Để trống (hoặc chỉ khoảng trắng) => hợp lệ. Nếu có nhập thì chuỗi phải chứa
    ký tự ``@`` và có dấu ``.`` ở phần sau ``@`` (ví dụ ``nguoiban@example.com``).
    Cố ý không kiểm tra địa chỉ email có tồn tại thật hay không để tránh chặn oan.
    """
    text = _to_text(value)
    if not text:
        return []
    if "@" in text and "." in text.split("@", 1)[1]:
        return []
    return [
        "Email không hợp lệ. Vui lòng nhập đúng dạng có ký tự @ và dấu chấm sau @ "
        "(ví dụ: nguoiban@example.com)."
    ]


def validate_registration(registration: dict) -> list[str]:
    """Kiểm tra toàn bộ phiếu đăng ký, trả về danh sách lỗi (rỗng là hợp lệ).

    Ngày cấp (``ngay_cap``) là trường KHÔNG bắt buộc và không bị kiểm soát
    (không chặn ngày tương lai, không bắt buộc chọn) — người đăng ký được để trống.

    6 trường mới theo phiếu đăng ký gốc (``ngay_sinh``, ``cho_o_hien_nay``, ``email``,
    ``van_bang_chuyen_mon``, ``linh_vuc_nghe_duoc``, ``noi_cong_tac``) đều KHÔNG bắt buộc
    và KHÔNG kiểm tra định dạng — riêng ``email`` chỉ kiểm tra nhẹ khi có nhập.
    """
    if not isinstance(registration, dict):
        return ["Dữ liệu đăng ký không hợp lệ."]

    errors: list[str] = []
    for key, message in REQUIRED_FIELDS:
        if _to_text(registration.get(key)) == "":
            errors.append(message)

    errors.extend(validate_so_chung_chi(registration.get("so_chung_chi")))
    errors.extend(validate_so_dien_thoai(registration.get("so_dien_thoai")))

    # Email không bắt buộc: chỉ kiểm tra khi người dùng có nhập,
    # để không sinh thêm thông báo trùng với nhóm trường bắt buộc.
    if _to_text(registration.get("email")) != "":
        errors.extend(validate_email(registration.get("email")))

    # Loại bỏ thông báo trùng nhau nhưng giữ nguyên thứ tự xuất hiện
    unique_errors: list[str] = []
    for error in errors:
        if error not in unique_errors:
            unique_errors.append(error)
    return unique_errors
