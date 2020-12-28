from connect_four.agents.victor import Before
from connect_four.agents.victor import Square


class Specialbefore:
    def __init__(self, before: Before, directly_playable_square: Square):
        """Initializes a Specialbefore instance.

        Args:
            before (Before): A before. At least one empty square of the Before group must be playable.
            directly_playable_square (Square): A directly playable square not part of the Before.
        """
        pass


def specialbefore(board: Board, befores):
    """specialbefore takes a Board and an iterable of Befores for the Board and
    outputs an iterable of Specialbefores for the Board.

    Args:
        board (Board): a Board instance
        befores (iterable<Before>): an iterable of Befores for board.

    Returns:
        specialbefores (iterable<Specialbefore>): an iterable of Specialbefores for board.
    """
    pass
