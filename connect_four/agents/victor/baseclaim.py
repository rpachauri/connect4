from connect_four.agents.victor import Board
from connect_four.agents.victor import Square


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


def baseclaim(board: Board):
    """baseclaim takes a Board and returns an iterable of Baseclaims for the Board.

    Args:
        board (Board): a Board instance.

    Returns:
        baseclaims (iterable<Baseclaim>): an iterable of Baseclaims for board.
    """
    pass
