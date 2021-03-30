import numpy as np

from collections import namedtuple
from connect_four.envs import TicTacToeEnv
from connect_four.hashing import Hasher
from enum import Enum
from typing import Dict, Set

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

        self.groups_removed_by_squares_by_move = []
        self.previous_square_types_by_move = []

    def move(self, action: int):
        """
        Assumptions:
            1. The current state of Tic-Tac-Toe is not a terminal state.

        Args:
            action (int): a valid action in the current state of Tic-Tac-Toe.
        """
        # Convert action into (row, col).
        row, col = action // 2, action % 2

        groups_removed_by_squares, previous_square_types = self._play_square(player=self.player, row=row, col=col)
        self.groups_removed_by_squares_by_move.append(groups_removed_by_squares)
        self.previous_square_types_by_move.append(previous_square_types)

        # Switch play.
        self.player = 1 - self.player

    def _play_square(self, player: int, row: int, col: int) -> (Dict[Square, Set[Group]], Dict[Square, SquareType]):
        """

        Args:
            player (int): the player making the move.
            row (int): the row to make the move in.
            col (int): the column to make the move in.

        Returns:
            groups_removed_by_squares (Dict[Square, Set[Group]]):
                A Dictionary mapping Squares to all Groups that were removed.
                For every square in groups_removed_by_squares, the opponent can no longer win using that Group.
            previous_square_types (Dict[Square, SquareType]):
                A Dictionary mapping Squares to the SquareType they were before this move was played.
                Only Squares that had their SquareType changed are included.
        """
        # Find all Groups that belong to the opponent at that square
        opponent = 1 - player
        groups = self.groups_by_squares[opponent][row][col].copy()
        groups_removed_by_square = {}

        # Change groups_by_squares to reflect that the opponent cannot win using any group in groups.
        # Also, find all indifferent squares.
        indifferent_squares = set()
        for g in groups:
            for s in g.squares:
                # If the opponent could win using this group, they no longer can.
                if g in self.groups_by_squares[opponent][s.row][s.col]:
                    self.groups_by_squares[opponent][s.row][s.col].remove(g)

                    # If groups_removed_by_square doesn't already contain this square, add it.
                    if s not in groups_removed_by_square:
                        groups_removed_by_square[s] = set()

                    # Add g as one of the groups removed.
                    groups_removed_by_square[s].add(g)

                # If neither player can win any groups at this square, this square is indifferent.
                if (not self.groups_by_squares[opponent][s.row][s.col]) and \
                        (not self.groups_by_squares[player][s.row][s.col]):
                    indifferent_squares.add(s)

        previous_square_types = {}
        # Change the square types of indifferent squares.
        for s in indifferent_squares:
            previous_square_types[s] = self.square_types[s.row][s.col]
            self.square_types[s.row][s.col] = SquareType.Indifferent

        # If the played square does not immediately become an indifferent square, it belongs to the player.
        if Square(row=row, col=col) not in indifferent_squares:
            if player == 0:
                self.square_types[row][col] = SquareType.Player1
            else:
                self.square_types[row][col] = SquareType.Player2

        previous_square_types[Square(row=row, col=col)] = SquareType.Empty

        return groups_removed_by_square, previous_square_types

    def undo_move(self):
        """
        Assumptions:
            1. The current state of Tic-Tac-Toe is not the initial state.
        """
        # Switch play.
        opponent = self.player
        self.player = 1 - self.player

        groups_removed_by_squares = self.groups_removed_by_squares_by_move.pop()
        for square in groups_removed_by_squares:
            for group in groups_removed_by_squares[square]:
                self.groups_by_squares[opponent][square.row][square.col].add(group)

        previous_square_types = self.previous_square_types_by_move.pop()
        for square in previous_square_types:
            self.square_types[square.row][square.col] = previous_square_types[square]

    def hash(self) -> str:
        """
        Returns:
            hash (str): a unique hash of the current state.
                        The encoding is a perfect hash (meaning there will be no collisions).
        """
        transposition_arr = self._convert_square_types_to_transposition_arr()
        transposition = self._get_transposition(transposition_arr=transposition_arr)

        for k in range(3):
            rotated_transposition = self._get_transposition(transposition_arr=np.rot90(m=transposition_arr, k=k))
            if rotated_transposition < transposition:
                transposition = rotated_transposition
        flipped = np.fliplr(m=transposition_arr)
        for k in range(4):
            flipped_rotated_transposition = self._get_transposition(transposition_arr=np.rot90(m=flipped, k=k))
            if flipped_rotated_transposition < transposition:
                transposition = flipped_rotated_transposition

        return transposition

    def _convert_square_types_to_transposition_arr(self):
        transposition_arr = []
        for row in range(3):
            cols = []
            for col in range(3):
                cols.append(SQUARE_TYPE_TO_SQUARE_CHAR[self.square_types[row][col]])
            transposition_arr.append(cols)
        return np.array(transposition_arr)

    @staticmethod
    def _get_transposition(transposition_arr):
        return f'{transposition_arr[0][0]}' + \
               f'{transposition_arr[0][1]}' + \
               f'{transposition_arr[0][2]}' + \
               f'{transposition_arr[1][0]}' + \
               f'{transposition_arr[1][1]}' + \
               f'{transposition_arr[1][2]}' + \
               f'{transposition_arr[2][0]}' + \
               f'{transposition_arr[2][1]}' + \
               f'{transposition_arr[2][2]}'
