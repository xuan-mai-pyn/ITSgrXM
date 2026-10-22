"""Các chỉ số đánh giá phát hiện sự cố: DR, FAR và TTD.

Quy ước (xem docs/evaluation.md):
- Sự cố tham chiếu là một khoảng thời gian [start, end].
- Cảnh báo là một thời điểm thuật toán báo sự cố.
- Thời gian là số (ví dụ chỉ số chu kỳ hoặc giây), cùng đơn vị ở mọi tham số.
- Cảnh báo thuộc cửa sổ [start, end + tolerance] của một sự cố là phát hiện đúng.
  Cảnh báo đầu tiên trong cửa sổ tính là phát hiện, các cảnh báo sau trong cùng
  cửa sổ là cảnh báo lặp (không tính là cảnh báo sai). Cảnh báo ngoài mọi cửa
  sổ là cảnh báo sai.
- Chỉ số không xác định (mẫu số bằng 0) trả về None, không tự gán 0 hoặc 100%.
"""

from __future__ import annotations

import math
import statistics
from dataclasses import dataclass, field
from typing import Iterable, Optional, Sequence

FAR_PER_SAMPLE = "per_sample"
FAR_PER_HOUR = "per_hour"
FAR_RATIO = "ratio"


@dataclass(frozen=True)
class Incident:
    """Sự cố tham chiếu, kéo dài từ `start` đến `end` (gồm cả hai đầu)."""

    start: float
    end: float
    id: Optional[str] = None

    def __post_init__(self) -> None:
        if not (math.isfinite(self.start) and math.isfinite(self.end)):
            raise ValueError("Thời điểm sự cố phải là số hữu hạn.")
        if self.end < self.start:
            raise ValueError(
                f"Sự cố có end ({self.end}) nhỏ hơn start ({self.start})."
            )


@dataclass
class EventMatch:
    """Kết quả ghép cảnh báo với sự cố tham chiếu."""

    n_incidents: int
    detected: list[Incident] = field(default_factory=list)
    missed: list[Incident] = field(default_factory=list)
    ttd_values: list[float] = field(default_factory=list)
    false_alarms: list[float] = field(default_factory=list)
    repeated_alarms: list[float] = field(default_factory=list)

    @property
    def tp(self) -> int:
        return len(self.detected)

    @property
    def fn(self) -> int:
        return len(self.missed)

    @property
    def fp(self) -> int:
        return len(self.false_alarms)


def match_events(
    incidents: Sequence[Incident],
    alarms: Iterable[float],
    tolerance: float = 0.0,
) -> EventMatch:
    """Ghép cảnh báo với sự cố tham chiếu.

    `tolerance` kéo dài cửa sổ ghép về phía sau `end` (cùng đơn vị thời gian),
    dùng khi sự cố đã kết thúc nhưng cảnh báo đến muộn vẫn được chấp nhận.
    """
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance phải là số hữu hạn, không âm.")

    alarm_times = sorted(alarms)
    for t in alarm_times:
        if not math.isfinite(t):
            raise ValueError("Thời điểm cảnh báo phải là số hữu hạn.")

    ordered = sorted(incidents, key=lambda inc: (inc.start, inc.end))
    result = EventMatch(n_incidents=len(ordered))
    first_alarm: dict[int, float] = {}

    for t in alarm_times:
        candidates = [
            i
            for i, inc in enumerate(ordered)
            if inc.start <= t <= inc.end + tolerance
        ]
        if not candidates:
            result.false_alarms.append(t)
            continue
        # Ưu tiên sự cố chưa được phát hiện; nếu đều đã phát hiện thì là cảnh báo lặp.
        target = next((i for i in candidates if i not in first_alarm), None)
        if target is None:
            result.repeated_alarms.append(t)
        else:
            first_alarm[target] = t

    for i, inc in enumerate(ordered):
        if i in first_alarm:
            result.detected.append(inc)
            result.ttd_values.append(first_alarm[i] - inc.start)
        else:
            result.missed.append(inc)
    return result


def detection_rate(match: EventMatch) -> Optional[float]:
    """DR = TP / (TP + FN), theo sự kiện. Trả về None nếu không có sự cố."""
    total = match.tp + match.fn
    if total == 0:
        return None
    return match.tp / total


def false_alarm_rate(
    match: EventMatch,
    definition: str = FAR_PER_SAMPLE,
    n_non_incident_samples: Optional[int] = None,
    monitoring_hours: Optional[float] = None,
) -> Optional[float]:
    """Tính FAR theo một trong ba định nghĩa (không tương đương nhau).

    - "per_sample": số cảnh báo sai / số mẫu đánh giá không có sự cố.
      Cần `n_non_incident_samples`.
    - "per_hour": số cảnh báo sai / số giờ giám sát. Cần `monitoring_hours`.
    - "ratio": FP / (TP + FP), tỷ lệ cảnh báo là sai trên tổng cảnh báo
      (không tính cảnh báo lặp).

    Trả về None nếu mẫu số bằng 0.
    """
    if definition == FAR_PER_SAMPLE:
        if n_non_incident_samples is None:
            raise ValueError("Cần n_non_incident_samples cho định nghĩa per_sample.")
        if n_non_incident_samples < 0:
            raise ValueError("n_non_incident_samples không được âm.")
        denominator: float = n_non_incident_samples
    elif definition == FAR_PER_HOUR:
        if monitoring_hours is None:
            raise ValueError("Cần monitoring_hours cho định nghĩa per_hour.")
        if monitoring_hours < 0:
            raise ValueError("monitoring_hours không được âm.")
        denominator = monitoring_hours
    elif definition == FAR_RATIO:
        denominator = match.tp + match.fp
    else:
        raise ValueError(
            f"Định nghĩa FAR không hợp lệ: {definition!r}. "
            f"Chọn một trong: {FAR_PER_SAMPLE}, {FAR_PER_HOUR}, {FAR_RATIO}."
        )
    if denominator == 0:
        return None
    return match.fp / denominator


def time_to_detection(match: EventMatch, statistic: str = "mean") -> Optional[float]:
    """TTD tổng hợp trên các sự cố được phát hiện (cùng đơn vị thời gian).

    `statistic` là "mean" hoặc "median". Trả về None nếu chưa phát hiện sự cố nào.
    Luôn báo TTD cùng DR vì TTD không tính các sự cố bị bỏ sót.
    """
    if not match.ttd_values:
        return None
    if statistic == "mean":
        return statistics.fmean(match.ttd_values)
    if statistic == "median":
        return statistics.median(match.ttd_values)
    raise ValueError("statistic phải là 'mean' hoặc 'median'.")


def summarize(
    incidents: Sequence[Incident],
    alarms: Iterable[float],
    tolerance: float = 0.0,
    far_definition: str = FAR_PER_SAMPLE,
    n_non_incident_samples: Optional[int] = None,
    monitoring_hours: Optional[float] = None,
    ttd_statistic: str = "mean",
) -> dict:
    """Ghép sự kiện và trả về toàn bộ chỉ số cùng các số đếm để báo cáo."""
    match = match_events(incidents, alarms, tolerance)
    return {
        "n_incidents": match.n_incidents,
        "tp": match.tp,
        "fn": match.fn,
        "fp": match.fp,
        "repeated_alarms": len(match.repeated_alarms),
        "dr": detection_rate(match),
        "far": false_alarm_rate(
            match, far_definition, n_non_incident_samples, monitoring_hours
        ),
        "far_definition": far_definition,
        "ttd": time_to_detection(match, ttd_statistic),
        "ttd_statistic": ttd_statistic,
    }
