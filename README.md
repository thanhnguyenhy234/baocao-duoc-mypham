# Hệ thống Thu thập Báo cáo Thống kê Dược - Mỹ phẩm

Hệ thống thu thập báo cáo thống kê lĩnh vực dược - mỹ phẩm theo Thông tư số 25/2021/TT-BYT.

## Tính năng

- **Form nhập liệu trực quan**: Các cơ sở điền báo cáo theo biểu mẫu tương ứng với loại cơ sở
- **Upload PDF**: Cơ sở upload file PDF ký số/scan
- **Lưu trữ Google Sheets**: Dữ liệu được lưu tự động vào Google Sheets
- **Dashboard tổng hợp**: Thống kê, biểu đồ, xem chi tiết từng cơ sở
- **Xuất Excel**: Xuất báo cáo tổng hợp ra file Excel

## Cài đặt

### 1. Clone repository

```bash
git clone https://github.com/your-username/baocao-duoc-mypham.git
cd baocao-duoc-mypham
```

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 3. Cấu hình Google APIs

#### Bước 3.1: Tạo Google Cloud Project
1. Truy cập https://console.cloud.google.com
2. Tạo project mới
3. Enable các APIs:
   - Google Sheets API
   - Google Drive API

#### Bước 3.2: Tạo Service Account
1. Vào IAM & Admin > Service Accounts
2. Tạo Service Account mới
3. Tải file credentials JSON

#### Bước 3.3: Tạo Google Sheet
1. Tạo Google Sheet mới
2. Share với email của Service Account (quyền Editor)
3. Lưu lại Sheet ID (phần trong URL giữa `/d/` và `/edit`)

#### Bước 3.4: Tạo thư mục Google Drive
1. Tạo thư mục mới trên Google Drive
2. Share với email của Service Account (quyền Editor)
3. Lưu lại Folder ID (phần cuối của URL)

### 4. Cấu hình secrets

#### Chạy local
Tạo file `.streamlit/secrets.toml`:

```toml
spreadsheet_id = "YOUR_SPREADSHEET_ID"
drive_folder_id = "YOUR_DRIVE_FOLDER_ID"

[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "123456789"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."
```

#### Deploy trên Streamlit Cloud
1. Vào Settings > Secrets
2. Paste nội dung tương tự như trên

### 5. Chạy ứng dụng

```bash
streamlit run app.py
```

## Deploy lên Streamlit Cloud

1. Push code lên GitHub
2. Truy cập https://share.streamlit.io
3. Connect GitHub repository
4. Chọn file `app.py`
5. Thêm secrets trong Settings
6. Deploy!

## Cấu trúc thư mục

```
baocao-duoc-mypham/
├── app.py                    # Trang chính
├── pages/
│   ├── 1_📝_Nhập_báo_cáo.py  # Form nhập liệu
│   └── 2_📊_Dashboard.py     # Dashboard tổng hợp
├── utils/
│   ├── google_sheets.py      # Kết nối Google Sheets
│   └── google_drive.py       # Upload file lên Drive
├── .streamlit/
│   └── secrets.toml          # Credentials (local only)
├── requirements.txt
├── README.md
└── .gitignore
```

## Các biểu mẫu

| Biểu mẫu | Tên | Áp dụng cho |
|----------|-----|-------------|
| 01 | Nhân lực dược lâm sàng | Cơ sở KCB |
| 02 | Giá trị thuốc sử dụng | Cơ sở KCB |
| 03 | Thuốc sản xuất trong nước | Cơ sở KCB |
| 04 | Chất lượng thuốc | TT Kiểm nghiệm |
| 05 | Hệ thống cung ứng thuốc | Cơ sở SX-KD dược |
| 06 | Sản xuất mỹ phẩm | Cơ sở SX-KD mỹ phẩm |

## Liên hệ

Phòng Nghiệp vụ Dược - Sở Y tế tỉnh Phú Thọ

Email: nghiepvuduocpt@gmail.com
