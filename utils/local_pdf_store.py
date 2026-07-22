"""Lưu PDF báo cáo local trên Pi (Dropbox) để admin đối chiếu với số liệu web.

Dashboard đọc file từ đây (st.pdf). Không dùng Google Drive.
"""
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

# Thư mục Dropbox trên Pi — sync backup tự động
DEFAULT_PDF_DIR = Path("/home/lediem/Dropbox/baocao-duoc-mypham-6thang-pdfs")


def _safe_name(text: str, max_len: int = 80) -> str:
    text = (text or "unknown").strip()
    text = re.sub(r"[\\/:*?\"<>|\s]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("._")
    return (text or "unknown")[:max_len]


def get_pdf_dir() -> Path:
    """Cho phép override bằng secrets['pdf_local_dir'] nếu có Streamlit."""
    try:
        import streamlit as st
        custom = st.secrets.get("pdf_local_dir", None)
        if custom:
            return Path(str(custom))
    except Exception:
        pass
    return DEFAULT_PDF_DIR


def save_pdf_local(file_bytes: bytes, filename: str, facility_name: str) -> str:
    """Lưu PDF ra Dropbox. Returns absolute path (str) hoặc '' nếu lỗi."""
    try:
        pdf_dir = get_pdf_dir()
        pdf_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base = _safe_name(Path(filename).stem) or "baocao"
        fac = _safe_name(facility_name)
        out_name = f"{stamp}_{fac}_{base}.pdf"
        out_path = pdf_dir / out_name
        out_path.write_bytes(file_bytes)
        return str(out_path.resolve())
    except Exception:
        return ""


def read_pdf_local(path: str) -> bytes | None:
    try:
        p = Path(path)
        if p.is_file() and p.suffix.lower() == ".pdf":
            return p.read_bytes()
    except Exception:
        return None
    return None
