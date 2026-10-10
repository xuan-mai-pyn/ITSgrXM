# ITSgrXM – Demo thuật toán California phát hiện sự cố giao thông

## 1. Giới thiệu

ITSgrXM là dự án xây dựng ứng dụng demo thuật toán California trong bài toán phát hiện sự cố giao thông thuộc lĩnh vực Hệ thống giao thông thông minh (Intelligent Transportation Systems – ITS).

Dự án mô phỏng quá trình tiếp nhận dữ liệu giao thông, xử lý dữ liệu bằng thuật toán California và trả về kết quả nhận diện trạng thái giao thông thông qua giao diện web.

Hệ thống được xây dựng theo mô hình Frontend – Backend, trong đó giao diện người dùng đảm nhiệm việc nhập và hiển thị dữ liệu, còn Backend thực hiện xử lý và chạy thuật toán phát hiện sự cố.

## 2. Mục tiêu dự án

- Tìm hiểu và minh họa nguyên lý hoạt động của thuật toán California.
- Xây dựng giao diện web đơn giản để tương tác với hệ thống.
- Xây dựng Backend tiếp nhận và xử lý dữ liệu giao thông.
- Kết nối Frontend với Backend để thực hiện quá trình phát hiện sự cố.
- Hiển thị kết quả xử lý nhằm giúp người dùng hiểu cách thuật toán nhận biết trạng thái giao thông bất thường.

## 3. Chức năng chính

### 3.1. Frontend (FE)

- Cung cấp giao diện tương tác với người dùng.
- Cho phép gửi dữ liệu đầu vào theo chức năng đã triển khai.
- Gửi yêu cầu xử lý đến Backend.
- Hiển thị kết quả do Backend trả về.

### 3.2. Backend (BE)

- Tiếp nhận yêu cầu từ Frontend.
- Xử lý dữ liệu đầu vào.
- Thực thi thuật toán California theo các điều kiện được cấu hình.
- Trả kết quả xử lý về Frontend.

### 3.3. Thuật toán California

Thuật toán California được sử dụng để minh họa việc phát hiện trạng thái giao thông bất thường dựa trên các thông số giao thông và điều kiện ngưỡng.

Về nguyên lý tổng quát, hệ thống kiểm tra dữ liệu giao thông, so sánh với các điều kiện phát hiện đã thiết lập và đưa ra kết quả tương ứng.

Các thông số đầu vào, giá trị ngưỡng và điều kiện phát hiện cụ thể phụ thuộc vào phần cài đặt thực tế của thuật toán trong dự án.

## 4. Công nghệ và kiến trúc hệ thống

Dự án sử dụng kiến trúc Frontend – Backend:

```text
+---------------------------+
|         Frontend          |
|    Giao diện người dùng   |
+-------------+-------------+
              |
              | Gửi yêu cầu
              v
+---------------------------+
|          Backend          |
| Tiếp nhận và xử lý dữ liệu|
+-------------+-------------+
              |
              v
+---------------------------+
|    Thuật toán California  |
|   Phát hiện bất thường    |
+-------------+-------------+
              |
              | Trả kết quả
              v
+---------------------------+
|         Frontend          |
|     Hiển thị kết quả      |
+---------------------------+
```

Công nghệ và framework cụ thể của FE, BE sẽ được cập nhật theo các thư viện thực tế trong repository.

## 5. Quy trình hoạt động

1. Người dùng truy cập giao diện Frontend.
2. Người dùng nhập hoặc lựa chọn dữ liệu giao thông theo chức năng được hỗ trợ.
3. Frontend gửi dữ liệu đến Backend.
4. Backend tiếp nhận và xử lý dữ liệu đầu vào.
5. Thuật toán California kiểm tra dữ liệu theo các điều kiện đã cấu hình.
6. Backend trả kết quả phát hiện về Frontend.
7. Frontend hiển thị kết quả cho người dùng.

## 6. Hướng dẫn cài đặt và sử dụng

### 6.1. Yêu cầu hệ thống

Cần chuẩn bị:

- Git để tải mã nguồn từ GitHub.
- Môi trường chạy phù hợp với công nghệ được sử dụng trong dự án.
- Các thư viện và gói phụ thuộc của Frontend và Backend.

### 6.2. Clone project về máy

Mở Terminal, CMD, PowerShell hoặc Git Bash tại thư mục muốn lưu project.

Ví dụ, muốn lưu project tại `D:\Projects`, hãy mở Terminal tại thư mục đó rồi chạy:

```bash
git clone https://github.com/xuan-mai-pyn/ITSgrXM.git
```

Di chuyển vào thư mục project:

```bash
cd ITSgrXM
```

Kiểm tra trạng thái Git:

```bash
git status
```

Nếu Git hiển thị nhánh hiện tại và trạng thái làm việc, bạn có thể tiếp tục các bước cài đặt.

### 6.3. Mở project bằng VS Code

Nếu đã cài Visual Studio Code và lệnh `code` hoạt động, chạy:

```bash
code .
```

Có thể mở trực tiếp thư mục `ITSgrXM` bằng chức năng **File → Open Folder** trong VS Code.

### 6.4. Cài đặt các thư viện

Cài đặt các thư viện cần thiết theo cấu hình của từng phần:

- Frontend: dựa trên file quản lý gói và hướng dẫn của framework FE.
- Backend: dựa trên file khai báo thư viện và hướng dẫn của môi trường BE.

Tên framework, lệnh cài đặt và lệnh chạy cụ thể cần được bổ sung theo cấu trúc thực tế của dự án.

### 6.5. Khởi chạy hệ thống

Khởi động Backend và Frontend theo hướng dẫn tương ứng của từng phần.

Sau khi hai phần hoạt động, truy cập địa chỉ Frontend được hiển thị trong Terminal để sử dụng giao diện demo.

## 7. Cấu trúc thư mục

Cấu trúc thư mục dưới đây mang tính minh họa. Tên thư mục cần được điều chỉnh theo repository thực tế.

```text
ITSgrXM/
├── frontend/       # Mã nguồn giao diện
├── backend/        # Mã nguồn xử lý và thuật toán
└── README.md       # Tài liệu dự án
```

## 8. Phạm vi và hạn chế

Đây là dự án demo phục vụ mục đích học tập và minh họa thuật toán phát hiện sự cố giao thông.

Kết quả phụ thuộc vào dữ liệu đầu vào, các ngưỡng phát hiện và cách thuật toán được triển khai. Hệ thống chưa được mặc định là giải pháp có thể triển khai trực tiếp trong môi trường giao thông thực tế.

Để ứng dụng thực tế, cần đánh giá thuật toán trên dữ liệu giao thông phù hợp, hiệu chỉnh ngưỡng và kiểm tra độ chính xác của kết quả.

## 9. Hướng phát triển

- Bổ sung dữ liệu giao thông thực tế hoặc dữ liệu mô phỏng đa dạng hơn.
- Cải thiện cách hiển thị kết quả phát hiện.
- Cho phép cấu hình các ngưỡng phát hiện.
- Xây dựng bộ dữ liệu kiểm thử để đánh giá thuật toán.
- So sánh thuật toán California với các phương pháp phát hiện sự cố khác.
- Nâng cao khả năng xử lý lỗi và kết nối giữa Frontend và Backend.
