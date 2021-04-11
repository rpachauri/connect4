from typing import Set

from connect_four.envs import TwoPlayerGameEnvVariables
from connect_four.evaluation.victor.solution.solution2 import Solution


class GraphManager:
    def __init__(self, env_variables: TwoPlayerGameEnvVariables):
        """Initializes the SolutionManager with the given env_variables.

        Args:
            env_variables (TwoPlayerGameEnvVariables): a TwoPlayerGame's env_variables.
        """
        pass

    def move(self, row: int, col: int):
        """Plays a move at the given row and column for the current player.

        Assumptions:
            1.  The internal state of the GraphManager is not at a terminal state.

        Args:
            row (int): the row to play
            col (int): the column to play

        Returns:
            Nothing.
        """
        pass

    def undo_move(self):
        """Undoes the most recent move.

        Raises:
            (AssertionError): if the internal state of the GraphManager is at the state given upon initialization.
        """
        pass

    def evaluate(self) -> Set[Solution]:
        """Evaluates the current position.

        Returns:
            chosen_set (Set[Solution]): A set of Solutions that solves the current state.
                                        None if no such set can be found for the current position.

            Implications of chosen_set depending on the current player:
            1. If chosen_set is None:
                No guarantees can be made on the game-theoretic value of the current position.
            2. Else if the current player is White:
                Black can guarantee at least a draw.
            3. Else: # the current player is Black:
                White can guarantee a win.
        """
        pass
