# California Traffic Incident Detection System

## 1. Giới thiệu

ITSgrXM là hệ thống demo học tập về phát hiện sự cố giao thông bằng thuật toán California trong lĩnh vực Hệ thống giao thông thông minh (Intelligent Transportation Systems – ITS). Repository có hai phần riêng:

- **Backend:** Python tạo dữ liệu giao thông mô phỏng, áp dụng logic phát hiện trong `src/california.py`, in kết quả ra Terminal hoặc cung cấp REST API qua `src/api.py`.
- **Frontend:** các trang HTML, CSS và JavaScript thuần được tổ chức trong `fe/`; hiện chưa gọi REST API.

Dự án phục vụ học tập, nghiên cứu và thuyết trình; không phải hệ thống giám sát giao thông thực tế. Dữ liệu mô phỏng và kết quả chạy demo không phải dữ liệu đo thực tế hay bằng chứng đánh giá độ chính xác.

## 2. Mục tiêu và phạm vi hiện tại

### Backend

- Các module Python tách riêng phần chạy demo, thuật toán và mô phỏng dữ liệu.
- `src/simulator.py` tạo ba kịch bản có seed cố định: giao thông bình thường, có sự cố và ùn tắc tự nhiên; có thể xuất dữ liệu CSV.
- `src/california.py` có lớp `CaliforniaAlgorithm`: so sánh chênh lệch occupancy tuyệt đối, chênh lệch tương đối và occupancy hạ lưu; yêu cầu điều kiện đúng liên tiếp theo tham số `persistence`.
- `src/main.py` chạy các kịch bản mô phỏng, gọi thuật toán và in một số bản ghi cùng các chu kỳ phát hiện.
- `src/metrics.py` ghép khoảng sự cố với thời điểm cảnh báo và tính DR, FAR, TTD cùng TP/FN/FP và cảnh báo lặp; `src/main.py` chưa gọi module này.
- `src/api.py` cung cấp REST API riêng cho health, mô phỏng/phát hiện, đánh giá và Dashboard. API không thay thế `src/main.py`.
- `tests/test_california.py` có các kiểm tra cho một hàm trợ giúp tự định nghĩa trong tệp test; các kiểm tra này chưa gọi `CaliforniaAlgorithm` trong `src/california.py`.

Các ngưỡng mặc định trong mã thuật toán là S1 = 10, S2 = 0.20, S3 = 20 và persistence = 2. Cần xác minh các công thức, ngưỡng và quy tắc với đặc tả môn học trước khi coi đây là triển khai đúng chuẩn California: [docs/algorithm.md](docs/algorithm.md) mô tả điều kiện theo TH1/TH2/TH3, khác với tên và chi tiết điều kiện trong mã. Vì vậy, không xem kết quả demo là xác nhận thuật toán đã được kiểm chứng.

### Frontend

Frontend trong `fe/` có trang chính, Dashboard, Simulation và Evaluation cùng CSS/JavaScript thuần. Frontend chưa tự gọi API; có thể tích hợp với `src/api.py` bằng HTTP. Dữ liệu hiển thị hiện tại phía Frontend vẫn độc lập với Backend.

## 3. Nguyên lý và luồng hoạt động

### Luồng Backend

```text
Kịch bản mô phỏng
    → src.simulator.generate_all_scenarios()
    → src.california.CaliforniaAlgorithm.evaluate()
    → in chu kỳ phát hiện ra Terminal
```

`src.main` hiện chưa dùng nhãn `incident` để tính metric. REST API có thể chuyển nhãn mô phỏng thành khoảng sự cố, lấy các thời điểm cảnh báo và gọi `metrics.py`.

### Luồng API

```text
HTTP client → src.api → simulator → CaliforniaAlgorithm → metrics
                         └──────────────→ kết quả JSON
```

`src.api` là ứng dụng riêng; `python -m src.main` tiếp tục chạy demo terminal.
Dashboard chỉ phản ánh kết quả API gần nhất trong bộ nhớ tiến trình và chưa có
lưu trữ bền vững.

### Luồng Frontend

```text
Trình duyệt → fe/ (hiện độc lập) → [HTTP tích hợp chưa triển khai] → src.api
```

Frontend cần được cấu hình để gọi API; hiện không có trao đổi dữ liệu tự động.

## 4. Công nghệ

### Backend

- Python 3.10 trở lên (mã nguồn sử dụng cú pháp tương thích Python hiện đại).
- Thư viện chuẩn Python cho mô phỏng và xử lý; FastAPI và Uvicorn cho REST API.
- `pytest` và `httpx` được khai báo để chạy test API bằng FastAPI TestClient.

### Frontend

- HTML5, CSS3 và JavaScript thuần.
- Biểu đồ frontend được dựng bằng SVG thuần, không cần thư viện ngoài.

## 5. Cấu trúc thư mục

```text
ITSgrXM/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── README.md
│   ├── edge_congestion.csv
│   ├── incident.csv
│   └── normal.csv
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── api.py
│   ├── california.py
│   ├── simulator.py
│   └── metrics.py
├── tests/
│   └── test_california.py
├── docs/
│   ├── algorithm.md
│   ├── api.md
│   ├── system_design.md
│   └── evaluation.md
└── fe/
    ├── README.md
    ├── index.html
    ├── assets/
    │   ├── css/
    │   │   └── style.css
    │   ├── images/
    │   │   └── .gitkeep
    │   └── js/
    │       ├── app.js
    │       ├── charts.js
    │       └── data.js
    └── pages/
        ├── dashboard.html
        ├── evaluation.html
        └── simulation.html
```

- `src/`: mã nguồn Backend; `main.py` điều phối demo terminal, `api.py` cung cấp REST API, `simulator.py` tạo dữ liệu, `california.py` chứa logic phát hiện, `metrics.py` tính các chỉ số đánh giá.
- `data/`: ba tệp CSV kịch bản mô phỏng và tài liệu schema/giả định dữ liệu. Đây không phải dữ liệu đo từ giao thông thực tế.
- `tests/`: kiểm thử thuật toán cũ và kiểm thử REST API; test thuật toán hiện có chưa gọi trực tiếp class trong Backend.
- `docs/`: tài liệu thuật toán, REST API, thiết kế hệ thống và đánh giá.
- `fe/`: giao diện tĩnh độc lập, hiện chưa kết nối API.
- `requirements.txt`: danh sách dependencies của API và test. Nội dung ghi chú dự án cũ được giữ lại dưới dạng comment.

## 6. Cài đặt và chạy Backend

Tại thư mục gốc repository, tạo môi trường ảo:

```bash
python -m venv .venv
```

Kích hoạt trên Windows bằng Git Bash:

```bash
source .venv/Scripts/activate
```

Trên macOS/Linux:

```bash
source .venv/bin/activate
```

Cài các dependencies cho API và kiểm thử:

```powershell
python -m pip install -r requirements.txt
```

Chạy demo từ thư mục gốc:

```bash
python -m src.main
```

Chương trình tạo ba kịch bản mô phỏng trong bộ nhớ, hiển thị một số bản ghi và in chu kỳ mà thuật toán hiện tại báo phát hiện. Với seed và tham số mặc định đang có, lần chạy kiểm tra cho thấy kịch bản incident được báo tại chu kỳ 42; đây chỉ là đầu ra của dữ liệu mô phỏng, không phải kết quả thực nghiệm hoặc đánh giá chất lượng. Chương trình không tính DR, FAR hay TTD.

Chạy REST API riêng từ thư mục gốc:

```powershell
python -m uvicorn src.api:app --reload
```

API docs: [docs/api.md](docs/api.md). Swagger UI mặc định tại
`http://127.0.0.1:8000/docs`.

Để chạy riêng module tạo và lưu lại các CSV trong `data/`:

```bash
python -m src.simulator
```

## 7. Chạy kiểm thử

Sau khi cài dependencies, chạy từ thư mục gốc:

```bash
python -m pytest
```

Lưu ý: các test trong `tests/test_california.py` kiểm tra hàm trợ giúp tự định nghĩa, không kiểm tra trực tiếp lớp thuật toán Backend. Test API kiểm tra việc API gọi đúng lớp và trả kết quả theo module hiện có; điều đó không thay thế xác minh thuật toán với đặc tả môn học.

## 8. Mở Frontend

Frontend là các tệp tĩnh và không cần chạy Backend. Từ thư mục `fe/`, có thể mở `index.html` bằng trình duyệt. Các trang có điều hướng và giao diện demo, nhưng hiện chưa gọi API.

Nếu cần mở qua HTTP server, chạy lệnh tại chính thư mục `fe/`:

```bash
python -m http.server 8000
```

Sau đó truy cập [http://localhost:8000](http://localhost:8000). Không cần Node.js, `npm install` hoặc khởi động Backend để mở Frontend.

## 9. Tài liệu liên quan

- [Tài liệu thuật toán](docs/algorithm.md)
- [Tài liệu REST API](docs/api.md)
- [Thiết kế hệ thống](docs/system_design.md)
- [Kế hoạch đánh giá](docs/evaluation.md)
- [Hướng dẫn và schema dữ liệu](data/README.md)
- [Ghi chú Frontend](fe/README.md)

## 10. Hướng phát triển tiếp theo

1. Đối chiếu và thống nhất đặc tả thuật toán California, ngưỡng và điều kiện xác nhận với tài liệu môn học.
2. Bổ sung kiểm thử trực tiếp `CaliforniaAlgorithm`, bao gồm dữ liệu bình thường, sự cố, ùn tắc tự nhiên và đầu vào biên.
3. Đánh giá API trên dữ liệu phù hợp và xác nhận định nghĩa DR, FAR, TTD với nhóm.
4. Tích hợp Frontend với REST API; thay dữ liệu minh họa trên Dashboard/Simulation/Evaluation bằng response API có nguồn gốc rõ ràng.

## 11. Giới hạn sử dụng

- Dữ liệu CSV và dữ liệu sinh khi chạy đều là mô phỏng, không đại diện cho điều kiện giao thông thực tế.
- Các kết quả API hiện chỉ dựa trên dữ liệu mô phỏng hoặc dữ liệu đánh giá do client gửi; chưa có kết quả thực nghiệm trên dữ liệu giao thông thực.
- Logic trong `california.py` chưa được xác minh với tài liệu đặc tả; các ngưỡng mặc định không nên được xem là ngưỡng vận hành đã được chứng thực.
- Frontend chưa tự gọi REST API; Dashboard API chỉ lưu tạm kết quả gần nhất trong bộ nhớ tiến trình.
- Dự án chỉ phục vụ demo, học tập và nghiên cứu; không dùng để giám sát giao thông thực tế hoặc hỗ trợ quyết định vận hành.
