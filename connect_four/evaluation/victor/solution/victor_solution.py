from typing import Iterable, FrozenSet, Dict, Set

from connect_four.evaluation.victor.rules import Claimeven, Rule, Baseinverse, Vertical, Aftereven, Lowinverse, \
    Highinverse, Baseclaim, Before, Specialbefore, Oddthreat
from connect_four.evaluation.victor.solution.solution import Solution
from connect_four.game import Square
from connect_four.problem import Group
from connect_four.problem.problem import Problem


class VictorSolution(Solution):
    """A VictorSolution is an application of a Rule.

    Two VictorSolutions may or may not work together depending on which squares each
    consists of and which rule they are an application of.
    """
    def __init__(self, rule_instance: Rule, squares: Iterable[Square],
                 claimeven_bottom_squares: Iterable[Square] = None):
        self.rule_instance = rule_instance

        self.squares = frozenset(squares)

        if claimeven_bottom_squares is None:
            claimeven_bottom_squares = set()
        self.claimeven_bottom_squares = frozenset(claimeven_bottom_squares)
        self.squares_by_column = self.cols_to_squares(squares=self.squares)

    def solves(self, problem: Problem) -> bool:
        if isinstance(problem, Group):
            return self.rule_instance.solves(group=problem)
        return False

    def is_useful(self, problems: Set[Problem]) -> bool:
        groups = set()
        for problem in problems:
            if isinstance(problem, Group):
                # if not self.rule_instance.solves(group=problem):
                #     raise ValueError("solution", self, "not able to solve", problem)
                groups.add(problem)
            else:
                raise TypeError(problem, "not of type", Group)

        return self.rule_instance.is_useful(groups=groups)

    def can_be_combined_with(self, solution: Solution) -> bool:
        if isinstance(solution, VictorSolution):
            from connect_four.evaluation.victor.solution import combination
            return combination.allowed(s1=self, s2=solution)
        return False

    @staticmethod
    def cols_to_squares(squares: FrozenSet[Square]) -> Dict[int, Set[Square]]:
        """Converts an iterable of Squares into a dictionary of Squares keyed by the column they belong in.

        Args:
            squares (iterable<Square>): an iterable of Square objects.

        Returns:
            col_to_squares_dict (Map<int, Set<Square>>): a dictionary of columns to Squares in that column.
        """
        col_to_squares_dict = {}
        for square in squares:
            if square.col not in col_to_squares_dict:
                col_to_squares_dict[square.col] = set()
            col_to_squares_dict[square.col].add(square)
        return col_to_squares_dict

    def __eq__(self, other):
        if isinstance(other, VictorSolution):
            return (self.rule_instance == other.rule_instance and
                    self.squares == other.squares and
                    self.claimeven_bottom_squares == other.claimeven_bottom_squares)

    def __hash__(self):
        return (self.rule_instance.__hash__() * 19441 +
                self.squares.__hash__() * 96137 +
                self.claimeven_bottom_squares.__hash__() * 24551)

    def __repr__(self):
        return str(self.rule_instance.__class__) + " -> " + str(self.squares)


# def from_rule(rule: Rule) -> VictorSolution:
#     """Converts a Rule into a VictorSolution.
#
#     Args:
#         rule (Rule): a Rule.
#
#     Returns:
#         solution (VictorSolution): a VictorSolution.
#     """
#     if isinstance(rule, Claimeven):
#         return from_claimeven(claimeven=rule)
#     if isinstance(rule, Baseinverse):
#         return from_baseinverse(baseinverse=rule)
#     if isinstance(rule, Vertical):
#         return from_vertical(vertical=rule)
#     if isinstance(rule, Aftereven):
#         return from_aftereven(aftereven=rule)
#     if isinstance(rule, Lowinverse):
#         return from_lowinverse(lowinverse=rule)
#     if isinstance(rule, Highinverse):
#         return from_highinverse(highinverse=rule)
#     if isinstance(rule, Baseclaim):
#         return from_baseclaim(baseclaim=rule)
#     if isinstance(rule, Before):
#         return from_before(before=rule)
#     if isinstance(rule, Specialbefore):
#         return from_specialbefore(specialbefore=rule)
#     if isinstance(rule, Oddthreat):
#         return from_odd_threat(odd_threat=rule)


def from_claimeven(claimeven: Claimeven) -> VictorSolution:
    """Converts a Claimeven into a VictorSolution.

    Args:
        claimeven (Claimeven): a Claimeven.

    Returns:
        solution (VictorSolution): a VictorSolution.
    """
    return VictorSolution(
        rule_instance=claimeven,
        squares=[claimeven.upper, claimeven.lower],
        claimeven_bottom_squares=[claimeven.lower],
    )


def from_baseinverse(baseinverse: Baseinverse) -> VictorSolution:
    return VictorSolution(
        rule_instance=baseinverse,
        squares=baseinverse.squares,
    )


def from_vertical(vertical: Vertical) -> VictorSolution:
    """Converts a Vertical into a VictorSolution.

    Args:
        vertical (Vertical): a Vertical.

    Returns:
        solution (VictorSolution): a VictorSolution.
    """
    return VictorSolution(
        rule_instance=vertical,
        squares=[vertical.upper, vertical.lower],
    )


def from_aftereven(aftereven: Aftereven) -> VictorSolution:
    """Converts an Aftereven into a VictorSolution.

    Args:
        aftereven (Aftereven): an Aftereven.

    Returns:
        solution (VictorSolution): a VictorSolution.
    """
    squares_involved = list(aftereven.group.squares)
    claimeven_bottom_squares = []
    for claimeven in aftereven.claimevens:
        squares_involved.append(claimeven.lower)
        claimeven_bottom_squares.append(claimeven.lower)

    return VictorSolution(
        rule_instance=aftereven,
        squares=frozenset(squares_involved),
        claimeven_bottom_squares=claimeven_bottom_squares,
    )


def from_lowinverse(lowinverse: Lowinverse) -> VictorSolution:
    """Converts a Lowinverse into a VictorSolution.

    Args:
        lowinverse (Lowinverse): a Lowinverse.

    Returns:
        solution (VictorSolution): a VictorSolution.
    """
    verticals_as_list = list(lowinverse.verticals)
    vertical_0, vertical_1 = verticals_as_list[0], verticals_as_list[1]

    return VictorSolution(
        rule_instance=lowinverse,
        squares=frozenset([vertical_0.upper, vertical_0.lower, vertical_1.upper, vertical_1.lower]),
    )


def from_highinverse(highinverse: Highinverse) -> VictorSolution:
    """Converts a Highinverse into a VictorSolution.

    Args:
        highinverse (Highinverse): a Highinverse.

    Returns:
        solution (VictorSolution): a VictorSolution.
    """
    if highinverse.columns:
        column_0, column_1 = tuple(highinverse.columns)
        squares = frozenset([
            column_0.upper,
            column_0.middle,
            column_0.lower,
            column_1.upper,
            column_1.middle,
            column_1.lower,
        ])
        return VictorSolution(
            squares=squares,
            rule_instance=highinverse,
        )

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
    return VictorSolution(
        squares=squares,
        rule_instance=highinverse,
    )


def from_baseclaim(baseclaim: Baseclaim) -> VictorSolution:
    """Converts a Baseclaim into a VictorSolution.

    Args:
        baseclaim (Baseclaim): a Baseclaim.

    Returns:
        solution (VictorSolution): a VictorSolution.
    """
    square_above_second = Square(row=baseclaim.second.row - 1, col=baseclaim.second.col)

    return VictorSolution(
        rule_instance=baseclaim,
        squares=[baseclaim.first, baseclaim.second, baseclaim.third, square_above_second],
        claimeven_bottom_squares=[baseclaim.second],
    )


def from_before(before: Before) -> VictorSolution:
    """Converts a Before into a VictorSolution.

    Args:
        before (Before): a Before.

    Returns:
        solution (VictorSolution): a VictorSolution.
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

    return VictorSolution(
        rule_instance=before,
        squares=frozenset(squares),
        claimeven_bottom_squares=claimeven_bottom_squares,
    )


def from_specialbefore(specialbefore: Specialbefore) -> VictorSolution:
    """Converts a Specialbefore into a VictorSolution.

    Args:
        specialbefore (Specialbefore): a Specialbefore.

    Returns:
        solution (VictorSolution): a VictorSolution.
    """
    # Find all groups that contain the internal directly playable square and
    # external directly playable square of the Specialbefore.
    sq1 = specialbefore.internal_directly_playable_square
    sq2 = specialbefore.external_directly_playable_square

    squares = {sq1, sq2}

    for vertical in specialbefore.before.verticals:
        if vertical != specialbefore.unused_vertical:
            # Add all squares part of Verticals which are part of the Before.
            squares.add(vertical.upper)
            squares.add(vertical.lower)

    claimeven_bottom_squares = []
    for claimeven in specialbefore.before.claimevens:
        # Add all squares part of Claimevens which are part of the Before.
        squares.add(claimeven.upper)
        squares.add(claimeven.lower)
        claimeven_bottom_squares.append(claimeven.lower)

    # The Specialbefore VictorSolution includes all squares that the Before VictorSolution has.
    return VictorSolution(
        squares=frozenset(squares),
        claimeven_bottom_squares=claimeven_bottom_squares,
        rule_instance=specialbefore,
    )


def from_odd_threat(odd_threat: Oddthreat) -> VictorSolution:
    """Converts an OddThreat into a VictorSolution.

    Args:
        odd_threat (Oddthreat): an OddThreat.

    Returns:
        solution (VictorSolution): a VictorSolution.
    """
    return VictorSolution(
        rule_instance=odd_threat,
        squares=[odd_threat.empty_square],
    )
