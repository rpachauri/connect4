from enum import Enum
from typing import List, Set, Dict

from connect_four.envs import TwoPlayerGameEnvVariables
from connect_four.game import Square
from connect_four.problem import ConnectingProblemManager


class SquareType(Enum):
    Empty = 0
    Indifferent = 1
    Player1 = 2
    Player2 = 3


class SquareTypeManager:

    def __init__(self, env_variables: TwoPlayerGameEnvVariables, num_to_connect: int):
        """Initializes the SquareTypeManager with the given env_variables.

        Args:
            env_variables (TwoPlayerGameEnvVariables): a TwoPlayerGame's env_variables.
        """
        state, self.player = env_variables
        num_rows, num_cols = len(state[0]), len(state[0][0])

        self.problem_manager = ConnectingProblemManager(env_variables=env_variables, num_to_connect=num_to_connect)
        self.square_types = self._create_initial_square_types(num_rows=num_rows, num_cols=num_cols)

        # Play squares that have already been played.
        # Change self.square_types accordingly.
        # Note that the order of the play does not matter because transition graph of SquareTypes has no cycles.
        for player in range(len(state)):
            for row in range(len(state[0])):
                for col in range(len(state[0][0])):
                    if state[player][row][col] == 1:
                        if (not self.problem_manager.groups_by_square_by_player[0][row][col] and
                                not self.problem_manager.groups_by_square_by_player[1][row][col]):
                            self.square_types[row][col] = SquareType.Indifferent
                        elif player == 0:
                            self.square_types[row][col] = SquareType.Player1
                        else:
                            self.square_types[row][col] = SquareType.Player2

        self.previous_square_types_by_move = []

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
        affected_squares, _ = self.problem_manager.move(player=self.player, row=row, col=col)

        indifferent_squares = self._find_indifferent_squares(
            player=self.player,
            row=row,
            col=col,
            affected_squares=affected_squares,
        )
        previous_square_types = self._update_square_types(row=row, col=col, indifferent_squares=indifferent_squares)

        # Add the dictionary of squares to previous SquareType to the stack so we can undo later.
        self.previous_square_types_by_move.append(previous_square_types)

        # Switch play.
        self.player = 1 - self.player

    def _find_indifferent_squares(self, player: int, row: int, col: int,
                                  affected_squares: Set[Square]) -> Set[Square]:
        """

        Args:
            row (int): the row being played
            col (int): the column being played
            affected_squares (Set[Square]):
                A Dictionary mapping Squares to all Groups that were removed.
                For every square in groups_removed_by_squares, the opponent can no longer win using that Group.

        Modifies:
            self.square_types: If the square at the given row and col is not indifferent,
                assigns a SquareType corresponding with the given player.
                Updates all squares that are indifferent to SquareType.Indifferent.

        Returns:
            indifferent_squares (Set[Square]): a Set of Squares that can no longer be used to
                complete any Groups for either player.
        """
        # Assign the played square a non-empty SquareType. This allows it be included when finding indifferent_squares.
        if player == 0:
            self.square_types[row][col] = SquareType.Player1
        else:
            self.square_types[row][col] = SquareType.Player2

        # Find all indifferent squares.
        indifferent_squares = set()
        if not affected_squares:
            indifferent_squares.add(Square(row=row, col=col))
        for s in affected_squares:
            # If neither player can win any groups at this square, this square is indifferent.
            if (self.square_types[s.row][s.col] != SquareType.Empty) and \
                    (not self.problem_manager.groups_by_square_by_player[0][s.row][s.col]) and \
                    (not self.problem_manager.groups_by_square_by_player[1][s.row][s.col]):
                indifferent_squares.add(s)
        return indifferent_squares

    def _update_square_types(self, row: int, col: int, indifferent_squares: Set[Square]) -> Dict[Square, SquareType]:
        """

        Args:
            row (int): the row being played
            col (int): the column being played
            indifferent_squares (Set[Square]): a Set of Squares that can no longer be used to
                complete any Groups for either player.

        Modifies:
            self.square_types: For every square in indifferent_squares, updates to SquareType.Indifferent.

        Returns:
            previous_square_types (Dict[Square, SquareType]): a dictionary mapping each Square to the SquareType it was
                before it was changed.
        """
        # Find the SquareType of all squares that are being changed.
        previous_square_types = {}
        # Change the square types of indifferent squares.
        for s in indifferent_squares:
            previous_square_types[s] = self.square_types[s.row][s.col]
            self.square_types[s.row][s.col] = SquareType.Indifferent

        previous_square_types[Square(row=row, col=col)] = SquareType.Empty

        return previous_square_types

    def undo_move(self):
        """Undoes the most recent move.

        Raises:
            (AssertionError): if the internal state of the SquareTypeManager is at the state given upon initialization.
        """
        self.problem_manager.undo_move()
        assert self.previous_square_types_by_move

        # Switch play.
        self.player = 1 - self.player

        previous_square_types = self.previous_square_types_by_move.pop()
        for square in previous_square_types:
            self.square_types[square.row][square.col] = previous_square_types[square]
