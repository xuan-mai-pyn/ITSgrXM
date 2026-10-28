"""Thuật toán California Algorithm #1 phát hiện sự cố giao thông.

Căn cứ lý thuyết:
- TS. Văn Hồng Tấn, Giáo trình Hệ thống Giao thông Thông minh, Chương 5, trang 68.
- TS. Lê Văn Quốc Anh, Bài giảng 03: Quản lý sự cố giao thông, Slide 41 - 45.
Người phụ trách: Khang (Người 1)
"""

from __future__ import annotations


class CaliforniaAlgorithm:
    """Phát hiện sự cố giao thông theo Giải thuật California cơ bản (California #1)."""

    STATE_NORMAL = "NORMAL"
    STATE_TENTATIVE = "TENTATIVE"
    STATE_INCIDENT = "INCIDENT"

    def __init__(
        self,
        t1: float = 20.0,
        t2: float = 0.25,
        t3: float = 0.50,
        persistence: int = 2,
        s1: float | None = None,
        s2: float | None = None,
        s3: float | None = None,
        **kwargs,
    ) -> None:
        """Khởi tạo các ngưỡng tham số (mặc định lấy chuẩn theo Slide 43 của Thầy).

        Hỗ trợ tương thích ngược cả s1, s2, s3 nếu API backend truyền vào.
        """
        if s1 is not None:
            t1 = s1
        if s2 is not None:
            t2 = s2
        if s3 is not None:
            t3 = s3

        self.t1 = float(t1)
        self.t2 = float(t2)
        self.t3 = float(t3)
        self.persistence = persistence
        self.state = self.STATE_NORMAL

    def evaluate(self, occ_up: float, occ_down: float) -> bool:
        """Đánh giá trạng thái giao thông tại thời điểm hiện tại.

        Theo Slide 42:
        - Bước 1: Chênh lệch tuyệt đối OCC_up - OCC_down > T1
        - Bước 2: Chênh lệch tương đối theo trạm thượng lưu (OCC_up - OCC_down) / OCC_up > T2
        - Bước 3: Chênh lệch tương đối theo trạm hạ lưu (OCC_up - OCC_down) / OCC_down > T3
        - Chu kỳ t thỏa cả Bước 1, 2, 3 -> TENTATIVE (khả năng cao, chưa báo động).
        - Chu kỳ t+1 tiếp tục vượt T2 và T3 -> INCIDENT (chính thức báo động sự cố).
        - Khi đang INCIDENT, sự cố kết thúc khi T2 không còn bị vượt nữa -> NORMAL.
        """
        # Tránh chia cho 0 hoặc dữ liệu âm bất thường
        if occ_up <= 0 or occ_down <= 0:
            self.state = self.STATE_NORMAL
            return False

        # 3 Bước kiểm tra theo chuẩn Slide 42
        diff = occ_up - occ_down
        ratio_up = diff / occ_up
        ratio_down = diff / occ_down

        cond1 = diff > self.t1         # Bước 1: Chênh lệch tuyệt đối
        cond2 = ratio_up > self.t2     # Bước 2: Chênh lệch tương đối theo trạm thượng lưu
        cond3 = ratio_down > self.t3   # Bước 3: Chênh lệch tương đối theo trạm hạ lưu

        # Máy trạng thái hữu hạn (Finite State Machine) chuẩn Slide 42
        if self.state == self.STATE_NORMAL:
            if cond1 and cond2 and cond3:
                self.state = self.STATE_TENTATIVE
            return False

        elif self.state == self.STATE_TENTATIVE:
            if cond2 and cond3:
                self.state = self.STATE_INCIDENT
                return True
            else:
                self.state = self.STATE_NORMAL
                return False

        elif self.state == self.STATE_INCIDENT:
            # Chú ý 1 Slide 42: Sự cố kết thúc nếu ngưỡng T2 không bị vượt qua nữa
            if cond2:
                return True
            else:
                self.state = self.STATE_NORMAL
                return False

        return False

    def reset(self) -> None:
        """Đặt lại trạng thái về bình thường khi chuyển kịch bản mô phỏng."""
        self.state = self.STATE_NORMAL
