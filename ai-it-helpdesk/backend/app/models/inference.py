from pydantic import BaseModel


class InferenceStep(BaseModel):
    """
    Represents one step in the reasoning process.
    """

    rule_id: str
    conditions: list[str]
    conclusion: str
    explanation: str


class InferenceResult(BaseModel):
    """
    Final result produced by an inference engine.
    """

    initial_facts: list[str]
    derived_facts: list[str]
    fired_rules: list[str]
    trace: list[InferenceStep]