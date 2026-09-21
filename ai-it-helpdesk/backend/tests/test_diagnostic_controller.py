from app.services.diagnostic_controller import DiagnosticController


def test_controller_asks_question_when_information_is_missing():

    controller = DiagnosticController()

    result = controller.evaluate(
        facts=set(),
        category="Network",
        asked_questions=[],
    )

    assert result["status"] == "question_required"
    assert result["next_question"] is not None


def test_controller_diagnoses_wifi_problem():

    controller = DiagnosticController()

    result = controller.evaluate(
        facts={
            "wifi_disconnected",
        },
        category="Network",
        asked_questions=[
            "NET-Q001",
        ],
    )

    assert result["status"] == "diagnosed"

    assert len(result["diagnoses"]) == 1

    assert (
        result["diagnoses"][0].code
        == "NET-WIFI-001"
    )


def test_controller_diagnoses_dns_problem():

    controller = DiagnosticController()

    result = controller.evaluate(
        facts={
            "wifi_connected",
            "ip_address_valid",
            "gateway_reachable",
            "dns_resolution_failed",
        },
        category="Network",
        asked_questions=[],
    )

    assert result["status"] == "diagnosed"

    assert (
        result["diagnoses"][0].code
        == "NET-DNS-001"
    )

def test_controller_returns_question_selection_reason():
    controller = DiagnosticController()

    result = controller.evaluate(
        facts={
            "wifi_connected",
            "ip_address_valid",
            "gateway_reachable",
        },
        category="Network",
        asked_questions=[
            "NET-Q001",
            "NET-Q002",
            "NET-Q003",
        ],
    )

    assert result["status"] == "question_required"
    assert result["next_question"].id == "NET-Q004"

    reason = result["selection_reason"]

    assert reason["rules_affected"] == 2
    assert "NET-004" in reason["affected_rules"]
    assert "NET-005" in reason["affected_rules"]