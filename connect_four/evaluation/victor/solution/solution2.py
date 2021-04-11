from connect_four.evaluation.victor.rules import Claimeven, Rule


class Solution:
    """A Solution is an application of a Rule that refutes at least one group.

    Two Solutions may or may not work together depending on which squares each
    consists of and which rule they are an application of.
    """
    def __init__(self, rule_instance: Rule):
        self.rule_instance = rule_instance
        self.squares = frozenset()
        self.claimeven_bottom_squares = frozenset()

        if isinstance(self.rule_instance, Claimeven):
            self._from_claimeven(claimeven=self.rule_instance)

    def _from_claimeven(self, claimeven: Claimeven):
        """Initializes Claimeven into a Solution.

        Args:
            claimeven (Claimeven): a Claimeven.

        Returns:
            solution (Solution): a Solution.
        """
        self.squares = frozenset([claimeven.upper, claimeven.lower])
        self.claimeven_bottom_squares = frozenset(claimeven.lower)


