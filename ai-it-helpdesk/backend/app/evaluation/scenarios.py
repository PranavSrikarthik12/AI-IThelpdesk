from dataclasses import dataclass


@dataclass
class EvaluationScenario:
    id: str
    name: str
    category: str
    facts: set[str]
    expected_diagnosis: str


SCENARIOS = [

    EvaluationScenario(
        id="NET-EVAL-001",
        name="Wi-Fi disconnected",
        category="Network",
        facts={
            "wifi_disconnected",
        },
        expected_diagnosis="wifi_connection_problem",
    ),

    EvaluationScenario(
        id="NET-EVAL-002",
        name="DHCP failure",
        category="Network",
        facts={
            "wifi_connected",
            "ip_address_invalid",
        },
        expected_diagnosis="dhcp_problem",
    ),

    EvaluationScenario(
        id="NET-EVAL-003",
        name="Gateway unreachable",
        category="Network",
        facts={
            "wifi_connected",
            "ip_address_valid",
            "gateway_unreachable",
        },
        expected_diagnosis="gateway_problem",
    ),

    EvaluationScenario(
        id="NET-EVAL-004",
        name="DNS resolution failure",
        category="Network",
        facts={
            "wifi_connected",
            "ip_address_valid",
            "gateway_reachable",
            "dns_resolution_failed",
        },
        expected_diagnosis="dns_failure",
    ),

    EvaluationScenario(
        id="NET-EVAL-005",
        name="ISP or upstream failure",
        category="Network",
        facts={
            "wifi_connected",
            "ip_address_valid",
            "gateway_reachable",
            "dns_working",
            "internet_unreachable",
        },
        expected_diagnosis="isp_or_upstream_problem",
    ),

    EvaluationScenario(
        id="SYS-EVAL-001",
        name="High CPU load",
        category="System Performance",
        facts={
            "cpu_usage_high",
            "many_background_processes",
        },
        expected_diagnosis="high_cpu_load",
    ),

    EvaluationScenario(
        id="SYS-EVAL-002",
        name="Memory pressure",
        category="System Performance",
        facts={
            "memory_usage_high",
            "many_background_processes",
        },
        expected_diagnosis="memory_pressure",
    ),

    EvaluationScenario(
        id="SYS-EVAL-003",
        name="Insufficient storage",
        category="System Performance",
        facts={
            "disk_space_low",
        },
        expected_diagnosis="insufficient_storage",
    ),

    EvaluationScenario(
        id="AUTH-EVAL-001",
        name="Invalid credentials",
        category="Authentication",
        facts={
            "login_failed",
            "credentials_invalid",
        },
        expected_diagnosis="invalid_credentials",
    ),

    EvaluationScenario(
        id="AUTH-EVAL-002",
        name="Locked account",
        category="Authentication",
        facts={
            "login_failed",
            "account_locked",
        },
        expected_diagnosis="locked_account",
    ),

    EvaluationScenario(
        id="AUTH-EVAL-003",
        name="Expired password",
        category="Authentication",
        facts={
            "login_failed",
            "password_expired",
        },
        expected_diagnosis="expired_password",
    ),
]