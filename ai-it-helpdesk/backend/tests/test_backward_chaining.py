from app.engine.backward_chaining import BackwardChainingEngine
from app.knowledge.knowledge_base import KnowledgeBase
from app.knowledge.rules import NETWORK_RULES


def test_dns_failure_can_be_proved():

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

    engine = BackwardChainingEngine()

    result = engine.run(
        knowledge_base=knowledge_base,
        goal="dns_failure",
    )

    assert "dns_failure" in result.derived_facts
    assert "NET-004" in result.fired_rules


def test_dns_failure_cannot_be_proved_without_dns_failure_fact():

    facts = {
        "wifi_connected",
        "ip_address_valid",
        "gateway_reachable",
    }

    knowledge_base = KnowledgeBase(
        facts=facts,
        rules=NETWORK_RULES,
    )

    engine = BackwardChainingEngine()

    result = engine.run(
        knowledge_base=knowledge_base,
        goal="dns_failure",
    )

    assert "dns_failure" not in result.derived_facts
    assert "NET-004" not in result.fired_rules


def test_dhcp_problem_can_be_proved():

    facts = {
        "wifi_connected",
        "ip_address_invalid",
    }

    knowledge_base = KnowledgeBase(
        facts=facts,
        rules=NETWORK_RULES,
    )

    engine = BackwardChainingEngine()

    result = engine.run(
        knowledge_base=knowledge_base,
        goal="dhcp_problem",
    )

    assert "dhcp_problem" in result.derived_facts
    assert "NET-002" in result.fired_rules