from connect_four.agents.victor import Board
from connect_four.agents.victor import Square
from connect_four.agents.victor import Threat


class Aftereven:
    def __init__(self, threat, columns):
        self.threat = threat
        self.columns = frozenset(columns)

    def __eq__(self, other):
        if isinstance(other, Aftereven):
            return self.threat == other.threat and self.columns == other.columns
        return False


def aftereven(board: Board, claimevens):
    """aftereven takes a Board and a set of Claimevens and returns a set of Afterevens for the Board.

    Args:
        board (Board): a Board instance.
        claimevens (set<Claimeven>): a set of Claimevens for board.

    Returns:
        afterevens (set<Aftereven>): a set of Afterevens for board.
    """
    pass