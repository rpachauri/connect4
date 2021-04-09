from typing import List, Set

from connect_four.evaluation.victor.board import Board

from connect_four.evaluation.victor.rules import Lowinverse, Rule
from connect_four.problem import Group


class Highinverse(Rule):
    def __init__(self, lowinverse: Lowinverse, directly_playable_squares=None):
        self.lowinverse = lowinverse

        if directly_playable_squares is None:
            directly_playable_squares = set()
        self.directly_playable_squares = frozenset(directly_playable_squares)

    def __eq__(self, other):
        if isinstance(other, Highinverse):
            return self.lowinverse == other.lowinverse
        return False

    def __hash__(self):
        return self.lowinverse.__hash__()

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
        pass


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
