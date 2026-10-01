# Hệ thống đăng ký cập nhật kiến thức chuyên môn dược

Ứng dụng Streamlit **một trang** thu thập phiếu đăng ký học **Cập nhật kiến thức chuyên môn dược**, dựng theo cùng mẫu với app đăng ký hội thảo ung bướu trong repo này. Mở URL là thấy ngay **form đăng ký** — không còn trang giới thiệu riêng, không còn tab chuyển trang; thông tin khóa học chỉ là phần header rút gọn (`st.title` / `st.caption` / `st.info`) ở đầu form. `app.py` dùng `st.navigation` để trang đăng ký là trang mặc định ở đường dẫn `/`.

- thu thập thông tin người đăng ký theo đúng 12 trường (5 trường bắt buộc + 6 trường mới theo phiếu đăng ký gốc + ngày cấp CCHND đều không bắt buộc), form chia 2 khối rõ ràng
- kiểm tra hợp lệ dữ liệu ngay trên form (số Chứng chỉ hành nghề dược, số điện thoại, email nhập nhẹ)
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
| 1. Thông tin chứng chỉ hành nghề dược | 2 | Ngày cấp | ❌ (không bắt buộc) | Ô nhập tự do (`st.text_input`), không phải lịch; không bắt buộc, không kiểm tra định dạng. Chuỗi người dùng nhập được lưu nguyên; để trống thì lưu ô trống trong CSV |
| 1. Thông tin chứng chỉ hành nghề dược | 3 | Nơi cấp | ✅ | Không được để trống. Đây là cơ quan cấp **Chứng chỉ hành nghề dược** (Sở Y tế tỉnh/thành phố), **không phải** cơ quan cấp CCCD/cư trú. Gợi ý trong ô nhập: `Ví dụ: Sở Y tế tỉnh Vĩnh Phúc`; người dùng tự gõ tên Sở của tỉnh mình (ô nhập tự do, không phải selectbox) |
| 1. Thông tin chứng chỉ hành nghề dược | 4 | Lĩnh vực hành nghề dược | ❌ (không bắt buộc) | Ô nhập tự do (`st.text_input`, 2 cột cùng văn bằng chuyên môn), placeholder `Ví dụ: Bán lẻ thuốc, Bán buôn thuốc`; không kiểm tra định dạng |
| 1. Thông tin chứng chỉ hành nghề dược | 5 | Văn bằng chuyên môn | ❌ (không bắt buộc) | Ô nhập tự do (`st.text_input`), placeholder `Ví dụ: Dược sĩ, Thạc sĩ Dược`; không kiểm tra định dạng |
| 2. Thông tin người đăng ký | 6 | Họ và tên | ✅ | Không được để trống |
| 2. Thông tin người đăng ký | 7 | Ngày, tháng, năm sinh | ❌ (không bắt buộc) | Ô nhập tự do (`st.text_input`, không dùng `st.date_input`), placeholder `Ví dụ: 01/02/1990`; không kiểm tra định dạng |
| 2. Thông tin người đăng ký | 8 | Số điện thoại | ✅ | Gồm 10 số, bắt đầu bằng số 0 (dạng `0XXXXXXXXX`) |
| 2. Thông tin người đăng ký | 9 | Email | ❌ (không bắt buộc) | Nếu để trống thì hợp lệ; nếu có nhập thì phải chứa ký tự `@` và có dấu `.` sau `@` (ví dụ `nguoiban@example.com`). Không kiểm tra email tồn tại thật |
| 2. Thông tin người đăng ký | 10 | Chỗ ở hiện nay | ❌ (không bắt buộc) | Ô nhập tự do (`st.text_input`), placeholder `Địa chỉ nơi ở hiện nay`; không kiểm tra định dạng |
| 2. Thông tin người đăng ký | 11 | Địa chỉ thường trú | ✅ | Không được để trống |
| 2. Thông tin người đăng ký | 12 | Nơi công tác | ❌ (không bắt buộc) | Ô nhập tự do (`st.text_input`), placeholder `Tên cơ quan, đơn vị`; không kiểm tra định dạng |
| — | — | Thời gian đăng ký | Trường hệ thống | Sinh tự động khi gửi phiếu |

> Ghi chú: phiếu giấy gốc có ô **Số CMND / Ngày cấp / Nơi cấp** — app dùng **Số Chứng chỉ hành nghề dược (CCHND)** thay cho số CMND theo yêu cầu trước của chủ app, nên **không** thêm trường CMND/CCCD.

Logic kiểm tra nằm trong `utils/validators.py` (`validate_registration` trả về danh sách lỗi tiếng Việt). Chi tiết các quy tắc:

- **Số Chứng chỉ hành nghề dược (CCHND):** chuỗi tự do do người đăng ký nhập theo đúng chứng chỉ thật, ví dụ `12345`, `12345/PTH-2024`, `V-PTH-00123`, `PT-CT-4567`. Không kiểm tra định dạng, độ dài hay thành phần ký tự — chỉ bắt buộc không để trống (kể cả khi chỉ gõ khoảng trắng). Lý do: mỗi Sở Y tế cấp CCHND theo mẫu riêng nên định dạng không thống nhất, siết quy tắc sẽ chặn nhầm người đăng ký hợp lệ.
- **Nơi cấp:** bắt buộc, chỉ kiểm tra không được để trống; là cơ quan cấp CCHND (**Sở Y tế** tỉnh/thành phố), không phải công an/cơ quan cấp CCCD. Ô nhập để tự do kèm placeholder `Ví dụ: Sở Y tế tỉnh Vĩnh Phúc` — cố ý không dùng selectbox và không validate cứng theo danh sách tỉnh vì người đăng ký có thể thuộc tỉnh khác.
- **Ngày cấp (CCHND):** KHÔNG bắt buộc — ô nhập tự do, không dùng lịch. Người đăng ký được để trống hoặc gõ chuỗi bất kỳ (ví dụ `22/02/2024`). Không kiểm tra định dạng; chuỗi đã nhập được lưu nguyên, khi để trống thì lưu ô rỗng trong CSV và hiển thị `—` trên thông báo Discord.
- **Số điện thoại:** gồm đúng 10 số và bắt đầu bằng số 0 (dạng `0XXXXXXXXX`).
- **Email:** KHÔNG bắt buộc. Để trống (hoặc chỉ khoảng trắng) ⇒ hợp lệ. Khi có nhập, chuỗi phải chứa ký tự `@` và phần sau `@` phải có dấu `.` (ví dụ `nguoiban@example.com`); sai quy tắc này mới báo lỗi. Không kiểm tra địa chỉ email có tồn tại thật hay không để tránh chặn oan người đăng ký.
- **5 trường mới còn lại** (`ngay_sinh`, `cho_o_hien_nay`, `van_bang_chuyen_mon`, `linh_vuc_nghe_duoc`, `noi_cong_tac`): KHÔNG bắt buộc và KHÔNG kiểm tra định dạng — người đăng ký gõ gì lưu nguyên đó.

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

Thứ tự cột trong cả hai chế độ (14 cột — 8 cột cũ giữ nguyên tên, 6 cột mới xen vào nhóm thông tin liên quan):

`Thời gian đăng ký`, `Họ và tên`, `Ngày, tháng, năm sinh`, `Chỗ ở hiện nay`, `Số Chứng chỉ hành nghề dược`, `Ngày cấp`, `Nơi cấp`, `Lĩnh vực hành nghề dược`, `Văn bằng chuyên môn`, `Nơi công tác`, `Địa chỉ thường trú`, `Email`, `Số điện thoại`, `Khóa học`

CSV cũ (chưa có 6 cột mới) vẫn đọc được bình thường: khi ghi nối tiếp, 6 cột mới của các bản ghi cũ sẽ để trống.

Ngày cấp được lưu nguyên chuỗi người dùng nhập (sau khi bỏ khoảng trắng đầu/cuối); nếu người đăng ký để trống thì ô này để rỗng.

## Gửi Discord

Mỗi lượt đăng ký mới gửi một tin nhắn (username webhook: `Đăng ký KKT chuyên môn dược`) gồm:

- họ và tên
- ngày, tháng, năm sinh
- số Chứng chỉ hành nghề dược
- ngày cấp, nơi cấp
- lĩnh vực hành nghề dược, văn bằng chuyên môn
- nơi công tác
- chỗ ở hiện nay, địa chỉ thường trú
- email
- số điện thoại
- khóa học + thời gian đăng ký

Nếu chưa cấu hình webhook, app vẫn lưu dữ liệu bình thường và chỉ cảnh báo chưa gửi được Discord.

## Lưu ý giao diện

- App một trang: chỉ có 1 trang trong `pages/`, được `app.py` đăng ký qua `st.navigation` làm trang mặc định nên URL gốc `/` render thẳng form đăng ký.
- Header giới thiệu rút gọn nằm ngay trên form (`st.title` + `st.caption` + `st.info`), không dùng tab/radio của Streamlit để chuyển trang.
- Form chia **2 khối** theo thứ tự: **Thông tin chứng chỉ hành nghề dược** (số CCHND + ngày cấp + nơi cấp + lĩnh vực hành nghề dược + văn bằng chuyên môn — cùng một giấy nên gom chung) → **Thông tin người đăng ký** (họ tên + ngày sinh + số điện thoại + email + chỗ ở hiện nay + địa chỉ thường trú + nơi công tác). Các ô ngắn đi theo cặp trên 2 cột (`st.columns`), ô địa chỉ để full-width. Tiêu đề khối dùng `st.subheader`, giữa các khối là `st.divider()`; CSS trong `utils/styles.py` thêm style cho tiêu đề khối và đường phân cách (không đổi widget nào).
- Cả **12 trường** đều dùng `st.text_input` (kể cả ngày sinh và ngày cấp) — KHÔNG dùng `st.date_input` và KHÔNG dùng selectbox để người dùng tự gõ nhanh theo phiếu giấy.
- Cỡ chữ giao diện đặt ở mức 18px cho dễ đọc (`apply_base_styles(18)`).
- Form dùng `clear_on_submit=False`: sau khi bấm **GỬI ĐĂNG KÝ**, toàn bộ 12 trường vẫn giữ nguyên dữ liệu đã nhập — kể cả khi `validate_registration()` báo lỗi — để người dùng chỉ sửa lại ô sai thay vì nhập lại từ đầu. Sau khi lưu thành công, form cũng không tự xoá (theo yêu cầu chủ app), nên chỉ bấm GỬI ĐĂNG KÝ lần nữa khi thật sự muốn tạo thêm bản ghi mới.
