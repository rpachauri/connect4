from abc import abstractmethod
from typing import Set

from connect_four.evaluation.victor.solution.solution2 import Solution
from connect_four.game import Square


class SolutionManager:

    @abstractmethod
    def move(self, player: int, row: int, col: int) -> Set[Square]:
        """Plays a move at the given row and column for the given player.

        Assumptions:
            1.  The internal state of the ProblemManager is not at a terminal state.

        Args:
            player (int): the player making the move.
            row (int): the row to play
            col (int): the column to play

        Returns:
            affected_squares (Set[Square]): all squares which had a Problem removed.
        """
        pass

    @abstractmethod
    def undo_move(self):
        """Undoes the most recent move.

        Raises:
            (AssertionError): if the internal state of the ProblemManager is
                at the state given upon initialization.
        """
        pass

    @abstractmethod
    def get_solutions(self) -> Set[Solution]:
        """Returns all Solutions for the current game position.

        Returns:
            solutions (Set[Solution]): the set of all Solutions that can be used in the current state.
        """
        pass
