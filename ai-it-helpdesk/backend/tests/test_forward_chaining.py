from app.engine.forward_chaining import ForwardChainingEngine
from app.knowledge.knowledge_base import KnowledgeBase
from app.knowledge.rules import NETWORK_RULES


def test_dns_failure_diagnosis():

    facts = {
        "wifi_connected",
        "ip_address_valid",
        "gateway_reachable",
        "dns_resolution_failed",
    }

    knowledge_base = KnowledgeBase(
        facts=facts,
        rules=NETWORK_RULES,
    )

    engine = ForwardChainingEngine()

    result = engine.run(knowledge_base)

    assert "dns_failure" in result.derived_facts
    assert "NET-004" in result.fired_rules


def test_dhcp_problem_diagnosis():

    facts = {
        "wifi_connected",
        "ip_address_invalid",
    }

    knowledge_base = KnowledgeBase(
        facts=facts,
        rules=NETWORK_RULES,
    )

    engine = ForwardChainingEngine()

    result = engine.run(knowledge_base)

    assert "dhcp_problem" in result.derived_facts
    assert "NET-002" in result.fired_rules


def test_no_diagnosis_without_required_facts():

    facts = {
        "wifi_connected",
    }

    knowledge_base = KnowledgeBase(
        facts=facts,
        rules=NETWORK_RULES,
    )

    engine = ForwardChainingEngine()

    result = engine.run(knowledge_base)

    assert result.derived_facts == []
    assert result.fired_rules == []