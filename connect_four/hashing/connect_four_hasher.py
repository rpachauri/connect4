import numpy as np

from connect_four.envs import ConnectFourEnv
from connect_four.hashing import Hasher, hasher_hash_utils
from connect_four.hashing.square_type_manager import SquareTypeManager


class ConnectFourHasher(Hasher):
    def __init__(self, env: ConnectFourEnv):
        self.stm = SquareTypeManager(env_variables=env.env_variables, num_to_connect=3)
        self.lowest_empty_row_by_col = self._find_lowest_empty_squares(state=env.env_variables.state)
        self.columns_played_by_move = []

    @staticmethod
    def _find_lowest_empty_squares(state):
        lowest_empty_squares = []
        for col in range(len(state[0][0])):
            lowest_empty_squares.append(ConnectFourHasher._find_lowest_empty_row(state=state, col=col))
        return lowest_empty_squares

    @staticmethod
    def _find_lowest_empty_row(state, col: int) -> int:
        for row in range(len(state[0])):
            if state[0][row][col] == 1 or state[1][row][col] == 1:
                return row - 1
        return len(state[0]) - 1

    def move(self, action: int):
        """
        Assumptions:
            1. The current state of Connect-Four is not a terminal state.

        Args:
            action (int): a valid action in the current state of Connect-Four.
        """
        # Convert action into (row, col).
        col = action
        row = self.lowest_empty_row_by_col[col]

        # Move the SquareTypeManager.
        self.stm.move(row=row, col=col)
        # Move the lowest empty row in col up by 1.
        self.lowest_empty_row_by_col[col] -= 1
        self.columns_played_by_move.append(col)

    def undo_move(self):
        """
        Assumptions:
            1. The current state of Connect-Four is not in the state given upon initialization.
        """
        last_played_column = self.columns_played_by_move.pop()
        self.lowest_empty_row_by_col[last_played_column] += 1

        self.stm.undo_move()

    def hash(self) -> str:
        """
        Returns:
            hash (str): a unique hash of the current state.
                        The encoding is a perfect hash (meaning there will be no collisions).
        """
        transposition_arr = np.flipud(m=hasher_hash_utils.convert_square_types_to_transposition_arr(
            square_types=self.stm.square_types,
        ))
        transposition = hasher_hash_utils.get_transposition(transposition_arr=transposition_arr)
        flipped = np.fliplr(m=transposition_arr)
        flipped_transposition = hasher_hash_utils.get_transposition(transposition_arr=flipped)
        if flipped_transposition < transposition:
            transposition = flipped_transposition

        return transposition
