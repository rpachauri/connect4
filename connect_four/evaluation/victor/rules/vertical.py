from typing import List, Set, Optional

from connect_four.evaluation.victor.rules import Rule
from connect_four.game import Square
from connect_four.evaluation.victor.board import Board
from connect_four.problem import Group

import warnings


class Vertical(Rule):
    def __init__(self, upper: Square, lower: Square):
        self.upper = upper
        self.lower = lower

    def __eq__(self, other):
        if isinstance(other, Vertical):
            return self.upper == other.upper and self.lower == other.lower
        return False

    def __hash__(self):
        return self.upper.__hash__() * 2141 + self.lower.__hash__() * 8243

    def solves(self, group: Group) -> bool:
        return {self.upper, self.lower}.issubset(group.squares)

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
        upper_groups = groups_by_square[self.upper.row][self.upper.col]
        lower_groups = groups_by_square[self.lower.row][self.lower.col]
        return upper_groups.intersection(lower_groups)


def find_all_verticals(board: Board) -> Set[Vertical]:
    """find_all_verticals takes a Board and returns a set of Verticals for it.

    It makes no assumptions about whose turn it is or who is the controller of the Zugzwang.

    Args:
        board (Board): a Board instance.

    Returns:
        vertical (set<Verticals>): a set of Verticals for board.
    """
    verticals = set()

    for row in range(1, len(board.state[0]) - 1, 2):
        for col in range(len(board.state[0][0])):
            upper = Square(row, col)
            lower = Square(row + 1, col)

            if board.is_empty(upper) and board.is_empty(lower):
                verticals.add(Vertical(upper, lower))

    return verticals


class VerticalManager:
    def __init__(self, board: Board):
        """Initializes the VerticalManager.

        Args:
            board (Board): a Board instance.
        """
        self.verticals = find_all_verticals(board=board)

    def move(self, square: Square) -> Optional[Vertical]:
        """Moves the internal state of the VerticalManager to after this square has been played.

        Args:
            square (Square): the square being played.

        Returns:
            removed_vertical (Optional[Vertical]): the Vertical being removed, if there is one.
        """
        removed_vertical = VerticalManager.vertical_at_square(square=square)
        if removed_vertical is not None:
            self.verticals.remove(removed_vertical)

        return removed_vertical

    @staticmethod
    def vertical_at_square(square: Square) -> Optional[Vertical]:
        if square.row % 2 == 0 and square.row != 0:  # row is even and is not the top row
            return Vertical(lower=square, upper=Square(row=square.row - 1, col=square.col))

    def undo_move(self, square: Square) -> Optional[Vertical]:
        """Undoes the most recent move, updating the set of Verticals.

        Args:
            square (Square): the square being undone.

        Returns:
            added_vertical (Optional[Vertical]): the Vertical being added, if there is one.
        """
        added_vertical = VerticalManager.vertical_at_square(square=square)
        if added_vertical is not None:
            self.verticals.add(added_vertical)

        return added_vertical
