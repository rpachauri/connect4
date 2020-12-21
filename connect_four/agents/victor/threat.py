from connect_four.agents.victor import Square


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

    def __eq__(self, other):
        if isinstance(other, Threat):
            return self.player == other.player and self.squares == other.squares
        return False

    def __hash__(self):
        return self.squares.__hash__() + self.player