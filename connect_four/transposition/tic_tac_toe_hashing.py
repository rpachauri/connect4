from enum import Enum

import numpy as np


class SquareType(Enum):
    Empty = 0
    Indifferent = 1
    Player1 = 2
    Player2 = 3


SQUARE_TYPE_TO_SQUARE_CHAR = {
    SquareType.Empty: "0",
    SquareType.Indifferent: "3",
    SquareType.Player1: "1",
    SquareType.Player2: "2",
}

GROUPS = [
    [(0, 0), (0, 1), (0, 2)],
    [(1, 0), (1, 1), (1, 2)],
    [(2, 0), (2, 1), (2, 2)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 1), (1, 1), (2, 1)],
    [(0, 2), (1, 2), (2, 2)],
    [(0, 0), (1, 1), (2, 2)],
    [(2, 0), (1, 1), (0, 2)],
]


def hash_position(state) -> str:
    """

    Args:
        state (np.ndarray): a state in the State space of TwoPlayerGameEnv.

    Returns:
        transposition (str): a string representing the transposition for state.
    """
    transposition = get_transposition(state=state)
    for k in range(3):
        rotated_transposition = get_transposition(state=np.rot90(m=state, k=k, axes=(1, 2)))
        if rotated_transposition < transposition:
            transposition = rotated_transposition
    flipped = np.fliplr(m=state)
    for k in range(4):
        flipped_rotated_transposition = get_transposition(state=np.rot90(m=flipped, k=k, axes=(1, 2)))
        if flipped_rotated_transposition < transposition:
            transposition = flipped_rotated_transposition

    # Return state to the given orientation.
    np.fliplr(m=state)
    np.rot90(m=state)

    return transposition


def get_transposition(state):
    transposition = ""
    for row in range(3):
        for col in range(3):
            square_type = determine_square_type(state=state, row=row, col=col)
            transposition += SQUARE_TYPE_TO_SQUARE_CHAR[square_type]
    return transposition


def determine_square_type(state, row: int, col: int) -> SquareType:
    if state[0][row][col] == 0 and state[1][row][col] == 0:
        return SquareType.Empty
    if is_indifferent(state=state, row=row, col=col):
        return SquareType.Indifferent
    if state[0][row][col] == 1:
        return SquareType.Player1
    # state[1][row][col] == 1
    return SquareType.Player2


def is_indifferent(state, row: int, col: int) -> bool:
    if state[0][row][col] == 1:
        return _is_indifferent(state=state, row=row, col=col, player=0)
    else:
        return _is_indifferent(state=state, row=row, col=col, player=1)


def _is_indifferent(state, row: int, col: int, player: int) -> bool:
    for group in GROUPS:
        # If the given (row, col) is in the group and the opponent does not contain a square in the group:
        if (row, col) in group and _is_clear(state=state, group=group, player=1-player):
            return False
    # If all of the groups the given (row, col) are in also contain a square that belongs to the opponent:
    return True


def _is_clear(state, group, player: int) -> bool:
    for (row, col) in group:
        if state[player][row][col] == 1:
            return False
    return True
