# Đánh giá hiệu quả phát hiện sự cố

Tài liệu này mô tả cách `src/metrics.py` tính ba chỉ số **DR**, **FAR** và **TTD**.

> **Lưu ý về nguồn:** các định nghĩa dưới đây là định nghĩa thông dụng trong phát hiện sự cố tự động (AID), chưa được đối chiếu với tài liệu bài giảng. Nếu bài giảng định nghĩa khác (ví dụ DR hoặc FAR tính theo mẫu thời gian), hãy dùng định nghĩa của bài giảng và cập nhật cả tài liệu này lẫn `metrics.py`.

Chưa có dữ liệu thử nghiệm, nên tài liệu này không báo cáo kết quả đo hay kết luận về chất lượng thuật toán. Các số trong ví dụ là số minh họa để kiểm tra cách tính.

## 1. Quy ước dữ liệu

- **Sự cố tham chiếu** (`Incident`): một khoảng `[start, end]`, gồm cả hai đầu, lấy từ nhãn `incident` của dữ liệu.
- **Cảnh báo**: một thời điểm mà thuật toán báo sự cố (thời điểm chuyển sang trạng thái "sự cố" đã được xác nhận).
- **Đơn vị thời gian**: là số, dùng cùng một đơn vị ở mọi tham số (chỉ số chu kỳ hoặc giây). TTD có cùng đơn vị đó.
- **Giá trị không hợp lệ** (`NaN`, vô hạn, `end < start`, `tolerance` âm) bị từ chối bằng `ValueError`, không bị thay thế âm thầm.

## 2. Quy tắc ghép cảnh báo với sự cố

Mỗi sự cố có cửa sổ ghép `[start, end + tolerance]`. `tolerance` mặc định là 0, và chỉ tăng lên khi cần chấp nhận cảnh báo đến muộn sau khi sự cố kết thúc.

| Trường hợp | Cách tính |
|---|---|
| Cảnh báo đầu tiên trong cửa sổ của một sự cố | **TP**: sự cố được phát hiện |
| Cảnh báo tiếp theo trong cửa sổ của sự cố đã được phát hiện | **Cảnh báo lặp**: báo riêng, không tính FP |
| Cảnh báo nằm ngoài mọi cửa sổ (kể cả trước `start`) | **FP**: cảnh báo sai |
| Sự cố không có cảnh báo nào trong cửa sổ | **FN**: sự cố bị bỏ sót |

Khi hai cửa sổ chồng nhau, cảnh báo được ưu tiên ghép với sự cố chưa được phát hiện.

## 3. Detection Rate (DR)

- **Ý nghĩa:** tỷ lệ sự cố thực tế được phát hiện.
- **Công thức:** `DR = TP / (TP + FN)`, tính theo sự kiện.
- **Không xác định:** nếu không có sự cố tham chiếu (`TP + FN = 0`), hàm trả về `None`, không gán 0 hoặc 100%.
- **Hạn chế:** DR không nói gì về cảnh báo sai hay độ trễ, và phụ thuộc vào chất lượng nhãn và `tolerance`.

## 4. False Alarm Rate (FAR)

"False alarm rate" có nhiều định nghĩa không tương đương. `false_alarm_rate()` hỗ trợ ba cách, chọn bằng tham số `definition`:

| `definition` | Công thức | Tham số bắt buộc |
|---|---|---|
| `"per_sample"` (mặc định) | số cảnh báo sai / số mẫu đánh giá không có sự cố | `n_non_incident_samples` |
| `"per_hour"` | số cảnh báo sai / số giờ giám sát | `monitoring_hours` |
| `"ratio"` | `FP / (TP + FP)`, tỷ lệ cảnh báo là sai trên tổng cảnh báo | không |

- Mẫu số bằng 0 thì trả về `None`.
- Cảnh báo lặp không được tính vào FP và không được tính vào mẫu số của `"ratio"`.
- Chỉ so sánh các giá trị FAR khi cùng định nghĩa, cùng tập dữ liệu và cùng quy tắc ghép. Khi báo cáo, ghi rõ định nghĩa và mẫu số.

## 5. Time to Detection (TTD)

- **Ý nghĩa:** độ trễ từ lúc sự cố bắt đầu theo nhãn đến lúc phát hiện.
- **Công thức:** với mỗi sự cố được phát hiện, `TTD = thời điểm cảnh báo đầu tiên - start`. Giá trị tổng hợp là trung bình (`"mean"`, mặc định) hoặc trung vị (`"median"`).
- **Không xác định:** nếu chưa phát hiện sự cố nào, trả về `None`.
- **Hạn chế:** TTD chỉ tính trên sự cố được phát hiện, nên có thể trông tốt khi nhiều sự cố bị bỏ sót. Luôn báo kèm DR và số FN. TTD còn phụ thuộc vào chu kỳ lấy mẫu và độ trễ gán nhãn.

## 6. Cách dùng `src/metrics.py`

```python
from src.metrics import Incident, summarize

incidents = [Incident(10, 20, "a"), Incident(50, 60, "b"), Incident(100, 110, "c")]
alarms = [12, 15, 30, 52, 200]

result = summarize(
    incidents,
    alarms,
    tolerance=0,
    far_definition="per_sample",
    n_non_incident_samples=1000,
)
```

Với ví dụ minh họa trên, kết quả là:

| Đại lượng | Giá trị | Giải thích |
|---|---|---|
| TP, FN | 2, 1 | phát hiện sự cố `a` và `b`, bỏ sót `c` |
| FP | 2 | cảnh báo ở thời điểm 30 và 200 nằm ngoài mọi cửa sổ |
| Cảnh báo lặp | 1 | cảnh báo ở thời điểm 15 nằm trong sự cố `a` đã được phát hiện |
| DR | 2/3 ≈ 0,667 | `TP / (TP + FN)` |
| FAR (`per_sample`) | 0,002 | `2 / 1000` |
| TTD (trung bình) | 2,0 | `(12 - 10)` và `(52 - 50)` |

Các hàm thành phần có thể gọi riêng: `match_events`, `detection_rate`, `false_alarm_rate`, `time_to_detection`.

## 7. Quy trình báo cáo

1. Ghi nguồn dữ liệu, schema, khoảng thời gian, cách chia tập và nhãn tham chiếu.
2. Ghi quy tắc ghép (`tolerance`), định nghĩa FAR đã chọn và công thức của mỗi chỉ số.
3. Báo số đếm (TP, FN, FP, cảnh báo lặp), mẫu số, đơn vị và các trường hợp không xác định cùng với giá trị chỉ số.
4. Không khẳng định hệ thống hoạt động tốt nếu chưa chạy thử nghiệm trên dữ liệu phù hợp, và nêu rõ giới hạn của dữ liệu.
