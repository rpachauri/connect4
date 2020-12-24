from connect_four.agents.victor import Board
from connect_four.agents.victor import Threat


class Before:
    def __init__(self, threat: Threat):
        """

        Args:
            threat (Threat): a Threat.
        """
        self.threat = Threat


def before(board: Board, threats):
    """before takes a Board and an iterable of Threats and returns an iterable of Befores for the Board.

    Args:
        board (Board): a Board instance.
        threats (iterable<Threat>): an iterable of Threats belonging to the opponent of the player to move on board.

    Returns:
        befores (iterable<Before>): an iterable of Befores for board.
    """
    pass
