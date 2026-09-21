from app.services.question_service import QuestionService


def test_network_question_is_returned():

    service = QuestionService()

    question = service.get_next_question(
        facts=set(),
        asked_questions=[],
        category="Network",
    )

    assert question is not None
    assert question.category == "Network"


def test_answered_question_is_not_returned_again():

    service = QuestionService()

    question = service.get_next_question(
        facts=set(),
        asked_questions=["NET-Q001"],
        category="Network",
    )

    assert question is not None
    assert question.id != "NET-Q001"


def test_unknown_category_returns_none():

    service = QuestionService()

    question = service.get_next_question(
        facts=set(),
        asked_questions=[],
        category="Unknown",
    )

    assert question is None

def test_question_selection_uses_rule_relevance():
    service = QuestionService()

    facts = {
        "wifi_connected",
        "ip_address_valid",
        "gateway_reachable",
    }

    question = service.get_next_question(
        facts=facts,
        asked_questions=[
            "NET-Q001",
            "NET-Q002",
            "NET-Q003",
        ],
        category="Network",
    )

    assert question is not None
    assert question.id == "NET-Q004"

def test_question_selection_avoids_irrelevant_answered_questions():
    service = QuestionService()

    facts = {
        "wifi_connected",
        "ip_address_valid",
        "gateway_reachable",
        "dns_working",
    }

    question = service.get_next_question(
        facts=facts,
        asked_questions=[
            "NET-Q001",
            "NET-Q002",
            "NET-Q003",
            "NET-Q004",
        ],
        category="Network",
    )

    assert question is not None
    assert question.id == "NET-Q005"

def test_question_selection_distinguishes_remaining_network_rules():
    service = QuestionService()

    facts = {
        "wifi_connected",
        "ip_address_valid",
        "gateway_reachable",
    }

    question = service.get_next_question(
        facts=facts,
        asked_questions=[
            "NET-Q001",
            "NET-Q002",
            "NET-Q003",
        ],
        category="Network",
    )

    assert question is not None
    assert question.id == "NET-Q004"

def test_question_selection_prefers_internet_question_after_dns_is_known():
    service = QuestionService()

    facts = {
        "wifi_connected",
        "ip_address_valid",
        "gateway_reachable",
        "dns_working",
    }

    question = service.get_next_question(
        facts=facts,
        asked_questions=[
            "NET-Q001",
            "NET-Q002",
            "NET-Q003",
            "NET-Q004",
        ],
        category="Network",
    )

    assert question is not None
    assert question.id == "NET-Q005"

def test_question_selection_returns_none_when_no_rules_remain():
    service = QuestionService()

    facts = {
        "wifi_connection_problem",
        "dhcp_problem",
        "gateway_problem",
        "dns_failure",
        "isp_or_upstream_problem",
    }

    question = service.get_next_question(
        facts=facts,
        asked_questions=[],
        category="Network",
    )

    assert question is None