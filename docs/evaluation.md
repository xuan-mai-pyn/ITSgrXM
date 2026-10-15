# Kế hoạch đánh giá hiệu quả

Chưa có dữ liệu thử nghiệm, nhãn tham chiếu, kết quả đo hoặc kết luận về chất lượng hệ thống. Các công thức dưới đây là định nghĩa dự kiến/thông dụng để nhóm xem xét, không được xác nhận là định nghĩa của tài liệu bài giảng. Trước khi triển khai, cần ưu tiên công thức trong bài giảng hoặc thống nhất rõ quy ước đánh giá của nhóm.

## Dữ liệu cần chuẩn bị chung

- Dự đoán phát hiện của thuật toán, kèm thời điểm và định danh sự kiện nếu có.
- Nhãn tham chiếu đáng tin cậy: thời điểm bắt đầu/kết thúc, vị trí và định danh sự cố.
- Khoảng thời gian giám sát không có sự cố để xác định cảnh báo sai.
- Quy tắc ghép một cảnh báo với một sự cố, cửa sổ ghép, đơn vị thời gian và cách xử lý cảnh báo lặp.

Không tạo hoặc báo cáo số liệu khi chưa chạy đánh giá trên dữ liệu phù hợp.

## Detection Rate (DR)

1. **Ý nghĩa:** Tỷ lệ sự cố thực tế được hệ thống phát hiện.
2. **Dữ liệu cần có:** Danh sách sự cố tham chiếu và danh sách phát hiện; cần quy tắc ghép phát hiện với sự cố.
3. **Cách tính dự kiến:** Theo cách đánh giá theo sự kiện, `DR = TP / (TP + FN)`, trong đó `TP` là sự cố được phát hiện và `FN` là sự cố bị bỏ sót. Nếu bài giảng dùng cách tính theo mẫu thời gian hoặc định nghĩa khác, phải dùng định nghĩa đó thay thế.
4. **Diễn giải:** DR cao hơn nghĩa là phát hiện được nhiều sự cố tham chiếu hơn trong tập đánh giá, nhưng không nói lên số cảnh báo sai hay độ trễ.
5. **Hạn chế:** Phụ thuộc vào chất lượng nhãn, quy tắc ghép, tính đại diện của dữ liệu và mẫu số khác 0. Khi không có sự cố tham chiếu (`TP + FN = 0`), cần báo “không xác định/không áp dụng”, không tự gán 0 hoặc 100%.

## False Alarm Rate (FAR)

1. **Ý nghĩa:** Mức độ hệ thống phát ra cảnh báo không tương ứng với sự cố thực.
2. **Dữ liệu cần có:** Cảnh báo, nhãn tham chiếu, khoảng thời gian giám sát và quy tắc ghép/đếm cảnh báo.
3. **Cách tính hoặc định nghĩa cần chọn:** “False alarm rate” có thể được định nghĩa theo mẫu là `FP / (FP + TN)`, theo cảnh báo trên đơn vị thời gian, hoặc theo số sự cố giả trên tổng cảnh báo (`FP / (TP + FP)`, thường gọi là false discovery proportion). Các định nghĩa này không tương đương. Chưa có công thức từ bài giảng, vì vậy cần xác minh và ghi rõ mẫu số, đơn vị thời gian, cách gom cảnh báo lặp trước khi báo FAR.
4. **Diễn giải:** Chỉ diễn giải sau khi đã xác định định nghĩa; giá trị thấp hơn thường biểu thị ít báo động sai hơn theo đúng mẫu số đã chọn.
5. **Hạn chế:** Kết quả thay đổi theo tỷ lệ sự cố, khoảng giám sát, quy tắc ghép và cách xử lý cảnh báo lặp. Không so sánh hai FAR nếu khác định nghĩa hoặc tập dữ liệu.

## Time to Detection (TTD)

1. **Ý nghĩa:** Thời gian từ lúc sự cố bắt đầu theo nhãn tham chiếu đến lúc hệ thống phát hiện.
2. **Dữ liệu cần có:** Thời điểm bắt đầu sự cố và thời điểm phát hiện đầu tiên được ghép hợp lệ cho từng sự cố.
3. **Cách tính dự kiến:** Với từng sự cố được phát hiện, `TTD = thời điểm phát hiện đầu tiên - thời điểm bắt đầu sự cố`. Khi tổng hợp, báo rõ thống kê sử dụng (ví dụ trung vị hoặc trung bình), đơn vị và tập sự cố được tính. Cần xác minh liệu tài liệu bài giảng có định nghĩa khác hay không.
4. **Diễn giải:** TTD nhỏ hơn biểu thị phát hiện nhanh hơn đối với các sự cố được ghép và tính; cần báo riêng số sự cố bị bỏ sót.
5. **Hạn chế:** Phụ thuộc độ chính xác dấu thời gian, chu kỳ lấy mẫu, định nghĩa lúc bắt đầu và độ trễ gán nhãn. Tính TTD chỉ trên sự cố được phát hiện có thể làm kết quả có vẻ tốt hơn nếu bỏ qua FN; cần báo DR cùng TTD.

## Quy trình báo cáo

1. Ghi nguồn dữ liệu, schema, khoảng thời gian, cách chia tập và nhãn tham chiếu.
2. Ghi chính xác định nghĩa TP/FP/TN/FN, quy tắc ghép cảnh báo và công thức mỗi chỉ số.
3. Báo mẫu số, số lượng sự cố/cảnh báo, đơn vị và trường hợp không xác định bên cạnh giá trị chỉ số.
4. Không khẳng định hệ thống hoạt động tốt nếu chưa chạy thử nghiệm và mô tả giới hạn dữ liệu.
