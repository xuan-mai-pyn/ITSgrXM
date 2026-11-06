from fastapi.testclient import TestClient

from src import api, metrics
from src.california import CaliforniaAlgorithm

client = TestClient(api.app, raise_server_exceptions=False)


def setup_function() -> None:
    api.app.state.latest_simulation = None
    api.app.state.latest_evaluation = None


def test_health_returns_service_status() -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "ITSgrXM"}


def test_simulation_rejects_unknown_scenario_and_invalid_parameters() -> None:
    invalid_scenario = client.post(
        "/api/simulations",
        json={"scenario": "unknown"},
    )
    invalid_parameters = client.post(
        "/api/simulations",
        json={"scenario": "normal", "parameters": {"num_periods": 0}},
    )

    assert invalid_scenario.status_code == 422
    assert invalid_scenario.json()["status"] == "error"
    assert invalid_parameters.status_code == 422
    assert invalid_parameters.json()["status"] == "error"


def test_simulation_rejects_parameters_not_supported_by_scenario() -> None:
    response = client.post(
        "/api/simulations",
        json={
            "scenario": "normal",
            "parameters": {"incident_start": 2},
        },
    )

    assert response.status_code == 422
    assert "incident_start" in response.json()["details"]


def test_simulation_returns_recorded_data_and_california_results() -> None:
    response = client.post(
        "/api/simulations",
        json={
            "scenario": "incident",
            "parameters": {
                "num_periods": 20,
                "incident_start": 5,
                "incident_duration": 8,
                "seed": 17,
            },
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "success"
    assert payload["scenario"] == "incident"
    assert len(payload["records"]) == 20
    assert any(record["actual_incident"] for record in payload["records"])

    algorithm = CaliforniaAlgorithm()
    expected_detections = []
    was_detected = False
    for record in payload["records"]:
        detected = algorithm.evaluate(record["occ_up"], record["occ_down"])
        assert record["detected"] is detected
        if detected and not was_detected:
            expected_detections.append(record["timestamp"])
        was_detected = detected
    assert payload["detection_times"] == expected_detections


def test_evaluation_uses_metrics_module_and_reports_partial_results() -> None:
    request = {
        "incidents": [{"start": 10, "end": 20, "id": "event-1"}],
        "alarms": [12, 15, 30],
        "far_definition": "per_sample",
        "n_non_incident_samples": 100,
    }
    response = client.post("/api/evaluations", json=request)
    expected = metrics.summarize(
        [metrics.Incident(start=10, end=20, id="event-1")],
        [12, 15, 30],
        far_definition=metrics.FAR_PER_SAMPLE,
        n_non_incident_samples=100,
    )

    assert response.status_code == 200
    result = response.json()
    for key in (
        "n_incidents",
        "tp",
        "fn",
        "fp",
        "repeated_alarms",
        "dr",
        "far",
        "ttd",
    ):
        assert result[key] == expected[key]
    assert result["status"] == "complete"

    no_incidents = client.post(
        "/api/evaluations",
        json={
            "incidents": [],
            "alarms": [],
            "far_definition": "ratio",
        },
    )
    assert no_incidents.status_code == 200
    assert no_incidents.json()["status"] == "partial"
    assert no_incidents.json()["dr"] is None
    assert no_incidents.json()["ttd"] is None


def test_evaluation_requires_denominator_for_selected_far_definition() -> None:
    response = client.post(
        "/api/evaluations",
        json={
            "incidents": [],
            "alarms": [],
            "far_definition": "per_sample",
        },
    )

    assert response.status_code == 422
    assert response.json()["status"] == "error"


def test_module_failure_returns_generic_error_without_success_fallback(
    monkeypatch,
) -> None:
    def fail_generation(**kwargs):
        raise RuntimeError("internal-secret-detail")

    monkeypatch.setattr(api.simulator, "generate_normal", fail_generation)
    response = client.post("/api/simulations", json={"scenario": "normal"})

    assert response.status_code == 500
    assert response.json()["status"] == "error"
    assert "internal-secret-detail" not in response.text
    assert api.app.state.latest_simulation is None


def test_dashboard_reflects_empty_and_completed_api_state() -> None:
    empty_dashboard = client.get("/api/dashboard")
    assert empty_dashboard.status_code == 200
    assert empty_dashboard.json()["status"] == "no_data"
    assert empty_dashboard.json()["latest_simulation"] is None

    simulation = client.post(
        "/api/simulations",
        json={
            "scenario": "normal",
            "parameters": {"num_periods": 5, "seed": 3},
        },
    )
    assert simulation.status_code == 200

    dashboard = client.get("/api/dashboard")
    assert dashboard.status_code == 200
    result = dashboard.json()
    assert result["status"] == "available"
    assert result["data_source"] == "in_memory_api_requests"
    assert result["latest_simulation"]["scenario"] == "normal"
    assert result["latest_simulation"]["record_count"] == 5
    assert result["latest_evaluation"] == simulation.json()["evaluation"]
