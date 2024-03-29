from typing import List, Set, Optional

from connect_four.evaluation.victor.rules import Vertical, Rule, connection
from connect_four.problem import Group

import warnings


class Lowinverse(Rule):
    def __init__(self, first_vertical: Vertical, second_vertical: Vertical):
        self.verticals = frozenset([
            first_vertical,
            second_vertical,
        ])

    def __eq__(self, other):
        if isinstance(other, Lowinverse):
            return self.verticals == other.verticals
        return False

    def __hash__(self):
        return self.verticals.__hash__() * 7159

    def solves(self, group: Group) -> bool:
        for vertical in self.verticals:
            if vertical.solves(group=group):
                return True

        vertical_0, vertical_1 = tuple(self.verticals)
        upper_squares = {vertical_0.upper, vertical_1.upper}
        return upper_squares.issubset(group.squares)

    def is_useful(self, groups: Set[Group]) -> bool:
        solved_vertical_groups = set()
        for group in groups:
            for vertical in self.verticals:
                if vertical.solves(group=group):
                    solved_vertical_groups.add(group)

        # Given that solved_vertical_groups is a subset of groups, it will not equal groups only if there exists
        # a Group this Lowinverse can solve that one of its Verticals cannot.
        return solved_vertical_groups != groups

    def find_problems_solved(self, groups_by_square_by_player: List[List[List[Set[Group]]]]) -> Set[Group]:
        """Finds all Problems this Rule solves.

        Args:
            groups_by_square_by_player (List[List[List[Set[Group]]]]): a 3D array of a Set of Groups.
                1. The first dimension is the player.
                2. The second dimension is the row.
                3. The third dimension is the col.

                For a given player and a given (row, col),
                you can retrieve all Groups that player can win from that Square with:
                    set_of_possible_winning_groups_at_player_row_col = groups_by_square_by_player[player][row][col]

        Returns:
            problems_solved (Set[Group]): All Problems in square_to_groups this Rule solves.
        """
        warnings.warn("find_problems_solved is deprecated. use solves() instead", DeprecationWarning)
        white_problems_solved = self.find_problems_solved_for_player(groups_by_square=groups_by_square_by_player[0])
        black_problems_solved = self.find_problems_solved_for_player(groups_by_square=groups_by_square_by_player[1])
        return white_problems_solved.union(black_problems_solved)

    def find_problems_solved_for_player(self, groups_by_square: List[List[Set[Group]]]) -> Set[Group]:
        vertical_0, vertical_1 = tuple(self.verticals)
        upper_0 = vertical_0.upper
        upper_1 = vertical_1.upper
        groups_0 = groups_by_square[upper_0.row][upper_0.col]
        groups_1 = groups_by_square[upper_1.row][upper_1.col]
        solved_by_two_upper_squares = groups_0.intersection(groups_1)
        vertical_0_problems = vertical_0.find_problems_solved_for_player(groups_by_square=groups_by_square)
        vertical_1_problems = vertical_1.find_problems_solved_for_player(groups_by_square=groups_by_square)
        return solved_by_two_upper_squares.union(vertical_0_problems).union(vertical_1_problems)


def find_all_lowinverses(verticals: Set[Vertical]) -> Set[Lowinverse]:
    """find_all_lowinverses takes an iterable of Verticals and returns an iterable of Lowinverses.

    Args:
        verticals (iterable<Vertical>): an iterable of Verticals.

    Returns:
        lowinverses (iterable<Lowinverse>): an iterable of Lowinverses.
    """
    lowinverses = set()
    for first_vertical in verticals:
        for second_vertical in verticals:
            if (first_vertical.upper.col != second_vertical.upper.col and
                    connection.is_possible(a=first_vertical.upper, b=second_vertical.upper)):
                lowinverses.add(Lowinverse(first_vertical, second_vertical))

    return lowinverses


class LowinverseManager:
    def __init__(self, verticals: Set[Vertical]):
        """Initializes the LowinverseManager.

        Args:
            verticals (Set[Vertical]): a set of Verticals to build Lowinverses off of.
        """
        self.lowinverses = find_all_lowinverses(verticals=verticals)

    def move(self, vertical: Optional[Vertical], verticals: Set[Vertical]) -> Set[Lowinverse]:
        """Moves the internal state of the LowinverseManager to after this square has been played.

        Args:
            vertical (Optional[Vertical]): an optional Vertical that may have been removed after move is played.
            verticals (Set[Vertical]): the set of Verticals in the current state.
                If vertical is not None, vertical will be in verticals

        Returns:
            removed_lowinverses (Set[Lowinverse]): the set of Lowinverses being removed.
        """
        removed_lowinverses = LowinverseManager._find_affected_lowinverses(vertical=vertical, verticals=verticals)
        self.lowinverses -= removed_lowinverses
        return removed_lowinverses

    @staticmethod
    def _find_affected_lowinverses(vertical: Optional[Vertical], verticals: Set[Vertical]) -> Set[Lowinverse]:
        """Returns the set of Lowinverses that results from the cross product between vertical and verticals.

        Args:
            vertical (Optional[Vertical]): an optional Vertical.
            verticals (Set[Vertical]): a set of Verticals.
                If vertical is not None, vertical will be in verticals

        Returns:
            affected_lowinverses (Set[Lowinverse]): the set of Lowinverses that results from
                the cross product between vertical and verticals.
                If vertical is None, returns an empty set.
        """
        if vertical is None:
            return set()

        affected_lowinverses = set()
        for other in verticals - {vertical}:
            if vertical.upper.col != other.upper.col and connection.is_possible(a=vertical.upper, b=other.upper):
                affected_lowinverses.add(Lowinverse(first_vertical=vertical, second_vertical=other))
        return affected_lowinverses

    def undo_move(self, vertical: Optional[Vertical], verticals: Set[Vertical]) -> Set[Lowinverse]:
        """Moves the internal state of the LowinverseManager to before this square was played.

        Args:
            vertical (Optional[Vertical]): an optional Vertical that may have been added after move is undone.
            verticals (Set[Vertical]): the set of Verticals in the current state.
                If vertical is not None, vertical will be in verticals

        Returns:
            added_lowinverses (Set[Lowinverse]): the set of Lowinverses being added.
        """
        added_lowinverses = LowinverseManager._find_affected_lowinverses(vertical=vertical, verticals=verticals)
        self.lowinverses.update(added_lowinverses)
        return added_lowinverses
