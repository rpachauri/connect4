import numpy as np

from enum import Enum
from typing import List


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


def convert_square_types_to_transposition_arr(square_types: List[List[SquareType]]):
    transposition_arr = []
    for row in range(len(square_types)):
        cols = []
        for col in range(len(square_types[0])):
            cols.append(SQUARE_TYPE_TO_SQUARE_CHAR[square_types[row][col]])
        transposition_arr.append(cols)
    return np.array(transposition_arr)


def get_transposition(transposition_arr):
    return ''.join(transposition_arr.flatten())
