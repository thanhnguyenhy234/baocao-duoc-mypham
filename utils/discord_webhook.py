"""
Discord utility functions for uploading PDF files via Webhook.
"""
import streamlit as st
import requests
import io


def get_webhook_url():
    """Get Discord webhook URL from secrets."""
    try:
        return st.secrets.get("discord_webhook_url", None)
    except:
        return None


def upload_pdf_to_discord(file_bytes: bytes, filename: str, facility_name: str, facility_type: str):
    """
    Upload PDF file to Discord channel via Webhook.
    
    Args:
        file_bytes: PDF file content as bytes
        filename: Original filename
        facility_name: Name of the facility
        facility_type: Type of facility
    
    Returns:
        str: Message URL if successful, None if failed
    """
    webhook_url = get_webhook_url()
    
    if not webhook_url:
        st.warning("Chưa cấu hình Discord Webhook. File PDF chưa được gửi.")
        return None
    
    try:
        # Prepare message content
        from datetime import datetime, timezone, timedelta
        vietnam_tz = timezone(timedelta(hours=7))
        timestamp = datetime.now(vietnam_tz).strftime("%Y-%m-%d %H:%M:%S")
        
        message_content = f"""📄 **BÁO CÁO MỚI**
        
🏥 **Cơ sở:** {facility_name}
📋 **Loại:** {facility_type}
📎 **File:** {filename}
⏰ **Thời gian:** {timestamp}
"""
        
        # Prepare file
        files = {
            'file': (f"{facility_name}_{filename}", io.BytesIO(file_bytes), 'application/pdf')
        }
        
        # Prepare payload
        payload = {
            'content': message_content,
            'username': 'Báo cáo Dược - Mỹ phẩm',
        }
        
        # Send to Discord
        response = requests.post(
            webhook_url,
            data=payload,
            files=files,
            timeout=30
        )
        
        if response.status_code in [200, 204]:
            return "Đã gửi thành công"
        else:
            st.error(f"Lỗi gửi Discord: {response.status_code} - {response.text}")
            return None
    
    except Exception as e:
        st.error(f"Lỗi gửi file Discord: {e}")
        return None
