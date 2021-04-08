from connect_four.evaluation.victor.game import Board
from connect_four.evaluation.victor.game import Square


class Baseclaim:
    def __init__(self, first: Square, second: Square, third: Square):
        """Initializes a Baseclaim instance.

        Args:
            first (Square): A directly playable Square. Left of the second square.
            second (Square): A directly playable odd Square.
            third (Square): A directly playable Square. Right of the second square.
        """
        self.first = first
        self.second = second
        self.third = third

    def __eq__(self, other):
        if isinstance(other, Baseclaim):
            return self.first == other.first and self.second == other.second and self.third == other.third
        return False

    def __hash__(self):
        return self.first.__hash__() * 41 + self.second.__hash__() * 31 + self.third.__hash__()


def find_all_baseclaims(board: Board):
    """find_all_baseclaims takes a Board and returns an iterable of Baseclaims for the Board.

    Args:
        board (Board): a Board instance.

    Returns:
        baseclaims (iterable<Baseclaim>): an iterable of Baseclaims for board.
    """
    baseclaims = set()
    playable_squares = board.playable_squares()

    for first in playable_squares:
        for second in playable_squares:
            if first == second or second.row % 2 == 0:
                continue
            for third in playable_squares:
                if third == first or third == second:
                    continue
                if in_order(first, second, third):
                    baseclaims.add(Baseclaim(first, second, third))

    return baseclaims


def in_order(first: Square, second: Square, third: Square):
    """Returns whether or not the three given squares are in order.

    Args:
        first (Square): A directly playable Square.
        second (Square): A directly playable odd Square.
        third (Square): A directly playable Square.

    Returns:
        ordered (bool): True if the squares can be numbered left-to-right starting
            from the first square and allowing for loops. Otherwise, False.
    """
    return ((first.col < second.col < third.col) or
            (second.col < third.col < first.col) or
            (third.col < first.col < second.col))
