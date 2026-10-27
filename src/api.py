"""REST API for the ITSgrXM traffic incident detection demo."""

from __future__ import annotations

import logging
import os
from typing import Any, Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from . import metrics, simulator
from .california import CaliforniaAlgorithm

logger = logging.getLogger(__name__)


class APIModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class SimulationParameters(APIModel):
    num_periods: int | None = Field(default=None, gt=0)
    base_occ: float | None = Field(default=None, ge=0, le=100, allow_inf_nan=False)
    noise_std: float | None = Field(default=None, ge=0, allow_inf_nan=False)
    sample_interval: int | None = Field(default=None, gt=0)
    seed: int | None = None
    incident_start: int | None = Field(default=None, ge=0)
    incident_duration: int | None = Field(default=None, gt=0)
    occ_up_peak: float | None = Field(default=None, ge=0, le=100, allow_inf_nan=False)
    occ_down_drop: float | None = Field(default=None, ge=0, le=100, allow_inf_nan=False)
    ramp_up_periods: int | None = Field(default=None, gt=0)
    ramp_down_periods: int | None = Field(default=None, ge=0)
    congestion_start: int | None = Field(default=None, ge=0)
    congestion_duration: int | None = Field(default=None, gt=0)
    congestion_occ: float | None = Field(default=None, ge=0, le=100, allow_inf_nan=False)


class AlgorithmParameters(APIModel):
    s1: float | None = Field(default=None, allow_inf_nan=False)
    s2: float | None = Field(default=None, allow_inf_nan=False)
    s3: float | None = Field(default=None, allow_inf_nan=False)
    persistence: int | None = Field(default=None, ge=1)


class SimulationRequest(APIModel):
    scenario: Literal["normal", "incident", "edge_congestion"] = "normal"
    parameters: SimulationParameters = Field(default_factory=SimulationParameters)
    algorithm: AlgorithmParameters = Field(default_factory=AlgorithmParameters)


class RecordResult(APIModel):
    timestamp: int
    occ_up: float
    occ_down: float
    actual_incident: bool
    detected: bool


class EvaluationResponse(APIModel):
    status: Literal["complete", "partial"]
    n_incidents: int
    tp: int
    fn: int
    fp: int
    repeated_alarms: int
    dr: float | None
    far: float | None
    far_definition: str
    ttd: float | None
    ttd_statistic: str
    unavailable_metrics: list[str]


class SimulationResponse(APIModel):
    status: Literal["success"]
    scenario: str
    description: str
    sample_interval: int
    incident_start: int | None
    incident_end: int | None
    seed: int
    detection_times: list[int]
    evaluation: EvaluationResponse
    records: list[RecordResult]


class IncidentInput(APIModel):
    start: float = Field(allow_inf_nan=False)
    end: float = Field(allow_inf_nan=False)
    id: str | None = None


class EvaluationRequest(APIModel):
    incidents: list[IncidentInput]
    alarms: list[float]
    tolerance: float = Field(default=0.0, ge=0, allow_inf_nan=False)
    far_definition: Literal["per_sample", "per_hour", "ratio"] = "per_sample"
    n_non_incident_samples: int | None = Field(default=None, ge=0)
    monitoring_hours: float | None = Field(default=None, ge=0, allow_inf_nan=False)
    ttd_statistic: Literal["mean", "median"] = "mean"


class DashboardSimulation(APIModel):
    scenario: str
    description: str
    record_count: int
    sample_interval: int
    seed: int
    detection_count: int
    evaluation: EvaluationResponse


class DashboardResponse(APIModel):
    status: Literal["available", "no_data"]
    data_source: Literal["in_memory_api_requests"]
    message: str | None
    latest_simulation: DashboardSimulation | None
    latest_evaluation: EvaluationResponse | None


app = FastAPI(
    title="ITSgrXM Traffic Incident Detection API",
    description=(
        "API demo dùng dữ liệu mô phỏng; kết quả không đại diện cho "
        "dữ liệu giao thông thực tế."
    ),
    version="1.0.0",
)

allowed_origins = [
    origin.strip()
    for origin in os.getenv("ITS_ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=(
        None
        if allowed_origins
        else r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$"
    ),
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)
app.state.latest_simulation = None
app.state.latest_evaluation = None


@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    del request
    details = [
        {
            "location": list(error["loc"]),
            "message": error["msg"],
        }
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "message": "Dữ liệu yêu cầu không hợp lệ.",
            "details": details,
        },
    )


@app.exception_handler(HTTPException)
async def http_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    del request
    if isinstance(exc.detail, dict):
        message = exc.detail.get("message", "Yêu cầu không thể xử lý.")
        details = exc.detail.get("details")
    else:
        message = str(exc.detail)
        details = None
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": message,
            "details": details,
        },
        headers=exc.headers,
    )


@app.exception_handler(Exception)
async def unexpected_error_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception(
        "Unhandled API error for %s %s",
        request.method,
        request.url.path,
        exc_info=exc,
    )
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Đã xảy ra lỗi nội bộ khi xử lý yêu cầu.",
            "details": None,
        },
    )


def _input_error(message: str, details: list[str] | None = None) -> HTTPException:
    return HTTPException(
        status_code=422,
        detail={"message": message, "details": details},
    )


def _explicit_fields(model: BaseModel) -> set[str]:
    return model.model_fields_set


def _validate_parameter_fields(
    scenario: str, parameters: SimulationParameters
) -> dict[str, Any]:
    allowed_fields = {
        "normal": {
            "num_periods",
            "base_occ",
            "noise_std",
            "sample_interval",
            "seed",
        },
        "incident": {
            "num_periods",
            "base_occ",
            "noise_std",
            "incident_start",
            "incident_duration",
            "occ_up_peak",
            "occ_down_drop",
            "ramp_up_periods",
            "ramp_down_periods",
            "sample_interval",
            "seed",
        },
        "edge_congestion": {
            "num_periods",
            "base_occ",
            "noise_std",
            "congestion_start",
            "congestion_duration",
            "congestion_occ",
            "sample_interval",
            "seed",
        },
    }[scenario]
    provided_fields = _explicit_fields(parameters)
    unsupported_fields = sorted(provided_fields - allowed_fields)
    if unsupported_fields:
        raise _input_error(
            f"Các tham số không áp dụng cho kịch bản '{scenario}'.",
            unsupported_fields,
        )

    null_fields = sorted(
        name for name in provided_fields if getattr(parameters, name) is None
    )
    if null_fields:
        raise _input_error(
            "Tham số đã gửi không được để null.",
            null_fields,
        )
    return parameters.model_dump(exclude_unset=True)


def _validate_scenario_bounds(
    scenario: str, parameters: dict[str, Any]
) -> None:
    num_periods = parameters.get(
        "num_periods", 60 if scenario == "edge_congestion" else 120
    )
    if scenario == "incident":
        start = parameters.get("incident_start", 40)
        duration = parameters.get("incident_duration", 30)
        if start + duration > num_periods:
            raise _input_error(
                "incident_start + incident_duration không được vượt num_periods."
            )
    elif scenario == "edge_congestion":
        start = parameters.get("congestion_start", 15)
        if start >= num_periods:
            raise _input_error(
                "congestion_start phải nhỏ hơn num_periods để có dữ liệu ùn tắc."
            )


def _incident_intervals(records: list[simulator.TrafficRecord]) -> list[metrics.Incident]:
    incidents: list[metrics.Incident] = []
    start: int | None = None
    end: int | None = None

    for record in records:
        if record.incident:
            if start is None:
                start = record.timestamp
            end = record.timestamp
        elif start is not None and end is not None:
            incidents.append(
                metrics.Incident(
                    start=float(start),
                    end=float(end),
                    id=f"incident-{len(incidents) + 1}",
                )
            )
            start = None
            end = None

    if start is not None and end is not None:
        incidents.append(
            metrics.Incident(
                start=float(start),
                end=float(end),
                id=f"incident-{len(incidents) + 1}",
            )
        )
    return incidents


def _evaluation_response(summary: dict[str, Any]) -> EvaluationResponse:
    unavailable = [
        key for key in ("dr", "far", "ttd") if summary[key] is None
    ]
    return EvaluationResponse(
        status="partial" if unavailable else "complete",
        n_incidents=summary["n_incidents"],
        tp=summary["tp"],
        fn=summary["fn"],
        fp=summary["fp"],
        repeated_alarms=summary["repeated_alarms"],
        dr=summary["dr"],
        far=summary["far"],
        far_definition=summary["far_definition"],
        ttd=summary["ttd"],
        ttd_statistic=summary["ttd_statistic"],
        unavailable_metrics=unavailable,
    )


@app.get(
    "/api/health",
    summary="Kiểm tra trạng thái API",
    description="Trả trạng thái hoạt động và tên dịch vụ.",
)
def health() -> dict[str, str]:
    return {"status": "ok", "service": "ITSgrXM"}


@app.post(
    "/api/simulations",
    response_model=SimulationResponse,
    summary="Mô phỏng và phát hiện sự cố",
    description=(
        "Sinh một kịch bản được hỗ trợ, chạy CaliforniaAlgorithm trên từng mẫu, "
        "và trả cả nhãn mô phỏng cùng kết quả dự đoán."
    ),
)
def run_simulation(request: SimulationRequest) -> SimulationResponse:
    parameters = _validate_parameter_fields(request.scenario, request.parameters)
    _validate_scenario_bounds(request.scenario, parameters)
    algorithm_parameters = request.algorithm.model_dump(exclude_unset=True)
    null_algorithm_fields = sorted(
        name
        for name in _explicit_fields(request.algorithm)
        if getattr(request.algorithm, name) is None
    )
    if null_algorithm_fields:
        raise _input_error(
            "Tham số thuật toán đã gửi không được để null.",
            null_algorithm_fields,
        )

    generator = {
        "normal": simulator.generate_normal,
        "incident": simulator.generate_incident,
        "edge_congestion": simulator.generate_edge_case,
    }[request.scenario]

    try:
        result = generator(**parameters)
    except ValueError as exc:
        raise _input_error(str(exc)) from exc

    algorithm = CaliforniaAlgorithm(**algorithm_parameters)
    detection_times: list[int] = []
    records: list[RecordResult] = []
    previously_detected = False
    for record in result.records:
        detected = algorithm.evaluate(record.occ_up, record.occ_down)
        if detected and not previously_detected:
            detection_times.append(record.timestamp)
        records.append(
            RecordResult(
                timestamp=record.timestamp,
                occ_up=record.occ_up,
                occ_down=record.occ_down,
                actual_incident=record.incident,
                detected=detected,
            )
        )
        previously_detected = detected

    incidents = _incident_intervals(result.records)
    try:
        evaluation = _evaluation_response(
            metrics.summarize(
                incidents,
                detection_times,
                far_definition=metrics.FAR_PER_SAMPLE,
                n_non_incident_samples=sum(
                    not record.incident for record in result.records
                ),
            )
        )
    except ValueError as exc:
        logger.exception("Could not evaluate generated simulation")
        raise HTTPException(
            status_code=500,
            detail="Không thể đánh giá kết quả mô phỏng.",
        ) from exc

    response = SimulationResponse(
        status="success",
        scenario=request.scenario,
        description=result.description,
        sample_interval=result.sample_interval,
        incident_start=result.incident_start,
        incident_end=result.incident_end,
        seed=result.seed,
        detection_times=detection_times,
        evaluation=evaluation,
        records=records,
    )
    app.state.latest_simulation = DashboardSimulation(
        scenario=response.scenario,
        description=response.description,
        record_count=len(response.records),
        sample_interval=response.sample_interval,
        seed=response.seed,
        detection_count=len(response.detection_times),
        evaluation=response.evaluation,
    )
    app.state.latest_evaluation = response.evaluation
    return response


@app.post(
    "/api/evaluations",
    response_model=EvaluationResponse,
    summary="Đánh giá kết quả phát hiện",
    description=(
        "Nhận các khoảng sự cố tham chiếu và thời điểm cảnh báo, "
        "sau đó gọi các hàm trong src.metrics."
    ),
)
def evaluate_detection(request: EvaluationRequest) -> EvaluationResponse:
    if (
        request.far_definition == metrics.FAR_PER_SAMPLE
        and request.n_non_incident_samples is None
    ):
        raise _input_error(
            "Cần n_non_incident_samples khi far_definition là 'per_sample'."
        )
    if (
        request.far_definition == metrics.FAR_PER_HOUR
        and request.monitoring_hours is None
    ):
        raise _input_error(
            "Cần monitoring_hours khi far_definition là 'per_hour'."
        )

    incidents: list[metrics.Incident] = []
    for index, incident in enumerate(request.incidents):
        if incident.end < incident.start:
            raise _input_error(
                f"incidents[{index}].end phải lớn hơn hoặc bằng start."
            )
        incidents.append(
            metrics.Incident(
                start=incident.start,
                end=incident.end,
                id=incident.id,
            )
        )

    try:
        summary = metrics.summarize(
            incidents=incidents,
            alarms=request.alarms,
            tolerance=request.tolerance,
            far_definition=request.far_definition,
            n_non_incident_samples=request.n_non_incident_samples,
            monitoring_hours=request.monitoring_hours,
            ttd_statistic=request.ttd_statistic,
        )
    except ValueError as exc:
        raise _input_error(str(exc)) from exc

    response = _evaluation_response(summary)
    app.state.latest_evaluation = response
    return response


@app.get(
    "/api/dashboard",
    response_model=DashboardResponse,
    summary="Lấy dữ liệu tổng quan",
    description=(
        "Trả kết quả mô phỏng/đánh giá gần nhất của tiến trình hiện tại; "
        "không tạo số liệu giả và không lưu bền vững."
    ),
)
def dashboard() -> DashboardResponse:
    latest_simulation = app.state.latest_simulation
    latest_evaluation = app.state.latest_evaluation
    has_data = latest_simulation is not None or latest_evaluation is not None
    return DashboardResponse(
        status="available" if has_data else "no_data",
        data_source="in_memory_api_requests",
        message=(
            None
            if has_data
            else "Chưa có mô phỏng hoặc đánh giá nào được thực hiện trong tiến trình này."
        ),
        latest_simulation=latest_simulation,
        latest_evaluation=latest_evaluation,
    )
