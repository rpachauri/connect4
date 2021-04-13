from abc import abstractmethod
from typing import List, Set

from connect_four.game import Square
from connect_four.problem import Group as Problem


class ProblemManager:

    @abstractmethod
    def move(self, player: int, row: int, col: int) -> (Set[Square], Set[Problem]):
        """Plays a move at the given row and column for the given player.

        Assumptions:
            1.  The internal state of the ProblemManager is not at a terminal state.

        Args:
            player (int): the player making the move.
            row (int): the row to play
            col (int): the column to play

        Returns:
            affected_squares (Set[Square]): all squares which had a Problem removed.
            removed_problems (Set[Problem]): all Problems that were removed.
        """
        pass

    @abstractmethod
    def undo_move(self) -> Set[Problem]:
        """Undoes the most recent move.

        Raises:
            (AssertionError): if the internal state of the ProblemManager is
                at the state given upon initialization.

        Returns:
            added_problems (Set[Problem]): the Problems that were added after undoing the most recent move.
        """
        pass

    @abstractmethod
    def get_problems_by_square_by_player(self) -> List[List[List[Set[Problem]]]]:
        """
        Returns:
            problems_by_square_by_player (List[List[List[Set[Problem]]]]): a 3D array of a Set of Groups.
                1. The first dimension is the player.
                2. The second dimension is the row.
                3. The third dimension is the col.

                For a given player and a given Square, you can retrieve all Problems
                that player can win from that Square with:
                    set_of_possible_winning_groups_at_player_row_col = groups_by_square_by_player[player][row][col]
        """
        pass

    @abstractmethod
    def get_current_problems(self) -> Set[Problem]:
        """

        Returns:
            problems (Set[Problem]): a set of all Problems that belong to the current player.
        """
        pass

    @abstractmethod
    def get_all_problems(self) -> Set[Problem]:
        """

        Returns:
            problems (Set[Problem]): a set of all Problems that belong to the either player.
        """
        pass
