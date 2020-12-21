from connect_four.agents.victor import Board
from connect_four.agents.victor import Vertical


class Lowinverse:
    def __init__(self, first_vertical: Vertical, second_vertical: Vertical):
        self.first_vertical = first_vertical
        self.second_vertical = second_vertical

    def __eq__(self, other):
        if isinstance(other, Lowinverse):
            return self.first_vertical == other.first_vertical and self.second_vertical == other.second_vertical
        return False

    def __hash__(self):
        return self.first_vertical.__hash__() * 31 + self.second_vertical.__hash__()


def lowinverse(board: Board, verticals):
    """lowinverse takes a Board and an iterable of Verticals and returns a set of Lowinverses for the Board.

    Args:
        board (Board): a Board instance.
        verticals (iterable<Vertical>): an iterable of Verticals for board.

    Returns:
        lowinverses (iterable<Lowinverse>): an iterable of Lowinverses for board.
    """
    pass