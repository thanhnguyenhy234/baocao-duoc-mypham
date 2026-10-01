# Hệ thống đăng ký cập nhật kiến thức chuyên môn dược

Ứng dụng Streamlit **một trang** thu thập phiếu đăng ký học **Cập nhật kiến thức chuyên môn dược**, dựng theo cùng mẫu với app đăng ký hội thảo ung bướu trong repo này. Mở URL là thấy ngay **form đăng ký** — không còn trang giới thiệu riêng, không còn tab chuyển trang; thông tin khóa học chỉ là phần header rút gọn (`st.title` / `st.caption` / `st.info`) ở đầu form. `app.py` dùng `st.navigation` để trang đăng ký là trang mặc định ở đường dẫn `/`.

- thu thập thông tin người đăng ký theo đúng 6 trường bắt buộc
- kiểm tra hợp lệ dữ liệu ngay trên form (số CCCND/CCCD, ngày cấp, số điện thoại)
- lưu danh sách đăng ký (Google Sheets, tự động chuyển sang CSV cục bộ nếu chưa cấu hình)
- gửi thông báo về Discord bằng webhook

## Thông tin khóa học

- **Tên khóa học:** Cập nhật kiến thức chuyên môn dược
- **Đơn vị tổ chức:** Trường Cao đẳng Y tế Phú Thọ
- **Địa điểm:** Hội trường Trường Cao đẳng Y tế Phú Thọ

## Các trường thu thập (đúng thứ tự)

| # | Trường | Bắt buộc | Kiểm tra hợp lệ |
|---|--------|----------|-----------------|
| 1 | Họ và tên | ✅ | Không được để trống |
| 2 | Số CCCND/CCCD | ✅ | Chỉ chữ số, gồm 9 số (CMND) hoặc 12 số (CCCD) |
| 3 | Ngày cấp | ✅ (bắt buộc tự chọn) | `st.date_input(value=None, max_value=date.today())` — không có giá trị mặc định, phải tự chọn ngày; không được sau ngày hôm nay |
| 4 | Nơi cấp | ✅ | Không được để trống |
| 5 | Địa chỉ thường trú | ✅ | Không được để trống |
| 6 | Số điện thoại | ✅ | Gồm 10 số, bắt đầu bằng số 0 (dạng `0XXXXXXXXX`) |
| — | Ghi chú / nhu cầu khác | ❌ (tùy chọn) | Văn bản tự do |
| — | Thời gian đăng ký | Trường hệ thống | Sinh tự động khi gửi phiếu |

Logic kiểm tra nằm trong `utils/validators.py` (`validate_registration` trả về danh sách lỗi tiếng Việt). Chi tiết các quy tắc:

- **Số CCCND/CCCD:** chỉ chứa chữ số, gồm 9 số (CMND) hoặc 12 số (CCCD).
- **Ngày cấp:** bắt buộc phải chọn, không được để trống và không được sau ngày hôm nay.
- **Số điện thoại:** gồm đúng 10 số và bắt đầu bằng số 0 (dạng `0XXXXXXXXX`).

## Cấu trúc thư mục

```text
dangky-kien-thuc-chuyen-mon/
├── app.py                     # entry point Streamlit (set_page_config + st.navigation)
├── assets/
│   └── logo-hoi-y-duoc-phutho.svg
├── pages/
│   └── 1_📝_Đăng_ký.py         # TRANG DUY NHẤT: header rút gọn + form đăng ký 6 trường + ghi chú
├── utils/
│   ├── __init__.py
│   ├── discord_webhook.py      # gửi thông báo Discord
│   ├── storage.py              # lưu Google Sheets / CSV
│   ├── styles.py               # CSS dùng chung
│   └── validators.py           # kiểm tra hợp lệ dữ liệu
├── data/                      # nơi ghi registrations.csv khi chạy fallback
├── .streamlit/
│   ├── config.toml            # theme (tone teal y tế)
│   └── secrets.toml.example   # mẫu secrets, KHÔNG chứa giá trị thật
├── requirements.txt
└── README.md
```

## Cài đặt

```bash
cd dangky-kien-thuc-chuyen-mon
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Sau đó sửa `.streamlit/secrets.toml`:

- `discord_webhook_url`: dán webhook Discord nhận thông báo
- `spreadsheet_id` + `gcp_service_account`: chỉ cần nếu muốn lưu Google Sheets

Không commit file `.streamlit/secrets.toml` (đã được liệt kê trong `.gitignore`).

## Chạy ứng dụng

```bash
streamlit run app.py
```

## Cơ chế lưu dữ liệu

- **Ưu tiên 1:** Google Sheets — khi secrets có đủ `spreadsheet_id` và `gcp_service_account`; dữ liệu ghi vào worksheet tên `Đăng ký cập nhật KKT chuyên môn dược`.
- **Ưu tiên 2 (fallback):** CSV cục bộ tại `data/registrations.csv`.

Số điện thoại và số CCCND/CCCD được lưu dưới dạng chuỗi và CSV được đọc/ghi với `dtype=str` (`keep_default_na=False`) để giữ nguyên chữ số, không bị mất số 0 đầu (ví dụ `0912345678`).

Thứ tự cột trong cả hai chế độ:

`Thời gian đăng ký`, `Họ và tên`, `Số CCCND`, `Ngày cấp`, `Nơi cấp`, `Địa chỉ thường trú`, `Số điện thoại`, `Ghi chú`, `Khóa học`

Ngày cấp được lưu ở định dạng `dd/mm/yyyy`.

## Gửi Discord

Mỗi lượt đăng ký mới gửi một tin nhắn (username webhook: `Đăng ký KKT chuyên môn dược`) gồm:

- họ và tên
- số CCCND/CCCD
- ngày cấp, nơi cấp
- địa chỉ thường trú
- số điện thoại
- ghi chú
- khóa học + thời gian đăng ký

Nếu chưa cấu hình webhook, app vẫn lưu dữ liệu bình thường và chỉ cảnh báo chưa gửi được Discord.

## Ghi chú giao diện

- App một trang: chỉ có 1 trang trong `pages/`, được `app.py` đăng ký qua `st.navigation` làm trang mặc định nên URL gốc `/` render thẳng form đăng ký.
- Header giới thiệu rút gọn nằm ngay trên form (`st.title` + `st.caption` + `st.info`), không dùng tab/radio của Streamlit để chuyển trang.
- Cỡ chữ giao diện đặt ở mức 18px cho dễ đọc (`apply_base_styles(18)`).
