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
    # Find all threats that belong to the opponent.
    pass


def aftereven_columns(board: Board, claimevens, threat: Threat):
    """aftereven_columns takes a Board, set of Claimevens and a Threat.
    It figures out if the Threat is an Aftereven group.
    If the Threat is an Aftereven group, then it returns the Aftereven columns.
    If the Threat is not an Aftereven group, then it returns None.

    Args:
        board (Board): a Board instance.
        claimevens (set<Claimeven>): a set of Claimevens for board.
        threat (Threat): a Threat on this board.

    Returns:
        aftereven_columns (iterable<int>):
            If the given Threat is an Aftereven group, an iterable of ints,
            where each int is the column of an empty square in the Aftereven group.

            If the given Threat is not an Aftereven group, returns None.
    """
    pass
