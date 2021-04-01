import numpy as np

from connect_four.envs import TicTacToeEnv
from connect_four.hashing import Hasher
from connect_four.hashing import hasher_hash_utils, hasher_init_utils, hasher_move_utils
from connect_four.hashing.data_structures import Square, Group

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


class TicTacToeHasher(Hasher):

    def __init__(self, env: TicTacToeEnv):
        """
        Assumptions:
            1.  The Hasher starts at the initial state of Tic-Tac-Toe,
                where neither player has made a move.
        """
        # Initialize groups_by_square_by_player.
        self.groups_by_square_by_player = hasher_init_utils.create_initial_groups_by_squares(
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
        self.square_types = hasher_init_utils.create_initial_square_types(num_rows=3, num_cols=3)

        state, self.player = env.env_variables
        hasher_move_utils.play_squares_from_state(
            state=state,
            groups_by_square_by_player=self.groups_by_square_by_player,
            square_types=self.square_types,
        )

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
        row, col = action // 3, action % 3

        groups_removed_by_squares, previous_square_types = hasher_move_utils.play_square(
            player=self.player,
            row=row,
            col=col,
            groups_by_square_by_player=self.groups_by_square_by_player,
            square_types=self.square_types,
        )
        self.groups_removed_by_squares_by_move.append(groups_removed_by_squares)
        self.previous_square_types_by_move.append(previous_square_types)

        # Switch play.
        self.player = 1 - self.player

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
        transposition_arr = hasher_hash_utils.convert_square_types_to_transposition_arr(square_types=self.square_types)
        transposition = hasher_hash_utils.get_transposition(transposition_arr=transposition_arr)

        for k in range(3):
            rotated_transposition = hasher_hash_utils.get_transposition(
                transposition_arr=np.rot90(m=transposition_arr, k=k),
            )
            if rotated_transposition < transposition:
                transposition = rotated_transposition
        flipped = np.fliplr(m=transposition_arr)
        for k in range(4):
            flipped_rotated_transposition = hasher_hash_utils.get_transposition(
                transposition_arr=np.rot90(m=flipped, k=k),
            )
            if flipped_rotated_transposition < transposition:
                transposition = flipped_rotated_transposition

        return transposition
