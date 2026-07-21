"""Regression tests for the telemetry ingest endpoint (Week-3 stub).

Covers the two behaviours the router actually owns: quality-based
classification (accepted vs quarantined) and contract validation at the
boundary (422 for anything that violates ``iot-measurement.v1.json``).

The endpoint does not touch the database, so ``TestClient(app)`` is used
without its context manager on purpose — that skips the app lifespan and
avoids creating a SQLite file just to exercise pure request validation.
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

INGEST_URL = "/api/v1/telemetry/ingest"


def valid_measurement(**overrides) -> dict:
    """A contract-valid measurement in the camelCase wire format."""
    payload = {
        "messageId": "m-1",
        "deviceId": "sim-gateway-plot-001",
        "plotId": "plot-001",
        "sensorType": "air_temperature",
        "value": 24.5,
        "unit": "celsius",
        "measuredAt": "2026-07-19T10:00:00Z",
        "quality": "valid",
    }
    payload.update(overrides)
    return payload


# ── Classification (accepted / quarantined) ──────────────────────────────────


def test_valid_reading_is_accepted():
    resp = client.post(INGEST_URL, json=valid_measurement())
    assert resp.status_code == 202
    body = resp.json()
    assert body["status"] == "accepted"
    assert body["messageId"] == "m-1"
    assert body["reason"] is None


def test_suspect_reading_is_quarantined():
    resp = client.post(INGEST_URL, json=valid_measurement(quality="suspect"))
    assert resp.status_code == 202
    body = resp.json()
    assert body["status"] == "quarantined"
    assert body["reason"] == "quality=suspect"


def test_invalid_reading_is_quarantined():
    resp = client.post(INGEST_URL, json=valid_measurement(quality="invalid"))
    assert resp.status_code == 202
    body = resp.json()
    assert body["status"] == "quarantined"
    assert body["reason"] == "quality=invalid"


# ── Contract validation (422) ────────────────────────────────────────────────


def test_missing_required_field_is_rejected():
    payload = valid_measurement()
    del payload["messageId"]
    resp = client.post(INGEST_URL, json=payload)
    assert resp.status_code == 422


def test_sensor_type_outside_enum_is_rejected():
    resp = client.post(INGEST_URL, json=valid_measurement(sensorType="pressure"))
    assert resp.status_code == 422


def test_quality_outside_enum_is_rejected():
    resp = client.post(INGEST_URL, json=valid_measurement(quality="unknown"))
    assert resp.status_code == 422


def test_unknown_field_is_rejected():
    # contract sets additionalProperties: false → schema uses extra="forbid".
    resp = client.post(INGEST_URL, json=valid_measurement(rogueField="x"))
    assert resp.status_code == 422


def test_non_numeric_value_is_rejected():
    resp = client.post(INGEST_URL, json=valid_measurement(value="hot"))
    assert resp.status_code == 422
