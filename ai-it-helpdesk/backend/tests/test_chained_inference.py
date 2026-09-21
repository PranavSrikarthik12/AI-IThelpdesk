from app.engine.forward_chaining import ForwardChainingEngine
from app.engine.backward_chaining import BackwardChainingEngine
from app.knowledge.knowledge_base import KnowledgeBase
from app.models.rule import Rule


CHAINED_RULES = [
    Rule(
        id="TEST-001",
        conditions=["device_powered"],
        conclusion="wifi_adapter_enabled",
        explanation="A powered device enables the network adapter.",
    ),
    Rule(
        id="TEST-002",
        conditions=["wifi_adapter_enabled"],
        conclusion="wifi_connected",
        explanation="An enabled adapter establishes the Wi-Fi connection.",
    ),
    Rule(
        id="TEST-003",
        conditions=[
            "wifi_connected",
            "ip_address_valid",
        ],
        conclusion="network_ready",
        explanation="A connected device with a valid IP is network ready.",
    ),
]


def test_forward_chaining_can_follow_multiple_rules():

    facts = {
        "device_powered",
        "ip_address_valid",
    }

    knowledge_base = KnowledgeBase(
        facts=facts,
        rules=CHAINED_RULES,
    )

    engine = ForwardChainingEngine()

    result = engine.run(knowledge_base)

    assert "wifi_adapter_enabled" in result.derived_facts
    assert "wifi_connected" in result.derived_facts
    assert "network_ready" in result.derived_facts


def test_backward_chaining_can_follow_multiple_rules():

    facts = {
        "device_powered",
        "ip_address_valid",
    }

    knowledge_base = KnowledgeBase(
        facts=facts,
        rules=CHAINED_RULES,
    )

    engine = BackwardChainingEngine()

    result = engine.run(
        knowledge_base=knowledge_base,
        goal="network_ready",
    )

    assert "network_ready" in result.derived_facts