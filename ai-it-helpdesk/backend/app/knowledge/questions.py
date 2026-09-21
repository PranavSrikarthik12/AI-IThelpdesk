from app.models.question import DiagnosticQuestion, QuestionOption


NETWORK_QUESTIONS = [
    DiagnosticQuestion(
        id="NET-Q001",
        text="Is the device connected to Wi-Fi?",
        category="Network",
        options=[
            QuestionOption(
                label="Yes",
                fact="wifi_connected",
            ),
            QuestionOption(
                label="No",
                fact="wifi_disconnected",
            ),
        ],
    ),

    DiagnosticQuestion(
        id="NET-Q002",
        text="Does the device have a valid IP address?",
        category="Network",
        options=[
            QuestionOption(
                label="Yes",
                fact="ip_address_valid",
            ),
            QuestionOption(
                label="No",
                fact="ip_address_invalid",
            ),
        ],
    ),

    DiagnosticQuestion(
        id="NET-Q003",
        text="Can the device reach the network gateway?",
        category="Network",
        options=[
            QuestionOption(
                label="Yes",
                fact="gateway_reachable",
            ),
            QuestionOption(
                label="No",
                fact="gateway_unreachable",
            ),
        ],
    ),

    DiagnosticQuestion(
        id="NET-Q004",
        text="Does DNS resolution work?",
        category="Network",
        options=[
            QuestionOption(
                label="Yes",
                fact="dns_working",
            ),
            QuestionOption(
                label="No",
                fact="dns_resolution_failed",
            ),
        ],
    ),

    DiagnosticQuestion(
        id="NET-Q005",
        text="Can the device access the internet?",
        category="Network",
        options=[
            QuestionOption(
                label="Yes",
                fact="internet_reachable",
            ),
            QuestionOption(
                label="No",
                fact="internet_unreachable",
            ),
        ],
    ),

    DiagnosticQuestion(
        id="NET-Q006",
        text="Can another device on the same network access the internet?",
        category="Network",
        options=[
            QuestionOption(
                label="Yes",
                fact="other_devices_internet_working",
            ),
            QuestionOption(
                label="No",
                fact="other_devices_internet_unavailable",
            ),
        ],
    ),
]


SYSTEM_QUESTIONS = [
    DiagnosticQuestion(
        id="SYS-Q001",
        text="Is CPU usage unusually high?",
        category="System Performance",
        options=[
            QuestionOption(
                label="Yes",
                fact="cpu_usage_high",
            ),
            QuestionOption(
                label="No",
                fact="cpu_usage_normal",
            ),
        ],
    ),

    DiagnosticQuestion(
        id="SYS-Q002",
        text="Are many applications or background processes running?",
        category="System Performance",
        options=[
            QuestionOption(
                label="Yes",
                fact="many_background_processes",
            ),
            QuestionOption(
                label="No",
                fact="background_processes_normal",
            ),
        ],
    ),

    DiagnosticQuestion(
        id="SYS-Q003",
        text="Is memory usage unusually high?",
        category="System Performance",
        options=[
            QuestionOption(
                label="Yes",
                fact="memory_usage_high",
            ),
            QuestionOption(
                label="No",
                fact="memory_usage_normal",
            ),
        ],
    ),

    DiagnosticQuestion(
        id="SYS-Q004",
        text="Is available disk space very low?",
        category="System Performance",
        options=[
            QuestionOption(
                label="Yes",
                fact="disk_space_low",
            ),
            QuestionOption(
                label="No",
                fact="disk_space_normal",
            ),
        ],
    ),
]


AUTHENTICATION_QUESTIONS = [
    DiagnosticQuestion(
        id="AUTH-Q001",
        text="Did the login attempt fail?",
        category="Authentication",
        options=[
            QuestionOption(
                label="Yes",
                fact="login_failed",
            ),
            QuestionOption(
                label="No",
                fact="login_successful",
            ),
        ],
    ),

    DiagnosticQuestion(
        id="AUTH-Q002",
        text="Are the supplied credentials invalid?",
        category="Authentication",
        options=[
            QuestionOption(
                label="Yes",
                fact="credentials_invalid",
            ),
            QuestionOption(
                label="No",
                fact="credentials_valid",
            ),
        ],
    ),

    DiagnosticQuestion(
        id="AUTH-Q003",
        text="Is the account locked?",
        category="Authentication",
        options=[
            QuestionOption(
                label="Yes",
                fact="account_locked",
            ),
            QuestionOption(
                label="No",
                fact="account_unlocked",
            ),
        ],
    ),

    DiagnosticQuestion(
        id="AUTH-Q004",
        text="Has the password expired?",
        category="Authentication",
        options=[
            QuestionOption(
                label="Yes",
                fact="password_expired",
            ),
            QuestionOption(
                label="No",
                fact="password_current",
            ),
        ],
    ),
]


ALL_QUESTIONS = (
    NETWORK_QUESTIONS
    + SYSTEM_QUESTIONS
    + AUTHENTICATION_QUESTIONS
)