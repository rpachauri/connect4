import numpy as np

from connect_four.agents.victor import Square
from connect_four.agents.victor import Threat


class Board:
    """Board is essentially a wrapper around the state of a ConnectFourEnv. It does not keep in sync with the
    environment's board. This means that if the state of the environment changes, this board will be out of date.
    """

    def __init__(self, state: np.array):
        self.state = state.copy()

    def is_valid(self, square: Square):
        return 0 <= square.row < len(self.state[0]) and 0 <= square.col < len(self.state[0][0])

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

    def potential_threats(self, player):
        """Returns a set of potential threats that this player has in this board state.

        Args:
            player (int): a player (0 or 1). Threats must belong to this player.

        Returns:
            threats (set<Threat>): a set of Threat instances. Each threat belongs to the given player.
        """
        directions = [
            (-1, 1),  # up-right diagonal
            (0, 1),  # horizontal
            (1, 1),  # down-right diagonal
            (1, 0),  # vertical
        ]
        threats = set()

        for row in range(len(self.state[0])):
            for col in range(len(self.state[0][0])):
                for row_diff, col_diff in directions:
                    if self.is_potential_threat(player, row, col, row_diff, col_diff):
                        threats.add(Threat(
                            player,
                            start=Square(row, col),
                            end=Square(row + 3 * row_diff, col + 3 * col_diff),
                        ))

        return threats

    def is_potential_threat(self, player: int, row: int, col: int, row_diff: int, col_diff: int):
        """Returns whether or not the given group is a threat that belongs to the player.

        Args:
            player (int): a player (0 or 1). Is the group a threat that belongs to this player?
            row (int): starting row
            col (int): starting column
            row_diff (int): direction in which to increment the row (-1, 0 or 1)
            col_diff (int): direction in which to increment the col (-1, 0 or 1)

        Returns:
            is_threat (bool): True if the group is a valid potential threat that belongs to the player.
                              Otherwise, false.
        """
        opponent = 1 - player
        for _ in range(4):
            square = Square(row, col)
            if not self.is_valid(square):
                return False
            if self.state[opponent][row][col]:
                # If there is a token that belongs to the opponent in this group,
                # then this group is not a potential threat that belongs to the given player.
                return False
            row, col = row + row_diff, col + col_diff
        return True
