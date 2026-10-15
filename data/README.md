# Thư mục dữ liệu

## Vai trò

Thư mục `data/` dành cho dữ liệu đầu vào, dữ liệu kiểm thử và (nếu cần) các tệp kết quả được tạo trong quá trình chạy. Hiện chưa có bộ dữ liệu nào được cung cấp hoặc tạo trong thư mục này.

## Định dạng đầu vào dự kiến

CSV là định dạng dự kiến để thuận tiện kiểm tra bằng công cụ phổ biến. Đây mới là đề xuất tổ chức, chưa phải định dạng đã được xác nhận từ tài liệu bài giảng hay một nguồn dữ liệu cụ thể. Tên tệp, mã hóa, dấu phân cách và quy ước thời gian cần được thống nhất trước khi viết bộ đọc dữ liệu.

Các trường dự kiến:

| Cột | Ý nghĩa dự kiến |
|---|---|
| `timestamp` | Thời điểm hoặc mốc thời gian của mẫu; cần thống nhất múi giờ và định dạng. |
| `OCC_up` | Thông số OCC tại trạm phía thượng lưu. |
| `OCC_down` | Thông số OCC tại trạm phía hạ lưu. |
| `incident` (tùy chọn) | Nhãn tham chiếu về sự cố, nếu nguồn dữ liệu có nhãn đáng tin cậy. |

Đơn vị, miền giá trị, khoảng lấy mẫu, cách xử lý bản ghi trùng và các cột bổ sung phải căn cứ vào nguồn dữ liệu thực tế; không suy ra từ tên cột.

## Bổ sung dữ liệu mới

1. Ghi rõ nguồn, thời gian thu thập, giấy phép/điều kiện sử dụng và ý nghĩa các cột.
2. Giữ nguyên dữ liệu gốc; không tự ghi đè hoặc sửa nhãn mà không lưu lại quy trình biến đổi.
3. Kiểm tra định dạng thời gian, giá trị OCC thiếu/không hợp lệ và tính đồng bộ giữa hai trạm.
4. Cập nhật tài liệu này khi schema hoặc quy ước dữ liệu thay đổi.

## Phân biệt dữ liệu minh họa và dữ liệu thực tế

Không ghi dữ liệu minh họa là dữ liệu thực tế. Nếu sau này tạo dữ liệu tổng hợp để kiểm tra luồng chương trình, hãy đặt tên và ghi chú rõ là dữ liệu tổng hợp, mô tả cách tạo và không dùng nó để khẳng định hiệu quả trên giao thông thực. Dữ liệu thực tế cần kèm thông tin nguồn và giới hạn sử dụng phù hợp.
