import numpy as np

from connect_four.agents.victor import Square


class Board:
    """Board is essentially a wrapper around the state of a ConnectFourEnv. It does not keep in sync with the
    environment's board. This means that if the state of the environment changes, this board will be out of date.
    """

    def __init__(self, state: np.array):
        self.state = state.copy()

    def is_valid(self, square: Square):
        return 0 <= square.row < len(self.state) and 0 <= square.col < len(self.state[0])

    def is_empty(self, square: Square):
        """Returns whether or not the given square is empty on this board.

        Args:
            square: a Square. Assumes that the given square is within this board.

        Returns:
            True if the given square on this board is empty.
            False if the given square is occupied by either player.
        """
        return self.state[0][square.row][square.col] == 0 and self.state[1][square.row][square.col] == 0

    def playable_squares(self):
        """Returns a set of playable squares on this board.

        Returns:
            squares: a set of playable squares. empty if there are none.
        """
        squares = set()
        for col in range(len(self.state[0][0])):
            square = self.playable_square(col)
            if square is not None:
                squares.add(square)
        return squares

    def playable_square(self, col):
        """Returns a playable square in this column if it exists.

        Args:
            col: (int) the column to find a playable square.

        Returns:
            square: (Square) the only playable square in this column if there is one.
                    If there is no playable square, returns None.
        """
        for row in reversed(range(len(self.state[0]))):
            square = Square(row, col)
            if self.is_empty(square):
                return square

    def threats(self, player):
        """Returns a set of threats that this player has in this board state.

        Args:
            player: (int) a player (0 or 1).

        Returns:
            threats: a set of Threat instances. Each threat belongs to the given player.
        """
        pass
