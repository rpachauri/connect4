from connect_four.envs import ConnectFourEnv
from connect_four.hashing import Hasher


class ConnectFourHasher(Hasher):
    def __init__(self, env: ConnectFourEnv):
        pass

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
