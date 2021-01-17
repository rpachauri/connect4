from collections import namedtuple

from connect_four.agents.victor.game import Board


"""A ThreatCombination is a combination of two Threats.

Both threats have exactly two squares filled by the player and two empty squares.

From Section 8.4 of the original paper:

    A threat combination consists of two groups, which both are filled with two [tokens]. One group needs two odd
    squares, while the second group needs one of the two squares of the first group, and another even square, directly
    above, or beneath the second odd square of the first group. The square which both groups share should not be
    directly playable.

Naming:
-   The threat with the even empty square (not the shared one) is known as the "even Threat".
-   The threat with the odd empty square (not the shared one) is known as the "odd Threat".
-   Despite the naming, either can be used as an odd Threat depending on the opponent's moves.
"""
ThreatCombination = namedtuple("ThreatCombination", [
    "even_threat", "odd_threat", "shared_square", "even_square", "odd_square"]
)


def find_threat_combination(board: Board):
    """find_threat_combination returns a ThreatCombination for White if one exists. Otherwise, returns None.
    If multiple ThreatCombinations exist, picks one arbitrarily.

    Args:
        board (Board): a Board instance.

    Returns:
        threat_combination (ThreatCombination): a ThreatCombination for White if one exists. Otherwise, None.
    """
    pass
