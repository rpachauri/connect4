from connect_four.agents.victor.game import Square
from enum import Enum


class ThreatDirection(Enum):
    horizontal = 0
    up_right_diagonal = 1
    vertical = 2
    up_left_diagonal = 3


# Maps (row_diff, col_diff) to a Threat Direction.
# Note that the mappings are counter-intuitive because
# we're mapping the unit-differences between the start and end square of a Threat.
# e.g. (1, 0) maps to the Vertical direction because there is a difference in row but not column.
ROW_COL_DIFFS_TO_THREAT_DIRECTION = {
    (1, 0): ThreatDirection.vertical,
    (1, 1): ThreatDirection.up_left_diagonal,
    (0, 1): ThreatDirection.horizontal,
    (-1, 1): ThreatDirection.up_right_diagonal,
    (-1, 0): ThreatDirection.vertical,
    (-1, -1): ThreatDirection.up_left_diagonal,
    (0, -1): ThreatDirection.horizontal,
    (1, -1): ThreatDirection.up_right_diagonal,
}


class Threat:
    """A Threat is a group of 4 squares on a Connect Four board.

    Each Threat belongs to a specific player (0 or 1).
    All four of the squares must be in a line.

    In order to specify a threat, a client only needs to specify:
        1.  Which player the Threat belongs to.
        2.  The start and end of the threat (since the threat must consist of 4 squares in a line).
    """

    def __init__(self, player: int, start: Square, end: Square):
        # Perform validation on player.
        if not (player == 0 or player == 1):
            raise ValueError("player must be 0 or 1. player =", player)
        self.player = player
        self.start = start
        self.end = end

        # Perform validation on start and end of threat.
        row_diff = end.row - start.row
        col_diff = end.col - start.col
        if not (row_diff == -3 or row_diff == 0 or row_diff == 3) or not (
                col_diff == -3 or col_diff == 0 or col_diff == 3):
            raise ValueError("Invalid threat line:", start, "-", end)

        # Derive the four squares of the threat from the start and end squares.
        row_diff, col_diff = row_diff // 3, col_diff // 3
        square_list = [start]
        for _ in range(3):
            next_square = Square(square_list[-1].row + row_diff, square_list[-1].col + col_diff)
            square_list.append(next_square)
        assert square_list[-1] == end

        self.squares = frozenset(square_list)
        assert len(self.squares) == 4

        self.direction = ROW_COL_DIFFS_TO_THREAT_DIRECTION[(row_diff, col_diff)]

    def __eq__(self, other):
        if isinstance(other, Threat):
            return self.player == other.player and self.squares == other.squares
        return False

    def __hash__(self):
        return self.squares.__hash__() + self.player

    def __str__(self):
        return ("[" + str(self.player) + " -> " +
                "(" + str(self.start.row) + "," + str(self.start.col) + ") -" +
                "(" + str(self.end.row) + "," + str(self.end.col) + ")]"
                )

    def __repr__(self):
        return self.__str__()


def square_to_threats(threats):
    """Accepts an iterable of Threats and outputs a dictionary mapping
    each Square to all Threats that contain that Square.

    Args:
        threats (iterable<Threat>): an iterable of Threats.

    Returns:
        d (Map<Square, Set<Threat>>): A dictionary mapping each Square to all Threats that contain that Square.
    """
    d = {}
    for threat in threats:
        for square in threat.squares:
            if square not in d:
                d[square] = set()
            d[square].add(threat)
    return d
