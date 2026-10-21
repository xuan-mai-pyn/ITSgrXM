"""Vị trí dành cho thuật toán California.

TODO: Bổ sung đặc tả bài giảng đã xác minh trước khi triển khai công thức,
ngưỡng, thứ tự kiểm tra và trạng thái xác nhận/kết thúc sự cố.
"""
"""
Thuật toán California (California Algorithm #8) phát hiện sự cố giao thông.
Người phụ trách: Khang (Người 1)
"""

from __future__ import annotations

class CaliforniaAlgorithm:
    """Thuật toán phát hiện sự cố giao thông California Algorithm #7.

    Sử dụng chênh lệch Occupancy giữa trạm thượng lưu (upstream) và 
    trạm hạ lưu (downstream) để phát hiện sự cố.
    """

    def __init__(
        self,
        s1: float = 10.0,
        s2: float = 0.20,
        s3: float = 20.0,
        persistence: int = 2,
    ):
        """Khởi tạo các ngưỡng tham số cho thuật toán.

        Args:
            s1: Ngưỡng chênh lệch tuyệt đối (OCC_up - OCC_down), mặc định 10.0%.
            s2: Ngưỡng chênh lệch tương đối ((OCC_up - OCC_down) / OCC_up), mặc định 0.20 (20%).
            s3: Ngưỡng occupancy trạm hạ lưu tối đa để tránh ùn tắc lan truyền, mặc định 20.0%.
            persistence: Số chu kỳ liên tiếp cần thỏa mãn điều kiện để xác nhận sự cố, mặc định 2 chu kỳ.
        """
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3
        self.persistence = persistence
        self._consecutive_count = 0

    def evaluate(self, occ_up: float, occ_down: float) -> bool:
        """Đánh giá một mẫu dữ liệu tại thời điểm hiện tại.

        Args:
            occ_up: Occupancy tại trạm thượng lưu (%).
            occ_down: Occupancy tại trạm hạ lưu (%).

        Returns:
            True nếu phát hiện sự cố, False nếu bình thường.
        """
        diff = occ_up - occ_down
        rel_diff = diff / occ_up if occ_up > 0 else 0.0

        # Ba điều kiện cốt lõi của thuật toán California #7:
        # 1. Chênh lệch tuyệt đối vượt ngưỡng S1
        cond1 = diff >= self.s1
        # 2. Chênh lệch tương đối vượt ngưỡng S2
        cond2 = rel_diff >= self.s2
        # 3. Trạm hạ lưu không quá tải (dưới hoặc bằng S3)
        cond3 = occ_down <= self.s3

        is_candidate = cond1 and cond2 and cond3

        # Bộ lọc duy trì (Persistence filter) tránh báo giả do nhiễu ngắn hạn
        if is_candidate:
            self._consecutive_count += 1
        else:
            self._consecutive_count = 0

        return self._consecutive_count >= self.persistence

    def reset(self) -> None:
        """Đặt lại bộ đếm trạng thái (dùng khi chuyển kịch bản mới)."""
        self._consecutive_count = 0