import numpy as np

from collections import namedtuple
from connect_four.envs import TicTacToeEnv
from connect_four.hashing import Hasher
from enum import Enum
from typing import Dict, Set, List, Sequence

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
        # Initialize groups_by_square_by_player.
        self.groups_by_square_by_player = self.create_initial_groups_by_squares(
            num_rows=3,
            num_cols=3,
            all_groups=ALL_GROUPS,
        )

        assert len(self.groups_by_square_by_player) == 2, \
            "number of players = %d" % len(self.groups_by_square_by_player)
        assert len(self.groups_by_square_by_player[0]) == 3, \
            "number of rows = %d" % len(self.groups_by_square_by_player[0])
        assert len(self.groups_by_square_by_player[0][0]) == 3, \
            "number of cols = %d" % len(self.groups_by_square_by_player[0][0])

        # Initialize square_types.
        self.square_types = self.create_initial_square_types(num_rows=3, num_cols=3)

        state, self.player = env.env_variables

        for row in range(3):
            for col in range(3):
                if state[0][row][col] == 1:
                    self._play_square(player=0, row=row, col=col)
                elif state[1][row][col] == 1:
                    self._play_square(player=1, row=row, col=col)

        self.groups_removed_by_squares_by_move = []
        self.previous_square_types_by_move = []

    @staticmethod
    def create_initial_groups_by_squares(num_rows: int, num_cols: int, all_groups: Sequence[Group]):
        groups_by_square = []
        for player in range(2):
            player_squares = []
            for row in range(num_rows):
                rows = []
                for col in range(num_cols):
                    groups_at_square = set()
                    square = Square(row=row, col=col)
                    for group in all_groups:
                        if square in group.squares:
                            groups_at_square.add(group)
                    rows.append(groups_at_square)
                player_squares.append(rows)
            groups_by_square.append(player_squares)
        return groups_by_square

    @staticmethod
    def create_initial_square_types(num_rows: int, num_cols: int) -> List[List[SquareType]]:
        square_types = []
        for row in range(num_rows):
            rows = []
            for col in range(num_cols):
                rows.append(SquareType.Empty)
            square_types.append(rows)
        return square_types

    def move(self, action: int):
        """
        Assumptions:
            1. The current state of Tic-Tac-Toe is not a terminal state.

        Args:
            action (int): a valid action in the current state of Tic-Tac-Toe.
        """
        # Convert action into (row, col).
        row, col = action // 3, action % 3

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
        # Change groups_by_square_by_player to reflect that the opponent cannot win using any group in groups.
        # Also, retrieve groups_removed_by_square.
        groups_removed_by_square = self.remove_groups(
            row=row,
            col=col,
            existing_groups_by_square=self.groups_by_square_by_player[1 - player],
        )

        # Find all indifferent squares.
        indifferent_squares = self.find_indifferent_squares(
            player=player,
            row=row,
            col=col,
            groups_removed_by_square=groups_removed_by_square,
            square_types=self.square_types,
            existing_groups_by_square_by_player=self.groups_by_square_by_player,
        )

        # Change the square types of indifferent squares.
        # Also, find the SquareType of all squares that are being changed.
        previous_square_types = self.update_square_types(
            row=row,
            col=col,
            indifferent_squares=indifferent_squares,
            square_types=self.square_types,
        )

        return groups_removed_by_square, previous_square_types

    @staticmethod
    def remove_groups(row: int, col: int,
                      existing_groups_by_square: List[List[Set[Group]]]) -> Dict[Square, Set[Group]]:
        """
        Args:
            row (int):
            col (int):
            existing_groups_by_square (List[List[Set[Group]]]): a 2D array containing a set of Groups at each cell.
                This set of Groups are all existing Groups the opponent can use to win at that square.

        Modifies:
            existing_groups_by_square: For every square in groups_removed_by_squares,
                every group in groups_removed_by_squares[square] will be removed from existing_groups_by_square.

        Returns:
            groups_removed_by_square (Dict[Square, Set[Group]]):
                A Dictionary mapping Squares to all Groups that were removed.
                For every square in groups_removed_by_squares, the opponent can no longer win using that Group.
        """
        groups_to_remove = existing_groups_by_square[row][col].copy()
        # Change existing_groups_by_square to reflect that the opponent cannot win using any group in groups.
        groups_removed_by_square = {}
        for g in groups_to_remove:
            for s in g.squares:
                # If the opponent could win using this group, they no longer can.
                if g in existing_groups_by_square[s.row][s.col]:
                    existing_groups_by_square[s.row][s.col].remove(g)

                    # If groups_removed_by_square doesn't already contain this square, add it.
                    if s not in groups_removed_by_square:
                        groups_removed_by_square[s] = set()

                    # Add g as one of the groups removed.
                    groups_removed_by_square[s].add(g)
        return groups_removed_by_square

    @staticmethod
    def find_indifferent_squares(player: int, row: int, col: int,
                                 groups_removed_by_square: Dict[Square, Set[Group]],
                                 square_types: List[List[SquareType]],
                                 existing_groups_by_square_by_player: List[List[List[Set[Group]]]]) -> Set[Square]:
        """

        Args:
            player (int):
            row (int):
            col (int):
            groups_removed_by_square (Dict[Square, Set[Group]]):
                A Dictionary mapping Squares to all Groups that were removed.
                For every square in groups_removed_by_squares, the opponent can no longer win using that Group.
            square_types (List[List[SquareType]]): a 2D array of the current SquareTypes.
            existing_groups_by_square_by_player (List[List[List[Set[Group]]]]):
                A 3D array containing a set of Groups at each cell.
                First dimension is the player. Second dimension is the row. Third dimension is the column.
                The Set of Groups at the cell are all existing Groups the player can use to win at that square.

        Modifies:
            square_types: If the square at the given row and col is not indifferent,
                assigns a SquareType corresponding with the given player.
                Updates all squares that are indifferent to SquareType.Indifferent.

        Returns:
            indifferent_squares (Set[Square]): a Set of Squares that can no longer be used to
                complete any Groups for either player.
        """
        # Assign the played square a non-empty SquareType. This allows it be included when finding indifferent_squares.
        if player == 0:
            square_types[row][col] = SquareType.Player1
        else:
            square_types[row][col] = SquareType.Player2

        # Find all indifferent squares.
        indifferent_squares = set()
        if not groups_removed_by_square:
            indifferent_squares.add(Square(row=row, col=col))
        for s in groups_removed_by_square:
            # If neither player can win any groups at this square, this square is indifferent.
            if (square_types[s.row][s.col] != SquareType.Empty) and \
                    (not existing_groups_by_square_by_player[0][s.row][s.col]) and \
                    (not existing_groups_by_square_by_player[1][s.row][s.col]):
                indifferent_squares.add(s)
        return indifferent_squares

    @staticmethod
    def update_square_types(row: int, col: int,
                            indifferent_squares: Set[Square],
                            square_types: List[List[SquareType]]) -> Dict[Square, SquareType]:
        """

        Args:
            row (int):
            col (int):
            indifferent_squares (Set[Square]): a Set of Squares that can no longer be used to
                complete any Groups for either player.
            square_types (List[List[SquareType]]): a 2D array of the current SquareTypes.

        Modifies:
            square_types: For every square in indifferent_squares, updates to SquareType.Indifferent.

        Returns:
            previous_square_types (Dict[Square, SquareType]): a dictionary mapping each Square to the SquareType it was
                before it was changed.
        """
        # Find the SquareType of all squares that are being changed.
        previous_square_types = {}
        # Change the square types of indifferent squares.
        for s in indifferent_squares:
            previous_square_types[s] = square_types[s.row][s.col]
            square_types[s.row][s.col] = SquareType.Indifferent

        previous_square_types[Square(row=row, col=col)] = SquareType.Empty

        return previous_square_types

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
                self.groups_by_square_by_player[opponent][square.row][square.col].add(group)

        previous_square_types = self.previous_square_types_by_move.pop()
        for square in previous_square_types:
            self.square_types[square.row][square.col] = previous_square_types[square]

    def hash(self) -> str:
        """
        Returns:
            hash (str): a unique hash of the current state.
                        The encoding is a perfect hash (meaning there will be no collisions).
        """
        transposition_arr = self._convert_square_types_to_transposition_arr(square_types=self.square_types)
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

    @staticmethod
    def _convert_square_types_to_transposition_arr(square_types: List[List[SquareType]]):
        transposition_arr = []
        for row in range(len(square_types)):
            cols = []
            for col in range(len(square_types[0])):
                cols.append(SQUARE_TYPE_TO_SQUARE_CHAR[square_types[row][col]])
            transposition_arr.append(cols)
        return np.array(transposition_arr)

    @staticmethod
    def _get_transposition(transposition_arr):
        return ''.join(transposition_arr.flatten())
