from app.engine.forward_chaining import ForwardChainingEngine
from app.engine.backward_chaining import BackwardChainingEngine
from app.knowledge.knowledge_base import KnowledgeBase
from app.knowledge.rules import ALL_RULES

from app.evaluation.scenarios import EvaluationScenario


class InferenceEvaluator:
    """
    Evaluates forward and backward chaining
    on predefined diagnostic scenarios.
    """

    def __init__(self):
        self.forward_engine = ForwardChainingEngine()
        self.backward_engine = BackwardChainingEngine()

    def evaluate_scenario(
        self,
        scenario: EvaluationScenario,
    ) -> dict:

        rules = [
            rule
            for rule in ALL_RULES
            if self._rule_matches_category(
                rule,
                scenario.category,
            )
        ]

        # --------------------------------------------------
        # Forward chaining
        # --------------------------------------------------

        forward_kb = KnowledgeBase(
            facts=set(scenario.facts),
            rules=rules,
        )

        forward_result = self.forward_engine.run(
            forward_kb
        )

        forward_correct = (
            scenario.expected_diagnosis
            in forward_result.derived_facts
        )

        # --------------------------------------------------
        # Backward chaining
        # --------------------------------------------------

        backward_kb = KnowledgeBase(
            facts=set(scenario.facts),
            rules=rules,
        )

        backward_result = self.backward_engine.run(
            backward_kb,
            goal=scenario.expected_diagnosis,
        )

        backward_correct = (
            scenario.expected_diagnosis
            in backward_result.derived_facts
        )

        # --------------------------------------------------
        # Evaluation result
        # --------------------------------------------------

        return {
            "scenario_id": scenario.id,
            "scenario": scenario.name,
            "category": scenario.category,
            "expected_diagnosis": scenario.expected_diagnosis,

            "forward": {
                "correct": forward_correct,
                "rules_fired": len(
                    forward_result.fired_rules
                ),
                "steps": len(
                    forward_result.trace
                ),
                "inference": forward_result,
            },

            "backward": {
                "correct": backward_correct,
                "rules_fired": len(
                    backward_result.fired_rules
                ),
                "steps": len(
                    backward_result.trace
                ),
                "inference": backward_result,
            },
        }

    def evaluate_all(self) -> list[dict]:
        """
        Evaluate every predefined scenario.
        """

        from app.evaluation.scenarios import SCENARIOS

        return [
            self.evaluate_scenario(scenario)
            for scenario in SCENARIOS
        ]

    @staticmethod
    def _rule_matches_category(
        rule,
        category: str,
    ) -> bool:

        if category == "Network":
            return rule.id.startswith("NET-")

        if category == "System Performance":
            return rule.id.startswith("SYS-")

        if category == "Authentication":
            return rule.id.startswith("AUTH-")

        return False