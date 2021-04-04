import numpy as np

from connect_four.envs import TicTacToeEnv
from connect_four.hashing import Hasher
from connect_four.hashing import hasher_hash_utils
from connect_four.hashing.square_type_manager import SquareTypeManager


class TicTacToeHasher(Hasher):

    def __init__(self, env: TicTacToeEnv):
        self.stm = SquareTypeManager(env_variables=env.env_variables, num_to_connect=3)

    def move(self, action: int):
        """
        Assumptions:
            1. The current state of Tic-Tac-Toe is not a terminal state.

        Args:
            action (int): a valid action in the current state of Tic-Tac-Toe.
        """
        # Convert action into (row, col).
        row, col = action // 3, action % 3
        self.stm.move(row=row, col=col)

    def undo_move(self):
        """
        Assumptions:
            1. The current state of Tic-Tac-Toe is not in the state given upon initialization.
        """
        self.stm.undo_move()

    def hash(self) -> str:
        """
        Returns:
            hash (str): a unique hash of the current state.
                        The encoding is a perfect hash (meaning there will be no collisions).
        """
        transposition_arr = hasher_hash_utils.convert_square_types_to_transposition_arr(
            square_types=self.stm.square_types,
        )
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
