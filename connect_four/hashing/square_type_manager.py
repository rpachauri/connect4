from typing import List, Set

from connect_four.envs import TwoPlayerGameEnvVariables
from connect_four.hashing.data_structures import SquareType, Group, Square


class SquareTypeManager:

    def __init__(self, env_variables: TwoPlayerGameEnvVariables, num_to_connect: int):
        """Initializes the SquareTypeManager with the given env_variables.

        Constraints:
            -

        Args:
            env_variables (TwoPlayerGameEnvVariables): a TwoPlayerGame's env_variables.
        """
        pass

    @staticmethod
    def _create_all_groups(num_rows: int, num_cols: int, num_to_connect: int) -> Set[Group]:
        """Creates a set of all Groups for an empty board with the given number of rows and columns.

        Args:
            num_rows (int): The number of rows there are in the board.
            num_cols (int): The number of columns there are in the board.
            num_to_connect (int): The number of squares that need to be connected for a win.

        Returns:
            all_groups (Set[Group]): the set of all Groups that can be used for a win.
                Each Group can be used by either player.
        """
        directions = [
            (-1, 1),  # up-right diagonal
            (0, 1),  # horizontal
            (1, 1),  # down-right diagonal
            (1, 0),  # vertical
        ]
        all_groups = set()
        for start_row in range(num_rows):
            for start_col in range(num_cols):
                for direction in directions:
                    group_squares = set()
                    for i in range(num_to_connect):
                        row = start_row + i * direction[0]
                        col = start_col + i * direction[1]
                        if SquareTypeManager._is_valid(row=row, col=col, num_rows=num_rows, num_cols=num_cols):
                            group_squares.add(Square(row=row, col=col))
                    if len(group_squares) == num_to_connect:
                        all_groups.add(Group(squares=frozenset(group_squares)))
        return all_groups

    @staticmethod
    def _is_valid(row: int, col: int, num_rows: int, num_cols: int) -> bool:
        return 0 <= row < num_rows and 0 <= col < num_cols

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
