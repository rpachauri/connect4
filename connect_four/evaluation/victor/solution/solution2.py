from typing import Sequence, Iterable

from connect_four.evaluation.victor.rules import Claimeven, Rule, Baseinverse, Vertical, Aftereven, Lowinverse, \
    Highinverse, Baseclaim, Before, Specialbefore
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


def from_aftereven(aftereven: Aftereven) -> Solution:
    """Converts an Aftereven into a Solution.

    Args:
        aftereven (Aftereven): an Aftereven.

    Returns:
        solution (Solution): a Solution.
    """
    squares_involved = list(aftereven.group.squares)
    claimeven_bottom_squares = []
    for claimeven in aftereven.claimevens:
        squares_involved.append(claimeven.lower)
        claimeven_bottom_squares.append(claimeven.lower)

    return Solution(
        rule_instance=aftereven,
        squares=frozenset(squares_involved),
        claimeven_bottom_squares=claimeven_bottom_squares,
    )


def from_lowinverse(lowinverse: Lowinverse) -> Solution:
    """Converts a Lowinverse into a Solution.

    Args:
        lowinverse (Lowinverse): a Lowinverse.

    Returns:
        solution (Solution): a Solution.
    """
    verticals_as_list = list(lowinverse.verticals)
    vertical_0, vertical_1 = verticals_as_list[0], verticals_as_list[1]

    return Solution(
        rule_instance=lowinverse,
        squares=frozenset([vertical_0.upper, vertical_0.lower, vertical_1.upper, vertical_1.lower]),
    )


def from_highinverse(highinverse: Highinverse) -> Solution:
    """Converts a Highinverse into a Solution.

    Args:
        highinverse (Highinverse): a Highinverse.

    Returns:
        solution (Solution): a Solution.
    """
    verticals_as_list = list(highinverse.lowinverse.verticals)
    vertical_0, vertical_1 = verticals_as_list[0], verticals_as_list[1]
    upper_square_0 = Square(row=vertical_0.upper.row - 1, col=vertical_0.upper.col)
    upper_square_1 = Square(row=vertical_1.upper.row - 1, col=vertical_1.upper.col)

    # Form the highinverse into a solution.
    squares = frozenset([
        upper_square_0,
        vertical_0.upper,
        vertical_0.lower,
        upper_square_1,
        vertical_1.upper,
        vertical_1.lower,
    ])
    return Solution(
        squares=squares,
        rule_instance=highinverse,
    )


def from_baseclaim(baseclaim: Baseclaim) -> Solution:
    """Converts a Baseclaim into a Solution.

    Args:
        baseclaim (Baseclaim): a Baseclaim.

    Returns:
        solution (Solution): a Solution.
    """
    square_above_second = Square(row=baseclaim.second.row - 1, col=baseclaim.second.col)

    return Solution(
        rule_instance=baseclaim,
        squares=[baseclaim.first, baseclaim.second, baseclaim.third, square_above_second],
        claimeven_bottom_squares=[baseclaim.second],
    )


def from_before(before: Before) -> Solution:
    """Converts a Before into a Solution.

    Args:
        before (Before): a Before.

    Returns:
        solution (Solution): a Solution.
    """
    empty_squares = before.empty_squares_of_before_group()

    squares = set(empty_squares)

    for vertical in before.verticals:
        # Add all squares part of Verticals which are part of the Before.
        squares.add(vertical.upper)
        squares.add(vertical.lower)

    claimeven_bottom_squares = []
    for claimeven in before.claimevens:
        # Add all squares part of Claimevens which are part of the Before.
        squares.add(claimeven.upper)
        squares.add(claimeven.lower)
        claimeven_bottom_squares.append(claimeven.lower)

    return Solution(
        rule_instance=before,
        squares=frozenset(squares),
        claimeven_bottom_squares=claimeven_bottom_squares,
    )


def from_specialbefore(specialbefore: Specialbefore) -> Solution:
    """Converts a Specialbefore into a Solution.

    Args:
        specialbefore (Specialbefore): a Specialbefore.

    Returns:
        solution (Solution): a Solution.
    """
    # Find all groups that contain the internal directly playable square and
    # external directly playable square of the Specialbefore.
    sq1 = specialbefore.internal_directly_playable_square
    sq2 = specialbefore.external_directly_playable_square

    squares = {sq1, sq2}

    for vertical in specialbefore.before.verticals:
        if vertical != specialbefore.unused_vertical():
            # Add all squares part of Verticals which are part of the Before.
            squares.add(vertical.upper)
            squares.add(vertical.lower)

    claimeven_bottom_squares = []
    for claimeven in specialbefore.before.claimevens:
        # Add all squares part of Claimevens which are part of the Before.
        squares.add(claimeven.upper)
        squares.add(claimeven.lower)
        claimeven_bottom_squares.append(claimeven.lower)

    # The Specialbefore Solution includes all squares that the Before Solution has.
    return Solution(
        squares=frozenset(squares),
        claimeven_bottom_squares=claimeven_bottom_squares,
        rule_instance=specialbefore,
    )
