# ITSgrXM — Hệ thống phát hiện sự cố giao thông bằng thuật toán California

## 1. Giới thiệu

ITSgrXM là dự án mô phỏng hệ thống phát hiện sự cố giao thông thuộc lĩnh vực Hệ thống giao thông thông minh (Intelligent Transportation Systems – ITS).

Dự án tập trung triển khai thuật toán California để phát hiện các dấu hiệu bất thường của dòng giao thông dựa trên dữ liệu chiếm dụng làn đường (Occupancy – OCC) tại các trạm quan trắc giao thông liên tiếp.

Hệ thống sử dụng dữ liệu giao thông mô phỏng để kiểm tra thuật toán, đánh giá hiệu quả phát hiện và trình bày kết quả thông qua giao diện dòng lệnh cùng giao diện web cơ bản.

## 2. Mục tiêu dự án

- Tìm hiểu nguyên lý hoạt động của thuật toán California trong phát hiện sự cố giao thông.
- Xây dựng chương trình Python triển khai thuật toán.
- Mô phỏng dữ liệu giao thông trong điều kiện bình thường và khi xảy ra sự cố.
- Đánh giá kết quả phát hiện bằng các chỉ số phù hợp.
- Xây dựng giao diện web cơ bản để trình bày dữ liệu và kết quả đánh giá.
- Tổ chức mã nguồn theo từng module nhằm thuận tiện cho việc phát triển, kiểm thử và tích hợp.

## 3. Chức năng chính

### 3.1. Phát hiện sự cố bằng thuật toán California

Đây là chức năng trọng tâm của dự án.

Thuật toán sử dụng dữ liệu occupancy tại các trạm quan trắc liên tiếp để đánh giá sự khác biệt trong trạng thái giao thông và xác định dấu hiệu có thể liên quan đến sự cố.

Các ngưỡng, điều kiện phát hiện và quy tắc xác nhận sự cố được triển khai theo tài liệu môn học đã thống nhất.

### 3.2. Mô phỏng dữ liệu giao thông

Chương trình tạo dữ liệu giao thông mô phỏng để phục vụ kiểm thử, bao gồm các kịch bản:

- Giao thông bình thường.
- Giao thông có sự cố.
- Các tình huống khác phục vụ đánh giá thuật toán nếu được triển khai.

Dữ liệu có thể bao gồm thời điểm quan sát, giá trị occupancy tại các trạm và nhãn sự cố thực tế của kịch bản mô phỏng.

Dữ liệu mô phỏng không được xem là dữ liệu giao thông thực tế thu thập từ đường phố.

### 3.3. Đánh giá hiệu quả phát hiện

Hệ thống có thể sử dụng các chỉ số đánh giá sau, tùy theo phương pháp được triển khai:

| Chỉ số                     | Ý nghĩa                                                                    |
| -------------------------- | -------------------------------------------------------------------------- |
| Detection Rate (DR)        | Tỷ lệ sự cố thực tế được phát hiện                                         |
| False Alarm Rate (FAR)     | Tỷ lệ báo động giả theo định nghĩa đánh giá được sử dụng                   |
| Mean Time to Detect (MTTD) | Thời gian phát hiện trung bình đối với các sự cố được phát hiện thành công |

Công thức, mẫu số, đơn vị và cách xác định các trường hợp phát hiện đúng, bỏ sót hoặc báo động giả được trình bày trong `docs/evaluation.md`.

Các chỉ số phải được tính từ dữ liệu và kết quả thực tế của chương trình, không sử dụng số liệu cố định để thay thế kết quả đánh giá.

### 3.4. Giao diện web cơ bản

Frontend được xây dựng bằng HTML, CSS và JavaScript thuần, không yêu cầu framework frontend.

Các trang giao diện dự kiến gồm:

- Trang giới thiệu dự án.
- Trang tổng quan dữ liệu và trạng thái mô phỏng.
- Trang mô phỏng giao thông.
- Trang đánh giá hiệu quả phát hiện.

Trong giai đoạn đầu, frontend có thể sử dụng dữ liệu mẫu và hoạt động độc lập với backend. Dữ liệu mẫu cần được phân biệt rõ với kết quả do thuật toán California tạo ra.

Việc kết nối frontend với backend thông qua API có thể được triển khai ở giai đoạn tích hợp tiếp theo.

## 4. Công nghệ sử dụng

| Thành phần           | Công nghệ             | Mục đích                                    |
| -------------------- | --------------------- | ------------------------------------------- |
| Ngôn ngữ lập trình   | Python                | Triển khai thuật toán, mô phỏng và đánh giá |
| Thuật toán phát hiện | California Algorithm  | Phát hiện dấu hiệu sự cố giao thông         |
| Frontend             | HTML, CSS, JavaScript | Xây dựng giao diện web                      |
| Kiểm thử             | pytest                | Kiểm thử thuật toán                         |
| Quản lý mã nguồn     | Git, GitHub           | Quản lý phiên bản và phối hợp nhóm          |
| Dữ liệu              | Dữ liệu mô phỏng      | Kiểm tra và đánh giá chương trình           |

## 5. Cấu trúc thư mục

```text
ITSgrXM/
├── README.md
├── requirements.txt
├── .gitignore
│
├── fe/
│   ├── index.html
│   ├── README.md
│   ├── assets/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   ├── app.js
│   │   │   ├── data.js
│   │   │   └── charts.js
│   │   └── images/
│   └── pages/
│       ├── dashboard.html
│       ├── simulation.html
│       └── evaluation.html
│
├── data/
│   └── README.md
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── california.py
│   ├── simulator.py
│   └── metrics.py
│
├── tests/
│   └── test_california.py
│
└── docs/
    ├── algorithm.md
    ├── system_design.md
    └── evaluation.md
```

### Mô tả các thành phần

| File/thư mục               | Chức năng                                                 |
| -------------------------- | --------------------------------------------------------- |
| `src/main.py`              | Điều phối luồng chạy chính của chương trình               |
| `src/california.py`        | Triển khai thuật toán California                          |
| `src/simulator.py`         | Tạo dữ liệu giao thông mô phỏng                           |
| `src/metrics.py`           | Tính toán các chỉ số đánh giá                             |
| `tests/test_california.py` | Kiểm thử thuật toán California                            |
| `data/`                    | Chứa tài liệu và dữ liệu phục vụ mô phỏng nếu cần lưu trữ |
| `docs/algorithm.md`        | Mô tả thuật toán và các điều kiện phát hiện               |
| `docs/system_design.md`    | Mô tả kiến trúc và cách các module phối hợp               |
| `docs/evaluation.md`       | Mô tả công thức và phương pháp đánh giá                   |
| `fe/`                      | Chứa mã nguồn frontend                                    |
| `requirements.txt`         | Khai báo các thư viện Python cần thiết                    |

## 6. Kiến trúc và luồng hoạt động

### 6.1. Luồng xử lý backend

```text
Khởi chạy chương trình
        |
        v
     main.py
        |
        v
   simulator.py
Tạo dữ liệu giao thông
        |
        v
   california.py
Phát hiện sự cố
        |
        v
    metrics.py
Đánh giá kết quả
        |
        v
Hiển thị kết quả trên Terminal
```

`main.py` đóng vai trò điều phối các module. Mỗi module chịu trách nhiệm xử lý một phần công việc riêng biệt.

### 6.2. Luồng hoạt động frontend

Trong giai đoạn frontend hoạt động độc lập:

```text
Người dùng
    |
    v
Giao diện HTML/CSS/JavaScript
    |
    v
Đọc dữ liệu mẫu
    |
    v
Hiển thị bảng, thông tin mô phỏng
và các chỉ số đánh giá mẫu
```

Khi API được triển khai và tích hợp, frontend có thể lấy dữ liệu từ backend thay vì sử dụng dữ liệu mẫu.

## 7. Cài đặt

### 7.1. Yêu cầu hệ thống

- Python 3.
- pip.
- Trình duyệt web hiện đại.
- Git nếu muốn sao chép repository.

### 7.2. Sao chép dự án

```bash
git clone https://github.com/xuan-mai-pyn/ITSgrXM.git
cd ITSgrXM
```

### 7.3. Tạo môi trường ảo

```bash
python -m venv .venv
```

Kích hoạt môi trường trên Windows:

```bash
.venv\Scripts\activate
```

Trên macOS hoặc Linux:

```bash
source .venv/bin/activate
```

### 7.4. Cài đặt thư viện

```bash
python -m pip install -r requirements.txt
```

Các thư viện cần thiết được quản lý trong `requirements.txt`.

## 8. Cách chạy chương trình

### 8.1. Chạy backend

Từ thư mục gốc của dự án, chạy:

```bash
python -m src.main
```

Khi các module đã được triển khai và tích hợp đầy đủ, chương trình sẽ thực hiện các bước:

1. Tạo dữ liệu giao thông mô phỏng.
2. Phân tích dữ liệu bằng thuật toán California.
3. Đánh giá kết quả phát hiện.
4. Hiển thị thông tin và các chỉ số trên Terminal.

### 8.2. Chạy kiểm thử

```bash
python -m pytest -q
```

Các bài kiểm thử được sử dụng để đánh giá hoạt động của thuật toán trong những tình huống giao thông khác nhau.

Kết quả kiểm thử cần được xác nhận bằng cách chạy lệnh trên môi trường thực tế.

### 8.3. Mở frontend

Mở file sau bằng trình duyệt:

```text
fe/index.html
```

Frontend sử dụng HTML, CSS và JavaScript thuần. Nếu các trang sử dụng dữ liệu mẫu, thông tin hiển thị chỉ có mục đích minh họa, không đại diện cho kết quả chạy backend.

## 9. Đánh giá hiệu quả

Việc đánh giá tập trung vào khả năng phát hiện sự cố của thuật toán California.

Các nội dung đánh giá có thể bao gồm:

- Tỷ lệ phát hiện sự cố.
- Tỷ lệ báo động giả.
- Thời gian phát hiện trung bình.
- Khả năng phân biệt trạng thái giao thông bình thường và trạng thái có sự cố.

Kết quả cần được tính từ dữ liệu mô phỏng, nhãn sự cố và đầu ra của thuật toán. Phương pháp đánh giá chi tiết được trình bày trong `docs/evaluation.md`.

## 10. Giới hạn của dự án

- Dữ liệu giao thông mô phỏng không đại diện cho toàn bộ điều kiện giao thông thực tế.
- Hiệu quả phát hiện phụ thuộc vào dữ liệu, kịch bản mô phỏng và tham số thuật toán.
- Frontend cơ bản có thể chưa được kết nối với backend.
- Dữ liệu mẫu trên giao diện không được xem là kết quả thực nghiệm của thuật toán.
- Việc ứng dụng vào hệ thống giao thông thực tế cần được kiểm thử thêm bằng dữ liệu thực phù hợp.

## 11. Hướng phát triển

- Hoàn thiện và kiểm thử thuật toán California.
- Mở rộng các kịch bản mô phỏng giao thông.
- Cải thiện phương pháp đánh giá hiệu quả phát hiện.
- Hoàn thiện dashboard và các biểu đồ trực quan.
- Xây dựng API để kết nối frontend với backend.
- Kiểm tra thuật toán với dữ liệu giao thông thực tế khi có nguồn dữ liệu phù hợp.

## 12. Tài liệu dự án

Các tài liệu kỹ thuật được lưu trong thư mục `docs/`:

- `algorithm.md`: Nguyên lý và điều kiện của thuật toán California.
- `system_design.md`: Thiết kế hệ thống và luồng phối hợp giữa các module.
- `evaluation.md`: Công thức, phương pháp và kết quả đánh giá.

## 13. Kết luận

ITSgrXM là dự án demo phục vụ học tập và nghiên cứu về phát hiện sự cố giao thông trong lĩnh vực Hệ thống giao thông thông minh.

Dự án lấy thuật toán California làm chức năng trọng tâm, kết hợp dữ liệu giao thông mô phỏng, các chỉ số đánh giá và giao diện web cơ bản. Thiết kế theo module giúp hệ thống thuận tiện cho việc kiểm thử, phát triển và tích hợp trong các giai đoạn tiếp theo.

Xem hướng dẫn request/response và các tùy chọn tại [docs/api.md](docs/api.md). Các tài liệu khác:

- [Thuật toán](docs/algorithm.md)
- [Thiết kế hệ thống](docs/system_design.md)
- [Đánh giá kết quả](docs/evaluation.md)
- [Dữ liệu mô phỏng](data/README.md)
- [Frontend](fe/README.md)
