# California Traffic Incident Detection System

ITSgrXM là dự án demo về phát hiện sự cố giao thông bằng thuật toán California. Dự án kết hợp backend Python tạo và phân tích dữ liệu giao thông mô phỏng với giao diện web để chạy mô phỏng và xem kết quả.

> Dự án phục vụ mục đích học tập và trình diễn. Dữ liệu được tạo bằng mô phỏng, không phải dữ liệu giao thông thực tế.

## Tính năng

- Tạo các kịch bản giao thông bình thường, có sự cố và ùn tắc tự nhiên.
- Phân tích occupancy tại trạm thượng lưu và hạ lưu bằng `CaliforniaAlgorithm`.
- Chạy mô phỏng qua REST API hoặc từ dòng lệnh.
- Xem kết quả mô phỏng, Dashboard và các chỉ số đánh giá trên giao diện web.
- Tính Detection Rate (DR), False Alarm Rate (FAR), Time to Detection (TTD), cùng các số liệu TP, FN, FP và cảnh báo lặp.

## Công nghệ sử dụng

- **Backend:** Python, FastAPI, Uvicorn
- **Frontend:** HTML, CSS và JavaScript thuần
- **Kiểm thử:** pytest, FastAPI TestClient

## Bắt đầu

### Yêu cầu

- Python 3.10 trở lên
- Trình duyệt web hiện đại

### Cài đặt

Mở terminal tại thư mục gốc dự án và tạo môi trường ảo:

```powershell
python -m venv .venv
```

Kích hoạt môi trường trên Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Trên macOS/Linux hoặc Git Bash:

```bash
source .venv/bin/activate
```

Cài đặt các thư viện cần thiết:

```bash
python -m pip install -r requirements.txt
```

## Chạy ứng dụng

### Khởi động REST API

Từ thư mục gốc dự án, chạy:

```bash
python -m uvicorn src.api:app --reload --port 8000
```

API mặc định chạy tại `http://127.0.0.1:8000`. Mở `http://127.0.0.1:8000/docs` để xem và thử các endpoint bằng Swagger UI.

### Mở giao diện web

Giữ API đang chạy, mở terminal thứ hai và chuyển đến thư mục frontend:

```powershell
Set-Location .\fe
python -m http.server 5500
```

Mở `http://localhost:5500` trong trình duyệt. Không mở trực tiếp `index.html` bằng `file://`. Frontend tự kết nối backend ở cổng 8000, sau đó thử cổng 8001 nếu cần.

Các trang trong giao diện:

- **Trang chủ:** giới thiệu hệ thống.
- **Mô phỏng:** chạy kịch bản và theo dõi kết quả phát hiện.
- **Dashboard:** xem tóm tắt kết quả mô phỏng và đánh giá gần nhất.
- **Đánh giá:** xem DR, FAR và TTD của kết quả gần nhất.

### Chạy demo trong terminal

Thay vì mở giao diện web, có thể chạy demo trực tiếp từ thư mục gốc:

```bash
python -m src.main
```

Chương trình tạo các kịch bản mô phỏng, in một số bản ghi và thời điểm thuật toán phát hiện sự cố.

### Tạo lại dữ liệu CSV

Để sinh lại các tệp CSV trong `data/`, chạy:

```bash
python -m src.simulator
```

## Chạy kiểm thử

Từ thư mục gốc, chạy:

```bash
python -m pytest
```

## API và tài liệu

API hỗ trợ kiểm tra trạng thái, chạy mô phỏng, gửi dữ liệu đánh giá và lấy kết quả Dashboard:

- `GET /api/health` — kiểm tra API.
- `POST /api/simulations` — chạy một kịch bản mô phỏng.
- `POST /api/evaluations` — tính các chỉ số từ khoảng sự cố và thời điểm cảnh báo.
- `GET /api/dashboard` — lấy kết quả mô phỏng và đánh giá gần nhất.

Xem hướng dẫn request/response và các tùy chọn tại [docs/api.md](docs/api.md). Các tài liệu khác:

- [Thuật toán](docs/algorithm.md)
- [Thiết kế hệ thống](docs/system_design.md)
- [Đánh giá kết quả](docs/evaluation.md)
- [Dữ liệu mô phỏng](data/README.md)
- [Frontend](fe/README.md)

## Cấu trúc dự án

```text
ITSgrXM/
├── data/          # Các bộ dữ liệu mô phỏng dạng CSV
├── docs/          # Tài liệu thuật toán, API, thiết kế và đánh giá
├── fe/            # Giao diện web tĩnh
├── src/
│   ├── api.py      # REST API
│   ├── california.py
│   ├── main.py     # Demo chạy trong terminal
│   ├── metrics.py  # Các hàm tính chỉ số đánh giá
│   └── simulator.py
├── tests/          # Kiểm thử thuật toán và API
└── requirements.txt
```

## Lưu ý

Dữ liệu mẫu trong `data/` và dữ liệu được tạo khi chạy mô phỏng đều là dữ liệu tổng hợp. Các ngưỡng và công thức trong thuật toán cần được đối chiếu với đặc tả sử dụng trước khi áp dụng ngoài phạm vi demo. Kết quả Dashboard được lưu trong bộ nhớ backend và sẽ mất khi tiến trình khởi động lại.
