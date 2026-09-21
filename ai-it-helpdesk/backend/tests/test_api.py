from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():

    response = client.get("/api/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"


def test_start_network_diagnosis():

    response = client.post(
        "/api/diagnosis/start",
        json={
            "category": "Network",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "session_id" in data
    assert data["category"] == "Network"
    assert data["status"] == "question_required"

    assert data["question"]["id"] == "NET-Q001"


def test_invalid_category_is_rejected():

    response = client.post(
        "/api/diagnosis/start",
        json={
            "category": "Gaming",
        },
    )

    assert response.status_code == 400


def test_valid_answer_completes_wifi_diagnosis():

    start_response = client.post(
        "/api/diagnosis/start",
        json={
            "category": "Network",
        },
    )

    start_data = start_response.json()

    session_id = start_data["session_id"]
    question_id = start_data["question"]["id"]

    response = client.post(
        f"/api/diagnosis/{session_id}/answer",
        json={
            "question_id": question_id,
            "fact": "wifi_disconnected",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "diagnosed"

    assert (
        data["diagnoses"][0]["code"]
        == "NET-WIFI-001"
    )


def test_invalid_fact_is_rejected():

    start_response = client.post(
        "/api/diagnosis/start",
        json={
            "category": "Network",
        },
    )

    start_data = start_response.json()

    session_id = start_data["session_id"]
    question_id = start_data["question"]["id"]

    response = client.post(
        f"/api/diagnosis/{session_id}/answer",
        json={
            "question_id": question_id,
            "fact": "dns_resolution_failed",
        },
    )

    assert response.status_code == 400


def test_nonexistent_session_is_rejected():

    response = client.post(
        "/api/diagnosis/nonexistent-session/answer",
        json={
            "question_id": "NET-Q001",
            "fact": "wifi_connected",
        },
    )

    assert response.status_code == 404

def test_question_selection_reason_is_returned():
    start_response = client.post(
        "/api/diagnosis/start",
        json={
            "category": "Network",
        },
    )

    assert start_response.status_code == 200

    data = start_response.json()

    assert data["question"]["id"] == "NET-Q001"

    assert "selection_reason" in data
    assert data["selection_reason"] is not None

def test_diagnosis_response_contains_forward_and_backward_inference():
    start_response = client.post(
        "/api/diagnosis/start",
        json={"category": "Network"},
    )

    assert start_response.status_code == 200

    session = start_response.json()
    session_id = session["session_id"]

    # Wi-Fi connected
    response = client.post(
        f"/api/diagnosis/{session_id}/answer",
        json={
            "question_id": session["question"]["id"],
            "fact": "wifi_connected",
        },
    )

    assert response.status_code == 200

    # Continue the diagnostic path until a diagnosis is reached.
    while response.json()["status"] == "question_required":

        data = response.json()
        question = data["question"]

        # Select the appropriate facts for the DNS-failure path.
        fact_by_question = {
            "NET-Q002": "ip_address_valid",
            "NET-Q003": "gateway_reachable",
            "NET-Q004": "dns_resolution_failed",
        }

        question_id = question["id"]

        assert question_id in fact_by_question

        response = client.post(
            f"/api/diagnosis/{session_id}/answer",
            json={
                "question_id": question_id,
                "fact": fact_by_question[question_id],
            },
        )

        assert response.status_code == 200

    data = response.json()

    assert data["status"] == "diagnosed"

    assert "forward_inference" in data
    assert "backward_inference" in data

    assert data["forward_inference"] is not None
    assert isinstance(data["backward_inference"], list)

    assert len(data["backward_inference"]) > 0