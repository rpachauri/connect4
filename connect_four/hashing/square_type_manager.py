from typing import List

from connect_four.envs import TwoPlayerGameEnvVariables
from connect_four.hashing.data_structures import SquareType


class SquareTypeManager:

    def __init__(self, env_variables: TwoPlayerGameEnvVariables, num_to_connect: int):
        """Initializes the SquareTypeManager with the given env_variables.

        Constraints:
            -

        Args:
            env_variables (TwoPlayerGameEnvVariables): a TwoPlayerGame's env_variables.
        """
        pass

    def move(self, row: int, col: int):
        """Plays a move at the given row and column.

        Assumptions:
            1.  The internal state of the SquareTypeManager is not at a terminal state.

        Args:
            row (int): the row to play
            col (int): the column to play
        """
        pass

    def undo_move(self):
        """Undoes the most recent move.

        Raises:
            (AssertionError): if the internal state of the SquareTypeManager is at the given state upon initialization.
        """
        pass

    def get_square_types(self) -> List[List[SquareType]]:
        """Retrieves the square types.

        Returns:
            square_types (List[List[SquareType]]): 2D array of SquareTypes summarizing the current state.
        """
        pass
