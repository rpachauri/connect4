from typing import Set

from connect_four.evaluation.victor import Board, Square
from connect_four.evaluation.victor import Group
from connect_four.evaluation.victor.threat_hunter.odd_group_guarantor import OddGroupGuarantor


class Threat(OddGroupGuarantor):
    def __init__(self, group: Group, empty_square: Square):
        self.group = group
        self.empty_square = empty_square

    def __eq__(self, other):
        if isinstance(other, Threat):
            return self.group == other.group and self.empty_square == other.empty_square
        return False

    def __hash__(self):
        return self.group.__hash__() * 97 + self.empty_square.__hash__() * 31

    def columns(self) -> Set[int]:
        return {self.empty_square.col}


def find_odd_threat(board: Board) -> Threat:
    """find_threat_combination returns an Odd Threat for White if one exists. Otherwise, returns None.
    If multiple Odd Threats exist, picks one arbitrarily.

    Args:
        board (Board): a Board instance.

    Returns:
        odd_group (Threat): a Threat with a single empty square. The single empty square will be odd.
            None if no such Threat exists for board.
    """
    directly_playable_squares = board.playable_squares()
    # Iterate through all groups that belong to White.
    for group in board.potential_groups(player=0):
        empty_squares = empty_squares_of_group(board, group)
        if len(empty_squares) == 1 and empty_squares[0] not in directly_playable_squares:
            return Threat(group, empty_squares[0])


def empty_squares_of_group(board: Board, group: Group):
    """Returns a list of all empty Squares that belong to group.

    Args:
        board (Board): a Board instance.
        group (Group): a Group on Board.

    Returns:
        empty_squares (List<Square>): a list of empty Squares that belong to group.
    """
    empty_squares = []
    for square in group.squares:
        if board.is_empty(square):
            empty_squares.append(square)
    return empty_squares
