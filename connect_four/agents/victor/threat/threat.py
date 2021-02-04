from collections import namedtuple

from connect_four.agents.victor.game import Board


Threat = namedtuple("Threat", ["group", "empty_square"])


def find_odd_threat(board: Board) -> Threat:
    """find_threat_combination returns an Odd Threat for White if one exists. Otherwise, returns None.
    If multiple Odd Threats exist, picks one arbitrarily.

    Args:
        board (Board): a Board instance.

    Returns:
        odd_threat (Threat): a Threat with a single empty square. The single empty square will be odd.
            None if no such Threat exists for board.
    """
    pass
