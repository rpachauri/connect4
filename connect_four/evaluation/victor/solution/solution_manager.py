from abc import abstractmethod
from typing import Set

from connect_four.evaluation.victor.solution.solution2 import Solution


class SolutionManager:

    @abstractmethod
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

    @abstractmethod
    def undo_move(self) -> (Set[Solution], Set[Solution]):
        """Undoes the most recent move.

        Raises:
            (AssertionError): if the internal state of the ProblemManager is
                at the state given upon initialization.

        Returns:
            removed_solutions (Set[Solution]): the Solutions that were removed by undoing the most recent move.
            added_solutions (Set[Solution]): the Solutions that were added by undoing the most recent move.
        """
        pass

    @abstractmethod
    def get_solutions(self) -> Set[Solution]:
        """Returns all Solutions for the current game position.

        Returns:
            solutions (Set[Solution]): the set of all Solutions that can be used in the current state.
        """
        pass

    @abstractmethod
    def get_win_conditions(self) -> Set[Solution]:
        """Returns all win conditions for the current game position.

        Returns:
            win_conditions (Set[Solution]): a subset of all Solutions in this state.

            Constraints on win_conditions:
                1. No Solution in win_conditions may be combined with another Solution in win_conditions.
        """
        pass
