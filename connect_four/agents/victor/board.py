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
