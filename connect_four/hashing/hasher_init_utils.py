from connect_four.hashing.data_structures import Square, Group, SquareType
from typing import List, Sequence


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
