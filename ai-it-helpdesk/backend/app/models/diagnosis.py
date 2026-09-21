from pydantic import BaseModel, Field


class RecommendedAction(BaseModel):
    """
    Action recommended to the user after a diagnosis.
    """

    step: int
    description: str


class Diagnosis(BaseModel):
    """
    Represents a domain-level IT diagnosis.
    """

    code: str
    category: str
    title: str
    description: str
    severity: str
    recommended_actions: list[RecommendedAction] = Field(
        default_factory=list
    )