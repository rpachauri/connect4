from typing import List, Set, Optional

from connect_four.evaluation.victor.rules import Vertical, Rule
from connect_four.problem import Group


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
        return self.verticals.__hash__()

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


def find_all_lowinverses(verticals: Set[Vertical]):
    """find_all_lowinverses takes an iterable of Verticals and returns an iterable of Lowinverses.

    Args:
        verticals (iterable<Vertical>): an iterable of Verticals.

    Returns:
        lowinverses (iterable<Lowinverse>): an iterable of Lowinverses.
    """
    lowinverses = set()
    for first_vertical in verticals:
        for second_vertical in verticals:
            if first_vertical.upper.col != second_vertical.upper.col:
                lowinverses.add(Lowinverse(first_vertical, second_vertical))

    return lowinverses


class LowinverseManager:
    def __init__(self, verticals: Set[Vertical]):
        """Initializes the LowinverseManager.

        Args:
            verticals (Set[Vertical]): a set of Verticals to build Lowinverses off of.
        """
        pass

    def move(self, vertical: Optional[Vertical], verticals: Set[Vertical]) -> Set[Lowinverse]:
        """Moves the internal state of the LowinverseManager to after this square has been played.

        Args:
            vertical (Optional[Vertical]): an optional Vertical that may have been removed after move is played.
            verticals (Set[Vertical]): the set of Verticals in the current state.
                If vertical is not None, vertical will be in verticals

        Returns:
            removed_lowinverses (Set[Lowinverse]): the set of Lowinverses being removed.
        """
        pass

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
        pass

    def undo_move(self, vertical: Optional[Vertical], verticals: Set[Vertical]) -> Set[Lowinverse]:
        """Moves the internal state of the LowinverseManager to before this square was played.

        Args:
            vertical (Optional[Vertical]): an optional Vertical that may have been added after move is undone.
            verticals (Set[Vertical]): the set of Verticals in the current state.
                If vertical is not None, vertical will be in verticals

        Returns:
            added_lowinverses (Set[Lowinverse]): the set of Lowinverses being added.
        """
        pass
