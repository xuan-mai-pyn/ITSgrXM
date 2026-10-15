# ITSgrXM – California Algorithm for Traffic Incident Detection

## 1. Giới thiệu dự án

ITSgrXM là dự án học tập thuộc lĩnh vực Hệ thống giao thông thông minh (Intelligent Transportation Systems – ITS), tập trung nghiên cứu và mô phỏng thuật toán California trong bài toán phát hiện sự cố giao thông.

Sự cố giao thông có thể làm giảm năng lực thông hành của đường, gây ùn tắc và kéo dài thời gian di chuyển. Vì vậy, việc phát hiện sự cố sớm có ý nghĩa quan trọng trong quản lý giao thông và hỗ trợ cơ quan chức năng đưa ra phương án xử lý kịp thời.

Dự án hướng đến việc xây dựng một chương trình Python có khả năng:

- Mô phỏng dữ liệu giao thông trong điều kiện bình thường và khi xảy ra sự cố.
- Sử dụng thuật toán California để phân tích dữ liệu và phát hiện dấu hiệu bất thường.
- Đánh giá hiệu quả phát hiện thông qua các chỉ số phù hợp.
- Kiểm thử thuật toán và trình bày kết quả thực nghiệm.

Đây là dự án phục vụ học tập và nghiên cứu, không phải hệ thống phát hiện sự cố đang vận hành trên đường giao thông thực tế.

## 2. Mục tiêu

Dự án tập trung vào các mục tiêu sau:

1. Tìm hiểu nguyên lý hoạt động của thuật toán California trong phát hiện sự cố giao thông.
2. Xây dựng dữ liệu mô phỏng để kiểm tra hoạt động của thuật toán.
3. Tổ chức chương trình theo các module riêng biệt nhằm thuận tiện cho việc phát triển và bảo trì.
4. Đánh giá khả năng phát hiện sự cố thông qua các chỉ số được xác định từ tài liệu môn học.
5. Kiểm thử chương trình, phân tích kết quả và rút ra nhận xét về hiệu quả của thuật toán.

## 3. Nguyên lý hoạt động

Chương trình được thiết kế theo quy trình tổng quát:

Mô phỏng dữ liệu → Phát hiện sự cố → Đánh giá kết quả → Xuất báo cáo

### 3.1. Mô phỏng dữ liệu

Module mô phỏng tạo dữ liệu giao thông phục vụ thử nghiệm, bao gồm các tình huống bình thường và tình huống có sự cố.

Dữ liệu dự kiến bao gồm thông tin occupancy tại hai trạm quan trắc và nhãn tham chiếu về trạng thái sự cố để phục vụ đánh giá.

### 3.2. Phát hiện sự cố

Thuật toán California phân tích dữ liệu từ các trạm quan trắc để xác định dấu hiệu bất thường trong trạng thái giao thông.

Các ngưỡng phát hiện, điều kiện xác nhận và điều kiện kết thúc sự cố cần được xác định theo tài liệu môn học trước khi triển khai.

### 3.3. Đánh giá hiệu quả

Kết quả phát hiện được so sánh với nhãn tham chiếu của dữ liệu mô phỏng để đánh giá hiệu quả thuật toán.

Các chỉ số cụ thể và công thức tính sẽ được xác định theo tài liệu môn học và phương pháp thực nghiệm của nhóm.

## 4. Công nghệ sử dụng

| Công nghệ          | Mục đích                          |
| ------------------ | --------------------------------- |
| Python 3.13.x      | Ngôn ngữ lập trình chính          |
| Git                | Quản lý phiên bản mã nguồn        |
| GitHub             | Lưu trữ mã nguồn và phối hợp nhóm |
| Visual Studio Code | Môi trường phát triển             |
| pytest             | Hỗ trợ kiểm thử tự động           |

Các thư viện bổ sung, nếu có, được khai báo trong file `requirements.txt`.

## 5. Cấu trúc dự án

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

### Mô tả các thư mục và file

**`README.md`**

Tài liệu giới thiệu dự án, hướng dẫn cài đặt, cách sử dụng và mô tả cấu trúc chương trình.

**`requirements.txt`**

Danh sách các thư viện Python cần thiết để cài đặt và chạy dự án.

**`.gitignore`**

Khai báo các file và thư mục không cần đưa lên GitHub, chẳng hạn môi trường ảo và file bộ nhớ đệm Python.

**`data/`**

Chứa tài liệu liên quan đến dữ liệu sử dụng trong dự án. File `data/README.md` mô tả định dạng, nguồn gốc và cách tạo dữ liệu mô phỏng.

**`src/`**

Chứa mã nguồn chính của chương trình:

- `main.py`: Điểm khởi chạy và điều phối các module.
- `california.py`: Triển khai thuật toán California.
- `simulator.py`: Tạo dữ liệu giao thông mô phỏng.
- `metrics.py`: Tính toán các chỉ số đánh giá.
- `__init__.py`: Khai báo package Python.

**`tests/`**

Chứa các bài kiểm thử. File `test_california.py` dùng để kiểm tra hoạt động của thuật toán.

**`docs/`**

Chứa tài liệu kỹ thuật:

- `algorithm.md`: Nguyên lý và các bước của thuật toán California.
- `system_design.md`: Thiết kế tổng thể và cách các module phối hợp.
- `evaluation.md`: Phương pháp, chỉ số và kết quả đánh giá thực nghiệm.

## 6. Yêu cầu hệ thống

Trước khi sử dụng dự án, cần chuẩn bị:

- Python phiên bản 3.13.x.
- Git.
- Visual Studio Code hoặc một trình soạn thảo Python tương đương.
- Terminal để chạy các lệnh cài đặt và thực thi chương trình.

Hướng dẫn bên dưới sử dụng Git Bash trên Windows. Với macOS/Linux, có thể sử dụng Terminal và điều chỉnh lệnh kích hoạt môi trường ảo theo hệ điều hành.

## 7. Cài đặt dự án

### Bước 1. Clone repository

Mở Terminal tại thư mục muốn lưu dự án và chạy:

```bash
git clone https://github.com/xuan-mai-pyn/ITSgrXM.git
cd ITSgrXM
```

### Bước 2. Tạo môi trường ảo

Windows:

```bash
python -m venv .venv
```

macOS/Linux:

```bash
python3 -m venv .venv
```

### Bước 3. Kích hoạt môi trường ảo

Windows – Git Bash:

```bash
source .venv/Scripts/activate
```

Windows – PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Sau khi kích hoạt thành công, Terminal thường hiển thị `(.venv)` ở đầu dòng.

### Bước 4. Cài đặt thư viện

Khi môi trường ảo đã được kích hoạt, chạy:

```bash
python -m pip install -r requirements.txt
```

### Bước 5. Kiểm tra môi trường

Kiểm tra phiên bản Python:

```bash
python --version
```

Kiểm tra trạng thái repository:

```bash
git status
```

## 8. Chạy chương trình

Sau khi các module đã được triển khai và tích hợp, có thể chạy chương trình chính từ thư mục gốc:

```bash
python -m src.main
```

Lệnh trên khởi chạy module `main.py` theo cấu trúc package của dự án.

Lưu ý: Chương trình chỉ hoạt động đầy đủ khi các module cần thiết đã được triển khai. Nếu dự án vẫn đang trong giai đoạn xây dựng, kết quả chạy có thể chưa đầy đủ.

## 9. Kiểm thử

Dự án sử dụng `pytest` để hỗ trợ kiểm thử.

Chạy toàn bộ bài kiểm thử từ thư mục gốc:

```bash
python -m pytest -v
```

Các bài kiểm thử dự kiến tập trung vào:

- Kiểm tra thuật toán với dữ liệu bình thường.
- Kiểm tra thuật toán với dữ liệu có sự cố.
- Kiểm tra các trường hợp biên.
- Kiểm tra kết quả đầu ra theo điều kiện đã xác định.

Kết quả kiểm thử cần được ghi nhận sau khi thực hiện thực tế.

## 10. Đánh giá hiệu quả

Việc đánh giá nhằm xác định khả năng phát hiện sự cố của thuật toán trên dữ liệu thử nghiệm.

Nhóm sẽ lựa chọn và áp dụng các chỉ số phù hợp theo tài liệu môn học, có thể bao gồm:

- Detection Rate (DR): Tỷ lệ phát hiện sự cố.
- False Alarm Rate (FAR): Tỷ lệ cảnh báo sai.
- Mean Time to Detect (MTTD): Thời gian phát hiện trung bình.

Định nghĩa, công thức và cách xác định các trường hợp phát hiện đúng, bỏ sót hoặc cảnh báo sai cần được thống nhất trước khi tính toán.

Các kết quả thực nghiệm và nhận xét sẽ được trình bày trong `docs/evaluation.md` sau khi chương trình chạy thành công.

## 11. Quy trình làm việc nhóm

Dự án được phát triển bằng Git và GitHub để các thành viên có thể làm việc trên các nhánh riêng.

Các nhánh được phân chia như sau:

| Nhánh    | Thành viên           |
| -------- | -------------------- |
| `XMai`   | Mai                  |
| `QCuong` | Cường                |
| `MHieu`  | Hiếu                 |
| `DKhang` | Khang                |
| `MKhoa`  | Khoa                 |
| `main`   | Nhánh tích hợp chính |

Quy trình làm việc đề xuất:

1. Cập nhật thông tin nhánh từ repository.
2. Chuyển sang nhánh cá nhân.
3. Chỉnh sửa các file được phân công.
4. Kiểm tra thay đổi trước khi commit.
5. Commit và push lên nhánh cá nhân.
6. Tạo Pull Request để đề xuất tích hợp vào `main`.
7. Kiểm tra và xử lý xung đột nếu có.

Ví dụ, thành viên làm việc trên nhánh `XMai` có thể sử dụng:

```bash
git switch XMai
git status
```

Sau khi chỉnh sửa và kiểm tra các file của mình:

```bash
git add .
git commit -m "Describe your changes"
git push
```

Nội dung commit nên ngắn gọn và thể hiện rõ thay đổi đã thực hiện.

## 12. Nguyên tắc phát triển

- Tuân thủ cấu trúc thư mục đã thống nhất.
- Đối chiếu thuật toán và công thức với tài liệu môn học.
- Thống nhất định dạng dữ liệu và giao diện hàm giữa các module.
- Không tự tạo kết quả thực nghiệm khi chưa chạy chương trình.
- Không đưa môi trường ảo `.venv` hoặc file tạm lên GitHub.
- Kiểm tra chương trình và bài kiểm thử trước khi tích hợp vào nhánh `main`.
- Cập nhật tài liệu khi có thay đổi về cách sử dụng hoặc thiết kế.

## 13. Giới hạn của dự án

Đây là dự án học tập sử dụng dữ liệu mô phỏng để nghiên cứu thuật toán phát hiện sự cố giao thông.

Kết quả thử nghiệm trên dữ liệu mô phỏng không đồng nghĩa với hiệu quả tương tự trong môi trường giao thông thực tế. Việc triển khai thực tế cần dữ liệu phù hợp, hiệu chỉnh ngưỡng và đánh giá thêm trong các điều kiện vận hành khác nhau.

## 14. Tác giả và thông tin dự án

Repository: https://github.com/xuan-mai-pyn/ITSgrXM

Lĩnh vực: Intelligent Transportation Systems (ITS)

Chủ đề: Traffic Incident Detection using the California Algorithm

Ngôn ngữ lập trình chính
: Python

Dự án được thực hiện với mục đích học tập, nghiên cứu thuật toán và thực hành phát triển phần mềm theo nhóm.
