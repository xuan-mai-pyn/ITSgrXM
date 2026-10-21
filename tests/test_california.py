import pytest

# Hàm kiểm tra sự cố giả định theo thuật toán California
def california_algorithm(occ_upstream, occ_downstream, th1=0.1, th2=0.2):
    occ_diff = occ_upstream - occ_downstream
    occ_rdf = occ_diff / occ_upstream if occ_upstream > 0 else 0
    
    # Phát hiện sự cố khi chênh lệch vượt ngưỡng
    if occ_diff > th1 and occ_rdf > th2:
        return "Incident Detected"
    return "Normal"

# Test case 1: Trạng thái giao thông bình thường
def test_california_normal():
    result = california_algorithm(occ_upstream=0.15, occ_downstream=0.12)
    assert result == "Normal"

# Test case 2: Trạng thái phát hiện sự cố giao thông
def test_california_incident():
    result = california_algorithm(occ_upstream=0.50, occ_downstream=0.10)
    assert result == "Incident Detected"