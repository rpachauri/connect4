from connect_four.game import Square
from connect_four.envs.connect_four_env import ConnectFourEnv


def is_possible(a: Square, b: Square) -> bool:
    if a == b:
        raise ValueError("a == b")

    # If the two Squares are further than 3 rows or columns apart, it is not possible for them to be connected.
    row_diff = a.row - b.row
    if abs(row_diff) > 3:
        return False
    col_diff = a.col - b.col
    if abs(col_diff) > 3:
        return False

    # If the two Squares are in the same row or column, return True.
    if row_diff == 0 or col_diff == 0:
        return True

    # If the row_diff equals the col_diff, then the two Squares can be connected diagonally.
    if abs(row_diff) != abs(col_diff):
        return False

    # Normalize row_diff and col_diff to 3.
    row_diff = row_diff // abs(row_diff) * 3
    col_diff = col_diff // abs(col_diff) * 3

    b_row_end = b.row + row_diff
    b_col_end = b.col + col_diff
    a_row_end = a.row - row_diff
    a_col_end = a.col - col_diff

    if (not (0 <= b_row_end < ConnectFourEnv.M) or not (0 <= b_col_end < ConnectFourEnv.N)) and (
            not (0 <= a_row_end < ConnectFourEnv.M) or not (0 <= a_col_end < ConnectFourEnv.N)):
        return False

    return True
