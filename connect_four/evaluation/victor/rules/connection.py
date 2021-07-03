from connect_four.game import Square


def is_possible(a: Square, b: Square) -> bool:
    if a == b:
        raise ValueError("a == b")

    # If the two Squares are further than 3 rows or columns apart, it is not possible for them to be connected.
    row_diff = abs(a.row - b.row)
    if row_diff > 3:
        return False
    col_diff = abs(a.col - b.col)
    if col_diff > 3:
        return False

    # If the two Squares are in the same row or column, return True.
    if row_diff == 0 or col_diff == 0:
        return True

    # If the row_diff equals the col_diff, then the two Squares can be connected diagonally.
    return row_diff == col_diff
