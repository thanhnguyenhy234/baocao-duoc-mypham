"""
Google Drive utility functions for uploading PDF files.
"""
import streamlit as st
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io


# Google Drive scopes - cần full drive access để upload vào shared folder
SCOPES = [
    "https://www.googleapis.com/auth/drive"
]


def get_drive_service():
    """Get authenticated Google Drive service."""
    try:
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=SCOPES
        )
        service = build('drive', 'v3', credentials=credentials)
        return service
    except Exception as e:
        st.error(f"Lỗi kết nối Google Drive: {e}")
        return None


def upload_pdf_to_drive(file_bytes: bytes, filename: str, facility_name: str):
    """
    Upload PDF file to Google Drive shared folder.
    
    Args:
        file_bytes: PDF file content as bytes
        filename: Original filename
        facility_name: Name of the facility for folder organization
    
    Returns:
        str: Public link to the uploaded file, or None if failed
    """
    service = get_drive_service()
    if not service:
        return None
    
    try:
        # Get folder ID from secrets - folder phải được share với service account
        folder_id = st.secrets.get("drive_folder_id", None)
        
        if not folder_id:
            st.error("Chưa cấu hình drive_folder_id trong secrets")
            return None
        
        # Prepare file metadata - PHẢI có parents để upload vào shared folder
        file_metadata = {
            'name': f"{facility_name}_{filename}",
            'parents': [folder_id]
        }
        
        # Upload file
        media = MediaIoBaseUpload(
            io.BytesIO(file_bytes),
            mimetype='application/pdf',
            resumable=True
        )
        
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink',
            supportsAllDrives=True  # Hỗ trợ shared drives
        ).execute()
        
        # Make file accessible via link
        try:
            service.permissions().create(
                fileId=file['id'],
                body={'type': 'anyone', 'role': 'reader'},
                supportsAllDrives=True
            ).execute()
        except:
            pass  # Có thể không cần nếu folder đã public
        
        return file.get('webViewLink', f"https://drive.google.com/file/d/{file['id']}/view")
    
    except Exception as e:
        st.error(f"Lỗi upload file: {e}")
        return None


def list_files_in_folder():
    """List all files in the designated folder."""
    service = get_drive_service()
    if not service:
        return []
    
    try:
        folder_id = st.secrets.get("drive_folder_id", None)
        
        query = f"'{folder_id}' in parents" if folder_id else ""
        
        results = service.files().list(
            q=query,
            pageSize=100,
            fields="files(id, name, webViewLink, createdTime)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()
        
        return results.get('files', [])
    
    except Exception as e:
        st.error(f"Lỗi lấy danh sách file: {e}")
        return []
