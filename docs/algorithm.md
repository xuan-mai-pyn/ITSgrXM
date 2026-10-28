# Thuật toán California (California Algorithm)

Tài liệu này mô tả cách triển khai hiện tại của `CaliforniaAlgorithm` trong
`src/california.py`. Thuật toán dùng occupancy tại hai trạm thượng lưu
(upstream) và hạ lưu (downstream) để xác định dấu hiệu sự cố giữa hai trạm.

## Các đại lượng

Với mỗi chu kỳ, gọi:

- `occ_up`: occupancy tại trạm thượng lưu, đơn vị phần trăm.
- `occ_down`: occupancy tại trạm hạ lưu, đơn vị phần trăm.
- `OCCDIFF = occ_up - occ_down`: chênh lệch occupancy tuyệt đối.
- `OCCRDF = OCCDIFF / occ_up`: chênh lệch occupancy tương đối. Nếu
  `occ_up <= 0`, phần triển khai đặt `OCCRDF = 0`.

## Điều kiện phát hiện

Một mẫu được xem là ứng viên sự cố khi đồng thời thỏa mãn cả ba điều kiện:

1. `OCCDIFF >= s1`.
2. `OCCRDF >= s2`.
3. `occ_down <= s3`.

Các ngưỡng mặc định:

| Tham số | Mặc định | Ý nghĩa |
|---|---:|---|
| `s1` | `10.0` | Chênh lệch occupancy tuyệt đối tối thiểu, tính theo điểm phần trăm |
| `s2` | `0.20` | Chênh lệch tương đối tối thiểu (20%) |
| `s3` | `20.0` | Occupancy hạ lưu tối đa để thỏa điều kiện phát hiện, tính theo phần trăm |
| `persistence` | `2` | Số mẫu ứng viên liên tiếp cần có để xác nhận phát hiện |

Có thể truyền giá trị khác khi khởi tạo `CaliforniaAlgorithm`; API cũng cho
phép override các ngưỡng này trong trường `algorithm`.

## Bộ lọc duy trì và kết quả

Thuật toán tăng bộ đếm liên tiếp khi một mẫu thỏa cả ba điều kiện. Nếu một mẫu
không thỏa, bộ đếm được đặt lại về 0. `evaluate(occ_up, occ_down)` trả về
`True` khi bộ đếm đạt ít nhất `persistence`, ngược lại trả về `False`.

Sau khi đã đạt ngưỡng persistence, các mẫu tiếp theo tiếp tục thỏa điều kiện
thì vẫn trả về `True`. Khi điều kiện không còn thỏa, bộ đếm được đặt lại và
hàm trả về `False`. Gọi `reset()` để đặt lại bộ đếm, ví dụ khi bắt đầu một kịch
bản mô phỏng mới.

## Giới hạn sử dụng

Đây là cách triển khai demo với các ngưỡng cấu hình được nêu trên. Kết quả phụ
thuộc vào occupancy đầu vào, các ngưỡng và `persistence`; không nên xem đây là
xác nhận hiệu quả thực tế nếu chưa đánh giá trên dữ liệu phù hợp.
