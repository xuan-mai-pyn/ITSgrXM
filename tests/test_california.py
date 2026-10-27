import pytest
from src.california import CaliforniaAlgorithm


@pytest.fixture
def algo():
  return CaliforniaAlgorithm()


# Test case 1: Giao thông bình thường (%)
def test_normal_traffic(algo):
  assert algo.evaluate(occ_up=15.0, occ_down=12.0) is False


# Test case 2: Phát hiện sự cố giao thông (Cần 2 chu kỳ liên tiếp theo persistence=2)
def test_incident_detected(algo):
  res1 = algo.evaluate(occ_up=50.0, occ_down=10.0)  # Chu kỳ 1: đếm = 1 -> False
  res2 = algo.evaluate(occ_up=50.0, occ_down=10.0)  # Chu kỳ 2: đếm = 2 -> True
  assert res1 is False
  assert res2 is True


# Test case 3: Ùn tắc tự nhiên (Hạ lưu cao > s3 = 20%)
def test_recurrent_congestion(algo):
  assert algo.evaluate(occ_up=85.0, occ_down=80.0) is False


# Test case 4: Trường hợp biên (occ_up = 0)
def test_boundary_conditions(algo):
  assert algo.evaluate(occ_up=0.0, occ_down=0.0) is False


# Test case 5: Tích hợp chuỗi dữ liệu giả lập (Simulator)
def test_with_simulator_data(algo):
  simulated_data = [
      {'occ_up': 15.0, 'occ_down': 10.0},
      {'occ_up': 45.0, 'occ_down': 5.0},
      {'occ_up': 45.0, 'occ_down': 5.0},
  ]
  results = [algo.evaluate(d['occ_up'], d['occ_down']) for d in simulated_data]
  assert results == [False, False, True]