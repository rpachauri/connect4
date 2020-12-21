from connect_four.agents.victor import Square


class Threat:
    def __init__(self, player: int, start: Square, end: Square):
        # Perform validation on player.
        if not(player == 0 or player == 1):
            raise ValueError("player must be 0 or 1. player =", player)
        self.player = player

        # Perform validation on start and end of threat.
        row_diff = start.row - end.row
        col_diff = start.col - end.col
        if not (row_diff == -3 or row_diff == 0 or row_diff == 3) or not(
                col_diff == -3 or col_diff == 0 or col_diff == 3):
            raise ValueError("Invalid threat line:", start, "-", end)

        self.squares = frozenset([
            start,
            end,
        ])
        assert len(self.squares) == 2
