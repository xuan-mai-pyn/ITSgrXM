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
  res1 = algo.evaluate(occ_up=50.0, occ_down=10.0)  # Chu kỳ 1: đếm = 1 -> False
  res2 = algo.evaluate(occ_up=50.0, occ_down=10.0)  # Chu kỳ 2: đếm = 2 -> True
  assert res1 is False
  assert res2 is True


# Test case 3: Ùn tắc tự nhiên (3. Recurrent Congestion - occ_down > s3 = 20%)
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