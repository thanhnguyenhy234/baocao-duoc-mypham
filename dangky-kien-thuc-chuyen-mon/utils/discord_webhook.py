"""Gửi thông báo đăng ký qua Discord webhook."""
from __future__ import annotations

import requests
import streamlit as st

from utils.storage import format_ngay_cap


def get_webhook_url() -> str | None:
    try:
        return st.secrets.get("discord_webhook_url") or None
    except Exception:
        return None


def send_registration_notification(registration: dict) -> dict:
    webhook_url = get_webhook_url()
    if not webhook_url:
        return {"ok": False, "message": "Chưa cấu hình discord_webhook_url trong secrets."}

    content = f"""🩺 **ĐĂNG KÝ CẬP NHẬT KIẾN THỨC CHUYÊN MÔN DƯỢC**

👤 **Họ và tên:** {registration.get("ho_ten", "")}
🎫 **Số CCHND:** {registration.get("so_chung_chi", "")}
📅 **Ngày cấp:** {format_ngay_cap(registration.get("ngay_cap", "")) or "—"}
🏛️ **Nơi cấp:** {registration.get("noi_cap", "") or "—"}
🏠 **Địa chỉ thường trú:** {registration.get("dia_chi_thuong_tru", "") or "—"}
📞 **Số điện thoại:** {registration.get("so_dien_thoai", "")}
🎓 **Khóa học:** {registration.get("khoa_hoc", "")}
⏰ **Thời gian đăng ký:** {registration.get("timestamp", "")}
"""

    try:
        response = requests.post(
            webhook_url,
            json={"content": content, "username": "Đăng ký KKT chuyên môn dược"},
            timeout=20,
        )
        if response.status_code in (200, 204):
            return {"ok": True, "message": "Đã gửi Discord."}
        return {"ok": False, "message": f"Discord trả về {response.status_code}: {response.text}"}
    except Exception as exc:
        return {"ok": False, "message": str(exc)}
