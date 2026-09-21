from app.models.rule import Rule


class KnowledgeBase:
    """
    Stores the facts and rules used by the expert system.
    """

    def __init__(
        self,
        facts: set[str] | None = None,
        rules: list[Rule] | None = None,
    ):
        self.facts: set[str] = facts or set()
        self.rules: list[Rule] = rules or []

    def add_fact(self, fact: str) -> None:
        """Add a fact to the knowledge base."""
        self.facts.add(fact)

    def add_rule(self, rule: Rule) -> None:
        """Add a rule to the knowledge base."""
        self.rules.append(rule)

    def get_facts(self) -> set[str]:
        """Return a copy of the current facts."""
        return set(self.facts)

    def get_rules(self) -> list[Rule]:
        """Return the currently registered rules."""
        return list(self.rules)