from connect_four.agents.victor import Vertical


class Lowinverse:
    def __init__(self, first_vertical: Vertical, second_vertical: Vertical):
        self.verticals = frozenset([
            first_vertical,
            second_vertical,
        ])

    def __eq__(self, other):
        if isinstance(other, Lowinverse):
            return self.verticals == other.verticals
        return False

    def __hash__(self):
        return self.verticals.__hash__()


def lowinverse(verticals):
    """lowinverse takes a Board and an iterable of Verticals and returns a set of Lowinverses for the Board.

    Args:
        verticals (iterable<Vertical>): an iterable of Verticals for board.

    Returns:
        lowinverses (iterable<Lowinverse>): an iterable of Lowinverses for board.
    """
    lowinverses = set()
    for first_vertical in verticals:
        for second_vertical in verticals:
            if first_vertical != second_vertical:
                lowinverses.add(Lowinverse(first_vertical, second_vertical))

    return lowinverses
