from connect_four.agents.victor import Board
from connect_four.agents.victor.game import Threat


class Aftereven:
    def __init__(self, threat: Threat, claimevens):
        """Initializes an Aftereven instance.

        Args:
            threat (Threat): a Threat representing the Aftereven group.
            claimevens (iterable<Claimeven>): an iterable of Claimevens which are part of the Aftereven.
        """
        self.threat = threat
        self.claimevens = frozenset(claimevens)

    def __eq__(self, other):
        if isinstance(other, Aftereven):
            return self.threat == other.threat and self.claimevens == other.claimevens
        return False

    def __hash__(self):
        return self.threat.__hash__() * 31 + self.claimevens.__hash__()


def find_all_afterevens(board: Board, claimevens):
    """find_all_afterevens takes a Board and a set of Claimevens and returns a set of Afterevens for the Board.

    Args:
        board (Board): a Board instance.
        claimevens (set<Claimeven>): a set of Claimevens for board.

    Returns:
        afterevens (set<Aftereven>): a set of Afterevens for board.
    """
    # Find all threats that belong to the opponent.
    threats_of_opponent = board.potential_threats(1 - board.player)

    # Dictionary of the upper square of a Claimeven to the Claimeven itself.
    even_squares_to_claimevens = {}
    for claimeven in claimevens:
        even_squares_to_claimevens[claimeven.upper] = claimeven

    afterevens = set()
    for threat in threats_of_opponent:
        aftereven_claimevens = get_aftereven_claimevens(board, even_squares_to_claimevens, threat)
        if aftereven_claimevens is not None:
            afterevens.add(Aftereven(threat, aftereven_claimevens))

    return afterevens


def get_aftereven_claimevens(board: Board, even_squares_to_claimevens, threat: Threat):
    """get_aftereven_claimevens takes a Board, set of Claimevens and a Threat.
    It figures out if the Threat is an Aftereven group.
    If the Threat is an Aftereven group, then it returns the Claimevens which are part of the Aftereven.
    If the Threat is not an Aftereven group, then it returns None.

    Args:
        board (Board): a Board instance.
        even_squares_to_claimevens (dict<Square, Claimeven>): dictionary of Squares to Claimevens.
            Each Square in the key set is the even square of a Claimeven on the board.
            It maps to the Claimeven it is a part of.
        threat (Threat): a Threat on this board.

    Returns:
        claimevens (iterable<Claimeven>):
            If the given Threat is an Aftereven group, an iterable of Claimevens,
            where the upper square of each Claimeven is an empty square in the Aftereven group.

            If the given Threat is not an Aftereven group, returns None.
    """
    claimevens = set()

    for square in threat.squares:
        # If a square is in the top row, then this would be a useless Aftereven.
        if square.row == 0:
            return None

        # If the square is not empty, we assume it already belongs to the player who owns the Threat.
        if board.is_empty(square):
            if square in even_squares_to_claimevens:
                claimevens.add(even_squares_to_claimevens[square])
            else:
                # If an empty square does not belong to any of the Claimeven even squares,
                # then the Threat is not an Aftereven group.
                return None

    return claimevens
