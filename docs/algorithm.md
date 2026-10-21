# Thuật toán California (California Algorithm)

## 1. Giới thiệu
Thuật toán California là một trong những thuật toán phổ biến được sử dụng trong Hệ thống Giao thông Thông minh (ITS) để phát hiện sự cố giao thông (Incident Detection) dựa trên dữ liệu thu thập từ các cảm biến vòng từ (loop detectors).

## 2. Nguyên lý hoạt động
Thuật toán so sánh sự khác biệt về độ chiếm dụng mặt đường (Occupancy - $OC$) giữa các cảm biến đặt nối tiếp nhau trên cùng một làn đường theo thời gian.

Các chỉ số chính được tính toán:
- **Spatial Difference ($OCCDIFF$):** Chênh lệch độ chiếm dụng giữa cảm biến phía trên (Upstream) và phía dưới (Downstream).
- **Relative Difference ($OCCRDF$):** Tỉ lệ chênh lệch độ chiếm dụng tương đối giữa 2 cảm biến.
- **Downstream Occupancy ($DOCX$):** Độ chiếm dụng tại cảm biến phía dưới theo thời gian.

## 3. Các bước ra quyết định (Decision Tree)
1. Kiểm tra $OCCDIFF$ có vượt ngưỡng $TH1$ hay không.
2. Kiểm tra $OCCRDF$ có vượt ngưỡng $TH2$ hay không.
3. Kiểm tra $DOCX$ có giảm xuống dưới ngưỡng $TH3$ hay không.
4. Nếu cả 3 điều kiện trên đều thỏa mãn, hệ thống sẽ phát cảnh báo sự cố giao thông (Incident Detected).