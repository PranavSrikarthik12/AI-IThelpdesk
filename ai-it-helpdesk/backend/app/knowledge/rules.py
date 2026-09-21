from app.models.rule import Rule


NETWORK_RULES = [
    Rule(
        id="NET-001",
        conditions=[
            "wifi_disconnected",
        ],
        conclusion="wifi_connection_problem",
        explanation=(
            "The device is not connected to Wi-Fi, "
            "so network connectivity cannot be established."
        ),
    ),

    Rule(
        id="NET-002",
        conditions=[
            "wifi_connected",
            "ip_address_invalid",
        ],
        conclusion="dhcp_problem",
        explanation=(
            "The device is connected to Wi-Fi but does not have "
            "a valid IP address, indicating a possible DHCP problem."
        ),
    ),

    Rule(
        id="NET-003",
        conditions=[
            "wifi_connected",
            "ip_address_valid",
            "gateway_unreachable",
        ],
        conclusion="gateway_problem",
        explanation=(
            "The device has a valid IP address but cannot reach "
            "the network gateway."
        ),
    ),

    Rule(
        id="NET-004",
        conditions=[
            "wifi_connected",
            "ip_address_valid",
            "gateway_reachable",
            "dns_resolution_failed",
        ],
        conclusion="dns_failure",
        explanation=(
            "The network connection and gateway are working, "
            "but DNS resolution is failing."
        ),
    ),

    Rule(
        id="NET-006",
        conditions=[
            "wifi_connected",
            "ip_address_valid",
        ],
        conclusion="local_network_configured",
        explanation=(
            "The device is connected to Wi-Fi and has a valid IP address, "
            "indicating that the local network configuration is established."
        ),
    ),

    Rule(
        id="NET-007",
        conditions=[
            "local_network_configured",
            "gateway_reachable",
        ],
        conclusion="local_network_reachable",
        explanation=(
            "The device has a valid local network configuration and can "
            "reach the gateway, indicating local network connectivity."
        ),
    ),

    Rule(
        id="NET-008",
        conditions=[
            "local_network_reachable",
            "dns_working",
        ],
        conclusion="network_services_operational",
        explanation=(
            "The local network and DNS services are operational, "
            "indicating that the essential local network services are working."
        ),
    ),

    Rule(
        id="NET-005",
        conditions=[
            "network_services_operational",
            "internet_unreachable",
        ],
        conclusion="isp_or_upstream_problem",
        explanation=(
            "The local network and essential network services are "
            "operational, but the internet remains unreachable, "
            "suggesting an upstream issue."
        ),
    ),
]


SYSTEM_RULES = [
    Rule(
        id="SYS-001",
        conditions=[
            "cpu_usage_high",
            "many_background_processes",
        ],
        conclusion="high_cpu_load",
        explanation=(
            "High CPU usage combined with many background "
            "processes indicates excessive CPU load."
        ),
    ),

    Rule(
        id="SYS-002",
        conditions=[
            "memory_usage_high",
            "many_background_processes",
        ],
        conclusion="memory_pressure",
        explanation=(
            "High memory usage combined with many background "
            "processes indicates memory pressure."
        ),
    ),

    Rule(
        id="SYS-003",
        conditions=[
            "disk_space_low",
        ],
        conclusion="insufficient_storage",
        explanation=(
            "Available disk space is below the configured threshold."
        ),
    ),
]


AUTHENTICATION_RULES = [
    Rule(
        id="AUTH-001",
        conditions=[
            "login_failed",
            "credentials_invalid",
        ],
        conclusion="invalid_credentials",
        explanation=(
            "The login attempt failed and the supplied credentials "
            "were identified as invalid."
        ),
    ),

    Rule(
        id="AUTH-002",
        conditions=[
            "login_failed",
            "account_locked",
        ],
        conclusion="locked_account",
        explanation=(
            "The login attempt failed because the account is locked."
        ),
    ),

    Rule(
        id="AUTH-003",
        conditions=[
            "login_failed",
            "password_expired",
        ],
        conclusion="expired_password",
        explanation=(
            "The login attempt failed because the account password "
            "has expired."
        ),
    ),
]


ALL_RULES = (
    NETWORK_RULES
    + SYSTEM_RULES
    + AUTHENTICATION_RULES
)