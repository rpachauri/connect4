from typing import Set

from connect_four.envs import TwoPlayerGameEnvVariables
from connect_four.evaluation.victor.solution import Solution


class SolutionManager:
    def __init__(self, env_variables: TwoPlayerGameEnvVariables):
        """Initializes the SolutionManager with the given env_variables.

        Args:
            env_variables (TwoPlayerGameEnvVariables): a TwoPlayerGame's env_variables.
        """
        pass

    def move(self, player: int, row: int, col: int) -> (Set[Solution], Set[Solution]):
        """Plays a move at the given row and column for the given player.

        Assumptions:
            1.  The internal state of the SolutionManager is not at a terminal state.

        Args:
            player (int): the player making the move.
            row (int): the row to play
            col (int): the column to play

        Returns:
            removed_solutions (Set[Solution]): the Solutions that were removed after the given move.
            added_solutions (Set[Solution]): the Solutions that were added after the given move.
        """
        pass

    def undo_move(self):
        """Undoes the most recent move.

        Raises:
            (AssertionError): if the internal state of the SolutionManager is at the state given upon initialization.
        """
        pass
