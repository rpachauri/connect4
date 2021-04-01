import numpy as np

from connect_four.hashing.data_structures import Square, Group, SquareType
from typing import List, Sequence


SQUARE_TYPE_TO_SQUARE_CHAR = {
    SquareType.Empty: "0",
    SquareType.Indifferent: "3",
    SquareType.Player1: "1",
    SquareType.Player2: "2",
}


def create_initial_groups_by_squares(num_rows: int, num_cols: int, all_groups: Sequence[Group]):
    groups_by_square = []
    for player in range(2):
        player_squares = []
        for row in range(num_rows):
            rows = []
            for col in range(num_cols):
                groups_at_square = set()
                square = Square(row=row, col=col)
                for group in all_groups:
                    if square in group.squares:
                        groups_at_square.add(group)
                rows.append(groups_at_square)
            player_squares.append(rows)
        groups_by_square.append(player_squares)
    return groups_by_square


def create_initial_square_types(num_rows: int, num_cols: int) -> List[List[SquareType]]:
    square_types = []
    for row in range(num_rows):
        rows = []
        for col in range(num_cols):
            rows.append(SquareType.Empty)
        square_types.append(rows)
    return square_types


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
