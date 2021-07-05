from typing import List, Set

from connect_four.evaluation.victor.rules import Rule, connection
from connect_four.game import Square
from connect_four.evaluation.victor.board import Board
from connect_four.problem import Group

import warnings


class Baseclaim(Rule):
    def __init__(self, first: Square, second: Square, third: Square):
        """Initializes a Baseclaim instance.

        Args:
            first (Square): A directly playable Square. Left of the second square.
            second (Square): A directly playable odd Square.
            third (Square): A directly playable Square. Right of the second square.
        """
        self.first = first
        self.second = second
        self.third = third

    def __eq__(self, other):
        if isinstance(other, Baseclaim):
            return self.first == other.first and self.second == other.second and self.third == other.third
        return False

    def __hash__(self):
        return self.first.__hash__() * 5347 + self.second.__hash__() * 9209 + self.third.__hash__() * 7549

    def solves(self, group: Group) -> bool:
        square_above_second = Square(row=self.second.row - 1, col=self.second.col)
        if self.first in group.squares and square_above_second in group.squares:
            return True

        return self.second in group.squares and self.third in group.squares

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
        groups = set()

        # Add all groups which contain the first playable square and the square above the second playable square.
        square_above_second = Square(row=self.second.row - 1, col=self.second.col)
        groups.update(groups_by_square[self.first.row][self.first.col].intersection(
            groups_by_square[square_above_second.row][square_above_second.col]))

        # Add all groups which contain the second and third playable square.
        groups.update(groups_by_square[self.second.row][self.second.col].intersection(
            groups_by_square[self.third.row][self.third.col]))
        return groups


def find_all_baseclaims(board: Board) -> Set[Baseclaim]:
    """find_all_baseclaims takes a Board and returns an iterable of Baseclaims for the Board.

    Args:
        board (Board): a Board instance.

    Returns:
        baseclaims (iterable<Baseclaim>): an iterable of Baseclaims for board.
    """
    baseclaims = set()
    playable_squares = board.playable_squares()

    for first in playable_squares:
        for second in playable_squares:
            square_above_second = Square(row=second.row - 1, col=second.col)
            if first == second or second.row % 2 == 0:
                continue
            for third in playable_squares:
                if third == first or third == second:
                    continue
                if connection.is_possible(a=first, b=square_above_second) and connection.is_possible(a=second, b=third):
                    baseclaims.add(Baseclaim(first=first, second=second, third=third))
                if connection.is_possible(a=third, b=square_above_second) and connection.is_possible(a=second, b=first):
                    baseclaims.add(Baseclaim(first=third, second=second, third=first))

    return baseclaims


class BaseclaimManager:
    def __init__(self, board: Board):
        """Initializes the BaseclaimManager.

        Args:
            board (Board): a Board instance.
        """
        self.baseclaims = find_all_baseclaims(board=board)

    def move(self, square: Square, directly_playable_squares: Set[Square]) -> (Set[Baseclaim], Set[Baseclaim]):
        """Moves the internal state of the BaseclaimManager to after this square has been played.

        Requires:
            1. square must be in directly_playable_squares.

        Args:
            square (Square): the square being played.
            directly_playable_squares (Set[Square]): the set of directly playable Squares in the current state.

        Returns:
            removed_baseclaims (Set[Baseclaim]): the set of Baseclaims removed after square is played.
            added_baseclaims (Set[Baseclaim]): the set of Baseclaims added after square is played.
        """
        removed_baseclaims = set()
        added_baseclaims = set()

        removed_baseclaims.update(BaseclaimManager._baseclaims_given_first_and_third_square(
            square=square,
            directly_playable_squares=directly_playable_squares,
        ))
        removed_baseclaims.update(BaseclaimManager._baseclaims_given_second_square(
            second=square,
            directly_playable_squares=directly_playable_squares,
        ))
        if square.row > 0:
            square_above = Square(row=square.row - 1, col=square.col)
            added_baseclaims.update(BaseclaimManager._baseclaims_given_first_and_third_square(
                square=square_above,
                directly_playable_squares=directly_playable_squares,
            ))
            added_baseclaims.update(BaseclaimManager._baseclaims_given_second_square(
                second=square_above,
                directly_playable_squares=directly_playable_squares,
            ))

        self.baseclaims.difference_update(removed_baseclaims)
        self.baseclaims.update(added_baseclaims)

        return removed_baseclaims, added_baseclaims

    @staticmethod
    def _baseclaims_given_first_and_third_square(
            square: Square, directly_playable_squares: Set[Square]) -> Set[Baseclaim]:
        """Given a square, find all Baseclaims that can be formed using square as
            either the first or third square of the Baseclaim.

        Args:
            square (Square): the square to be used as either the first or third square of the created Baseclaims.
            directly_playable_squares (Set[Square]): the set of directly playable squares that can be used to create
                Baseclaims.

        Returns:
            baseclaims (Set[Baseclaim]): the set of Baseclaims that can be formed using square as either the first
                or third square of the Baseclaim.
        """
        first = square
        baseclaims = set()
        for second in directly_playable_squares:
            square_above_second = Square(row=second.row - 1, col=second.col)
            if first.col == second.col or second.row % 2 == 0:
                continue
            for third in directly_playable_squares:
                if first.col == third.col or second.col == third.col:
                    continue
                if connection.is_possible(a=first, b=square_above_second) and connection.is_possible(a=second, b=third):
                    baseclaims.add(Baseclaim(first=first, second=second, third=third))
                if connection.is_possible(a=third, b=square_above_second) and connection.is_possible(a=second, b=first):
                    baseclaims.add(Baseclaim(first=third, second=second, third=first))

        return baseclaims

    @staticmethod
    def _baseclaims_given_second_square(
            second: Square, directly_playable_squares: Set[Square]) -> Set[Baseclaim]:
        """Given a square, find all Baseclaims that can be formed using square as
            the second square of the Baseclaim.

        Args:
            second (Square): the square to be used as second square of the created Baseclaims.
            directly_playable_squares (Set[Square]): the set of directly playable squares that can be used to create
                Baseclaims.

        Returns:
            baseclaims (Set[Baseclaim]): the set of Baseclaims that can be formed using square as the second
                square of the Baseclaim.
        """
        # If square is even, return an empty set because square must be odd to be the second square of a Baseclaim.
        if second.row % 2 == 0:
            return set()

        square_above_second = Square(row=second.row - 1, col=second.col)

        baseclaims = set()
        for first in directly_playable_squares:
            if first.col == second.col:
                continue
            for third in directly_playable_squares:
                if first.col == third.col or second.col == third.col:
                    continue
                if connection.is_possible(a=first, b=square_above_second) and connection.is_possible(a=second, b=third):
                    baseclaims.add(Baseclaim(first=first, second=second, third=third))
                if connection.is_possible(a=third, b=square_above_second) and connection.is_possible(a=second, b=first):
                    baseclaims.add(Baseclaim(first=third, second=second, third=first))

        return baseclaims

    def undo_move(self, square: Square, directly_playable_squares: Set[Square]) -> (Set[Baseclaim], Set[Baseclaim]):
        """Moves the internal state of the BaseclaimManager to before this square has been played.

        Requires:
            1. square must be in directly_playable_squares.

        Args:
            square (Square): the square being played.
            directly_playable_squares (Set[Square]): the set of directly playable Squares in the current state.

        Returns:
            added_baseclaims (Set[Baseclaim]): the set of Baseclaims removed after square is undone.
            removed_baseclaims (Set[Baseclaim]): the set of Baseclaims removed after square is undone.
        """
        added_baseclaims = set()
        removed_baseclaims = set()

        added_baseclaims.update(BaseclaimManager._baseclaims_given_first_and_third_square(
            square=square,
            directly_playable_squares=directly_playable_squares,
        ))
        added_baseclaims.update(BaseclaimManager._baseclaims_given_second_square(
            second=square,
            directly_playable_squares=directly_playable_squares,
        ))
        if square.row > 0:
            square_above = Square(row=square.row - 1, col=square.col)
            removed_baseclaims.update(BaseclaimManager._baseclaims_given_first_and_third_square(
                square=square_above,
                directly_playable_squares=directly_playable_squares,
            ))
            removed_baseclaims.update(BaseclaimManager._baseclaims_given_second_square(
                second=square_above,
                directly_playable_squares=directly_playable_squares,
            ))

        self.baseclaims.difference_update(removed_baseclaims)
        self.baseclaims.update(added_baseclaims)

        return added_baseclaims, removed_baseclaims
