from collections import namedtuple

from connect_four.agents.victor.game import Board
from connect_four.agents.victor.game import Square


EvenThreat = namedtuple("EvenThreat", ["threat_hunter", "odd_square", "even_square"])
OddThreat = namedtuple("OddThreat", ["threat_hunter", "odd_square1", "odd_square2"])

"""A ThreatCombination is a combination of two threats.

Both threats have exactly two squares filled by the player and two empty squares.

From Section 8.4 of the original paper:

    A threat_hunter combination consists of two threats, which both are filled with two [tokens]. One threat_hunter needs two odd
    squares, while the second threat_hunter needs one of the two squares of the first threat_hunter, and another even square, directly
    above, or beneath the second odd square of the first threat_hunter. The square which both threats share should not be
    directly playable.

Naming:
-   The threat_hunter with the even empty square (not the shared one) is known as the "even threat_hunter".
-   The threat_hunter with the odd empty square (not the shared one) is known as the "odd threat_hunter".
-   Despite the naming, either can be used as an odd threat_hunter depending on the opponent's moves.
"""
ThreatCombination = namedtuple(
    "ThreatCombination",
    ["even_threat", "odd_threat", "shared_square", "even_square", "odd_square"],
)


def find_threat_combination(board: Board):
    """find_threat_combination returns a ThreatCombination for White if one exists. Otherwise, returns None.
    If multiple threatCombinations exist, picks one arbitrarily.

    Args:
        board (Board): a Board instance.

    Returns:
        threat_combination (ThreatCombination): a ThreatCombination for White if one exists. Otherwise, None.
    """
    white_threats = board.potential_groups(0)

    even_threats = []
    odd_threats = []
    for threat in white_threats:
        empty_squares = []
        for square in threat.squares:
            if board.is_empty(square):
                empty_squares.append(square)

        if len(empty_squares) != 2:
            continue

        square1, square2 = empty_squares[0], empty_squares[1]
        if square1.row % 2 == 1 and square2.row % 2 == 1:  # odd threat_hunter.
            odd_threats.append(OddThreat(threat=threat, odd_square1=square1, odd_square2=square2))
        elif square1.row % 2 == 0 and square2.row % 2 == 1:  # even threat_hunter with square1 as the even square.
            even_threats.append(EvenThreat(threat=threat, odd_square=square2, even_square=square1))
        elif square1.row % 2 == 1 and square2.row % 2 == 0:  # even threat_hunter with square2 as the even square.
            even_threats.append(EvenThreat(threat=threat, odd_square=square1, even_square=square2))

    for even_threat in even_threats:
        for odd_threat in odd_threats:
            threats_share_a_square, odd_unshared_square = share_square(even_threat=even_threat, odd_threat=odd_threat)
            if (threats_share_a_square and
                    even_threat.even_square.col == odd_unshared_square.col and
                    abs(even_threat.even_square.row - odd_unshared_square.row) == 1):
                return ThreatCombination(
                    even_threat=even_threat.threat,
                    odd_threat=odd_threat.threat,
                    shared_square=even_threat.odd_square,
                    even_square=even_threat.even_square,
                    odd_square=odd_unshared_square,
                )


def share_square(even_threat: EvenThreat, odd_threat: OddThreat) -> (bool, Square):
    if even_threat.odd_square == odd_threat.odd_square1:
        return True, odd_threat.odd_square2
    if even_threat.odd_square == odd_threat.odd_square2:
        return True, odd_threat.odd_square1
    return False, None
