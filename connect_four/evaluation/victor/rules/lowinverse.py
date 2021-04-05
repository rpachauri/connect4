from connect_four.evaluation.victor.rules import Vertical


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


def find_all_lowinverses(verticals):
    """find_all_lowinverses takes an iterable of Verticals and returns an iterable of Lowinverses.

    Args:
        verticals (iterable<Vertical>): an iterable of Verticals.

    Returns:
        lowinverses (iterable<Lowinverse>): an iterable of Lowinverses.
    """
    lowinverses = set()
    for first_vertical in verticals:
        for second_vertical in verticals:
            if first_vertical.upper.col != second_vertical.upper.col:
                lowinverses.add(Lowinverse(first_vertical, second_vertical))

    return lowinverses
