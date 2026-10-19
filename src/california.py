"""Vị trí dành cho thuật toán California.

TODO: Bổ sung đặc tả bài giảng đã xác minh trước khi triển khai công thức,
ngưỡng, thứ tự kiểm tra và trạng thái xác nhận/kết thúc sự cố.
"""
"""
Thuật toán California (California Algorithm #8) phát hiện sự cố giao thông.
Người phụ trách: Khang (Người 1)
"""

def detect_incident(occ_up: float, occ_down: float, thresholds: dict = None) -> bool:
    """
    Hàm thực thi thuật toán California phát hiện sự cố giao thông dựa trên độ chiếm dòng (Occupancy).
    
    Parameters:
    - occ_up (float): Độ chiếm dòng tại trạm thượng lưu (Upstream - OCC_up).
    - occ_down (float): Độ chiếm dòng tại trạm hạ lưu (Downstream - OCC_down).
    - thresholds (dict): Bộ các ngưỡng T1, T2, T3 theo tài liệu môn học. 
                         Nếu không truyền vào, sẽ dùng giá trị mặc định tiêu chuẩn.
                         
    Returns:
    - bool: True nếu phát hiện sự cố, False nếu giao thông bình thường.
    """
    # Các giá trị ngưỡng mặc định (có thể điều chỉnh theo tài liệu môn học cụ thể của nhóm)
    if thresholds is None:
        thresholds = {
            "T1": 8.0,   # Ngưỡng chênh lệch tuyệt đối giữa trạm trên và trạm dưới (OCC_up - OCC_down)
            "T2": 0.5,   # Ngưỡng tỷ lệ chênh lệch (OCC_up - OCC_down) / OCC_up
            "T3": 2.0    # Ngưỡng giảm độ chiếm dòng tại trạm hạ lưu hoặc điều kiện phụ trợ
        }
        
    t1 = thresholds.get("T1", 8.0)
    t2 = thresholds.get("T2", 0.5)
    t3 = thresholds.get("T3", 2.0)
    
    # Kiểm tra xử lý đầu vào không hợp lệ cơ bản
    if occ_up is None or occ_down is None or occ_up < 0 or occ_down < 0:
        return False

    # Logic thuật toán California cơ bản (Thuật toán số 8):
    # Điều kiện 1: Độ chênh lệch tuyệt đối giữa thượng lưu và hạ lưu vượt ngưỡng T1
    cond1 = (occ_up - occ_down) > t1
    
    # Điều kiện 2: Tỷ lệ chênh lệch tương đối vượt ngưỡng T2
    # Tránh lỗi chia cho 0 bằng cách kiểm tra occ_up > 0
    cond2 = False
    if occ_up > 0:
        cond2 = ((occ_up - occ_down) / occ_up) > t2
        
    # Điều kiện 3: Trạm hạ lưu thấp hơn ngưỡng bất thường T3 hoặc điều kiện không gian phụ
    cond3 = occ_down < (occ_up / t3)

    # Sự cố được xác nhận khi thỏa mãn đồng thời các điều kiện cốt lõi của thuật toán
    if cond1 and cond2 and cond3:
        return True
        
    return False


if __name__ == "__main__":
    # Test thử nghiệm cục bộ khi chạy file trực tiếp
    print("Test thử nghiệm thuật toán California:")
    print("Trường hợp bình thường (Up: 5.0, Down: 4.5):", detect_incident(5.0, 4.5))
    print("Trường hợp có sự cố (Up: 25.0, Down: 8.0):", detect_incident(25.0, 8.0))
