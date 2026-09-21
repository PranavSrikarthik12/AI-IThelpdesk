from app.engine.forward_chaining import ForwardChainingEngine
from app.engine.backward_chaining import BackwardChainingEngine
from app.knowledge.knowledge_base import KnowledgeBase
from app.knowledge.rules import ALL_RULES
from app.knowledge.diagnoses import DIAGNOSES
from app.services.question_service import QuestionService


class DiagnosticController:
    """
    Coordinates questions, facts, and inference.
    """

    def __init__(self):
        self.forward_engine = ForwardChainingEngine()
        self.backward_engine = BackwardChainingEngine()
        self.question_service = QuestionService()

    def evaluate(
        self,
        facts: set[str],
        category: str,
        asked_questions: list[str],
    ):

        rules = [
            rule
            for rule in ALL_RULES
            if self._rule_matches_category(rule, category)
        ]

        knowledge_base = KnowledgeBase(
            facts=facts,
            rules=rules,
        )

        # --------------------------------------------------
        # Forward chaining
        # --------------------------------------------------

        forward_result = self.forward_engine.run(
            knowledge_base
        )

        candidate_facts = [
            fact
            for fact in forward_result.derived_facts
            if fact in DIAGNOSES
        ]

        # --------------------------------------------------
        # Backward verification
        # --------------------------------------------------

        backward_results = []

        for fact in candidate_facts:
            backward_kb = KnowledgeBase(
                facts=set(facts),
                rules=rules,
            )

            backward_result = self.backward_engine.run(
                backward_kb,
                goal=fact,
            )

            if fact in backward_result.derived_facts:
                backward_results.append(
                    {
                        "fact": fact,
                        "inference": backward_result,
                    }
                )

        diagnoses = [
            DIAGNOSES[item["fact"]]
            for item in backward_results
        ]

        # --------------------------------------------------
        # Diagnosis found
        # --------------------------------------------------

        if diagnoses:
            return {
                "status": "diagnosed",
                "diagnoses": diagnoses,

                # Keep existing inference field for
                # backward compatibility.
                "inference": forward_result,

                # New explicit inference results.
                "forward_inference": forward_result,
                "backward_inference": [
                    item["inference"]
                    for item in backward_results
                ],

                "next_question": None,
                "selection_reason": None,
            }

        # --------------------------------------------------
        # No diagnosis yet → select next question
        # --------------------------------------------------

        next_question, selection_reason = (
            self.question_service.get_next_question_with_reason(
                facts=facts,
                asked_questions=asked_questions,
                category=category,
            )
        )

        if next_question is None:
            return {
                "status": "insufficient_information",
                "diagnoses": [],
                "inference": forward_result,
                "forward_inference": forward_result,
                "backward_inference": [],
                "next_question": None,
                "selection_reason": None,
            }

        return {
            "status": "question_required",
            "diagnoses": [],
            "inference": forward_result,
            "forward_inference": forward_result,
            "backward_inference": [],
            "next_question": next_question,
            "selection_reason": selection_reason,
        }

    @staticmethod
    def _rule_matches_category(rule, category: str):

        if category == "Network":
            return rule.id.startswith("NET-")

        if category == "System Performance":
            return rule.id.startswith("SYS-")

        if category == "Authentication":
            return rule.id.startswith("AUTH-")

        return False