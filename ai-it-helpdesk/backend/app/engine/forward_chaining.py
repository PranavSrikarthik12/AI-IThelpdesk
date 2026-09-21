from app.knowledge.knowledge_base import KnowledgeBase
from app.models.inference import InferenceResult, InferenceStep


class ForwardChainingEngine:
    """
    Forward chaining inference engine.

    Starts with known facts and repeatedly applies rules
    whose conditions are satisfied.
    """

    def run(self, knowledge_base: KnowledgeBase) -> InferenceResult:
        facts = knowledge_base.get_facts()
        rules = knowledge_base.get_rules()

        initial_facts = set(facts)
        derived_facts: set[str] = set()
        fired_rules: list[str] = []
        trace: list[InferenceStep] = []

        changed = True

        while changed:
            changed = False

            for rule in rules:

                # Do not fire the same rule repeatedly.
                if rule.id in fired_rules:
                    continue

                # Check whether all conditions are satisfied.
                if rule.can_fire(facts):

                    # Avoid generating an already known fact.
                    if rule.conclusion not in facts:

                        facts.add(rule.conclusion)
                        derived_facts.add(rule.conclusion)

                        fired_rules.append(rule.id)

                        trace.append(
                            InferenceStep(
                                rule_id=rule.id,
                                conditions=rule.conditions,
                                conclusion=rule.conclusion,
                                explanation=rule.explanation,
                            )
                        )

                        changed = True

        return InferenceResult(
            initial_facts=sorted(initial_facts),
            derived_facts=sorted(derived_facts),
            fired_rules=fired_rules,
            trace=trace,
        )