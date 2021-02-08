from collections import namedtuple

from connect_four.agents.victor.game import Board
from connect_four.agents.victor.game import Group


Threat = namedtuple("Threat", ["group", "empty_square"])


def find_odd_threat(board: Board) -> Threat:
    """find_threat_combination returns an Odd Threat for White if one exists. Otherwise, returns None.
    If multiple Odd Threats exist, picks one arbitrarily.

    Args:
        board (Board): a Board instance.

    Returns:
        odd_group (Threat): a Threat with a single empty square. The single empty square will be odd.
            None if no such Threat exists for board.
    """
    # Iterate through all groups that belong to White.
    for group in board.potential_groups(player=0):
        empty_squares = empty_squares_of_group(board, group)
        if len(empty_squares) == 1:
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
