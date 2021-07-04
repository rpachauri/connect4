from typing import List, Set
from collections import namedtuple

from connect_four.evaluation.victor.board import Board

from connect_four.evaluation.victor.rules import Rule, Vertical
from connect_four.game import Square
from connect_four.problem import Group

import warnings

HighinverseColumn = namedtuple("HighinverseColumn", ["upper", "middle", "lower", "directly_playable"])


class Highinverse(Rule):
    def __init__(self, columns: Set[HighinverseColumn]):
        if columns is None:
            columns = set()
        self.columns = frozenset(columns)

    def __eq__(self, other):
        if isinstance(other, Highinverse):
            return self.columns == other.columns
        return False

    def __hash__(self):
        return self.columns.__hash__() * 5189

    def solves(self, group: Group) -> bool:
        column_0, column_1 = tuple(self.columns)

        #  All groups which contain the two upper squares.
        if column_0.upper in group.squares and column_1.upper in group.squares:
            return True

        #  All groups which contain the two middle squares.
        if column_0.middle in group.squares and column_1.middle in group.squares:
            return True

        # All vertical groups which contain the two upper squares of the first column.
        if column_0.upper in group.squares and column_0.middle in group.squares:
            return True

        # All vertical groups which contain the two upper squares of the second column.
        if column_1.upper in group.squares and column_1.middle in group.squares:
            return True

        # All groups which contain both the lower square of the first column and the upper square of the second
        # column.
        if column_0.directly_playable and column_0.lower in group.squares and column_1.upper in group.squares:
            return True

        # All groups which contain both the lower square of the second column and the upper square of the first
        # column.
        if column_1.directly_playable and column_1.lower in group.squares and column_0.upper in group.squares:
            return True

        return False

    def is_useful(self, groups: Set[Group]) -> bool:
        return not not groups

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
        highinverse_groups = set()
        column_0, column_1 = tuple(self.columns)

        #  Add all groups which contain the two upper squares.
        upper_square_0 = column_0.upper
        upper_square_1 = column_1.upper
        upper_squares_groups = groups_by_square[upper_square_0.row][upper_square_0.col].intersection(
            groups_by_square[upper_square_1.row][upper_square_1.col],
        )
        highinverse_groups.update(upper_squares_groups)

        # Add all groups which contain the two middle squares.
        middle_squares_groups = groups_by_square[column_0.middle.row][column_0.middle.col].intersection(
            groups_by_square[column_1.middle.row][column_1.middle.col],
        )
        highinverse_groups.update(middle_squares_groups)

        # For each Highinverse column, add all (vertical) groups which contain the two highest squares of the
        # column.
        upper_vertical_0 = Vertical(upper=column_0.upper, lower=column_0.middle)
        upper_vertical_1 = Vertical(upper=column_1.upper, lower=column_1.middle)
        highinverse_groups.update(
            upper_vertical_0.find_problems_solved_for_player(groups_by_square=groups_by_square))
        highinverse_groups.update(
            upper_vertical_1.find_problems_solved_for_player(groups_by_square=groups_by_square))

        # If the lower square of the first column is directly playable:
        if column_0.directly_playable:
            # Add all groups which contain both the lower square of the first column and
            # the upper square of the second column.
            lower_0_upper_1_groups = groups_by_square[column_0.lower.row][column_0.lower.col].intersection(
                groups_by_square[upper_square_1.row][upper_square_1.col],
            )
            highinverse_groups.update(lower_0_upper_1_groups)

        # If the lower square of the second column is directly playable:
        if column_1.directly_playable:
            # Add all groups which contain both the lower square of the second column and
            # the upper square of the first column.
            lower_1_upper_0_groups = groups_by_square[column_1.lower.row][column_1.lower.col].intersection(
                groups_by_square[upper_square_0.row][upper_square_0.col],
            )
            highinverse_groups.update(lower_1_upper_0_groups)

        return highinverse_groups


def find_all_highinverse_columns(board: Board) -> Set[HighinverseColumn]:
    """find_all_highinverse_columns returns the set of HighinverseColumns for the board.

    Args:
        board (Board): a Board instance.

    Returns:
        columns (Set[HighinverseColumn]): the set of HighinverseColumns for the board.
    """
    columns = set()
    playable_squares = board.playable_squares()
    for row in range(0, len(board.state[0]) - 2, 2):
        for col in range(len(board.state[0][0])):
            upper = Square(row=row, col=col)
            middle = Square(row + 1, col)
            lower = Square(row + 2, col)
            directly_playable = lower in playable_squares
            if board.is_empty(square=upper) and board.is_empty(square=middle) and board.is_empty(square=lower):
                columns.add(HighinverseColumn(
                    upper=upper, middle=middle, lower=lower, directly_playable=directly_playable,
                ))
    return columns


def highinverses_given_column(column: HighinverseColumn, columns: Set[HighinverseColumn]) -> Set[Highinverse]:
    """

    Args:
        column (HighinverseColumn): a HighinverseColumn that all Highinverses will have.
        columns (Set[HighinverseColumn): a set of HighinverseColumns to create Highinverses with column.

    Returns:
        highinverses (Set[Highinverse]): a set of Highinverses created using the cross product
            between column and columns.
    """
    highinverses = set()
    for other_column in columns:
        if column.upper.col != other_column.upper.col:
            highinverses.add(Highinverse(columns={column, other_column}))
    return highinverses


def find_all_highinverses_using_highinverse_columns(board: Board) -> Set[Highinverse]:
    """find_all_highinverses_using_highinverse_columns returns the set of Highinverses for the board.

    Args:
        board (Board): a Board instance.

    Returns:
        highinverses (Set[Highinverse]): the set of Highinverses for the board.
    """
    columns = find_all_highinverse_columns(board=board)
    highinverses = set()
    for column in columns:
        highinverses.update(highinverses_given_column(column=column, columns=columns))
    return highinverses


class HighinverseManager:
    def __init__(self, board: Board):
        """Initializes the HighinverseManager.

        Args:
            board (Board): a Board instance.
        """
        self.columns = find_all_highinverse_columns(board=board)
        self.highinverses = set()
        for column in self.columns:
            self.highinverses.update(highinverses_given_column(column=column, columns=self.columns))

    def move(self, square: Square) -> (Set[Highinverse], Set[Highinverse]):
        """Moves the internal state of the HighinverseManager to after this square has been played.

        Args:
            square (Square): the Square being played.

        Returns:
            removed_highinverses (Set[Highinverse]): the set of Highinverses removed after square is played.
            added_highinverses (Set[Highinverse]): the set of Highinverses added after square is played.
        """
        removed_highinverses, added_highinverses = \
            HighinverseManager._removed_added_highinverses_using_highinverse_column(square=square, columns=self.columns)

        self.highinverses.difference_update(removed_highinverses)
        self.highinverses.update(added_highinverses)

        return removed_highinverses, added_highinverses

    @staticmethod
    def _removed_added_highinverses_using_highinverse_column(
            square: Square, columns: Set[HighinverseColumn]) -> (Set[Highinverse], Set[Highinverse]):
        # Try to make a column out of square
        above_2 = Square(row=square.row - 2, col=square.col)
        above = Square(row=square.row - 1, col=square.col)
        column = HighinverseColumn(upper=above_2, middle=above, lower=square, directly_playable=True)
        if square.row % 2 == 0:
            # If column is not in columns, no Highinverses are affected.
            if column not in columns:
                return set(), set()

            # Since square is an even Square, only one HighinverseColumn is removed. Thus, any Highinverses with that
            # column should be removed.
            removed_highinverses = highinverses_given_column(column=column, columns=columns)
            return removed_highinverses, set()

        # Since square is odd, the square above it was not directly playable, but now is.
        above_3 = Square(row=square.row - 3, col=square.col)
        old_column = HighinverseColumn(upper=above_3, middle=above_2, lower=above, directly_playable=False)

        # If old_column is not in columns, no Highinverses are affected.
        if old_column not in columns:
            return set(), set()

        new_column = HighinverseColumn(upper=above_3, middle=above_2, lower=above, directly_playable=True)

        removed_highinverses = highinverses_given_column(column=old_column, columns=columns)
        added_highinverses = highinverses_given_column(column=new_column, columns=columns)
        return removed_highinverses, added_highinverses

    def undo_move(self, square: Square) -> (Set[Highinverse], Set[Highinverse]):
        """Moves the internal state of the HighinverseManager to before this square has been played.

        Args:
            square (Square): the Square being undone.

        Returns:
            added_highinverses (Set[Highinverse]): the set of Highinverses added after square is undone.
            removed_highinverses (Set[Highinverse]): the set of Highinverses removed after square is undone.
        """
        added_highinverses, removed_highinverses = \
            HighinverseManager._removed_added_highinverses_using_highinverse_column(square=square, columns=self.columns)

        self.highinverses.difference_update(removed_highinverses)
        self.highinverses.update(added_highinverses)

        return added_highinverses, removed_highinverses
