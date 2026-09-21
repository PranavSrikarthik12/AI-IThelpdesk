from pydantic import BaseModel, Field


class Rule(BaseModel):
    """
    Represents an IF-THEN production rule.

    Example:

        IF wifi_connected
        AND ip_address_valid
        THEN network_ready
    """

    id: str = Field(..., description="Unique identifier for the rule")
    conditions: list[str] = Field(
        ...,
        min_length=1,
        description="Facts that must all be true for the rule to fire",
    )
    conclusion: str = Field(
        ...,
        description="Fact derived when all conditions are satisfied",
    )
    explanation: str = Field(
        ...,
        description="Human-readable explanation of what this rule represents",
    )

    def can_fire(self, facts: set[str]) -> bool:
        """
        Returns True if every condition required by the rule
        exists in the current fact set.
        """

        return all(condition in facts for condition in self.conditions)