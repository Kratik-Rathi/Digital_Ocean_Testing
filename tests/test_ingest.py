def test_ingest_valid_payload(client):
    payload = {
        "service_name": "payments",
        "event_type": "payment.completed",
        "timestamp": "2024-01-15T10:30:00Z",
        "metadata": {"user_id": "u_123", "amount": 4900}
    }
    response = client.post("/ingest", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["service_name"] == "payments"
    assert data["event_type"] == "payment.completed"
    assert "id" in data
    assert "created_at" in data


def test_ingest_missing_service_name(client):
    payload = {
        "event_type": "payment.completed",
        "timestamp": "2024-01-15T10:30:00Z"
    }
    response = client.post("/ingest", json=payload)
    assert response.status_code == 422


def test_ingest_missing_event_type(client):
    payload = {
        "service_name": "payments",
        "timestamp": "2024-01-15T10:30:00Z"
    }
    response = client.post("/ingest", json=payload)
    assert response.status_code == 422


def test_ingest_invalid_timestamp(client):
    payload = {
        "service_name": "payments",
        "event_type": "payment.completed",
        "timestamp": "not-a-timestamp"
    }
    response = client.post("/ingest", json=payload)
    assert response.status_code == 422


def test_ingest_empty_service_name(client):
    payload = {
        "service_name": "   ",
        "event_type": "payment.completed",
        "timestamp": "2024-01-15T10:30:00Z"
    }
    response = client.post("/ingest", json=payload)
    assert response.status_code == 422


def test_ingest_without_metadata(client):
    payload = {
        "service_name": "payments",
        "event_type": "payment.completed",
        "timestamp": "2024-01-15T10:30:00Z"
    }
    response = client.post("/ingest", json=payload)
    assert response.status_code == 201
    assert response.json()["metadata"] is None
