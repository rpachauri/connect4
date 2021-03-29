from collections import namedtuple

from connect_four.envs import TicTacToeEnv
from connect_four.hashing import Hasher
from enum import Enum

Square = namedtuple("Square", ["row", "col"])
Group = namedtuple("Group", ["squares"])

ALL_GROUPS = [
    Group(squares=frozenset([Square(row=0, col=0), Square(row=0, col=1), Square(row=0, col=2)])),
    Group(squares=frozenset([Square(row=1, col=0), Square(row=1, col=1), Square(row=1, col=2)])),
    Group(squares=frozenset([Square(row=2, col=0), Square(row=2, col=1), Square(row=2, col=2)])),
    Group(squares=frozenset([Square(row=0, col=0), Square(row=1, col=0), Square(row=2, col=0)])),
    Group(squares=frozenset([Square(row=0, col=1), Square(row=1, col=1), Square(row=2, col=1)])),
    Group(squares=frozenset([Square(row=0, col=2), Square(row=1, col=2), Square(row=2, col=2)])),
    Group(squares=frozenset([Square(row=0, col=0), Square(row=1, col=1), Square(row=2, col=2)])),
    Group(squares=frozenset([Square(row=2, col=0), Square(row=1, col=1), Square(row=0, col=2)])),
]


class SquareType(Enum):
    Empty = 0
    Indifferent = 1
    Player1 = 2
    Player2 = 3


SQUARE_TYPE_TO_SQUARE_CHAR = {
    SquareType.Empty: "0",
    SquareType.Indifferent: "3",
    SquareType.Player1: "1",
    SquareType.Player2: "2",
}


class TicTacToeHasher(Hasher):

    def __init__(self, env: TicTacToeEnv):
        """
        Assumptions:
            1.  The Hasher starts at the initial state of Tic-Tac-Toe,
                where neither player has made a move.
        """
        self.groups_by_squares = []
        for player in range(2):
            player_squares = []
            for row in range(3):
                rows = []
                for col in range(3):
                    groups_at_square = set()
                    square = Square(row=row, col=col)
                    for group in ALL_GROUPS:
                        if square in group.squares:
                            groups_at_square.add(group)
                    rows.append(groups_at_square)
                player_squares.append(rows)
            self.groups_by_squares.append(player_squares)

        self.square_types = []
        for row in range(3):
            rows = []
            for col in range(3):
                rows.append(SquareType.Empty)
            self.square_types.append(rows)

        state, self.player = env.env_variables

        for row in range(3):
            for col in range(3):
                if state[0][row][col] == 1:
                    self._play_square(player=0, row=row, col=col)
                elif state[1][row][col] == 1:
                    self._play_square(player=1, row=row, col=col)

    def move(self, action: int):
        """
        Assumptions:
            1. The current state of Tic-Tac-Toe is not a terminal state.

        Args:
            action (int): a valid action in the current state of Tic-Tac-Toe.
        """
        # Convert action into (row, col).
        row, col = action // 2, action % 2

        self._play_square(player=self.player, row=row, col=col)

        # Switch play.
        self.player = 1 - self.player

    def _play_square(self, player: int, row: int, col: int):
        # Find all Groups that belong to the opponent at that square
        opponent = 1 - player
        groups = self.groups_by_squares[opponent][row][col].copy()

        # Change groups_by_squares to reflect that the opponent cannot win using any group in groups.
        # Also, find all indifferent squares.
        indifferent_squares = set()
        for g in groups:
            for s in g.squares:
                self.groups_by_squares[opponent][s.row][s.col].discard(g)
                if (not self.groups_by_squares[opponent][s.row][s.col]) and \
                        (not self.groups_by_squares[self.player][s.row][s.col]):
                    indifferent_squares.add(s)

        # Change the square types of indifferent squares.
        for s in indifferent_squares:
            self.square_types[s.row][s.col] = SquareType.Indifferent

        # If the played square does not immediately become an indifferent square, it belongs to the player.
        if Square(row=row, col=col) not in indifferent_squares:
            if player == 0:
                self.square_types[row][col] = SquareType.Player1
            else:
                self.square_types[row][col] = SquareType.Player2

    def undo_move(self):
        """
        Assumptions:
            1. The current state of Tic-Tac-Toe is not the initial state.
        """
        pass

    def hash(self) -> str:
        """
        Returns:
            hash (str): a unique hash of the current state.
                        The encoding is a perfect hash (meaning there will be no collisions).
        """
        pass
