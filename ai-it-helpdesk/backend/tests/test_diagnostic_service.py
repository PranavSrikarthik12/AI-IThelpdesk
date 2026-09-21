from app.services.diagnostic_service import DiagnosticService


def test_forward_diagnosis_returns_dns_failure():

    facts = {
        "wifi_connected",
        "ip_address_valid",
        "gateway_reachable",
        "dns_resolution_failed",
    }

    service = DiagnosticService()

    result, diagnoses = service.diagnose_forward(facts)

    assert "dns_failure" in result.derived_facts

    assert len(diagnoses) == 1

    diagnosis = diagnoses[0]

    assert diagnosis.code == "NET-DNS-001"
    assert diagnosis.category == "Network"
    assert diagnosis.title == "DNS Resolution Failure"


def test_forward_diagnosis_returns_dhcp_problem():

    facts = {
        "wifi_connected",
        "ip_address_invalid",
    }

    service = DiagnosticService()

    result, diagnoses = service.diagnose_forward(facts)

    assert "dhcp_problem" in result.derived_facts

    assert len(diagnoses) == 1

    assert diagnoses[0].code == "NET-DHCP-001"


def test_backward_diagnosis_returns_dns_failure():

    facts = {
        "wifi_connected",
        "ip_address_valid",
        "gateway_reachable",
        "dns_resolution_failed",
    }

    service = DiagnosticService()

    result, diagnosis = service.diagnose_backward(
        facts=facts,
        goal="dns_failure",
    )

    assert diagnosis is not None
    assert diagnosis.code == "NET-DNS-001"


def test_backward_diagnosis_returns_none_when_goal_not_proved():

    facts = {
        "wifi_connected",
        "ip_address_valid",
        "gateway_reachable",
    }

    service = DiagnosticService()

    result, diagnosis = service.diagnose_backward(
        facts=facts,
        goal="dns_failure",
    )

    assert diagnosis is None