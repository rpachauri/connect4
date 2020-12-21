from connect_four.agents.victor import Square


class Threat:
    def __init__(self, player: int, start: Square, end: Square):
        # Perform validation on player.
        if not(player == 0 or player == 1):
            raise ValueError("player must be 0 or 1. player =", player)
        self.player = player

        # Perform validation on start and end of threat.
        row_diff = end.row - start.row
        col_diff = end.col - start.col
        if not (row_diff == -3 or row_diff == 0 or row_diff == 3) or not(
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
