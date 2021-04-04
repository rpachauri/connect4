from connect_four.envs import ConnectFourEnv
from connect_four.hashing import Hasher
from connect_four.hashing.square_type_manager import SquareTypeManager


class ConnectFourHasher(Hasher):
    def __init__(self, env: ConnectFourEnv):
        self.stm = SquareTypeManager(env_variables=env.env_variables, num_to_connect=3)
        self.lowest_empty_squares = self._find_lowest_empty_squares(state=env.env_variables.state)

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
        pass

    def undo_move(self):
        """
        Assumptions:
            1. The current state of Connect-Four is not in the state given upon initialization.
        """
        pass

    def hash(self) -> str:
        """
        Returns:
            hash (str): a unique hash of the current state.
                        The encoding is a perfect hash (meaning there will be no collisions).
        """
        pass
