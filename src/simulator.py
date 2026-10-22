"""Mô phỏng dữ liệu giao thông cho demo thuật toán California.

Module tạo dữ liệu occupancy tại hai trạm quan trắc (thượng lưu và hạ lưu)
cho các tình huống giao thông bình thường và có sự cố.

Dữ liệu là MÔ PHỎNG, không phải dữ liệu giao thông thực tế."""

from __future__ import annotations

import csv
import math
import os
import random
from dataclasses import dataclass, field
from typing import List, Optional


# Cấu trúc dữ liệu

@dataclass
class TrafficRecord:
    """Một bản ghi quan trắc tại một chu kỳ thời gian.

    Attributes:
        timestamp: Chỉ số chu kỳ (0, 1, 2, ...).  Mỗi chu kỳ tương ứng
            ``sample_interval`` giây; giá trị mặc định 30 giây.
        occ_up: Occupancy tại trạm thượng lưu (upstream), đơn vị phần trăm
            (0–100).
        occ_down: Occupancy tại trạm hạ lưu (downstream), đơn vị phần trăm
            (0–100).
        incident: Nhãn tham chiếu – ``True`` nếu tại chu kỳ này thực sự
            đang có sự cố giữa hai trạm, ``False`` nếu không.
    """

    timestamp: int
    occ_up: float
    occ_down: float
    incident: bool


@dataclass
class SimulationResult:
    """Kết quả trả về từ một lần mô phỏng.

    Attributes:
        records: Danh sách các bản ghi theo thứ tự thời gian.
        sample_interval: Khoảng cách giữa hai chu kỳ liên tiếp (giây).
        incident_start: Chỉ số chu kỳ bắt đầu sự cố (``None`` nếu kịch
            bản không có sự cố).
        incident_end: Chỉ số chu kỳ kết thúc sự cố (``None`` nếu kịch
            bản không có sự cố).
        seed: Seed đã dùng để tạo dữ liệu (phục vụ tái tạo).
        description: Mô tả ngắn về kịch bản.
    """

    records: List[TrafficRecord]
    sample_interval: int
    incident_start: Optional[int]
    incident_end: Optional[int]
    seed: int
    description: str


# Hàm tiện ích nội bộ

def _clamp(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    """Giới hạn giá trị trong khoảng [lo, hi]."""
    return max(lo, min(hi, value))


def _add_noise(rng: random.Random, base: float, std: float) -> float:
    """Thêm nhiễu Gaussian vào giá trị cơ sở và giới hạn trong [0, 100]."""
    return _clamp(base + rng.gauss(0, std))



# Các hàm tạo kịch bản

def generate_normal(
    num_periods: int = 120,
    base_occ: float = 20.0,
    noise_std: float = 2.0,
    sample_interval: int = 30,
    seed: int = 42,
) -> SimulationResult:
    """Tạo dữ liệu giao thông bình thường (không có sự cố).

    Trong điều kiện bình thường, occupancy tại hai trạm dao động quanh
    cùng một mức cơ sở với nhiễu ngẫu nhiên nhỏ.

    Args:
        num_periods: Số chu kỳ cần tạo.
        base_occ: Giá trị occupancy trung bình (%).
        noise_std: Độ lệch chuẩn của nhiễu Gaussian.
        sample_interval: Khoảng cách giữa hai chu kỳ (giây).
        seed: Seed cho bộ sinh ngẫu nhiên.

    Returns:
        SimulationResult chứa danh sách bản ghi, tất cả có ``incident=False``.
    """
    rng = random.Random(seed)
    records: List[TrafficRecord] = []

    for t in range(num_periods):
        occ_up = _add_noise(rng, base_occ, noise_std)
        occ_down = _add_noise(rng, base_occ, noise_std)
        records.append(TrafficRecord(
            timestamp=t,
            occ_up=round(occ_up, 2),
            occ_down=round(occ_down, 2),
            incident=False,
        ))

    return SimulationResult(
        records=records,
        sample_interval=sample_interval,
        incident_start=None,
        incident_end=None,
        seed=seed,
        description=(
            f"Giao thông bình thường: {num_periods} chu kỳ, "
            f"OCC cơ sở ≈ {base_occ}%, nhiễu σ = {noise_std}"
        ),
    )


def generate_incident(
    num_periods: int = 120,
    base_occ: float = 20.0,
    noise_std: float = 2.0,
    incident_start: int = 40,
    incident_duration: int = 30,
    occ_up_peak: float = 55.0,
    occ_down_drop: float = 8.0,
    ramp_up_periods: int = 5,
    ramp_down_periods: int = 8,
    sample_interval: int = 30,
    seed: int = 123,
) -> SimulationResult:
    """Tạo dữ liệu có một sự cố xảy ra giữa hai trạm.

    Khi sự cố xảy ra:
    - OCC_up tăng dần (giao thông ùn ứ phía thượng lưu).
    - OCC_down giảm (ít xe đi qua phía hạ lưu).

    Sau khi sự cố kết thúc, các giá trị dần trở về mức bình thường.

    Args:
        num_periods: Số chu kỳ cần tạo.
        base_occ: Giá trị occupancy trung bình khi bình thường (%).
        noise_std: Độ lệch chuẩn của nhiễu Gaussian.
        incident_start: Chu kỳ bắt đầu sự cố.
        incident_duration: Số chu kỳ sự cố kéo dài.
        occ_up_peak: Giá trị OCC_up đỉnh trong lúc sự cố (%).
        occ_down_drop: Giá trị OCC_down thấp nhất trong lúc sự cố (%).
        ramp_up_periods: Số chu kỳ để OCC_up tăng từ mức bình thường
            lên đỉnh.
        ramp_down_periods: Số chu kỳ để các giá trị phục hồi sau sự cố.
        sample_interval: Khoảng cách giữa hai chu kỳ (giây).
        seed: Seed cho bộ sinh ngẫu nhiên.

    Returns:
        SimulationResult chứa danh sách bản ghi với nhãn sự cố.

    Raises:
        ValueError: Nếu tham số không hợp lệ.
    """
    if incident_start < 0:
        raise ValueError("incident_start phải >= 0")
    if incident_duration < 1:
        raise ValueError("incident_duration phải >= 1")
    if incident_start + incident_duration > num_periods:
        raise ValueError(
            "Sự cố vượt quá số chu kỳ: "
            f"incident_start({incident_start}) + "
            f"incident_duration({incident_duration}) > "
            f"num_periods({num_periods})"
        )

    rng = random.Random(seed)
    records: List[TrafficRecord] = []

    incident_end = incident_start + incident_duration  # chu kỳ đầu tiên hết sự cố
    recovery_end = min(incident_end + ramp_down_periods, num_periods)

    for t in range(num_periods):
        is_incident = incident_start <= t < incident_end

        if t < incident_start:
            # --- Giai đoạn bình thường trước sự cố ---
            occ_up = _add_noise(rng, base_occ, noise_std)
            occ_down = _add_noise(rng, base_occ, noise_std)

        elif t < incident_start + ramp_up_periods and t < incident_end:
            # --- Giai đoạn tăng dần (onset) ---
            progress = (t - incident_start + 1) / ramp_up_periods
            current_up = base_occ + (occ_up_peak - base_occ) * progress
            current_down = base_occ + (occ_down_drop - base_occ) * progress
            occ_up = _add_noise(rng, current_up, noise_std * 0.5)
            occ_down = _add_noise(rng, current_down, noise_std * 0.5)

        elif t < incident_end:
            # --- Giai đoạn sự cố ổn định ---
            occ_up = _add_noise(rng, occ_up_peak, noise_std)
            occ_down = _add_noise(rng, occ_down_drop, noise_std)

        elif t < recovery_end:
            # --- Giai đoạn phục hồi ---
            progress = (t - incident_end + 1) / ramp_down_periods
            current_up = occ_up_peak + (base_occ - occ_up_peak) * progress
            current_down = occ_down_drop + (base_occ - occ_down_drop) * progress
            occ_up = _add_noise(rng, current_up, noise_std)
            occ_down = _add_noise(rng, current_down, noise_std)

        else:
            # --- Giai đoạn bình thường sau phục hồi ---
            occ_up = _add_noise(rng, base_occ, noise_std)
            occ_down = _add_noise(rng, base_occ, noise_std)

        records.append(TrafficRecord(
            timestamp=t,
            occ_up=round(occ_up, 2),
            occ_down=round(occ_down, 2),
            incident=is_incident,
        ))

    return SimulationResult(
        records=records,
        sample_interval=sample_interval,
        incident_start=incident_start,
        incident_end=incident_end - 1,  # chu kỳ cuối cùng còn sự cố
        seed=seed,
        description=(
            f"Sự cố tại chu kỳ {incident_start}–{incident_end - 1}: "
            f"OCC_up đỉnh ≈ {occ_up_peak}%, OCC_down đáy ≈ {occ_down_drop}%"
        ),
    )


def generate_edge_case(
    num_periods: int = 60,
    base_occ: float = 20.0,
    noise_std: float = 2.0,
    congestion_start: int = 15,
    congestion_duration: int = 20,
    congestion_occ: float = 45.0,
    sample_interval: int = 30,
    seed: int = 456,
) -> SimulationResult:
    """Tạo dữ liệu ùn tắc tự nhiên (KHÔNG phải sự cố).

    Khi ùn tắc do mật độ cao, occupancy tại CẢ HAI trạm đều tăng
    (khác với sự cố khi chỉ trạm thượng lưu tăng). Đây là trường hợp
    biên để kiểm tra khả năng phân biệt của thuật toán.

    Args:
        num_periods: Số chu kỳ.
        base_occ: OCC cơ sở khi bình thường (%).
        noise_std: Độ lệch chuẩn nhiễu.
        congestion_start: Chu kỳ bắt đầu ùn tắc.
        congestion_duration: Số chu kỳ ùn tắc.
        congestion_occ: Mức OCC khi ùn tắc (%).
        sample_interval: Khoảng cách chu kỳ (giây).
        seed: Seed cho bộ sinh ngẫu nhiên.

    Returns:
        SimulationResult với tất cả ``incident=False``.
    """
    rng = random.Random(seed)
    records: List[TrafficRecord] = []
    congestion_end = min(congestion_start + congestion_duration, num_periods)

    for t in range(num_periods):
        if congestion_start <= t < congestion_end:
            # Ùn tắc: CẢ HAI trạm đều tăng occupancy
            occ_up = _add_noise(rng, congestion_occ, noise_std)
            occ_down = _add_noise(rng, congestion_occ, noise_std)
        else:
            occ_up = _add_noise(rng, base_occ, noise_std)
            occ_down = _add_noise(rng, base_occ, noise_std)

        records.append(TrafficRecord(
            timestamp=t,
            occ_up=round(occ_up, 2),
            occ_down=round(occ_down, 2),
            incident=False,
        ))

    return SimulationResult(
        records=records,
        sample_interval=sample_interval,
        incident_start=None,
        incident_end=None,
        seed=seed,
        description=(
            f"Ùn tắc tự nhiên (không phải sự cố) chu kỳ "
            f"{congestion_start}–{congestion_end - 1}: "
            f"OCC cả hai trạm ≈ {congestion_occ}%"
        ),
    )


# Xuất dữ liệu ra CSV

def save_to_csv(result: SimulationResult, filepath: str) -> str:
    """Lưu kết quả mô phỏng thành file CSV.

    Cột: timestamp, occ_up, occ_down, incident

    Args:
        result: Kết quả mô phỏng cần lưu.
        filepath: Đường dẫn file CSV đầu ra.

    Returns:
        Đường dẫn tuyệt đối của file đã lưu.
    """
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "occ_up", "occ_down", "incident"])
        for rec in result.records:
            writer.writerow([
                rec.timestamp,
                rec.occ_up,
                rec.occ_down,
                1 if rec.incident else 0,
            ])

    return os.path.abspath(filepath)


# Hàm tổng hợp – tạo tất cả kịch bản

def generate_all_scenarios() -> dict[str, SimulationResult]:
    """Tạo tất cả các kịch bản mô phỏng.

    Returns:
        Dict với key là tên kịch bản, value là SimulationResult:
        - ``"normal"``: giao thông bình thường
        - ``"incident"``: có một sự cố
        - ``"edge_congestion"``: ùn tắc tự nhiên (không phải sự cố)
    """
    return {
        "normal": generate_normal(),
        "incident": generate_incident(),
        "edge_congestion": generate_edge_case(),
    }


# Hàm hiển thị tóm tắt ra Terminal

def print_summary(result: SimulationResult) -> None:
    """In tóm tắt kết quả mô phỏng ra Terminal.

    Args:
        result: Kết quả mô phỏng cần hiển thị.
    """
    print(f"\n{'='*60}")
    print(f"  Kịch bản: {result.description}")
    print(f"  Seed: {result.seed}")
    print(f"  Số chu kỳ: {len(result.records)}")
    print(f"  Khoảng lấy mẫu: {result.sample_interval}s")
    if result.incident_start is not None:
        print(f"  Sự cố: chu kỳ {result.incident_start} → {result.incident_end}")
    else:
        print("  Sự cố: không có")
    print(f"{'='*60}")

    # In 5 dòng đầu + 5 dòng cuối
    records = result.records
    show = min(5, len(records))
    print(f"  {'Chu kỳ':>8}  {'OCC_up':>8}  {'OCC_down':>10}  {'Sự cố':>7}")
    print(f"  {'-'*8}  {'-'*8}  {'-'*10}  {'-'*7}")
    for rec in records[:show]:
        label = "CÓ" if rec.incident else "không"
        print(f"  {rec.timestamp:>8}  {rec.occ_up:>8.2f}  {rec.occ_down:>10.2f}  {label:>7}")
    if len(records) > show * 2:
        print(f"  {'...':>8}  {'...':>8}  {'...':>10}  {'...':>7}")
    for rec in records[-show:]:
        label = "CÓ" if rec.incident else "không"
        print(f"  {rec.timestamp:>8}  {rec.occ_up:>8.2f}  {rec.occ_down:>10.2f}  {label:>7}")


# Chạy trực tiếp để kiểm tra nhanh

if __name__ == "__main__":
    print("=== Mô phỏng dữ liệu giao thông cho thuật toán California ===")
    print("Lưu ý: Đây là dữ liệu MÔ PHỎNG, không phải dữ liệu thực tế.\n")

    scenarios = generate_all_scenarios()

    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")

    for name, result in scenarios.items():
        print_summary(result)
        filepath = save_to_csv(result, os.path.join(data_dir, f"{name}.csv"))
        print(f"  → Đã lưu: {filepath}\n")

    print("Hoàn tất tạo dữ liệu mô phỏng.")
