# California Traffic Incident Detection System

## 1. Giới thiệu

ITSgrXM là hệ thống demo học tập về phát hiện sự cố giao thông bằng thuật toán California trong lĩnh vực Hệ thống giao thông thông minh (Intelligent Transportation Systems – ITS). Repository có hai phần riêng:

- **Backend:** Python tạo dữ liệu giao thông mô phỏng, áp dụng logic phát hiện trong `src/california.py` và in kết quả ra Terminal.
- **Frontend:** các tệp HTML, CSS và JavaScript thuần được tổ chức trong `fe/`. Hiện các tệp giao diện chính còn trống nên chưa có trang hoặc tương tác hoạt động.

Dự án phục vụ học tập, nghiên cứu và thuyết trình; không phải hệ thống giám sát giao thông thực tế. Dữ liệu mô phỏng và kết quả chạy demo không phải dữ liệu đo thực tế hay bằng chứng đánh giá độ chính xác.

## 2. Mục tiêu và phạm vi hiện tại

### Backend

- Các module Python tách riêng phần chạy demo, thuật toán và mô phỏng dữ liệu.
- `src/simulator.py` tạo ba kịch bản có seed cố định: giao thông bình thường, có sự cố và ùn tắc tự nhiên; có thể xuất dữ liệu CSV.
- `src/california.py` có lớp `CaliforniaAlgorithm`: so sánh chênh lệch occupancy tuyệt đối, chênh lệch tương đối và occupancy hạ lưu; yêu cầu điều kiện đúng liên tiếp theo tham số `persistence`.
- `src/main.py` chạy các kịch bản mô phỏng, gọi thuật toán và in một số bản ghi cùng các chu kỳ phát hiện.
- `src/metrics.py` hiện chỉ là khung tài liệu; chưa tính DR, FAR hoặc TTD và chưa được gọi bởi chương trình chính.
- `tests/test_california.py` có các kiểm tra cho một hàm trợ giúp tự định nghĩa trong tệp test; các kiểm tra này chưa gọi `CaliforniaAlgorithm` trong `src/california.py`.

Các ngưỡng mặc định trong mã thuật toán là S1 = 10, S2 = 0.20, S3 = 20 và persistence = 2. Cần xác minh các công thức, ngưỡng và quy tắc với đặc tả môn học trước khi coi đây là triển khai đúng chuẩn California: [docs/algorithm.md](docs/algorithm.md) mô tả điều kiện theo TH1/TH2/TH3, khác với tên và chi tiết điều kiện trong mã. Vì vậy, không xem kết quả demo là xác nhận thuật toán đã được kiểm chứng.

### Frontend

Frontend được tách riêng trong `fe/`, không nằm trong `src/`. Tuy nhiên, `index.html`, ba trang trong `fe/pages/`, cùng các tệp CSS và JavaScript hiện đang trống. Vì vậy, trang chính, Dashboard, Simulation và Evaluation mới chỉ có tên/vị trí trong cấu trúc; chưa có bố cục, dữ liệu mẫu, biểu đồ hay hành vi giao diện để mô tả như chức năng đã hoàn tất.

Frontend hiện chạy độc lập theo nghĩa chưa có mã kết nối: không có API, không gọi Backend và không trao đổi dữ liệu với Python. `fe/assets/js/data.js` hiện cũng trống nên chưa có dữ liệu mẫu được triển khai trên giao diện. Nếu sau này bổ sung dữ liệu hiển thị, cần phân biệt rõ dữ liệu mô phỏng với kết quả do Backend tạo ra. Kết quả của `python -m src.main` hiện không được đồng bộ lên Frontend.

## 3. Nguyên lý và luồng hoạt động

### Luồng Backend

```text
Kịch bản mô phỏng
    → src.simulator.generate_all_scenarios()
    → src.california.CaliforniaAlgorithm.evaluate()
    → in chu kỳ phát hiện ra Terminal
```

Trong mã hiện tại, nhãn `incident` được tạo cùng dữ liệu mô phỏng nhưng `src.main` chưa dùng nhãn đó để tính chỉ số đánh giá. `metrics.py` chưa triển khai bước đánh giá.

### Luồng Frontend

```text
Trình duyệt → fe/index.html → các trang dự kiến trong fe/pages/
```

Các tệp trang và tài nguyên frontend hiện trống. Hai luồng chưa liên thông và không có API hoặc cơ chế trao đổi dữ liệu giữa chúng.

## 4. Công nghệ

### Backend

- Python 3.10 trở lên (mã nguồn sử dụng cú pháp tương thích Python hiện đại).
- Thư viện chuẩn Python cho mô phỏng và xử lý; thuật toán cũng không sử dụng thư viện bên ngoài.
- `pytest` được import trong tệp kiểm thử nhưng hiện không được khai báo hợp lệ trong `requirements.txt`.

### Frontend

- HTML5, CSS3 và JavaScript thuần là công nghệ dự kiến theo cấu trúc frontend.
- Hiện chưa có thư viện biểu đồ hoặc thư viện bên ngoài nào được sử dụng; các tệp frontend đang trống.

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
│   ├── california.py
│   ├── simulator.py
│   └── metrics.py
├── tests/
│   └── test_california.py
├── docs/
│   ├── algorithm.md
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

- `src/`: mã nguồn Backend; `main.py` điều phối demo, `simulator.py` tạo dữ liệu, `california.py` chứa logic phát hiện, `metrics.py` là khung dành cho đánh giá.
- `data/`: ba tệp CSV kịch bản mô phỏng và tài liệu schema/giả định dữ liệu. Đây không phải dữ liệu đo từ giao thông thực tế.
- `tests/`: kiểm thử hiện có cho hàm trợ giúp trong tệp test, chưa kiểm thử module thuật toán.
- `docs/`: tài liệu thuật toán, thiết kế hệ thống và kế hoạch đánh giá; cần đối chiếu với tình trạng mã hiện tại.
- `fe/`: các vị trí dành cho giao diện tĩnh độc lập. Các trang, stylesheet và script hiện chưa có nội dung.
- `requirements.txt`: hiện nội dung là ghi chú/phân công dự án, không phải danh sách gói cài đặt hợp lệ; chưa thể dùng tệp này với `pip install -r`.

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

Backend hiện chỉ dùng thư viện chuẩn Python nên không cần cài thêm package để chạy. `requirements.txt` hiện không phải tệp requirements hợp lệ, vì vậy không chạy `pip install -r requirements.txt` cho đến khi nội dung tệp được sửa ở một thay đổi riêng.

Chạy demo từ thư mục gốc:

```bash
python -m src.main
```

Chương trình tạo ba kịch bản mô phỏng trong bộ nhớ, hiển thị một số bản ghi và in chu kỳ mà thuật toán hiện tại báo phát hiện. Với seed và tham số mặc định đang có, lần chạy kiểm tra cho thấy kịch bản incident được báo tại chu kỳ 42; đây chỉ là đầu ra của dữ liệu mô phỏng, không phải kết quả thực nghiệm hoặc đánh giá chất lượng. Chương trình không tính DR, FAR hay TTD.

Để chạy riêng module tạo và lưu lại các CSV trong `data/`:

```bash
python -m src.simulator
```

## 7. Chạy kiểm thử

Kiểm thử dùng `pytest`, nhưng gói này chưa được khai báo trong `requirements.txt`. Nếu môi trường chưa có pytest, có thể cài riêng trong môi trường ảo:

```bash
python -m pip install pytest
```

Sau đó chạy từ thư mục gốc:

```bash
python -m pytest
```

Lưu ý: các test hiện tại kiểm tra hàm trợ giúp trong `tests/test_california.py`, không kiểm tra trực tiếp lớp thuật toán trong Backend. Do đó, kết quả test đạt không chứng minh thuật toán California đã được xác minh.

## 8. Mở Frontend

Frontend là các tệp tĩnh và không cần chạy Backend. Từ thư mục `fe/`, có thể mở `index.html` bằng trình duyệt. Hiện tệp này và các trang giao diện đều trống, nên chưa hiển thị nội dung hoặc cung cấp điều hướng/chức năng sử dụng được.

Nếu cần mở qua HTTP server, chạy lệnh tại chính thư mục `fe/`:

```bash
python -m http.server 8000
```

Sau đó truy cập [http://localhost:8000](http://localhost:8000). Không cần Node.js, `npm install` hoặc khởi động Backend để mở Frontend.

## 9. Tài liệu liên quan

- [Tài liệu thuật toán](docs/algorithm.md)
- [Thiết kế hệ thống](docs/system_design.md)
- [Kế hoạch đánh giá](docs/evaluation.md)
- [Hướng dẫn và schema dữ liệu](data/README.md)
- [Ghi chú Frontend](fe/README.md)

## 10. Hướng phát triển tiếp theo

1. Đối chiếu và thống nhất đặc tả thuật toán California, ngưỡng, điều kiện xác nhận và điều kiện kết thúc; cập nhật tài liệu cho khớp với mã.
2. Bổ sung kiểm thử trực tiếp `CaliforniaAlgorithm`, bao gồm dữ liệu bình thường, sự cố, ùn tắc tự nhiên và đầu vào biên.
3. Hoàn thiện `metrics.py` sau khi thống nhất định nghĩa DR, FAR, TTD và quy tắc đối chiếu nhãn.
4. Xây dựng nội dung và hành vi thật cho trang chủ, Dashboard, Simulation và Evaluation; ghi rõ nguồn dữ liệu hiển thị.
5. Thống nhất định dạng dữ liệu trao đổi và chỉ xây dựng API/kết nối Frontend–Backend trong giai đoạn sau nếu có yêu cầu.

## 11. Giới hạn sử dụng

- Dữ liệu CSV và dữ liệu sinh khi chạy đều là mô phỏng, không đại diện cho điều kiện giao thông thực tế.
- Chưa có kết quả đánh giá DR, FAR hoặc TTD.
- Logic trong `california.py` chưa được xác minh với tài liệu đặc tả; các ngưỡng mặc định không nên được xem là ngưỡng vận hành đã được chứng thực.
- Frontend chưa có nội dung hoặc chức năng và chưa kết nối với Backend.
- Dự án chỉ phục vụ demo, học tập và nghiên cứu; không dùng để giám sát giao thông thực tế hoặc hỗ trợ quyết định vận hành.
