import pytest
from src.california import CaliforniaAlgorithm  # 1. Import class thật của Khang (Mục 1)
from src.simulator import (  # 4. Import module simulator thật của Cường (Mục 4)
    generate_edge_case,
    generate_incident,
    generate_normal,
)


@pytest.fixture
def algo():
    return CaliforniaAlgorithm()


# Test case 1: Giao thông bình thường với dữ liệu tĩnh (2. Dùng đơn vị %: 15.0, 12.0)
def test_normal_traffic(algo):
    assert algo.evaluate(occ_up=15.0, occ_down=12.0) is False


# Test case 2: Phát hiện sự cố giao thông (Cần 2 chu kỳ liên tiếp thỏa mãn theo persistence=2)
def test_incident_detected(algo):
    res1 = algo.evaluate(occ_up=50.0, occ_down=10.0)  # Chu kỳ 1: TENTATIVE -> False
    res2 = algo.evaluate(occ_up=50.0, occ_down=10.0)  # Chu kỳ 2: INCIDENT -> True
    assert res1 is False
    assert res2 is True


# Test case 3: Ùn tắc tự nhiên (3. Recurrent Congestion - occ_down cao, diff thấp)
def test_recurrent_congestion(algo):
    assert algo.evaluate(occ_up=85.0, occ_down=80.0) is False


# Test case 4: Trường hợp biên (3. Boundary Test - occ_up = 0%)
def test_boundary_conditions(algo):
    assert algo.evaluate(occ_up=0.0, occ_down=0.0) is False


# Test case 5: Tích hợp dữ liệu thực tế từ simulator.py của Cường - Kịch bản có sự cố
def test_with_real_simulator_incident_scenario(algo):
    # Gọi hàm mô phỏng sự cố thật của Cường
    sim_result = generate_incident(num_periods=50, incident_start=10)

    detected_periods = []
    for rec in sim_result.records:
        # Truyền dữ liệu occ_up và occ_down thật từ simulator vào thuật toán của Khang
        is_incident = algo.evaluate(occ_up=rec.occ_up, occ_down=rec.occ_down)
        if is_incident:
            detected_periods.append(rec.timestamp)

    # Xác nhận thuật toán phát hiện được sự cố tại các chu kỳ xảy ra sự cố
    assert len(detected_periods) > 0


# Test case 6: Tích hợp dữ liệu từ simulator.py của Cường - Kịch bản ùn tắc tự nhiên (Không báo giả)
def test_with_real_simulator_edge_case_scenario(algo):
    # Gọi hàm mô phỏng ùn tắc tự nhiên của Cường
    sim_result = generate_edge_case(num_periods=30)

    detected = False
    for rec in sim_result.records:
        if algo.evaluate(occ_up=rec.occ_up, occ_down=rec.occ_down):
            detected = True

    # Ùn tắc tự nhiên thì thuật toán không được báo nhầm là sự cố
    assert detected is False


# Test case 7: Bài tập mẫu 12 Time Step đối chứng theo Slide 43 - 45 của TS. Lê Văn Quốc Anh
def test_slide_example_12_steps():
    """Kiểm tra đối chiếu bài tập 12 bước trong Slide 43 - 45.

    Ngưỡng: T1 = 20, T2 = 0.25, T3 = 0.50.
    Kết quả mong đợi theo Slide 45:
    - Bắt đầu có cảnh báo: Time step 2 (chu kỳ 1 là tentative).
    - Cảnh báo duy trì từ Time step 2 đến Time step 8.
    - Kết thúc ghi nhận sự cố: Time step 9.
    - Time step 10 - 12: Bình thường (không cảnh báo).
    """
    algo = CaliforniaAlgorithm(t1=20.0, t2=0.25, t3=0.50)
    data = [
        (60, 10),  # Step 1: TENTATIVE -> False
        (62, 15),  # Step 2: INCIDENT -> True (Bắt đầu có cảnh báo)
        (59, 17),  # Step 3: INCIDENT -> True
        (65, 14),  # Step 4: INCIDENT -> True
        (67, 22),  # Step 5: INCIDENT -> True
        (64, 19),  # Step 6: INCIDENT -> True
        (59, 22),  # Step 7: INCIDENT -> True
        (48, 27),  # Step 8: INCIDENT -> True
        (37, 29),  # Step 9: NORMAL -> False (Kết thúc sự cố)
        (32, 29),  # Step 10: NORMAL -> False
        (30, 28),  # Step 11: NORMAL -> False
        (32, 31),  # Step 12: NORMAL -> False
    ]
    results = [algo.evaluate(up, down) for up, down in data]
    expected = [
        False,  # Step 1
        True,   # Step 2 (Cảnh báo bắt đầu)
        True,   # Step 3
        True,   # Step 4
        True,   # Step 5
        True,   # Step 6
        True,   # Step 7
        True,   # Step 8
        False,  # Step 9 (Kết thúc sự cố)
        False,  # Step 10
        False,  # Step 11
        False,  # Step 12
    ]
    assert results == expected
