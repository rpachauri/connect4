from connect_four.game import Square
from enum import Enum

from connect_four.problem.problem import Problem


class GroupDirection(Enum):
    horizontal = 0
    up_right_diagonal = 1
    vertical = 2
    up_left_diagonal = 3


# Maps (row_diff, col_diff) to a Group Direction.
# Note that the mappings are counter-intuitive because
# we're mapping the unit-differences between the start and end square of a Group.
# e.g. (1, 0) maps to the Vertical direction because there is a difference in row but not column.
ROW_COL_DIFFS_TO_group_DIRECTION = {
    (1, 0): GroupDirection.vertical,
    (1, 1): GroupDirection.up_left_diagonal,
    (0, 1): GroupDirection.horizontal,
    (-1, 1): GroupDirection.up_right_diagonal,
    (-1, 0): GroupDirection.vertical,
    (-1, -1): GroupDirection.up_left_diagonal,
    (0, -1): GroupDirection.horizontal,
    (1, -1): GroupDirection.up_right_diagonal,
}


class Group(Problem):
    """A Group is a group of squares in a line on a TwoPlayerGameEnv state.

    Each Group belongs to a specific player (0 or 1).
    All four of the squares must be in a line.

    In order to specify a group, a client only needs to specify:
        1.  Which player the Group belongs to.
        2.  The start and end of the group (since the group must consist of 4 squares in a line).
    """

    def __init__(self, player: int, start: Square, end: Square):
        # Perform validation on player.
        if not (player == 0 or player == 1):
            raise ValueError("player must be 0 or 1. player =", player)
        self.player = player
        self.start = start
        self.end = end

        # Perform validation on start and end of group.
        row_diff = end.row - start.row
        col_diff = end.col - start.col

        # Should be a vector in one of the 8 acceptable directions.
        if row_diff != 0 and col_diff != 0:
            assert abs(row_diff) == abs(col_diff)

        # max_abs_diff is the number of squares in the group - 1.
        max_abs_diff = max(abs(row_diff), abs(col_diff))
        if max_abs_diff not in {2, 3}:
            # For now, only support lengths of 3 and 4 for Tic-Tac-Toe and ConnectFour.
            raise ValueError("Group length", max_abs_diff + 1, "not in {3, 4}")

        # Derive the squares of the group from the start and end squares.
        row_diff, col_diff = row_diff // max_abs_diff, col_diff // max_abs_diff
        square_list = [start]
        for _ in range(max_abs_diff):
            next_square = Square(square_list[-1].row + row_diff, square_list[-1].col + col_diff)
            square_list.append(next_square)
        assert square_list[-1] == end

        self.squares = frozenset(square_list)
        assert len(self.squares) == max_abs_diff + 1

        self.direction = ROW_COL_DIFFS_TO_group_DIRECTION[(row_diff, col_diff)]

    def __eq__(self, other):
        if isinstance(other, Group):
            return self.player == other.player and self.squares == other.squares
        return False

    def __hash__(self):
        return self.squares.__hash__() + self.player

    def __str__(self):
        return ("[" + str(self.player) + " -> " +
                "(" + str(self.start.row) + "," + str(self.start.col) + ")-" +
                "(" + str(self.end.row) + "," + str(self.end.col) + ")]"
                )

    def __repr__(self):
        return self.__str__()
