from connect_four.agents.victor import Lowinverse


class Highinverse:
    def __init__(self, lowinverse: Lowinverse):
        self.lowinverse = lowinverse

    def __eq__(self, other):
        if isinstance(other, Highinverse):
            return self.lowinverse == other.lowinverse
        return False

    def __hash__(self):
        return self.lowinverse.__hash__()


def find_all_highinverses(lowinverses):
    """find_all_highinverses takes an iterable of Lowinverses and returns an iterable of Highinverses.

    Args:
        lowinverses (iterable<Lowinverse>): an iterable of Lowinverses.

    Returns:
        highinverses (iterable<Highinverse>): an iterable of Highinverses.
    """
    highinverses = set()
    for lowinverse in lowinverses:
        highinverses.add(Highinverse(lowinverse))
    return highinverses
