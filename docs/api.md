# REST API ITSgrXM

API này cung cấp một lớp HTTP riêng cho các module Python hiện có. `src/main.py`
vẫn là chương trình demo chạy trên Terminal. Mô phỏng dùng dữ liệu được sinh
trong `src/simulator.py`, không phải dữ liệu giao thông thực tế.

## Cài đặt và chạy

Từ thư mục gốc, tạo và kích hoạt môi trường ảo trên Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Khởi động API:

```powershell
python -m uvicorn src.api:app --reload
```

- API: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

Dừng server bằng `Ctrl+C`.

## CORS khi phát triển

Mặc định API cho phép origin HTTP trên `localhost` hoặc `127.0.0.1` với port
bất kỳ; cấu hình này dành cho phát triển local. CORS không bật credentials.
Frontend nên chạy qua HTTP server tĩnh, không mở bằng `file://`.

Để chỉ định origins khác, đặt biến môi trường `ITS_ALLOWED_ORIGINS` thành danh
sách origin phân tách bằng dấu phẩy, ví dụ trong PowerShell:

```powershell
$env:ITS_ALLOWED_ORIGINS = "https://frontend.example"
```

Biến môi trường cần được đặt trong cùng terminal trước khi chạy Uvicorn.

## Quy ước lỗi

Request không hợp lệ trả HTTP `422` theo dạng:

```json
{
  "status": "error",
  "message": "Dữ liệu yêu cầu không hợp lệ.",
  "details": [
    {"location": ["body", "scenario"], "message": "Input should be ..."}
  ]
}
```

Lỗi nội bộ trả HTTP `500` với thông báo chung; chi tiết lỗi chỉ được ghi log
phía server.

## Endpoint

### `GET /api/health`

Kiểm tra API:

```json
{"status": "ok", "service": "ITSgrXM"}
```

### `POST /api/simulations`

Sinh dữ liệu, chạy California cho từng chu kỳ và đối chiếu các mốc cảnh báo với
nhãn `incident` mô phỏng qua `src.metrics`.

Các kịch bản hỗ trợ: `normal`, `incident`, `edge_congestion`. Các trường trong
`parameters` phải thuộc generator tương ứng. Có thể bỏ các tham số để dùng
mặc định hiện tại của `src/simulator.py`. Các tham số trong `algorithm` là
override tùy chọn; nếu bỏ qua, `CaliforniaAlgorithm` dùng mặc định trong module.

Ví dụ request:

```json
{
  "scenario": "incident",
  "parameters": {
    "num_periods": 120,
    "incident_start": 40,
    "incident_duration": 30,
    "seed": 123
  },
  "algorithm": {
    "persistence": 2
  }
}
```

Response gồm `records` theo chu kỳ, `actual_incident` lấy từ dữ liệu mô phỏng,
`detected` là kết quả bool thực tế từ `CaliforniaAlgorithm.evaluate`, và
`detection_times` là thời điểm bắt đầu mỗi đợt phát hiện. Phần `evaluation`
được tính từ các khoảng nhãn sự cố và các thời điểm cảnh báo:

```json
{
  "status": "success",
  "scenario": "incident",
  "description": "Sự cố tại chu kỳ 40–69: OCC_up đỉnh ≈ 55.0%, OCC_down đáy ≈ 8.0%",
  "sample_interval": 30,
  "incident_start": 40,
  "incident_end": 69,
  "seed": 123,
  "detection_times": [42],
  "evaluation": {
    "status": "complete",
    "n_incidents": 1,
    "tp": 1,
    "fn": 0,
    "fp": 0,
    "repeated_alarms": 0,
    "dr": 1.0,
    "far": 0.0,
    "far_definition": "per_sample",
    "ttd": 2.0,
    "ttd_statistic": "mean",
    "unavailable_metrics": []
  },
  "records": [
    {
      "timestamp": 0,
      "occ_up": 20.81,
      "occ_down": 20.28,
      "actual_incident": false,
      "detected": false
    }
  ]
}
```

Đoạn response trên chỉ minh họa schema; các số liệu occupancy và metric phụ
thuộc dữ liệu sinh và không được xem là kết quả thực nghiệm.

### `POST /api/evaluations`

Nhận danh sách khoảng sự cố tham chiếu và thời điểm cảnh báo theo cùng đơn vị
thời gian. `Incident.start/end` là khoảng bao gồm cả hai đầu. `alarms` là các
thời điểm dự đoán, thường là lúc kết quả thuật toán chuyển từ `False` sang
`True`.

Ví dụ request:

```json
{
  "incidents": [
    {"start": 40, "end": 69, "id": "incident-1"}
  ],
  "alarms": [42, 90],
  "tolerance": 0,
  "far_definition": "per_sample",
  "n_non_incident_samples": 90,
  "ttd_statistic": "mean"
}
```

`far_definition` hỗ trợ `per_sample`, `per_hour`, `ratio`. Cần cung cấp
`n_non_incident_samples` cho `per_sample`, hoặc `monitoring_hours` cho
`per_hour`. Khi một chỉ số không xác định (ví dụ không có sự cố), API trả
`null` cho chỉ số đó và `status: "partial"` kèm tên chỉ số trong
`unavailable_metrics`; không tự gán giá trị thay thế.

Response:

```json
{
  "status": "complete",
  "n_incidents": 1,
  "tp": 1,
  "fn": 0,
  "fp": 1,
  "repeated_alarms": 0,
  "dr": 1.0,
  "far": 0.011111111111111112,
  "far_definition": "per_sample",
  "ttd": 2.0,
  "ttd_statistic": "mean",
  "unavailable_metrics": []
}
```

### `GET /api/dashboard`

Trả kết quả mô phỏng và/hoặc đánh giá thành công gần nhất của tiến trình hiện
tại. Trước khi có dữ liệu, response có `status: "no_data"` và các mục kết quả
là `null`. Sau khi chạy, response có `status: "available"`, `data_source` là
`in_memory_api_requests`, và các bản tóm tắt tính từ kết quả thật của các
endpoint.

Không có database: dữ liệu chỉ nằm trong bộ nhớ, mất khi tiến trình khởi động
lại và không được chia sẻ giữa nhiều worker Uvicorn. Dashboard không tự tạo số
liệu mặc định.

## Kiểm thử

```powershell
python -m pytest
```

Các test API dùng FastAPI `TestClient` và kiểm tra hành vi của simulator,
California, metrics, validation, lỗi module và trạng thái Dashboard.

## Giới hạn hiện tại

- Mô phỏng hoàn toàn là dữ liệu tổng hợp có seed; không kết nối nguồn giao thông
  thực hoặc Frontend tự động.
- Dashboard chỉ giữ kết quả gần nhất trong bộ nhớ của từng tiến trình.
- `metrics.py` hiện hỗ trợ DR, FAR và TTD cùng TP/FN/FP/cảnh báo lặp; không có
  TN, Precision hoặc F1-score.
- Đơn vị của các thời điểm cảnh báo, khoảng sự cố, tolerance và TTD phải nhất
  quán (chu kỳ hoặc giây).
- API không xác nhận tính khoa học của ngưỡng thuật toán hoặc định nghĩa metric;
  các kết quả chỉ dành cho demo.
