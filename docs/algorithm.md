# Nguyên lý thuật toán California

## Tình trạng nguồn tham khảo

Trong workspace được kiểm tra không có tài liệu bài giảng, công thức thuật toán hoặc dữ liệu tham chiếu về California. Vì vậy tài liệu này không khẳng định công thức, giá trị ngưỡng, thứ tự kiểm tra hay quy tắc trạng thái cụ thể nào. Các mục chưa có căn cứ được đánh dấu để nhóm bổ sung sau khi đối chiếu tài liệu gốc.

## 1. Mục đích

Mục tiêu dự kiến của thuật toán là nhận biết sự cố giao thông từ các thông số đo tại các trạm giám sát. Cách thức cụ thể mà thuật toán California kết hợp các thông số phải lấy từ tài liệu bài giảng đã xác minh.

## 2. Dữ liệu OCC tại hai trạm

- `OCC_up`: thông số OCC tại trạm phía thượng lưu.
- `OCC_down`: thông số OCC tại trạm phía hạ lưu.

Tên trường và vị trí tương đối được dùng theo yêu cầu dự án. Đơn vị, cách tính OCC, khoảng lấy mẫu và yêu cầu đồng bộ thời gian chưa được cung cấp; cần xác minh trước khi so sánh hai giá trị.

## 3. Ngưỡng T1, T2 và T3

Ý nghĩa chính xác của T1, T2 và T3 chưa thể xác định nếu thiếu bài giảng. Không đặt giá trị hoặc gán ý nghĩa như ngưỡng OCC, ngưỡng tỷ số hay thời gian duy trì khi chưa có căn cứ.

| Ngưỡng | Nội dung cần trích/xác minh từ bài giảng |
|---|---|
| T1 | Đại lượng được so sánh, giá trị/đơn vị, toán tử so sánh và vai trò trong quy tắc. |
| T2 | Đại lượng được so sánh, giá trị/đơn vị, toán tử so sánh và vai trò trong quy tắc. |
| T3 | Đại lượng được so sánh, giá trị/đơn vị, toán tử so sánh và vai trò trong quy tắc. |

Khi có tài liệu, ghi lại đúng công thức, toán tử biên (`<`, `<=`, `>`, `>=`) và thứ tự áp dụng; không hiệu chỉnh ngưỡng mà không ghi rõ nguồn/cách hiệu chỉnh.

## 4. Các bước kiểm tra điều kiện

Luồng kiểm tra ở mức khái quát (không phải các điều kiện California đã xác minh):

1. Nhận bản ghi và thời điểm của hai trạm.
2. Kiểm tra bản ghi có đủ, hợp lệ và đồng bộ để áp dụng thuật toán hay không.
3. Tính/đọc các đại lượng cần thiết theo đúng định nghĩa trong bài giảng.
4. Áp dụng tuần tự các điều kiện T1, T2, T3 theo đúng công thức gốc.
5. Nếu quy tắc chỉ ra khả năng sự cố, lưu trạng thái chờ xác nhận để kiểm tra chu kỳ kế tiếp.
6. Xuất trạng thái cùng thời điểm và thông tin giải thích cần thiết.

Các bước 3–5 mới là phác thảo quy trình phần mềm; các phép tính và nhánh quyết định chưa được xác định. Không dùng luồng này như đặc tả đủ để cài đặt thuật toán.

## 5. Xác nhận qua chu kỳ tiếp theo

Yêu cầu dự án đề cập đến cơ chế xác nhận sự cố qua chu kỳ kế tiếp, nhưng điều kiện xác nhận, số chu kỳ, cách xử lý mẫu không hợp lệ xen giữa và thời điểm gắn nhãn sự cố chưa được cung cấp. Cần trích đúng điều kiện và thứ tự từ bài giảng trước khi triển khai.

## 6. Kết thúc trạng thái sự cố

Điều kiện đưa hệ thống ra khỏi trạng thái sự cố chưa được xác minh. Cần làm rõ điều kiện phục hồi, số chu kỳ cần theo dõi, xử lý mất dữ liệu và cách phân biệt “đã kết thúc” với “chưa đủ dữ liệu”.

## 7. Đầu vào và đầu ra dự kiến

**Đầu vào dự kiến:** mốc thời gian, `OCC_up`, `OCC_down`; có thể cần thêm các trường hoặc trạng thái từ chu kỳ trước tùy theo bài giảng. Schema hiện tại chỉ là đề xuất trong [data/README.md](../data/README.md).

**Đầu ra dự kiến:** trạng thái giao thông (ví dụ: bình thường, chờ xác nhận, sự cố, hoặc chưa đủ dữ liệu), thời điểm đánh giá và thông tin điều kiện đã kích hoạt. Các tên trạng thái và nội dung thực tế cần thống nhất khi triển khai.

## 8. Trường hợp cần xử lý

- Thiếu `OCC_up`, `OCC_down` hoặc thời gian.
- Giá trị ngoài miền hợp lệ, sai định dạng hoặc không đồng bộ giữa hai trạm.
- Mẫu trùng, đến sai thứ tự hoặc có khoảng trống trong chuỗi thời gian.
- Mẫu số bằng 0 nếu công thức đã xác minh có phép chia.
- Giá trị không hữu hạn hoặc đơn vị/định dạng không nhất quán.

Đây là các trường hợp kỹ thuật cần thiết kế xử lý, không phải quy tắc gốc của thuật toán. Không thay dữ liệu lỗi bằng giá trị mặc định một cách âm thầm; cần quy định rõ cách báo lỗi, bỏ mẫu hay giữ trạng thái chờ.

## 9. Các vấn đề cần xác minh trước khi triển khai

1. Bài giảng/nguồn gốc và phiên bản của thuật toán California.
2. Định nghĩa chính xác OCC, đơn vị và cách lấy mẫu tại mỗi trạm.
3. Công thức, ngưỡng, toán tử biên và thứ tự kiểm tra T1, T2, T3.
4. Quy tắc xác nhận ở chu kỳ kế tiếp và điều kiện kết thúc sự cố.
5. Cách xử lý thiếu dữ liệu, mẫu không hợp lệ và mẫu số bằng 0.
6. Định nghĩa nhãn tham chiếu và mốc bắt đầu/kết thúc sự cố để đánh giá.

## Phân biệt nguồn và đề xuất

Nội dung duy nhất có căn cứ từ yêu cầu dự án là sử dụng `OCC_up`, `OCC_down`, các ngưỡng T1–T3, xác nhận qua chu kỳ kế tiếp và có điều kiện kết thúc sự cố. Chi tiết của chúng chưa được cung cấp. Luồng dữ liệu, trường đầu vào/đầu ra và các tình huống xử lý ở trên là đề xuất tổ chức kỹ thuật, không phải trích dẫn hay diễn giải đã xác minh từ bài giảng.
