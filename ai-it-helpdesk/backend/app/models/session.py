from pydantic import BaseModel, Field


class DiagnosticSession(BaseModel):
    """
    Represents the state of one interactive diagnostic session.
    """

    session_id: str

    category: str

    facts: set[str] = Field(default_factory=set)

    asked_questions: list[str] = Field(default_factory=list)

    answered_questions: list[str] = Field(default_factory=list)

    status: str = "active"

    diagnosis_codes: list[str] = Field(default_factory=list)