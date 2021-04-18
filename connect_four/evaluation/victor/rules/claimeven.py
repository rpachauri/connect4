from typing import List, Set, Optional

from connect_four.evaluation.victor.rules import Rule
from connect_four.game import Square
from connect_four.evaluation.victor.board import Board
from connect_four.problem import Group


class Claimeven(Rule):
    def __init__(self, upper: Square, lower: Square):
        self.upper = upper
        self.lower = lower

    def __eq__(self, other):
        if isinstance(other, Claimeven):
            return self.upper == other.upper and self.lower == other.lower
        return False

    def __hash__(self):
        return self.upper.__hash__() * 31 + self.lower.__hash__()

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
        # Return problems that belong to either player at the upper square.
        white_problems_solved = self.find_problems_solved_for_player(groups_by_square=groups_by_square_by_player[0])
        black_problems_solved = self.find_problems_solved_for_player(groups_by_square=groups_by_square_by_player[1])
        return white_problems_solved.union(black_problems_solved)

    def find_problems_solved_for_player(self, groups_by_square: List[List[Set[Group]]]) -> Set[Group]:
        return groups_by_square[self.upper.row][self.upper.col]


def find_all_claimevens(board: Board):
    """find_all_claimevens takes a Board and returns a set of Claimevens for it.

    It makes no assumptions about whose turn it is or who is the controller of the Zugzwang.

    Args:
        board (Board): a Board instance.

    Returns:
        claimevens (set<Claimeven>): a set of Claimevens for board.
    """
    claimevens = set()

    for row in range(0, len(board.state[0]), 2):
        for col in range(len(board.state[0][0])):
            upper = Square(row, col)
            lower = Square(row + 1, col)

            if board.is_empty(upper) and board.is_empty(lower):
                claimevens.add(Claimeven(upper, lower))

    return claimevens


class ClaimevenManager:
    def __init__(self, board: Board):
        """

        Args:
            board (Board): a Board instance.
        """
        self.claimevens = find_all_claimevens(board=board)

    def find_all_claimevens(self) -> Set[Claimeven]:
        """

        Returns:
            claimevens (set<Claimeven>): the set of Claimevens for the current state.
        """
        return self.claimevens

    def move(self, row: int, col: int) -> Optional[Claimeven]:
        """Moves the internal state of the ClaimevenManager to after this square has been played.

        Args:
            row (int): the row being played.
            col (int): the col being played.

        Returns:
            removed_claimeven (Optional[Claimeven]): the Claimeven being removed, if there is one.
        """
        pass

    def undo_move(self) -> Optional[Claimeven]:
        """Undoes the most recent move, updating the set of Claimevens.

        Returns:
            added_claimeven (Optional[Claimeven]): the Claimeven being added, if there is one.
        """
        pass
