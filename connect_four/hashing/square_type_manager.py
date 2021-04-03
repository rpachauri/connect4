from typing import List, Set

from connect_four.envs import TwoPlayerGameEnvVariables
from connect_four.hashing.data_structures import SquareType, Group, Square


class SquareTypeManager:

    def __init__(self, env_variables: TwoPlayerGameEnvVariables, num_to_connect: int):
        """Initializes the SquareTypeManager with the given env_variables.

        Args:
            env_variables (TwoPlayerGameEnvVariables): a TwoPlayerGame's env_variables.
        """
        state, self.player = env_variables
        num_rows, num_cols = len(state[0]), len(state[0][0])

        all_groups = self._create_all_groups(
            num_rows=num_rows,
            num_cols=num_cols,
            num_to_connect=num_to_connect,
        )
        self.groups_by_square_by_player = self._create_all_groups_by_square_by_player(
            num_rows=num_rows,
            num_cols=num_cols,
            all_groups=all_groups,
        )
        self.square_types = self._create_initial_square_types(num_rows=num_rows, num_cols=num_cols)

        pass

    @staticmethod
    def _create_all_groups(num_rows: int, num_cols: int, num_to_connect: int) -> Set[Group]:
        """Creates a set of all Groups for an empty board with the given number of rows and columns.

        Args:
            num_rows (int): The number of rows there are in the board.
            num_cols (int): The number of columns there are in the board.
            num_to_connect (int): The number of squares that need to be connected for a win.

        Returns:
            all_groups (Set[Group]): the set of all Groups that can be used by either player in an empty board.
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
        """

        Args:
            row (int): the row to validate
            col (int): the column to validate
            num_rows (int): the upper bound of valid rows (exclusive)
            num_cols (int): the upper bound of valid columns (exclusive)

        Returns:
            is_valid (bool): whether or not the given (row, col) pair is valid.
        """
        return 0 <= row < num_rows and 0 <= col < num_cols

    @staticmethod
    def _create_all_groups_by_square_by_player(
            num_rows: int, num_cols: int, all_groups: Set[Group]) -> List[List[List[Set[Group]]]]:
        """

        Args:
            num_rows (int): the number of rows in the board.
            num_cols (int): the number of columns in the board.
            all_groups (Set[Group]): the set of all Groups that can be used by either player in an empty board.

        Returns:
            groups_by_square_by_player (List[List[List[Set[Group]]]]): a 3D array of a Set of Groups.
                1. The first dimension is the player.
                2. The second dimension is the row.
                3. The third dimension is the col.

                For a given player and a given Square, you can retrieve all Groups that player can win from that Square
                with:
                    set_of_possible_winning_groups_at_player_row_col = groups_by_square_by_player[player][row][col]
        """
        groups_by_square_by_player = []
        for player in range(2):
            player_squares = []
            for row in range(num_rows):
                rows = []
                for col in range(num_cols):
                    groups_at_square = set()
                    square = Square(row=row, col=col)
                    for group in all_groups:
                        if square in group.squares:
                            groups_at_square.add(group)
                    rows.append(groups_at_square)
                player_squares.append(rows)
            groups_by_square_by_player.append(player_squares)
        return groups_by_square_by_player

    @staticmethod
    def _create_initial_square_types(num_rows: int, num_cols: int) -> List[List[SquareType]]:
        """

        Args:
            num_rows (int): the number of rows in the board.
            num_cols (int): the number of columns in the board.

        Returns:
            square_types (List[List[SquareType]]): a 2D array of SquareTypes all with SquareType.Empty
        """
        square_types = []
        for row in range(num_rows):
            rows = []
            for col in range(num_cols):
                rows.append(SquareType.Empty)
            square_types.append(rows)
        return square_types

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
