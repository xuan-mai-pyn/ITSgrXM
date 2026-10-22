# ITSgrXM Frontend

Frontend độc lập minh họa giao diện demo phát hiện sự cố giao thông bằng thuật toán California. Thành viên phụ trách: Khang.

## Chạy frontend

Không cần cài đặt package hoặc khởi động Python backend:

1. Mở `fe/index.html` trực tiếp bằng trình duyệt; hoặc
2. Chạy một static file server trong thư mục `fe/` (ví dụ `python -m http.server 8000`) rồi truy cập `http://localhost:8000`.

Các trang dùng đường dẫn tương đối và có thể hoạt động độc lập khi mở từ thư mục này.

## Cấu trúc

```text
fe/
├── index.html
├── README.md
├── assets/
│   ├── css/style.css
│   ├── js/
│   │   ├── app.js
│   │   ├── data.js
│   │   └── charts.js
│   └── images/.gitkeep
└── pages/
    ├── dashboard.html
    ├── simulation.html
    └── evaluation.html
```

## Nguồn dữ liệu

`assets/js/data.js` khai báo rõ fixture tĩnh chỉ dành cho frontend: các mẫu occupancy cho hai trạm, nhãn tình trạng minh họa và ba chỉ số mẫu. Các giá trị này không được lấy từ backend, không phải kết quả thực nghiệm và không thể hiện độ chính xác thật của thuật toán California. Biểu đồ được vẽ bằng SVG thuần trong `assets/js/charts.js`, không phụ thuộc thư viện bên ngoài.

Frontend hiện **chưa kết nối backend**, không gọi API và không import module Python. Để tích hợp trong tương lai, có thể thay lớp nguồn dữ liệu trong `data.js` bằng một adapter đọc API có cùng cấu trúc dữ liệu; phần giao diện và thành phần biểu đồ vẫn có thể tái sử dụng.
