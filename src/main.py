from __future__ import annotations

import math
import sys
from collections.abc import Mapping
from numbers import Real
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- PHẦN 1: CẤU HÌNH FASTAPI (CHO FRONTEND GỌI API) ---
app = FastAPI(title="ITS Traffic Incident Detection API")
@app.get("/")
def read_root():
    return {"message": "API Mạng giao thông thông minh (ITS) đang hoạt động!"}


@app.get("/api/run-simulation")
def run_simulation_api():
    """API chạy mô phỏng thuật toán California và trả về kết quả JSON cho Frontend"""
    try:
        from . import simulator
        from .california import CaliforniaAlgorithm

        generator = getattr(simulator, "generate_all_scenarios", None)
        if not callable(generator):
            return {"status": "error", "message": "Hàm generate_all_scenarios không tồn tại."}

        scenarios = generator()
        results_data = {}

        for name, result in scenarios.items():
            records, description = _validate_result(str(name), result)
            sample_interval = getattr(result, "sample_interval", 30)

            algorithm = CaliforniaAlgorithm()
            detection_starts: list[int] = []
            previously_detected = False
            
            records_list = []
            for record in records:
                detected = algorithm.evaluate(record.occ_up, record.occ_down)
                if detected and not previously_detected:
                    detection_starts.append(record.timestamp)
                previously_detected = detected
                
                records_list.append({
                    "timestamp": record.timestamp,
                    "occ_up": record.occ_up,
                    "occ_down": record.occ_down,
                    "incident": record.incident
                })

            results_data[str(name)] = {
                "description": description,
                "sample_interval": sample_interval,
                "records": records_list,
                "detected_cycles": detection_starts
            }

        return {
            "status": "success",
            "message": "Chạy thuật toán thành công",
            "data": results_data
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Cấu hình CORS để cho phép Frontend gọi API không bị lỗi chặn
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép mọi nguồn gọi
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "API Mạng giao thông thông minh (ITS) đang hoạt động!"}


@app.get("/api/run-simulation")
def run_simulation_api():
    """API chạy mô phỏng thuật toán California và trả về kết quả JSON cho Frontend"""
    try:
        from . import simulator
        from .california import CaliforniaAlgorithm

        generator = getattr(simulator, "generate_all_scenarios", None)
        if not callable(generator):
            return {"status": "error", "message": "Hàm generate_all_scenarios không tồn tại."}

        scenarios = generator()
        results_data = {}

        for name, result in scenarios.items():
            records, description = _validate_result(str(name), result)
            sample_interval = getattr(result, "sample_interval", 30)

            algorithm = CaliforniaAlgorithm()
            detection_starts: list[int] = []
            previously_detected = False
            
            records_list = []
            for record in records:
                detected = algorithm.evaluate(record.occ_up, record.occ_down)
                if detected and not previously_detected:
                    detection_starts.append(record.timestamp)
                previously_detected = detected
                
                records_list.append({
                    "timestamp": record.timestamp,
                    "occ_up": record.occ_up,
                    "occ_down": record.occ_down,
                    "incident": record.incident
                })

            results_data[str(name)] = {
                "description": description,
                "sample_interval": sample_interval,
                "records": records_list,
                "detected_cycles": detection_starts
            }

        return {
            "status": "success",
            "message": "Chạy thuật toán thành công",
            "data": results_data
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# --- PHẦN 2: CÁC HÀM XỬ LÝ DEMO TRÊN TERMINAL ---
def _is_number(value: object) -> bool:
    return isinstance(value, Real) and not isinstance(value, bool) and math.isfinite(value)


def _validate_result(name: str, result: object) -> tuple[list[object], str]:
    description = getattr(result, "description", None)
    records = getattr(result, "records", None)

    if not isinstance(description, str) or not isinstance(records, list):
        raise ValueError(
            f"Kịch bản '{name}' không đúng định dạng SimulationResult "
            "(cần description dạng chuỗi và records dạng danh sách)."
        )

    for index, record in enumerate(records):
        timestamp = getattr(record, "timestamp", None)
        occ_up = getattr(record, "occ_up", None)
        occ_down = getattr(record, "occ_down", None)
        incident = getattr(record, "incident", None)
        if (
            not isinstance(timestamp, int)
            or isinstance(timestamp, bool)
            or not _is_number(occ_up)
            or not _is_number(occ_down)
            or not isinstance(incident, bool)
        ):
            raise ValueError(
                f"Bản ghi số {index} trong kịch bản '{name}' không đúng định dạng "
                "(cần timestamp nguyên, occ_up/occ_down dạng số và incident dạng bool)."
            )

    return records, description


def _print_records(records: list[object]) -> None:
    print("  Dữ liệu tiêu biểu (OCC tính theo %):")
    print(f"  {'Chu kỳ':>8}  {'OCC thượng lưu':>15}  {'OCC hạ lưu':>12}  {'Nhãn mô phỏng':>14}")
    print(f"  {'-' * 8}  {'-' * 15}  {'-' * 12}  {'-' * 14}")

    sample_size = 5
    indices = list(range(min(sample_size, len(records))))
    if len(records) > sample_size * 2:
        indices.append(-1)
        indices.extend(range(len(records) - sample_size, len(records)))
    elif len(records) > sample_size:
        indices.extend(range(sample_size, len(records)))

    for index in indices:
        if index == -1:
            print("  " + "...")
            continue
        record = records[index]
        incident_label = "có" if record.incident else "không"
        print(
            f"  {record.timestamp:>8}  {record.occ_up:>15.2f}  "
            f"{record.occ_down:>12.2f}  {incident_label:>14}"
        )


def main() -> None:
    reconfigure_stdout = getattr(sys.stdout, "reconfigure", None)
    if callable(reconfigure_stdout):
        reconfigure_stdout(encoding="utf-8", errors="replace")

    print("=" * 72)
    print("Demo phát hiện sự cố giao thông bằng thuật toán California")
    print("=" * 72)
    print("Lưu ý: Dữ liệu dưới đây là dữ liệu mô phỏng, không phải dữ liệu thực tế.")

    try:
        from . import simulator
        from .california import CaliforniaAlgorithm
    except ModuleNotFoundError as error:
        if error.name in {"src.simulator", "src.california"}:
            missing = error.name.removeprefix("src.")
            print(f"\nChưa thể chạy: module src.{missing} chưa sẵn sàng.")
            return
        raise
    except SyntaxError as error:
        module_paths = {
            Path(__file__).with_name("simulator.py").resolve(): "simulator",
            Path(__file__).with_name("california.py").resolve(): "california",
        }
        module_name = module_paths.get(Path(error.filename).resolve()) if error.filename else None
        if module_name is None:
            raise
        print(
            f"\nChưa thể chạy: src.{module_name} có lỗi cú pháp "
            f"ở dòng {error.lineno}: {error.msg}"
        )
        return

    generator = getattr(simulator, "generate_all_scenarios", None)
    if not callable(generator):
        print(
            "\nChưa thể chạy: src.simulator chưa cung cấp hàm "
            "generate_all_scenarios()."
        )
        return

    evaluate = getattr(CaliforniaAlgorithm, "evaluate", None)
    if not callable(evaluate):
        print(
            "\nChưa thể chạy: lớp CaliforniaAlgorithm trong src.california "
            "chưa cung cấp phương thức evaluate(occ_up, occ_down)."
        )
        return

    try:
        scenarios = generator()
    except ValueError as error:
        print(f"\nKhông thể tạo dữ liệu mô phỏng: {error}")
        return

    if not isinstance(scenarios, Mapping) or not scenarios:
        print(
            "\nDữ liệu mô phỏng không đúng định dạng: "
            "cần một tập kịch bản không rỗng."
        )
        return

    prepared: list[tuple[str, object, list[object], str]] = []
    try:
        for name, result in scenarios.items():
            records, description = _validate_result(str(name), result)
            prepared.append((str(name), result, records, description))
    except ValueError as error:
        print(f"\nDữ liệu mô phỏng không đúng định dạng: {error}")
        return

    if any(not records for _, _, records, _ in prepared):
        for name, _, records, _ in prepared:
            if not records:
                print(f"\nKịch bản '{name}' không có bản ghi dữ liệu; dừng xử lý an toàn.")
        return

    for name, result, records, description in prepared:
        print(f"\nKịch bản: {name}")
        print(f"  Mô tả: {description}")
        print(f"  Số bản ghi: {len(records)}")
        sample_interval = getattr(result, "sample_interval", None)
        if isinstance(sample_interval, int) and not isinstance(sample_interval, bool):
            print(f"  Khoảng lấy mẫu: {sample_interval} giây")
        _print_records(records)

        algorithm = CaliforniaAlgorithm()
        detection_starts: list[int] = []
        previously_detected = False
        for record in records:
            detected = algorithm.evaluate(record.occ_up, record.occ_down)
            if detected and not previously_detected:
                detection_starts.append(record.timestamp)
            previously_detected = detected

        print("  Kết quả California:")
        if detection_starts:
            detected_cycles = ", ".join(str(timestamp) for timestamp in detection_starts)
            print(f"    Phát hiện sự cố tại chu kỳ: {detected_cycles}")
        else:
            print("    Thuật toán không phát hiện sự cố trong kịch bản này.")


if __name__ == "__main__":
    import uvicorn
    # Chạy server FastAPI bằng uvicorn khi chạy trực tiếp file
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)