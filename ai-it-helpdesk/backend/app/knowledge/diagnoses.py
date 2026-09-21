from app.models.diagnosis import Diagnosis, RecommendedAction


DIAGNOSES = {
    "wifi_connection_problem": Diagnosis(
        code="NET-WIFI-001",
        category="Network",
        title="Wi-Fi Connection Problem",
        description=(
            "The device is not connected to a Wi-Fi network."
        ),
        severity="Medium",
        recommended_actions=[
            RecommendedAction(
                step=1,
                description="Check whether Wi-Fi is enabled on the device.",
            ),
            RecommendedAction(
                step=2,
                description="Check whether the correct wireless network is selected.",
            ),
            RecommendedAction(
                step=3,
                description="Reconnect to the Wi-Fi network.",
            ),
            RecommendedAction(
                step=4,
                description="Restart the wireless adapter if the problem persists.",
            ),
        ],
    ),

    "dhcp_problem": Diagnosis(
        code="NET-DHCP-001",
        category="Network",
        title="DHCP / IP Configuration Problem",
        description=(
            "The device is connected to Wi-Fi but does not appear "
            "to have a valid IP address."
        ),
        severity="High",
        recommended_actions=[
            RecommendedAction(
                step=1,
                description="Disconnect and reconnect to the Wi-Fi network.",
            ),
            RecommendedAction(
                step=2,
                description="Renew the device's DHCP lease.",
            ),
            RecommendedAction(
                step=3,
                description="Check the network adapter configuration.",
            ),
            RecommendedAction(
                step=4,
                description="Restart the router if multiple devices are affected.",
            ),
        ],
    ),

    "gateway_problem": Diagnosis(
        code="NET-GW-001",
        category="Network",
        title="Gateway Connectivity Problem",
        description=(
            "The device has a valid IP address but cannot communicate "
            "with the network gateway."
        ),
        severity="High",
        recommended_actions=[
            RecommendedAction(
                step=1,
                description="Check the configured default gateway.",
            ),
            RecommendedAction(
                step=2,
                description="Reconnect to the network.",
            ),
            RecommendedAction(
                step=3,
                description="Restart the router or access point.",
            ),
            RecommendedAction(
                step=4,
                description="Check whether other devices can reach the gateway.",
            ),
        ],
    ),

    "dns_failure": Diagnosis(
        code="NET-DNS-001",
        category="Network",
        title="DNS Resolution Failure",
        description=(
            "The device has network connectivity, but domain names "
            "cannot be resolved."
        ),
        severity="Medium",
        recommended_actions=[
            RecommendedAction(
                step=1,
                description="Flush the local DNS cache.",
            ),
            RecommendedAction(
                step=2,
                description="Check the configured DNS servers.",
            ),
            RecommendedAction(
                step=3,
                description="Test DNS resolution using another DNS server.",
            ),
            RecommendedAction(
                step=4,
                description="Restart the network adapter if necessary.",
            ),
        ],
    ),

    "isp_or_upstream_problem": Diagnosis(
        code="NET-ISP-001",
        category="Network",
        title="Possible ISP or Upstream Network Problem",
        description=(
            "The local network, gateway, and DNS appear to be working, "
            "but internet connectivity is still unavailable."
        ),
        severity="High",
        recommended_actions=[
            RecommendedAction(
                step=1,
                description="Check whether other devices have internet access.",
            ),
            RecommendedAction(
                step=2,
                description="Check the router's internet/WAN status.",
            ),
            RecommendedAction(
                step=3,
                description="Restart the router if appropriate.",
            ),
            RecommendedAction(
                step=4,
                description="Contact the internet service provider if the outage persists.",
            ),
        ],
    ),

    "high_cpu_load": Diagnosis(
        code="SYS-CPU-001",
        category="System Performance",
        title="High CPU Load",
        description=(
            "High CPU utilization combined with many background "
            "processes may be causing system slowdown."
        ),
        severity="Medium",
        recommended_actions=[
            RecommendedAction(
                step=1,
                description="Open the system task manager.",
            ),
            RecommendedAction(
                step=2,
                description="Identify processes consuming excessive CPU.",
            ),
            RecommendedAction(
                step=3,
                description="Close unnecessary applications.",
            ),
            RecommendedAction(
                step=4,
                description="Restart the system if the high CPU usage persists.",
            ),
        ],
    ),

    "memory_pressure": Diagnosis(
        code="SYS-MEM-001",
        category="System Performance",
        title="High Memory Usage",
        description=(
            "High memory utilization and numerous background processes "
            "may be causing system performance problems."
        ),
        severity="Medium",
        recommended_actions=[
            RecommendedAction(
                step=1,
                description="Check memory usage in the task manager.",
            ),
            RecommendedAction(
                step=2,
                description="Close applications that are not required.",
            ),
            RecommendedAction(
                step=3,
                description="Reduce unnecessary startup applications.",
            ),
            RecommendedAction(
                step=4,
                description="Restart the system if memory usage remains unusually high.",
            ),
        ],
    ),

    "insufficient_storage": Diagnosis(
        code="SYS-DISK-001",
        category="System Performance",
        title="Insufficient Disk Space",
        description=(
            "The available storage space is too low for normal operation."
        ),
        severity="Medium",
        recommended_actions=[
            RecommendedAction(
                step=1,
                description="Check which files and applications are using disk space.",
            ),
            RecommendedAction(
                step=2,
                description="Remove unnecessary temporary files.",
            ),
            RecommendedAction(
                step=3,
                description="Uninstall unused applications.",
            ),
            RecommendedAction(
                step=4,
                description="Move large personal files to external or cloud storage.",
            ),
        ],
    ),
        "invalid_credentials": Diagnosis(
        code="AUTH-CRED-001",
        category="Authentication",
        title="Invalid Credentials",
        description=(
            "The login attempt failed because the provided credentials "
            "appear to be invalid."
        ),
        severity="Medium",
        recommended_actions=[
            RecommendedAction(
                step=1,
                description="Verify that the username or email address is correct.",
            ),
            RecommendedAction(
                step=2,
                description="Re-enter the password carefully.",
            ),
            RecommendedAction(
                step=3,
                description="Use the password reset option if the password is forgotten.",
            ),
            RecommendedAction(
                step=4,
                description="Contact the system administrator if the credentials remain invalid.",
            ),
        ],
    ),

    "locked_account": Diagnosis(
        code="AUTH-LOCK-001",
        category="Authentication",
        title="Account Locked",
        description=(
            "The account is locked and cannot be used to complete "
            "the current login attempt."
        ),
        severity="High",
        recommended_actions=[
            RecommendedAction(
                step=1,
                description="Check whether the account has been locked due to repeated failed login attempts.",
            ),
            RecommendedAction(
                step=2,
                description="Wait for the account lockout period to expire if applicable.",
            ),
            RecommendedAction(
                step=3,
                description="Use the account recovery or unlock procedure.",
            ),
            RecommendedAction(
                step=4,
                description="Contact the system administrator if the account remains locked.",
            ),
        ],
    ),

    "expired_password": Diagnosis(
        code="AUTH-PASS-001",
        category="Authentication",
        title="Password Expired",
        description=(
            "The account password has expired and must be changed "
            "before authentication can continue."
        ),
        severity="Medium",
        recommended_actions=[
            RecommendedAction(
                step=1,
                description="Use the password change option provided by the authentication system.",
            ),
            RecommendedAction(
                step=2,
                description="Set a new password that satisfies the required password policy.",
            ),
            RecommendedAction(
                step=3,
                description="Sign in again using the updated password.",
            ),
            RecommendedAction(
                step=4,
                description="Contact the system administrator if the password cannot be changed.",
            ),
        ],
    ),
}