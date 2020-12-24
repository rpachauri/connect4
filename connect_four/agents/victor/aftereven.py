from connect_four.agents.victor import Board
from connect_four.agents.victor import Threat


class Aftereven:
    def __init__(self, threat: Threat, columns):
        self.threat = threat
        self.columns = frozenset(columns)

    def __eq__(self, other):
        if isinstance(other, Aftereven):
            return self.threat == other.threat and self.columns == other.columns
        return False

    def __hash__(self):
        return self.threat.__hash__() * 31 + self.columns.__hash__()


def aftereven(board: Board, claimevens):
    """aftereven takes a Board and a set of Claimevens and returns a set of Afterevens for the Board.

    Args:
        board (Board): a Board instance.
        claimevens (set<Claimeven>): a set of Claimevens for board.

    Returns:
        afterevens (set<Aftereven>): a set of Afterevens for board.
    """
    # Find all threats that belong to the opponent.
    threats_of_opponent = board.potential_threats(1 - board.player)

    # Find all even squares of Claimevens.
    claimeven_even_squares = set()
    for claimeven in claimevens:
        claimeven_even_squares.add(claimeven.upper)

    afterevens = set()
    for threat in threats_of_opponent:
        columns = aftereven_columns(board, claimeven_even_squares, threat)
        if columns is not None:
            afterevens.add(Aftereven(threat, columns))

    return afterevens


def aftereven_columns(board: Board, claimeven_even_squares, threat: Threat):
    """aftereven_columns takes a Board, set of Claimevens and a Threat.
    It figures out if the Threat is an Aftereven group.
    If the Threat is an Aftereven group, then it returns the Aftereven columns.
    If the Threat is not an Aftereven group, then it returns None.

    Args:
        board (Board): a Board instance.
        claimeven_even_squares (set<Square>): a set of Squares for board.
            Each Square is the even square of a Claimeven on the board.
        threat (Threat): a Threat on this board.

    Returns:
        aftereven_columns (iterable<int>):
            If the given Threat is an Aftereven group, an iterable of ints,
            where each int is the column of an empty square in the Aftereven group.

            If the given Threat is not an Aftereven group, returns None.
    """
    columns = set()

    for square in threat.squares:
        # If the square is not empty, we assume it already belongs to the player who owns the Threat.
        if board.is_empty(square):
            if square in claimeven_even_squares:
                columns.add(square.col)
            else:
                # If an empty square does not belong to any of the Claimeven even squares,
                # then the Threat is not an Aftereven group.
                return None

    return columns
