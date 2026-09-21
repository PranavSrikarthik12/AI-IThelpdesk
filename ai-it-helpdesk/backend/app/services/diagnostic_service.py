from app.engine.backward_chaining import BackwardChainingEngine
from app.engine.forward_chaining import ForwardChainingEngine
from app.knowledge.diagnoses import DIAGNOSES
from app.knowledge.knowledge_base import KnowledgeBase
from app.knowledge.rules import ALL_RULES
from app.models.diagnosis import Diagnosis
from app.models.inference import InferenceResult


class DiagnosticService:
    """
    High-level service responsible for performing IT diagnosis.
    """

    def __init__(self):
        self.forward_engine = ForwardChainingEngine()
        self.backward_engine = BackwardChainingEngine()

    def _build_knowledge_base(
        self,
        facts: set[str],
    ) -> KnowledgeBase:
        return KnowledgeBase(
            facts=facts,
            rules=ALL_RULES,
        )

    def diagnose_forward(
        self,
        facts: set[str],
    ) -> tuple[InferenceResult, list[Diagnosis]]:

        knowledge_base = self._build_knowledge_base(facts)

        result = self.forward_engine.run(knowledge_base)

        diagnoses = [
            DIAGNOSES[fact]
            for fact in result.derived_facts
            if fact in DIAGNOSES
        ]

        return result, diagnoses

    def diagnose_backward(
        self,
        facts: set[str],
        goal: str,
    ) -> tuple[InferenceResult, Diagnosis | None]:

        knowledge_base = self._build_knowledge_base(facts)

        result = self.backward_engine.run(
            knowledge_base=knowledge_base,
            goal=goal,
        )

        diagnosis = DIAGNOSES.get(goal)

        if goal not in result.derived_facts:
            diagnosis = None

        return result, diagnosis