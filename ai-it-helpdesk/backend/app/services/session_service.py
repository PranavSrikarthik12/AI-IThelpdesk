import uuid

from app.models.session import DiagnosticSession


class SessionService:
    """
    Manages active diagnostic sessions.

    This is intentionally in-memory for the first version.
    """

    def __init__(self):
        self.sessions: dict[str, DiagnosticSession] = {}

    def create_session(
        self,
        category: str,
    ) -> DiagnosticSession:

        session_id = str(uuid.uuid4())

        session = DiagnosticSession(
            session_id=session_id,
            category=category,
        )

        self.sessions[session_id] = session

        return session

    def get_session(
        self,
        session_id: str,
    ) -> DiagnosticSession | None:

        return self.sessions.get(session_id)

    def save_session(
        self,
        session: DiagnosticSession,
    ) -> None:

        self.sessions[session.session_id] = session