from typing import List, Set

from connect_four.evaluation.victor.board import Board

from connect_four.evaluation.victor.rules import Lowinverse, Rule, Vertical
from connect_four.game import Square
from connect_four.problem import Group


class Highinverse(Rule):
    def __init__(self, lowinverse: Lowinverse, directly_playable_squares=None):
        self.lowinverse = lowinverse

        if directly_playable_squares is None:
            directly_playable_squares = set()
        self.directly_playable_squares = frozenset(directly_playable_squares)

    def __eq__(self, other):
        if isinstance(other, Highinverse):
            return (self.lowinverse == other.lowinverse and
                    self.directly_playable_squares == other.directly_playable_squares)
        return False

    def __hash__(self):
        return self.lowinverse.__hash__() * 37 + self.directly_playable_squares.__hash__()

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
        highinverse_groups = set()

        # Add all groups which contain the two upper squares.
        verticals_as_list = list(self.lowinverse.verticals)
        vertical_0, vertical_1 = verticals_as_list[0], verticals_as_list[1]
        upper_square_0 = Square(row=vertical_0.upper.row - 1, col=vertical_0.upper.col)
        upper_square_1 = Square(row=vertical_1.upper.row - 1, col=vertical_1.upper.col)
        upper_squares_groups = groups_by_square[upper_square_0.row][upper_square_0.col].intersection(
            groups_by_square[upper_square_1.row][upper_square_1.col],
        )
        highinverse_groups.update(upper_squares_groups)

        # Add all groups which contain the two middle squares.
        middle_squares_groups = groups_by_square[vertical_0.upper.row][vertical_0.upper.col].intersection(
            groups_by_square[vertical_1.upper.row][vertical_1.upper.col],
        )
        highinverse_groups.update(middle_squares_groups)

        # For each Highinverse column, add all (vertical) groups which contain the two highest squares of the column.
        upper_vertical_0 = Vertical(upper=upper_square_0, lower=vertical_0.upper)
        upper_vertical_1 = Vertical(upper=upper_square_1, lower=vertical_1.upper)
        highinverse_groups.update(upper_vertical_0.find_problems_solved_for_player(groups_by_square=groups_by_square))
        highinverse_groups.update(upper_vertical_1.find_problems_solved_for_player(groups_by_square=groups_by_square))

        # If the lower square of the first column is directly playable:
        if vertical_0.lower in self.directly_playable_squares:
            # Add all groups which contain both the lower square of the first column and
            # the upper square of the second column.
            lower_0_upper_1_groups = groups_by_square[vertical_0.lower.row][vertical_0.lower.col].intersection(
                groups_by_square[upper_square_1.row][upper_square_1.col],
            )
            highinverse_groups.update(lower_0_upper_1_groups)

        # If the lower square of the second column is directly playable:
        if vertical_1.lower in self.directly_playable_squares:
            # Add all groups which contain both the lower square of the second column and
            # the upper square of the first column.
            lower_1_upper_0_groups = groups_by_square[vertical_1.lower.row][vertical_1.lower.col].intersection(
                groups_by_square[upper_square_0.row][upper_square_0.col],
            )
            highinverse_groups.update(lower_1_upper_0_groups)

        # Add all groups solved by the lowinverse.
        highinverse_groups.update(self.lowinverse.find_problems_solved_for_player(groups_by_square=groups_by_square))

        return highinverse_groups


def find_all_highinverses(board: Board, lowinverses):
    """find_all_highinverses takes an iterable of Lowinverses and returns an iterable of Highinverses.

    Args:
        board (Board): a Board instance.
        lowinverses (iterable<Lowinverse>): an iterable of Lowinverses.

    Returns:
        highinverses (iterable<Highinverse>): an iterable of Highinverses.
    """
    directly_playable_squares = board.playable_squares()
    highinverses = set()
    for lowinverse in lowinverses:
        highinverse_directly_playable_squares = set()
        for vertical in lowinverse.verticals:
            if vertical.lower in directly_playable_squares:
                highinverse_directly_playable_squares.add(vertical.lower)
        highinverses.add(Highinverse(
            lowinverse=lowinverse,
            directly_playable_squares=highinverse_directly_playable_squares,
        ))
    return highinverses
