from pydantic import BaseModel, Field


class StartDiagnosisRequest(BaseModel):
    category: str


class StartDiagnosisResponse(BaseModel):
    session_id: str
    category: str
    status: str
    question: object | None = None
    selection_reason: dict | None = None


class AnswerRequest(BaseModel):
    question_id: str
    fact: str


class AnswerResponse(BaseModel):
    session_id: str
    status: str
    question: object | None = None
    diagnoses: list = Field(default_factory=list)
    inference: object | None = None
    forward_inference: object | None = None
    backward_inference: list = Field(default_factory=list)
    selection_reason: dict | None = None