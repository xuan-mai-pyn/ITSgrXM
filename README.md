# California Traffic Incident Detection System

## 1. Giới thiệu dự án

Đây là dự án demo thuật toán California trong bài toán phát hiện sự cố giao thông thuộc lĩnh vực Hệ thống giao thông thông minh (Intelligent Transportation Systems – ITS). Dự án hướng đến mục đích học tập và thuyết trình, với cách tổ chức đơn giản để sinh viên có thể đọc, chạy và mở rộng.

Phiên bản hiện tại mới thiết lập cấu trúc và phần khung. Chưa có triển khai thuật toán, dữ liệu mẫu hoặc kết quả đánh giá.

## 2. Mục tiêu dự án

- Tìm hiểu nguyên lý phát hiện sự cố từ dữ liệu các trạm giám sát.
- Tổ chức chương trình Python chạy trực tiếp trong Terminal.
- Chuẩn bị nơi lưu dữ liệu, mã nguồn, kiểm thử và tài liệu thiết kế.
- Tạo nền tảng để sau này kiểm thử và đánh giá hiệu quả phát hiện một cách có thể lặp lại.

## 3. Phạm vi thực hiện

Trong giai đoạn khởi tạo, dự án chỉ cung cấp cấu trúc thư mục, tài liệu và khung mã nguồn. Chưa cài đặt logic thuật toán California, bộ mô phỏng dữ liệu, phép tính các chỉ số đánh giá hoặc bộ dữ liệu đầu vào.

Đây là ứng dụng Python chạy cục bộ. Dự án không có Frontend, Backend riêng, API server hay giao diện web.

## 4. Nguyên lý hoạt động tổng quát

Khi được triển khai, chương trình dự kiến đọc dữ liệu OCC tại trạm phía thượng lưu (`OCC_up`) và trạm phía hạ lưu (`OCC_down`), kiểm tra tính hợp lệ, áp dụng đúng các điều kiện và ngưỡng của thuật toán California, rồi xuất trạng thái giao thông. Kết quả sẽ được đối chiếu với nhãn sự cố đã biết để tính các chỉ số đánh giá.

Đây chỉ là luồng khái quát, không thay thế công thức hoặc thứ tự kiểm tra của tài liệu bài giảng. Các ngưỡng T1, T2, T3, điều kiện xác nhận qua chu kỳ tiếp theo và điều kiện kết thúc sự cố cần được xác minh trước khi triển khai. Xem [docs/algorithm.md](docs/algorithm.md).

## 5. Công nghệ sử dụng

- Python 3.10 trở lên.
- `pytest` để tổ chức và chạy kiểm thử.
- Thư viện chuẩn Python cho phần khung ban đầu.

`pytest` là phụ thuộc phát triển/kiểm thử duy nhất hiện được khai báo. Chưa cần `pandas` vì chưa có mã đọc hoặc xử lý CSV; chỉ bổ sung nếu triển khai thực tế cần đến.

## 6. Cấu trúc thư mục và chức năng từng thành phần

```text
ITSgrXM/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   └── README.md
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── california.py
│   ├── simulator.py
│   └── metrics.py
├── tests/
│   └── test_california.py
└── docs/
    ├── algorithm.md
    ├── system_design.md
    └── evaluation.md
```

- `src/main.py`: điểm vào chương trình Terminal; hiện chỉ thông báo phần xử lý chưa được triển khai.
- `src/california.py`: vị trí dành cho logic thuật toán California.
- `src/simulator.py`: vị trí dành cho mô phỏng/chuẩn bị dữ liệu khi có đặc tả phù hợp; chưa sinh dữ liệu.
- `src/metrics.py`: vị trí dành cho các chỉ số đánh giá; chưa tính chỉ số.
- `data/`: hướng dẫn cách tổ chức dữ liệu, không chứa dữ liệu giả hoặc dữ liệu thực tế trong phiên bản này.
- `tests/`: kiểm thử thuật toán; kiểm thử California hiện được đánh dấu bỏ qua cho đến khi có đặc tả và mã triển khai.
- `docs/`: tài liệu nguyên lý, thiết kế hệ thống và kế hoạch đánh giá.

## 7. Yêu cầu cài đặt

- Python 3.10 trở lên và `pip`.
- Terminal, PowerShell hoặc Command Prompt.
- Git là tùy chọn nếu bạn cần quản lý mã nguồn theo phiên bản.

## 8. Hướng dẫn thiết lập môi trường Python

Tại thư mục gốc dự án, tạo môi trường ảo:

```bash
python -m venv .venv
```

Kích hoạt môi trường trên Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

Trên Windows (Command Prompt):

```bat
.venv\Scripts\activate.bat
```

Trên macOS/Linux:

```bash
source .venv/bin/activate
```

## 9. Hướng dẫn cài đặt thư viện

Sau khi kích hoạt môi trường ảo:

```bash
pip install -r requirements.txt
```

Tệp phụ thuộc hiện chỉ có `pytest`, phục vụ kiểm thử. Không cần cài thư viện xử lý dữ liệu hoặc giao diện cho phần khung hiện tại.

## 10. Hướng dẫn chạy chương trình khi phần mã nguồn đã được triển khai

Từ thư mục gốc repository:

```bash
python -m src.main
```

Hiện lệnh này chỉ hiển thị thông báo rằng thuật toán chưa được triển khai. Luồng phát hiện sự cố đầy đủ chỉ hoạt động sau khi hoàn thành việc đọc/kiểm tra dữ liệu và cài đặt thuật toán theo tài liệu đã xác minh.

## 11. Hướng dẫn chạy kiểm thử

Sau khi cài phụ thuộc, chạy từ thư mục gốc:

```bash
pytest
```

Kiểm thử California hiện là khung được bỏ qua, chưa kiểm tra khả năng phát hiện. Bộ kiểm thử chỉ có thể đánh giá đầy đủ hành vi sau khi thuật toán và các trường hợp kiểm thử được triển khai. Không xem việc thu thập hoặc bỏ qua kiểm thử khung là bằng chứng thuật toán hoạt động đúng.

## 12. Hướng phát triển tiếp theo

1. Bổ sung tài liệu bài giảng/đặc tả gốc, xác minh công thức và thứ tự điều kiện của California.
2. Chốt định dạng dữ liệu, đơn vị OCC, khoảng thời gian lấy mẫu và quy ước nhãn sự cố.
3. Triển khai kiểm tra dữ liệu và thuật toán có xử lý dữ liệu thiếu/không hợp lệ.
4. Bổ sung dữ liệu kiểm thử có nguồn gốc, nhãn tham chiếu và kiểm thử các tình huống biên.
5. Tính DR, FAR, TTD theo định nghĩa đã thống nhất và báo cáo kết quả thực nghiệm có thể tái lập.

## 13. Giới hạn của phiên bản demo

- Chưa triển khai thuật toán California và chưa xác minh ngưỡng T1, T2, T3.
- Chưa có dữ liệu đầu vào; không có kết quả thực nghiệm.
- Chưa triển khai mô phỏng, đánh giá hoặc xử lý dữ liệu.
- Chưa thể dùng cho giám sát giao thông thực tế hay ra quyết định vận hành.
- Các lệnh chạy/kiểm thử mới chỉ chạy phần khung tương ứng; chúng không chứng minh hệ thống phát hiện sự cố đã hoàn chỉnh.
