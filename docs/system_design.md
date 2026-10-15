# Thiết kế hệ thống

## Phạm vi

Đây là chương trình Python chạy cục bộ từ Terminal, phục vụ demo và học tập. Không có Frontend, Backend/API server riêng hoặc giao diện web. Thiết kế giữ ở mức các mô-đun Python nhỏ, chưa bổ sung kiến trúc triển khai phức tạp.

## Luồng xử lý dự kiến

```text
Dữ liệu giao thông
    → Đọc dữ liệu
    → Kiểm tra dữ liệu
    → Thuật toán California
    → Xác định trạng thái giao thông
    → Xuất kết quả
    → Đánh giá hiệu quả phát hiện
```

Luồng trên là mục tiêu thiết kế; hiện chưa có mô-đun đọc/kiểm tra dữ liệu, thuật toán, đầu ra kết quả hay đánh giá được triển khai.

## Trách nhiệm các thành phần

- `src/main.py`: điểm vào dòng lệnh; điều phối luồng xử lý khi các thành phần được xây dựng.
- `src/california.py`: chứa quy tắc phát hiện California sau khi công thức và thứ tự điều kiện được xác minh.
- `src/simulator.py`: dành cho tạo chuỗi mô phỏng có đặc tả rõ ràng; không thay thế dữ liệu thực tế và hiện chưa tạo mẫu.
- `src/metrics.py`: tính các chỉ số đánh giá từ kết quả phát hiện và nhãn tham chiếu khi định nghĩa đã được thống nhất.
- `data/`: lưu trữ có tổ chức dữ liệu đầu vào/kiểm thử và tài liệu nguồn gốc; hiện chưa có dữ liệu.
- `tests/`: chứa kiểm thử thuật toán và xử lý dữ liệu; kiểm thử hiện tại được bỏ qua cho đến khi có mã và đặc tả.

## Cách chạy và ranh giới mô-đun

Điểm vào dự kiến là `python -m src.main` từ thư mục gốc. `main.py` sẽ đọc/chuẩn bị dữ liệu, gọi phần kiểm tra đầu vào, chuyển dữ liệu hợp lệ cho `california.py`, rồi chuyển kết quả và nhãn tham chiếu cho phần xuất kết quả/đánh giá. Chi tiết giao tiếp giữa mô-đun cần được chốt cùng định dạng dữ liệu và đặc tả thuật toán.

Hiện tại chỉ có thông báo khung từ `main.py`; những bước còn lại chưa được triển khai. Không có tiến trình server chạy nền hoặc API cần khởi động.
