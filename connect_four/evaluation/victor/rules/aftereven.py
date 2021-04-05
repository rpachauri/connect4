from connect_four.evaluation.victor import Board
from connect_four.evaluation.victor import Group


class Aftereven:
    def __init__(self, group: Group, claimevens):
        """Initializes an Aftereven instance.

        Args:
            group (Group): a group representing the Aftereven group.
            claimevens (iterable<Claimeven>): an iterable of Claimevens which are part of the Aftereven.
        """
        self.group = group
        self.claimevens = frozenset(claimevens)

    def __eq__(self, other):
        if isinstance(other, Aftereven):
            return self.group == other.group and self.claimevens == other.claimevens
        return False

    def __hash__(self):
        return self.group.__hash__() * 31 + self.claimevens.__hash__()

    def empty_squares_of_aftereven_group(self):
        empty_squares = []

        for claimeven in self.claimevens:
            # claimeven.upper should be an empty square part of the Aftereven group by definition.
            # Otherwise, something is wrong.
            empty_squares.append(claimeven.upper)

        return empty_squares


def find_all_afterevens(board: Board, claimevens, opponent_groups):
    """find_all_afterevens takes a Board and a set of Claimevens and returns a set of Afterevens for the Board.

    Args:
        board (Board): a Board instance.
        claimevens (set<Claimeven>): a set of Claimevens for board.
        opponent_groups (iterable<Group>): an iterable of Groups belonging to the
            opponent of the player to move on board.

    Returns:
        afterevens (set<Aftereven>): a set of Afterevens for board.
    """
    # Dictionary of the upper square of a Claimeven to the Claimeven itself.
    even_squares_to_claimevens = {}
    for claimeven in claimevens:
        even_squares_to_claimevens[claimeven.upper] = claimeven

    afterevens = set()
    for group in opponent_groups:
        aftereven_claimevens = get_aftereven_claimevens(board, even_squares_to_claimevens, group)
        if aftereven_claimevens is not None:
            afterevens.add(Aftereven(group, aftereven_claimevens))

    return afterevens


def get_aftereven_claimevens(board: Board, even_squares_to_claimevens, group: Group):
    """get_aftereven_claimevens takes a Board, set of Claimevens and a group.
    It figures out if the group is an Aftereven group.
    If the group is an Aftereven group, then it returns the Claimevens which are part of the Aftereven.
    If the group is not an Aftereven group, then it returns None.

    Args:
        board (Board): a Board instance.
        even_squares_to_claimevens (dict<Square, Claimeven>): dictionary of Squares to Claimevens.
            Each Square in the key set is the even square of a Claimeven on the board.
            It maps to the Claimeven it is a part of.
        group (Group): a group on this board.

    Returns:
        claimevens (iterable<Claimeven>):
            If the given group is an Aftereven group, an iterable of Claimevens,
            where the upper square of each Claimeven is an empty square in the Aftereven group.

            If the given group is not an Aftereven group, returns None.
    """
    claimevens = set()

    for square in group.squares:
        # If the square is not empty, we assume it already belongs to the player who owns the Group.
        if board.is_empty(square):
            # If a square is in the top row, then this would be a useless Aftereven.
            if square.row == 0:
                return None
            if square in even_squares_to_claimevens:
                claimevens.add(even_squares_to_claimevens[square])
            else:
                # If an empty square does not belong to any of the Claimeven even squares,
                # then the Group is not an Aftereven group.
                return None

    return claimevens
