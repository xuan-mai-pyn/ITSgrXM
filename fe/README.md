# ITSgrXM Frontend

Frontend demo phát hiện sự cố giao thông bằng thuật toán California. Thành viên phụ trách chính: Cường ......

## Chạy frontend

Không cần cài đặt package frontend. Cần khởi động backend theo hướng dẫn tại `docs/api.md`:

1. Từ thư mục gốc, chạy `python -m uvicorn src.api:app --reload --port 8000`.
2. Chạy static file server trong thư mục `fe/` (ví dụ `python -m http.server 5500`) rồi truy cập `http://localhost:5500`.

Không mở bằng `file://`; backend cho phép CORS mặc định với `localhost` và `127.0.0.1`.
Frontend tự thử API trên cổng `8000`, sau đó `8001` nếu cổng mặc định không
khả dụng. Nếu `8000` đang bị chiếm, có thể chạy backend bằng
`python -m uvicorn src.api:app --reload --port 8001`.

## Cấu trúc frontend

```text
fe/
├── index.html
├── README.md
├── assets/
│   ├── css/style.css
│   ├── js/
│   │   ├── app.js
│   │   ├── api-client.js
│   │   ├── dashboard.js
│   │   ├── evaluation.js
│   │   └── charts.js
│   └── images/.gitkeep
└── pages/
    ├── dashboard.html
    ├── simulation.html
    └── evaluation.html
```

## Nguồn dữ liệu

Trang Mô Phỏng lấy các chu kỳ và kết quả phát hiện từ `POST /api/simulations`.
Dashboard và Đánh Giá lấy kết quả gần nhất từ `GET /api/dashboard`; trước khi
có kết quả, giao diện hiển thị trạng thái chưa có dữ liệu thay vì số liệu mẫu.
Backend chỉ lưu kết quả trong bộ nhớ tiến trình, nên dữ liệu mất khi backend
khởi động lại. Dữ liệu mô phỏng là dữ liệu tổng hợp, không phải dữ liệu giao
thông thực tế. `charts.js` là mã minh họa cũ, không được các trang hiện tại
nạp.

<!-- test-git-change -->
