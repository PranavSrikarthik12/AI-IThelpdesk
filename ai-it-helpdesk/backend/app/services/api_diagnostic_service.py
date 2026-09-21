from app.models.session import DiagnosticSession
from app.services.diagnostic_controller import DiagnosticController


class APIDiagnosticService:
    """
    Coordinates a diagnostic session with the diagnostic controller.
    """

    def __init__(self):
        self.controller = DiagnosticController()

    def evaluate_session(
        self,
        session: DiagnosticSession,
    ):

        return self.controller.evaluate(
            facts=session.facts,
            category=session.category,
            asked_questions=session.asked_questions,
        )