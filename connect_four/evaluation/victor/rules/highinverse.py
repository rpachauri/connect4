from typing import List, Set
from collections import namedtuple

from connect_four.evaluation.victor.board import Board

from connect_four.evaluation.victor.rules import Lowinverse, Rule, Vertical
from connect_four.game import Square
from connect_four.problem import Group

import warnings


HighinverseColumn = namedtuple("HighinverseColumn", ["upper", "middle", "lower", "directly_playable"])


class Highinverse(Rule):
    def __init__(self, lowinverse: Lowinverse, directly_playable_squares=None, columns=None):
        self.lowinverse = lowinverse

        if directly_playable_squares is None:
            directly_playable_squares = set()
        self.directly_playable_squares = frozenset(directly_playable_squares)

        if columns is None:
            columns = set()
        self.columns = frozenset(columns)

    def __eq__(self, other):
        if isinstance(other, Highinverse):
            return (self.lowinverse == other.lowinverse and
                    self.directly_playable_squares == other.directly_playable_squares)
        return False

    def __hash__(self):
        return (self.lowinverse.__hash__() * 3217 +
                self.directly_playable_squares.__hash__() * 7207 +
                self.columns.__hash__() * 5189)

    def solves(self, group: Group) -> bool:
        if self.lowinverse.solves(group=group):
            return True

        verticals_as_list = list(self.lowinverse.verticals)
        vertical_0, vertical_1 = verticals_as_list[0], verticals_as_list[1]
        upper_square_0 = Square(row=vertical_0.upper.row - 1, col=vertical_0.upper.col)
        upper_square_1 = Square(row=vertical_1.upper.row - 1, col=vertical_1.upper.col)

        # If the lower square of the first column is directly playable:
        if (vertical_0.lower in self.directly_playable_squares and
                vertical_0.lower in group.squares and
                upper_square_1 in group.squares):
            # Return True if the Group contains both the lower square of the first column and
            # the upper square of the second column.
            return True

        # If the lower square of the second column is directly playable:
        if (vertical_1.lower in self.directly_playable_squares and
                vertical_1.lower in group.squares and
                upper_square_0 in group.squares):
            # Return True if the Group contains both the lower square of the second column and
            # the upper square of the first column.
            return True

        upper_vertical_0 = Vertical(upper=upper_square_0, lower=vertical_0.upper)
        if upper_vertical_0.solves(group=group):
            return True

        upper_vertical_1 = Vertical(upper=upper_square_1, lower=vertical_1.upper)
        if upper_vertical_1.solves(group=group):
            return True

        return upper_square_0 in group.squares and upper_square_1 in group.squares

    def is_useful(self, groups: Set[Group]) -> bool:
        already_solved_groups = set()
        for group in groups:
            for vertical in self.lowinverse.verticals:
                if vertical.solves(group=group):
                    already_solved_groups.add(group)

            if self.lowinverse.solves(group=group):
                already_solved_groups.add(group)

        # Given that already_solved_groups is a subset of groups, it will not equal groups only if there exists
        # a Group this Highinverse can solve that one of its Verticals or its Lowinverse cannot.
        return already_solved_groups != groups

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


def find_all_highinverses(board: Board, lowinverses: Set[Lowinverse]) -> Set[Highinverse]:
    """find_all_highinverses takes a set of Lowinverses and returns an set of Highinverses.

    Args:
        board (Board): a Board instance.
        lowinverses (Set<Lowinverse>): a set of Lowinverses.

    Returns:
        highinverses (Set<Highinverse>): a set of Highinverses.
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


class HighinverseManager:
    def __init__(self, board: Board, lowinverses: Set[Lowinverse]):
        """Initializes the LowinverseManager.

        Args:
            board (Board): a Board instance.
            lowinverses (Set[Lowinverse]): an set of Lowinverses for board.
        """
        self.highinverses = find_all_highinverses(board=board, lowinverses=lowinverses)

    def move(self, square: Square,
             removed_lowinverses: Set[Lowinverse],
             verticals: Set[Vertical],
             directly_playable_squares: Set[Square]) -> (Set[Highinverse], Set[Highinverse]):
        """Moves the internal state of the HighinverseManager to after this square has been played.

        Args:
            square (Square): the Square being played.
            removed_lowinverses (Set[Lowinverse]): the set of Lowinverses removed after square is played.
            verticals (Set[Vertical]): the set of Verticals in the current state.
            directly_playable_squares (Set[Square]): the set of directly playable Squares in the current state.

        Returns:
            removed_highinverses (Set[Highinverse]): the set of Highinverses removed after square is played.
            added_highinverses (Set[Highinverse]): the set of Highinverses added after square is played.
        """
        removed_highinverses, added_highinverses = HighinverseManager._removed_added_highinverses(
            square=square,
            removed_lowinverses=removed_lowinverses,
            verticals=verticals,
            directly_playable_squares=directly_playable_squares,
        )

        self.highinverses.difference_update(removed_highinverses)
        self.highinverses.update(added_highinverses)

        return removed_highinverses, added_highinverses

    @staticmethod
    def _removed_added_highinverses(
            square: Square,
            removed_lowinverses: Set[Lowinverse],
            verticals: Set[Vertical],
            directly_playable_squares: Set[Square]) -> (Set[Highinverse], Set[Highinverse]):
        """

        Args:
            square (Square): the Square being played.
            removed_lowinverses (Set[Lowinverse]): the set of Lowinverses removed after square is played.
            verticals (Set[Vertical]): the set of Verticals in the current state.
            directly_playable_squares (Set[Square]): the set of directly playable Squares in the current state.

        Returns:
            removed_highinverses (Set[Highinverse]): the set of Highinverses removed after square is played.
            added_highinverses (Set[Highinverse]): the set of Highinverses added after square is played.
        """
        removed_highinverses = set()
        added_highinverses = set()

        removed_highinverses.update(HighinverseManager._highinverse_given_lowinverses(
            lowinverses=removed_lowinverses,
            directly_playable_squares=directly_playable_squares,
        ))

        # If square is an odd square and is not in the second-from-the-top row:
        if square.row % 2 == 1 and square.row != 1:
            lower = Square(row=square.row - 1, col=square.col)
            upper = Square(row=lower.row - 1, col=square.col)
            vertical = Vertical(upper=upper, lower=lower)

            not_directly_playable_highinverses, directly_playable_highinverses = \
                HighinverseManager._directly_playable_highinverse_changes(
                    vertical=vertical,
                    verticals=verticals,
                    directly_playable_squares=directly_playable_squares
                )
            removed_highinverses.update(not_directly_playable_highinverses)
            added_highinverses.update(directly_playable_highinverses)

        return removed_highinverses, added_highinverses

    @staticmethod
    def _highinverse_given_lowinverses(
            lowinverses: Set[Lowinverse], directly_playable_squares: Set[Square]) -> Set[Highinverse]:
        """Derive a set of Highinverses given a set of Lowinverses and the set of directly playable squares.

        Args:
            lowinverses (Set[Lowinverse]): a set of Lowinverses to derive Highinverses from.
            directly_playable_squares (Set[Square]): the set of directly playable Squares.

        Returns:
            highinverses (Set[Highinverse]): a set of Highinverses derived from lowinverses and
                directly_playable_squares.
        """
        highinverses = set()

        for lowinverse in lowinverses:
            vertical0, vertical1 = tuple(lowinverse.verticals)
            lower0, lower1 = vertical0.lower, vertical1.lower
            highinverse = Highinverse(
                lowinverse=lowinverse,
                directly_playable_squares=directly_playable_squares.intersection({lower0, lower1}),
            )
            highinverses.add(highinverse)

        return highinverses

    @staticmethod
    def _directly_playable_highinverse_changes(
            vertical: Vertical,
            verticals: Set[Vertical],
            directly_playable_squares: Set[Square]) -> (Set[Highinverse], Set[Highinverse]):
        """

        Requires:
            1. The square below vertical.lower is in directly_playable_squares.
            2. vertical.lower is not in directly_playable_squares.

        Args:
            vertical (Vertical): a directly playable Vertical.
            verticals (Set[Vertical]): a set of Verticals, including vertical.
            directly_playable_squares (Set[Square]): the set of directly playable Squares.

        Returns:
            removed_highinverses (Set[Highinverse]): a set of Highinverses that would be removed after vertical.lower
                becomes directly playable.
            added_highinverses (Set[Highinverse]): a set of Highinverses that would be added after vertical.lower
                becomes directly playable.
        """
        removed_highinverses = set()
        added_highinverses = set()

        for other in verticals - {vertical}:
            if vertical.upper.col != other.upper.col:
                lowinverse = Lowinverse(first_vertical=vertical, second_vertical=other)
                removed_highinverse_directly_playable_squares = directly_playable_squares.intersection({other.lower})
                removed_highinverses.add(Highinverse(
                    lowinverse=lowinverse,
                    directly_playable_squares=removed_highinverse_directly_playable_squares,
                ))

                added_highinverse_directly_playable_squares = removed_highinverse_directly_playable_squares.union(
                    {vertical.lower},
                )
                added_highinverses.add(Highinverse(
                    lowinverse=lowinverse,
                    directly_playable_squares=added_highinverse_directly_playable_squares,
                ))
        return removed_highinverses, added_highinverses

    def undo_move(self, square: Square,
                  added_lowinverses: Set[Lowinverse],
                  verticals: Set[Vertical],
                  directly_playable_squares: Set[Square]) -> (Set[Highinverse], Set[Highinverse]):
        """Moves the internal state of the HighinverseManager to before this square has been played.

        Args:
            square (Square): the Square being undone.
            added_lowinverses (Set[Lowinverse]): the set of Lowinverses added after square is undone.
            verticals (Set[Vertical]): the set of Verticals in the state after square is undone.
            directly_playable_squares (Set[Square]): the set of directly playable Squares in the
                state after square is undone.

        Returns:
            added_highinverses (Set[Highinverse]): the set of Highinverses added after square is undone.
            removed_highinverses (Set[Highinverse]): the set of Highinverses removed after square is undone.
        """
        added_highinverses, removed_highinverses = HighinverseManager._removed_added_highinverses(
            square=square,
            removed_lowinverses=added_lowinverses,
            verticals=verticals,
            directly_playable_squares=directly_playable_squares,
        )

        self.highinverses.update(added_highinverses)
        self.highinverses.difference_update(removed_highinverses)

        return added_highinverses, removed_highinverses
