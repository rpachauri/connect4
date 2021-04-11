from typing import Sequence, Iterable

from connect_four.evaluation.victor.rules import Claimeven, Rule, Baseinverse, Vertical
from connect_four.game import Square


class Solution:
    """A Solution is an application of a Rule.

    Two Solutions may or may not work together depending on which squares each
    consists of and which rule they are an application of.
    """

    def __init__(self, rule_instance: Rule, squares: Iterable[Square],
                 claimeven_bottom_squares: Iterable[Square] = None):
        self.rule_instance = rule_instance

        self.squares = frozenset(squares)

        if claimeven_bottom_squares is None:
            claimeven_bottom_squares = set()
        self.claimeven_bottom_squares = frozenset(claimeven_bottom_squares)

    def __eq__(self, other):
        if isinstance(other, Solution):
            return (self.rule_instance == other.rule_instance and
                    self.squares == other.squares and
                    self.claimeven_bottom_squares == other.claimeven_bottom_squares)


def from_claimeven(claimeven: Claimeven) -> Solution:
    """Converts a Claimeven into a Solution.

    Args:
        claimeven (Claimeven): a Claimeven.

    Returns:
        solution (Solution): a Solution.
    """
    return Solution(
        rule_instance=claimeven,
        squares=[claimeven.upper, claimeven.lower],
        claimeven_bottom_squares=[claimeven.lower],
    )


def from_baseinverse(baseinverse: Baseinverse) -> Solution:
    return Solution(
        rule_instance=baseinverse,
        squares=baseinverse.squares,
    )


def from_vertical(vertical: Vertical) -> Solution:
    """Converts a Vertical into a Solution.

    Args:
        vertical (Vertical): a Vertical.

    Returns:
        solution (Solution): a Solution.
    """
    return Solution(
        rule_instance=vertical,
        squares=[vertical.upper, vertical.lower],
    )
