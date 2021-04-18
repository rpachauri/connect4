from typing import List, Set

from connect_four.evaluation.victor.rules import Rule
from connect_four.game import Square
from connect_four.evaluation.victor.board import Board
from connect_four.problem import Group


class Baseinverse(Rule):
    def __init__(self, playable1: Square, playable2: Square):
        if playable1 == playable2:
            raise ValueError(playable1, "==", playable2)

        self.squares = frozenset([
            playable1,
            playable2,
        ])

    def __eq__(self, other):
        if isinstance(other, Baseinverse):
            return self.squares == other.squares
        return False

    def __hash__(self):
        return self.squares.__hash__()

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
        square1, square2 = tuple(self.squares)
        groups1 = groups_by_square[square1.row][square1.col]
        groups2 = groups_by_square[square2.row][square2.col]
        return groups1.intersection(groups2)


def find_all_baseinverses(board: Board):
    """find_all_baseinverses takes a Board and returns a set of Baseinverses for it.

    It makes no assumptions about whose turn it is or who is the controller of the Zugzwang.

    Args:
        board (Board): a Board instance.

    Returns:
        baseinverses (set<Baseinverse>): a set of Baseinverses for board.
    """
    baseinverses = set()
    playable_squares = board.playable_squares()

    for playable1 in playable_squares:
        for playable2 in playable_squares:
            if playable1 != playable2:
                baseinverses.add(Baseinverse(playable1, playable2))
    return baseinverses


class BaseinverseManager:
    def __init__(self, board: Board):
        """Initializes the BaseinverseManager.

        Args:
            board (Board): a Board instance.
        """
        pass

    def move(self, square: Square, playable_squares: Set[Square]) -> (Set[Baseinverse], Set[Baseinverse]):
        """Moves the internal state of the BaseinverseManager to after this square has been played.

        Args:
            square (Square): the square being played.
            playable_squares (Set[Square]): the set of directly playable squares, including square.

        Returns:
            removed_baseinverses (Set[Baseinverse]): the set of Baseinverses Claimeven being removed.
            added_baseinverses (Set[Baseinverse]): the set of Baseinverses Claimeven being added.
        """
        pass

    def undo_move(self) -> (Set[Baseinverse], Set[Baseinverse]):
        """Undoes the most recent move, updating the set of Baseinverses.

        Returns:
            removed_baseinverses (Set[Baseinverse]): the set of Baseinverses Claimeven being removed.
            added_baseinverses (Set[Baseinverse]): the set of Baseinverses Claimeven being added.
        """
        pass
