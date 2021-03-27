from collections import namedtuple
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

    def __init__(self):
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

        self.player = 0

    def move(self, action: int):
        """
        Assumptions:
            1. The current state of Tic-Tac-Toe is not a terminal state.

        Args:
            action (int): a valid action in the current state of Tic-Tac-Toe.
        """
        pass

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
