from app.knowledge.knowledge_base import KnowledgeBase
from app.models.inference import InferenceResult, InferenceStep


class BackwardChainingEngine:
    """
    Backward chaining inference engine.

    Starts with a goal and attempts to prove it by recursively
    proving the conditions required by relevant rules.
    """

    def run(
        self,
        knowledge_base: KnowledgeBase,
        goal: str,
    ) -> InferenceResult:

        facts = knowledge_base.get_facts()
        rules = knowledge_base.get_rules()

        initial_facts = set(facts)
        derived_facts: set[str] = set()
        fired_rules: list[str] = []
        trace: list[InferenceStep] = []

        visited_goals: set[str] = set()

        proved = self._prove(
            goal=goal,
            facts=facts,
            rules=rules,
            derived_facts=derived_facts,
            fired_rules=fired_rules,
            trace=trace,
            visited_goals=visited_goals,
        )

        if proved:
            derived_facts.add(goal)

        return InferenceResult(
            initial_facts=sorted(initial_facts),
            derived_facts=sorted(derived_facts),
            fired_rules=fired_rules,
            trace=trace,
        )

    def _prove(
        self,
        goal: str,
        facts: set[str],
        rules,
        derived_facts: set[str],
        fired_rules: list[str],
        trace: list[InferenceStep],
        visited_goals: set[str],
    ) -> bool:

        # If the goal is already known, it is immediately proven.
        if goal in facts:
            return True

        # Prevent recursive loops.
        if goal in visited_goals:
            return False

        visited_goals.add(goal)

        # Find rules capable of producing the desired goal.
        matching_rules = [
            rule
            for rule in rules
            if rule.conclusion == goal
        ]

        # No rule can establish this goal.
        if not matching_rules:
            return False

        # Try each possible rule.
        for rule in matching_rules:

            all_conditions_proven = True

            for condition in rule.conditions:

                condition_proven = self._prove(
                    goal=condition,
                    facts=facts,
                    rules=rules,
                    derived_facts=derived_facts,
                    fired_rules=fired_rules,
                    trace=trace,
                    visited_goals=visited_goals,
                )

                if not condition_proven:
                    all_conditions_proven = False
                    break

            if all_conditions_proven:

                facts.add(rule.conclusion)

                derived_facts.add(rule.conclusion)

                if rule.id not in fired_rules:
                    fired_rules.append(rule.id)

                trace.append(
                    InferenceStep(
                        rule_id=rule.id,
                        conditions=rule.conditions,
                        conclusion=rule.conclusion,
                        explanation=rule.explanation,
                    )
                )

                return True

        return False