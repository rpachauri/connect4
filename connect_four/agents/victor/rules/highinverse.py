from connect_four.agents.victor.game import Board

from connect_four.agents.victor.rules import Lowinverse


class Highinverse:
    def __init__(self, lowinverse: Lowinverse, directly_playable_squares=None):
        self.lowinverse = lowinverse

        if directly_playable_squares is None:
            directly_playable_squares = set()
        self.directly_playable_squares = frozenset(directly_playable_squares)

    def __eq__(self, other):
        if isinstance(other, Highinverse):
            return self.lowinverse == other.lowinverse
        return False

    def __hash__(self):
        return self.lowinverse.__hash__()


def find_all_highinverses(board: Board, lowinverses):
    """find_all_highinverses takes an iterable of Lowinverses and returns an iterable of Highinverses.

    Args:
        board (Board): a Board instance.
        lowinverses (iterable<Lowinverse>): an iterable of Lowinverses.

    Returns:
        highinverses (iterable<Highinverse>): an iterable of Highinverses.
    """
    directly_playable_squares = board.playable_squares()
    highinverses = set()
    for lowinverse in lowinverses:
        highinverse_directly_playable_squares = set()
        for vertical in lowinverse.verticals:
            if vertical.lower in directly_playable_squares:
                highinverse_directly_playable_squares.add(vertical.lower)
        highinverses.add(Highinverse(
            lowinverse=lowinverse,
            directly_playable_squares=highinverse_directly_playable_squares,
        ))
    return highinverses
