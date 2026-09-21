from pydantic import BaseModel, Field


class QuestionOption(BaseModel):
    """
    A possible answer to a diagnostic question.
    """

    label: str
    fact: str


class DiagnosticQuestion(BaseModel):
    """
    A question asked during an interactive diagnosis.
    """

    id: str
    text: str
    options: list[QuestionOption] = Field(default_factory=list)
    category: str