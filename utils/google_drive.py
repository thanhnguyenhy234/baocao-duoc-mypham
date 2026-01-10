"""
Google Drive utility functions for uploading PDF files.
"""
import streamlit as st
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io


# Google Drive scopes
SCOPES = [
    "https://www.googleapis.com/auth/drive.file"
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
    Upload PDF file to Google Drive.
    
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
        # Get folder ID from secrets
        folder_id = st.secrets.get("drive_folder_id", None)
        
        # Prepare file metadata
        file_metadata = {
            'name': f"{facility_name}_{filename}",
            'mimeType': 'application/pdf'
        }
        
        if folder_id:
            file_metadata['parents'] = [folder_id]
        
        # Upload file
        media = MediaIoBaseUpload(
            io.BytesIO(file_bytes),
            mimetype='application/pdf',
            resumable=True
        )
        
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink'
        ).execute()
        
        # Make file accessible via link
        service.permissions().create(
            fileId=file['id'],
            body={'type': 'anyone', 'role': 'reader'}
        ).execute()
        
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
            fields="files(id, name, webViewLink, createdTime)"
        ).execute()
        
        return results.get('files', [])
    
    except Exception as e:
        st.error(f"Lỗi lấy danh sách file: {e}")
        return []
