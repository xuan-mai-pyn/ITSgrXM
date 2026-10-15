"""Khung kiểm thử California; chưa có hành vi thuật toán để kiểm chứng."""

import pytest


@pytest.mark.skip(
    reason="Chờ xác minh đặc tả California và triển khai thuật toán."
)
def test_california_incident_detection():
    """Bổ sung ca kiểm thử có dữ liệu và kết quả tham chiếu đã xác minh."""
    pytest.fail("Thay khung này bằng kiểm thử thuật toán đã triển khai.")
