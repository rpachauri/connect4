from collections import namedtuple
from connect_four.hashing import Hasher

Square = namedtuple("Square", ["row", "col"])
Group = namedtuple("Group", ["squares"])

ALL_GROUPS = [
    frozenset([Square(row=0, col=0), Square(row=0, col=1), Square(row=0, col=2)]),
    frozenset([Square(row=1, col=0), Square(row=1, col=1), Square(row=1, col=2)]),
    frozenset([Square(row=2, col=0), Square(row=2, col=1), Square(row=2, col=2)]),
    frozenset([Square(row=0, col=0), Square(row=1, col=0), Square(row=2, col=0)]),
    frozenset([Square(row=0, col=1), Square(row=1, col=1), Square(row=2, col=1)]),
    frozenset([Square(row=0, col=2), Square(row=1, col=2), Square(row=2, col=2)]),
    frozenset([Square(row=0, col=0), Square(row=1, col=1), Square(row=2, col=2)]),
    frozenset([Square(row=2, col=0), Square(row=1, col=1), Square(row=0, col=2)]),
]


class TicTacToeHasher(Hasher):

    def __init__(self):
        """
        Assumptions:
            1.  The Hasher starts at the initial state of Tic-Tac-Toe,
                where neither player has made a move.
        """
        pass

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
