# Hệ thống đăng ký cập nhật kiến thức chuyên môn dược

Ứng dụng Streamlit **một trang** thu thập phiếu đăng ký học **Cập nhật kiến thức chuyên môn dược**, dựng theo cùng mẫu với app đăng ký hội thảo ung bướu trong repo này. Mở URL là thấy ngay **form đăng ký** — không còn trang giới thiệu riêng, không còn tab chuyển trang; thông tin khóa học chỉ là phần header rút gọn (`st.title` / `st.caption` / `st.info`) ở đầu form. `app.py` dùng `st.navigation` để trang đăng ký là trang mặc định ở đường dẫn `/`.

- thu thập thông tin người đăng ký theo đúng 6 trường bắt buộc, form chia 2 khối rõ ràng
- kiểm tra hợp lệ dữ liệu ngay trên form (số Chứng chỉ hành nghề dược, ngày cấp, số điện thoại)
- lưu danh sách đăng ký (Google Sheets, tự động chuyển sang CSV cục bộ nếu chưa cấu hình)
- gửi thông báo về Discord bằng webhook

## Thông tin khóa học

- **Tên khóa học:** Cập nhật kiến thức chuyên môn dược
- **Đơn vị tổ chức:** Trường Cao đẳng Y tế Phú Thọ
- **Địa điểm:** Hội trường Trường Cao đẳng Y tế Phú Thọ

## Các trường thu thập (đúng thứ tự và theo khối trên form)

Form chia **2 khối** (dùng `st.subheader` + `st.divider`), số CCHND + ngày cấp + nơi cấp được gom chung một khối vì thuộc cùng một giấy chứng chỉ:

| Khối | # | Trường | Bắt buộc | Kiểm tra hợp lệ |
|------|---|--------|----------|-----------------|
| 1. Thông tin chứng chỉ hành nghề dược | 1 | Số Chứng chỉ hành nghề dược | ✅ | Chuỗi tự do do người đăng ký nhập theo đúng chứng chỉ thật (ví dụ `12345`, `12345/PTH-2024`, `V-PTH-00123`); chỉ bắt buộc không để trống, không kiểm tra định dạng, độ dài hay ký tự |
| 1. Thông tin chứng chỉ hành nghề dược | 2 | Ngày cấp | ✅ (bắt buộc tự chọn) | `st.date_input(value=None, max_value=date.today())` — không có giá trị mặc định, phải tự chọn ngày; không được sau ngày hôm nay |
| 1. Thông tin chứng chỉ hành nghề dược | 3 | Nơi cấp | ✅ | Không được để trống. Đây là cơ quan cấp **Chứng chỉ hành nghề dược** (Sở Y tế tỉnh/thành phố), **không phải** cơ quan cấp CCCD/cư trú. Gợi ý trong ô nhập: `Ví dụ: Sở Y tế tỉnh Vĩnh Phúc`; người dùng tự gõ tên Sở của tỉnh mình (ô nhập tự do, không phải selectbox) |
| 2. Thông tin người đăng ký | 4 | Họ và tên | ✅ | Không được để trống |
| 2. Thông tin người đăng ký | 5 | Số điện thoại | ✅ | Gồm 10 số, bắt đầu bằng số 0 (dạng `0XXXXXXXXX`) |
| 2. Thông tin người đăng ký | 6 | Địa chỉ thường trú | ✅ | Không được để trống |
| — | — | Thời gian đăng ký | Trường hệ thống | Sinh tự động khi gửi phiếu |

Logic kiểm tra nằm trong `utils/validators.py` (`validate_registration` trả về danh sách lỗi tiếng Việt). Chi tiết các quy tắc:

- **Số Chứng chỉ hành nghề dược (CCHND):** chuỗi tự do do người đăng ký nhập theo đúng chứng chỉ thật, ví dụ `12345`, `12345/PTH-2024`, `V-PTH-00123`, `PT-CT-4567`. Không kiểm tra định dạng, độ dài hay thành phần ký tự — chỉ bắt buộc không để trống (kể cả khi chỉ gõ khoảng trắng). Lý do: mỗi Sở Y tế cấp CCHND theo mẫu riêng nên định dạng không thống nhất, siết quy tắc sẽ chặn nhầm người đăng ký hợp lệ.
- **Nơi cấp:** bắt buộc, chỉ kiểm tra không được để trống; là cơ quan cấp CCHND (**Sở Y tế** tỉnh/thành phố), không phải công an/cơ quan cấp CCCD. Ô nhập để tự do kèm placeholder `Ví dụ: Sở Y tế tỉnh Vĩnh Phúc` — cố ý không dùng selectbox và không validate cứng theo danh sách tỉnh vì người đăng ký có thể thuộc tỉnh khác.
- **Ngày cấp:** bắt buộc phải chọn, không được để trống và không được sau ngày hôm nay.
- **Số điện thoại:** gồm đúng 10 số và bắt đầu bằng số 0 (dạng `0XXXXXXXXX`).

## Cấu trúc thư mục

```text
dangky-kien-thuc-chuyen-mon/
├── app.py                     # entry point Streamlit (set_page_config + st.navigation)
├── assets/
│   └── logo-hoi-y-duoc-phutho.svg
├── pages/
│   └── 1_📝_Đăng_ký.py         # TRANG DUY NHẤT: header rút gọn + form 2 khối (chứng chỉ HND / người đăng ký)
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

Số điện thoại và số Chứng chỉ hành nghề dược được lưu dưới dạng chuỗi và CSV được đọc/ghi với `dtype=str` (`keep_default_na=False`) để giữ nguyên chữ số, không bị mất số 0 đầu (ví dụ `0912345678`).

Thứ tự cột trong cả hai chế độ:

`Thời gian đăng ký`, `Họ và tên`, `Số Chứng chỉ hành nghề dược`, `Ngày cấp`, `Nơi cấp`, `Địa chỉ thường trú`, `Số điện thoại`, `Khóa học`

Ngày cấp được lưu ở định dạng `dd/mm/yyyy`.

## Gửi Discord

Mỗi lượt đăng ký mới gửi một tin nhắn (username webhook: `Đăng ký KKT chuyên môn dược`) gồm:

- họ và tên
- số Chứng chỉ hành nghề dược
- ngày cấp, nơi cấp
- địa chỉ thường trú
- số điện thoại
- khóa học + thời gian đăng ký

Nếu chưa cấu hình webhook, app vẫn lưu dữ liệu bình thường và chỉ cảnh báo chưa gửi được Discord.

## Lưu ý giao diện

- App một trang: chỉ có 1 trang trong `pages/`, được `app.py` đăng ký qua `st.navigation` làm trang mặc định nên URL gốc `/` render thẳng form đăng ký.
- Header giới thiệu rút gọn nằm ngay trên form (`st.title` + `st.caption` + `st.info`), không dùng tab/radio của Streamlit để chuyển trang.
- Form chia **2 khối** theo thứ tự: **Thông tin chứng chỉ hành nghề dược** (số CCHND + ngày cấp + nơi cấp — cùng một giấy nên gom chung) → **Thông tin người đăng ký** (họ tên + số điện thoại + địa chỉ thường trú). Tiêu đề khối dùng `st.subheader`, giữa các khối là `st.divider()`; CSS trong `utils/styles.py` thêm style cho tiêu đề khối và đường phân cách (không đổi widget nào).
- Cỡ chữ giao diện đặt ở mức 18px cho dễ đọc (`apply_base_styles(18)`).
- Form dùng `clear_on_submit=False`: sau khi bấm **GỬI ĐĂNG KÝ**, toàn bộ 6 trường vẫn giữ nguyên dữ liệu đã nhập — kể cả khi `validate_registration()` báo lỗi — để người dùng chỉ sửa lại ô sai thay vì nhập lại từ đầu. Sau khi lưu thành công, form cũng không tự xoá (theo yêu cầu chủ app), nên chỉ bấm GỬI ĐĂNG KÝ lần nữa khi thật sự muốn tạo thêm bản ghi mới.
