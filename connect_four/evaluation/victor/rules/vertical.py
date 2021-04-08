from connect_four.evaluation.victor.game import Board
from connect_four.evaluation.victor.game import Square


class Vertical:
    def __init__(self, upper: Square, lower: Square):
        self.upper = upper
        self.lower = lower

    def __eq__(self, other):
        if isinstance(other, Vertical):
            return self.upper == other.upper and self.lower == other.lower
        return False

    def __hash__(self):
        return self.upper.__hash__() * 31 + self.lower.__hash__()


def find_all_verticals(board: Board):
    """find_all_verticals takes a Board and returns a set of Verticals for it.

    It makes no assumptions about whose turn it is or who is the controller of the Zugzwang.

    Args:
        board (Board): a Board instance.

    Returns:
        vertical (set<Verticals>): a set of Verticals for board.
    """
    verticals = set()

    for row in range(1, len(board.state[0]) - 1, 2):
        for col in range(len(board.state[0][0])):
            upper = Square(row, col)
            lower = Square(row + 1, col)

            if board.is_empty(upper) and board.is_empty(lower):
                verticals.add(Vertical(upper, lower))

    return verticals
