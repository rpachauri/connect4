from connect_four.agents.victor import Before
from connect_four.agents.victor import Board
from connect_four.agents.victor import Square


class Specialbefore:
    def __init__(self, before: Before, directly_playable_square: Square):
        """Initializes a Specialbefore instance.

        Args:
            before (Before): A before. At least one empty square of the Before group must be playable.
            directly_playable_square (Square): A directly playable square not part of the Before.
        """
        self.before = before
        self.directly_playable_square = directly_playable_square

    def __eq__(self, other):
        if isinstance(other, Specialbefore):
            return self.before == other.before and self.directly_playable_square == other.directly_playable_square
        return False

    def __hash__(self):
        return self.before.__hash__() * 59 + self.directly_playable_square.__hash__()


def specialbefore(board: Board, befores):
    """specialbefore takes a Board and an iterable of Befores for the Board and
    outputs an iterable of Specialbefores for the Board.

    Args:
        board (Board): a Board instance
        befores (iterable<Before>): an iterable of Befores for board.

    Returns:
        specialbefores (iterable<Specialbefore>): an iterable of Specialbefores for board.
    """
    specialbefores = set()
    directly_playable_squares = board.playable_squares()

    for before in befores:
        if contains_directly_playable_square(before, directly_playable_squares):
            for directly_playable_square in directly_playable_squares:
                if directly_playable_square not in before.threat.squares:
                    # Recall that a requirement of the Specialbefore is that the directly playable square
                    # must not be a part of the Before.
                    specialbefores.add(Specialbefore(before, directly_playable_square))

    return specialbefores


def contains_directly_playable_square(before: Before, directly_playable_squares):
    """Returns true if there exists a square in before.threat.squares that also exists in directly_playable_squares.
    Otherwise, returns false.

    Args:
        before (Before): a Before.
        directly_playable_squares (iterable<Square>): an iterable of directly playable squares.

    Returns:
        Returns true if there exists a square in before.threat that also exists in directly_playable_squares.
        Returns false otherwise.
    """
    for square in before.threat.squares:
        if square in directly_playable_squares:
            return True
    return False
