# Thư mục dữ liệu

## Vai trò

Thư mục `data/` chứa dữ liệu đầu vào cho chương trình phát hiện sự cố giao thông. Dữ liệu hiện tại được **tạo bằng mô phỏng** từ module `src/simulator.py`, không phải dữ liệu đo từ hệ thống giao thông thực tế.

## Các file dữ liệu

| File | Kịch bản | Số chu kỳ | Sự cố | Seed |
|---|---|---|---|---|
| `normal.csv` | Giao thông bình thường | 120 | Không | 42 |
| `incident.csv` | Có một sự cố giữa hai trạm | 120 | Chu kỳ 40–69 | 123 |
| `edge_congestion.csv` | Ùn tắc tự nhiên (không phải sự cố) | 60 | Không | 456 |

## Định dạng CSV

Mỗi file CSV có 4 cột, phân cách bằng dấu phẩy, mã hóa UTF-8:

| Cột | Kiểu | Ý nghĩa |
|---|---|---|
| `timestamp` | int | Chỉ số chu kỳ (0, 1, 2, ...). Mỗi chu kỳ cách nhau 30 giây. |
| `occ_up` | float | Occupancy tại trạm thượng lưu (upstream), đơn vị phần trăm (0–100). |
| `occ_down` | float | Occupancy tại trạm hạ lưu (downstream), đơn vị phần trăm (0–100). |
| `incident` | int | Nhãn tham chiếu: `1` = đang có sự cố, `0` = không có sự cố. |

Ví dụ nội dung file `incident.csv`:

```csv
timestamp,occ_up,occ_down,incident
0,20.81,20.28,0
1,19.2,20.53,0
...
40,27.43,18.09,1
41,33.96,16.13,1
...
70,48.36,12.25,0
```

## Mô tả các kịch bản

### normal.csv — Giao thông bình thường

- OCC tại cả hai trạm dao động quanh mức cơ sở 20% với nhiễu Gaussian (σ = 2.0).
- Không có sự cố trong toàn bộ 120 chu kỳ.
- Dùng để kiểm tra thuật toán không tạo cảnh báo sai khi giao thông bình thường.

### incident.csv — Có sự cố

- 40 chu kỳ đầu: giao thông bình thường (OCC ≈ 20%).
- Chu kỳ 40–44: giai đoạn khởi phát (onset) — OCC_up tăng dần từ 20% lên 55%, OCC_down giảm dần từ 20% xuống 8%.
- Chu kỳ 45–69: sự cố ổn định — OCC_up ≈ 55%, OCC_down ≈ 8%.
- Chu kỳ 70–77: giai đoạn phục hồi — các giá trị dần trở về mức bình thường.
- Chu kỳ 78–119: giao thông bình thường trở lại.
- Dùng để kiểm tra khả năng phát hiện sự cố và đo thời gian phát hiện (TTD).

### edge_congestion.csv — Ùn tắc tự nhiên

- Chu kỳ 15–34: OCC tại **cả hai trạm** đều tăng lên ≈ 45% (ùn tắc do mật độ cao).
- Không có sự cố — đây là trường hợp biên để kiểm tra thuật toán phân biệt được ùn tắc tự nhiên và sự cố.
- Khi có sự cố thực sự, chỉ OCC_up tăng còn OCC_down giảm. Khi ùn tắc tự nhiên, cả hai đều tăng.

## Các giả định quan trọng

1. **Dữ liệu là mô phỏng**: các giá trị OCC được tạo bằng công thức toán học với nhiễu ngẫu nhiên, không lấy từ thiết bị đo thực tế.
2. **Đơn vị**: occupancy tính bằng phần trăm (%), giá trị từ 0 đến 100.
3. **Chu kỳ lấy mẫu**: 30 giây, đồng bộ giữa hai trạm (cùng chỉ số `timestamp`).
4. **Hai trạm**: thượng lưu (upstream) và hạ lưu (downstream) trên cùng một đoạn đường, sự cố xảy ra giữa hai trạm.
5. **Nhãn sự cố**: nhãn `incident` cho biết trạng thái thực tế, không phải kết quả phát hiện của thuật toán.
6. **Tái tạo**: mỗi kịch bản có seed cố định, chạy lại `simulator.py` sẽ cho cùng kết quả.

## Tái tạo dữ liệu

Để tạo lại các file CSV, chạy từ thư mục gốc dự án:

```bash
python -m src.simulator
```

Hoặc sử dụng trong code Python:

```python
from src.simulator import generate_all_scenarios, save_to_csv

scenarios = generate_all_scenarios()
for name, result in scenarios.items():
    save_to_csv(result, f"data/{name}.csv")
```