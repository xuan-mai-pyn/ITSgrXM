# Thiết kế hệ thống

## Kiến trúc & Luồng dữ liệu

```text
                        ┌─────────────────────────────┐
                        │   main.py  (Mai - Người 4)  │
                        │   Điều phối & hiển thị      │
                        └─────────────────────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          │                           │                           │
          ▼                           ▼                           ▼
  ┌──────────────┐          ┌──────────────────┐        ┌──────────────┐
  │ simulator.py │          │  california.py   │        │  metrics.py  │
  │ (Cường-P.2)  │          │  (Khang - P.1)   │        │ (Hiếu - P.3) │
  └──────────────┘          └──────────────────┘        └──────────────┘
         │                       │        ▲                      │
         │  occ_up, occ_down     │        │ kiểm thử độc lập     │
         │ ──────────────────────▶        │                      │
         │                       │  ┌─────────────────┐         │
         │                       │  │ test_california  │         │
         │                       │  │  (Khoa - P.5)   │         │
         │                       │  └─────────────────┘         │
         │                       │  kết quả phát hiện           │
         │                       └──────────────────────────────▶│
         │                                                        │
         │  nhãn incident (ground truth)                         │
         │ ──────────────────────────────────────────────────────▶│
         │                                                        │
         │                                              DR, FAR, TTD
```

---

## Lớp REST API

`src/api.py` cung cấp HTTP API độc lập, không biến `src/main.py` thành server:

```text
HTTP client → src.api → simulator → CaliforniaAlgorithm → metrics
                └──────────────────────────────→ JSON response
```

- `GET /api/health`: trạng thái dịch vụ.
- `POST /api/simulations`: tạo một kịch bản đã hỗ trợ, chạy California trên
  từng bản ghi, rồi dùng nhãn mô phỏng và mốc cảnh báo để tính metrics.
- `POST /api/evaluations`: nhận các khoảng sự cố và thời điểm cảnh báo, gọi
  `metrics.summarize`.
- `GET /api/dashboard`: trả tóm tắt kết quả API gần nhất trong bộ nhớ tiến trình.

API không dùng database. Dashboard không có dữ liệu trước khi có request mô
phỏng/đánh giá thành công; dữ liệu trong bộ nhớ mất khi tiến trình kết thúc và
không được chia sẻ giữa nhiều worker. CORS mặc định chỉ cho phép origin
`localhost`/`127.0.0.1` khi phát triển; có thể cấu hình thêm bằng
`ITS_ALLOWED_ORIGINS`. Chi tiết schema, ví dụ và lệnh chạy nằm trong
[`docs/api.md`](api.md).

---

## Trách nhiệm từng module

### `simulator.py` — Cường (Người 2)
Tạo dữ liệu occupancy mô phỏng cho 3 kịch bản:

| Kịch bản | Hàm gọi | Mô tả |
|---|---|---|
| Bình thường | `generate_normal()` | OCC cả 2 trạm ≈ 20%, không sự cố |
| Có sự cố | `generate_incident()` | OCC_up tăng, OCC_down giảm đột ngột |
| Ùn tắc tự nhiên | `generate_edge_case()` | OCC cả 2 trạm đều tăng (không phải sự cố) |

Cách Khang và Hiếu lấy dữ liệu:
```python
from src.simulator import generate_incident

result = generate_incident()
for rec in result.records:
    rec.occ_up      # → Khang dùng để chạy thuật toán
    rec.occ_down    # → Khang dùng để chạy thuật toán
    rec.incident    # → Hiếu dùng để chấm điểm (True/False)
```

---

### `california.py` — Khang (Người 1)
Nhận `occ_up`, `occ_down` từng chu kỳ, áp dụng thuật toán California, trả về kết quả phát hiện.

**Khang cần cung cấp cho nhóm:**
- Tên hàm phát hiện và cách gọi.
- Định dạng kết quả trả về tại mỗi chu kỳ (ví dụ: `True/False` hoặc trạng thái `"normal"/"incident"`).

---

### `metrics.py` — Hiếu (Người 3)
Nhận kết quả phát hiện từ `california.py` và nhãn thực tế `rec.incident` từ `simulator.py`, tính các chỉ số:

| Chỉ số | Ý nghĩa |
|---|---|
| DR (Detection Rate) | Tỷ lệ sự cố được phát hiện đúng |
| FAR (False Alarm Rate) | Tỷ lệ báo động sai khi không có sự cố |
| TTD (Time to Detection) | Thời gian từ lúc sự cố xảy ra đến lúc phát hiện |

---

### `main.py` — Mai (Người 4)
Gọi các module theo đúng thứ tự và hiển thị kết quả ra Terminal:
```
simulator → california → metrics → in kết quả
```

---

### `tests/test_california.py` — Khoa (Người 5)
Kiểm thử độc lập thuật toán California, đảm bảo kết quả đúng trước khi tích hợp vào chương trình chính.

**Khoa cần kiểm thử:**

| Trường hợp | Dữ liệu đầu vào | Kết quả mong đợi |
|---|---|---|
| Bình thường | OCC_up ≈ OCC_down ≈ 20% | Không phát hiện sự cố |
| Có sự cố | OCC_up ≈ 55%, OCC_down ≈ 8% | Phát hiện sự cố |
| Ùn tắc tự nhiên | OCC_up ≈ OCC_down ≈ 45% | Không phát hiện sự cố |

Khoa có thể lấy dữ liệu trực tiếp từ `simulator.py`:
```python
from src.simulator import generate_normal, generate_incident, generate_edge_case
```

---

## Quy ước dữ liệu chung

| Thuộc tính | Quy ước |
|---|---|
| Đơn vị OCC | Phần trăm (%), giá trị 0–100 |
| Chu kỳ lấy mẫu | 30 giây |
| Đồng bộ thời gian | Hai trạm dùng chung `timestamp` |
| Nhãn sự cố | `True`/`False` (Python), `1`/`0` (CSV) |
| Seed | Cố định theo từng kịch bản — tái tạo được cùng dữ liệu |

---

## Cách chạy

```bash
# Chạy toàn bộ chương trình
python -m src.main

# Tạo lại dữ liệu mô phỏng
python -m src.simulator

# Chạy kiểm thử
python -m pytest -v
```


