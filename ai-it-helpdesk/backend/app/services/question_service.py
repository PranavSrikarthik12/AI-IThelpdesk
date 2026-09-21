from app.knowledge.questions import ALL_QUESTIONS
from app.knowledge.rules import ALL_RULES
from app.knowledge.diagnoses import DIAGNOSES
from app.models.question import DiagnosticQuestion
from typing import Any

class QuestionService:
    """
    Selects the next diagnostic question using a simple
    information-gain-inspired heuristic.

    A question receives a higher score when its possible
    answers distinguish between more remaining diagnostic rules.
    """

    def get_next_question(
    self,
    category: str,
    facts: set[str],
    asked_questions: list[str],
    return_reason: bool = False,
) -> DiagnosticQuestion | tuple[DiagnosticQuestion, dict[str, Any]] | None:

        questions = [
            question
            for question in ALL_QUESTIONS
            if question.category == category
            and question.id not in asked_questions
        ]

        if not questions:
            return None
        if not facts:
            return questions[0]

        rules = self._get_category_rules(category)

        candidate_rules = [
            rule
            for rule in rules
            if rule.conclusion not in facts
            and self._rule_can_still_be_reached(
                rule,
                facts,
            )
        ]

        if not candidate_rules:
            return None

        best_question = None
        best_score = -1

        for question in questions:
            score = self._score_question(
                question,
                candidate_rules,
                facts,
            )

            if score > best_score:
                best_score = score
                best_question = question

        return best_question
    
    def get_next_question_with_reason(
    self,
    category: str,
    facts: set[str],
    asked_questions: list[str],
) -> tuple[DiagnosticQuestion | None, dict[str, Any]]:
        
        questions = [
            question
            for question in ALL_QUESTIONS
            if question.category == category
            and question.id not in asked_questions
        ]

        if not questions:
            return None, {
                "reason": "No unanswered questions remain.",
                "candidate_rules": [],
                "rules_affected": 0,
            }

        if not facts:
            question = questions[0]

            return question, {
                "reason": "Initial diagnostic question selected because no evidence has been collected yet.",
                "candidate_rules": [
                    rule.id
                    for rule in self._get_category_rules(category)
                ],
                "rules_affected": 0,
            }

        rules = self._get_category_rules(category)

        candidate_rules = [
            rule
            for rule in rules
            if rule.conclusion not in facts
            and self._rule_can_still_be_reached(
                rule,
                facts,
            )
        ]

        if not candidate_rules:
            return None, {
                "reason": "No remaining diagnostic rules can produce a new diagnosis from the current knowledge state.",
                "candidate_rules": [],
                "rules_affected": 0,
            }

        best_question = None
        best_score = -1
        best_affected_rules = set()

        for question in questions:
            score = self._score_question(
                question,
                candidate_rules,
                facts,
            )

            affected_rules = self._get_affected_rules(
                question,
                candidate_rules,
                facts,
            )

            if score > best_score:
                best_score = score
                best_question = question
                best_affected_rules = affected_rules

        if best_question is None:
            return None, {
                "reason": "No useful diagnostic question was found.",
                "candidate_rules": [rule.id for rule in candidate_rules],
                "rules_affected": 0,
            }

        return best_question, {
            "reason": (
                "This question helps distinguish between "
                "the remaining possible diagnostic rules."
            ),
            "candidate_rules": [
                rule.id
                for rule in candidate_rules
            ],
            "affected_rules": sorted(best_affected_rules),
            "rules_affected": len(best_affected_rules),
            "selection_score": best_score,
        }

    def _get_category_rules(self, category: str):
        prefix_map = {
            "Network": "NET-",
            "System Performance": "SYS-",
            "Authentication": "AUTH-",
        }

        prefix = prefix_map.get(category)

        if not prefix:
            return []

        return [
            rule
            for rule in ALL_RULES
            if rule.id.startswith(prefix)
            and rule.conclusion in DIAGNOSES
        ]

    def _can_be_derived(
        self,
        fact: str,
        facts: set[str],
        visited: set[str] | None = None,
    ) -> bool:
        """
        Determine whether a fact is already known or can be
        derived through the current rule dependency graph.
        """

        if fact in facts:
            return True

        if visited is None:
            visited = set()

        if fact in visited:
            return False

        visited.add(fact)

        producing_rules = [
            rule
            for rule in ALL_RULES
            if rule.conclusion == fact
        ]

        for rule in producing_rules:

            if all(
                self._can_be_derived(
                    condition,
                    facts,
                    visited.copy(),
                )
                for condition in rule.conditions
            ):
                return True

        return False

    def _rule_can_still_be_reached(
        self,
        rule,
        facts: set[str],
    ) -> bool:
        """
        Determine whether a diagnostic rule remains potentially
        reachable from the current knowledge state.
        """

        for condition in rule.conditions:

            if condition in facts:
                continue

            # The condition may be an intermediate fact that
            # can eventually be derived.
            if self._can_be_derived(
                condition,
                facts,
            ):
                continue

            # Otherwise this condition requires future
            # user-provided evidence.
            return True

        return True

    def _score_question(
        self,
        question: DiagnosticQuestion,
        candidate_rules,
        facts: set[str],
    ) -> float:
        """
        Estimate how effectively a question separates
        the remaining candidate rules.

        A question gets credit when:
        - one of its possible answers appears in a rule
        - the corresponding condition is still unknown
        - different answers affect different candidate rules

        A balanced split is preferred over a question
        that only affects one side.
        """

        option_facts = {
            option.fact
            for option in question.options
        }

        yes_rules = set()
        no_rules = set()

        for rule in candidate_rules:
            unknown_conditions = [
                condition
                for condition in rule.conditions
                if condition not in facts
            ]

            if not unknown_conditions:
                continue

            for condition in unknown_conditions:
                if condition in option_facts:
                    # Record the rule affected by this question.
                    option = next(
                        (
                            option
                            for option in question.options
                            if option.fact == condition
                        ),
                        None,
                    )

                    if option is None:
                        continue

                    if option.label.lower() == "yes":
                        yes_rules.add(rule.id)
                    elif option.label.lower() == "no":
                        no_rules.add(rule.id)

        total_rules = len(candidate_rules)

        if total_rules == 0:
            return 0.0

        covered_rules = len(yes_rules | no_rules)

        if covered_rules == 0:
            return 0.0

        # Reward coverage of the remaining diagnostic rules.
        coverage_score = covered_rules / total_rules

        # Reward questions whose two answers affect different
        # candidate rules rather than only one outcome.
        if yes_rules and no_rules:
            balance = min(
                len(yes_rules),
                len(no_rules),
            ) / max(
                len(yes_rules),
                len(no_rules),
            )
        else:
            balance = 0.0

        return coverage_score + balance

    def _get_affected_rules(
        self,
        question: DiagnosticQuestion,
        candidate_rules,
        facts: set[str],
    ) -> set[str]:

        option_facts = {
            option.fact
            for option in question.options
        }

        affected_rules = set()

        for rule in candidate_rules:

            # Direct dependency
            if any(
                condition in option_facts
                for condition in rule.conditions
                if condition not in facts
            ):
                affected_rules.add(rule.id)
                continue

            # Indirect dependency through intermediate rules
            for condition in rule.conditions:

                if condition in facts:
                    continue

                dependent_rules = [
                    dependency
                    for dependency in ALL_RULES
                    if dependency.conclusion == condition
                ]

                for dependency in dependent_rules:

                    if any(
                        dependency_condition in option_facts
                        for dependency_condition in dependency.conditions
                        if dependency_condition not in facts
                    ):
                        affected_rules.add(rule.id)
                        break

                if rule.id in affected_rules:
                    break

        return affected_rules