from typing import List, Set, Dict

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

        # Play squares that have already been played.
        # Change self.groups_by_square_by_player and self.square_types accordingly.
        # Note that the order of the play does not matter because groups in self.groups_by_square_by_player() can only
        # be removed by self._play_square() and the transition graph of SquareTypes has no cycles.
        for player in range(len(state)):
            for row in range(len(state[0])):
                for col in range(len(state[0][0])):
                    if state[player][row][col] == 1:
                        self._play_square(player=player, row=row, col=col)

        self.groups_removed_by_squares_by_move = []
        self.previous_square_types_by_move = []

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
        # Play the given square with the current player.
        groups_removed_by_squares, previous_square_types = self._play_square(
            player=self.player,
            row=row,
            col=col,
        )

        # Add the dictionary of squares to set of groups removed to the stack so we can undo later.
        self.groups_removed_by_squares_by_move.append(groups_removed_by_squares)
        # Add the dictionary of squares to previous SquareType to the stack so we can undo later.
        self.previous_square_types_by_move.append(previous_square_types)

        # Switch play.
        self.player = 1 - self.player

    def _play_square(self, player: int, row: int, col: int) -> (Dict[Square, Set[Group]], Dict[Square, SquareType]):
        """Plays the given square for the given player.

        Args:
            player (int): the player playing the square
            row (int): the row of the square
            col (int): the column of the square

        Modifies:
            self.groups_by_square_by_player: Removes any groups the opponent of player cannot win with after this
                square is played.
            self.square_types:
                1. Change the given square into one of {Player1, Player2, Indifferent}.
                2. May also change other squares to Indifferent. Those squares must be one of {Player1, Player2}.

        Returns:
            groups_removed_by_squares (Dict[Square, Set[Group]]):
                A Dictionary mapping Squares to the Set of Groups that were removed from that Square.
                For every square in groups_removed_by_squares, the opponent can no longer win using that Group.
            previous_square_types (Dict[Square, SquareType]):
                A Dictionary mapping each Square to the SquareType it was before this move was played.
                Only Squares that had their SquareType changed are included.
        """
        opponent = 1 - player
        groups_removed_by_square = self._remove_groups(opponent=opponent, row=row, col=col)
        indifferent_squares = self._find_indifferent_squares(
            player=player,
            row=row,
            col=col,
            groups_removed_by_square=groups_removed_by_square,
        )
        previous_square_types = self._update_square_types(row=row, col=col, indifferent_squares=indifferent_squares)
        return groups_removed_by_square, previous_square_types

    def _remove_groups(self, opponent: int, row: int, col: int) -> Dict[Square, Set[Group]]:
        """
        Args:
            opponent (int): the player whose Groups we are removing.
            row (int): the row being played
            col (int): the column being played

        Modifies:
            self.groups_by_square_by_player: For every square in groups_removed_by_squares,
                every group in groups_removed_by_squares[square] will be removed from
                self.groups_by_square_by_player[opponent][square.row][square.col].

        Returns:
            groups_removed_by_square (Dict[Square, Set[Group]]):
                A Dictionary mapping Squares to all Groups that were removed.
                For every square in groups_removed_by_squares, the opponent can no longer win using that Group.
        """
        groups_to_remove = self.groups_by_square_by_player[opponent][row][col].copy()
        # Change existing_groups_by_square to reflect that the opponent cannot win using any group in groups.
        groups_removed_by_square = {}
        for g in groups_to_remove:
            for s in g.squares:
                # If the opponent could win using this group, they no longer can.
                if g in self.groups_by_square_by_player[opponent][s.row][s.col]:
                    self.groups_by_square_by_player[opponent][s.row][s.col].remove(g)

                    # If groups_removed_by_square doesn't already contain this square, add it.
                    if s not in groups_removed_by_square:
                        groups_removed_by_square[s] = set()

                    # Add g as one of the groups removed.
                    groups_removed_by_square[s].add(g)
        return groups_removed_by_square

    def _find_indifferent_squares(self, player: int, row: int, col: int,
                                  groups_removed_by_square: Dict[Square, Set[Group]]) -> Set[Square]:
        """

        Args:
            row (int): the row being played
            col (int): the column being played
            groups_removed_by_square (Dict[Square, Set[Group]]):
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
        if not groups_removed_by_square:
            indifferent_squares.add(Square(row=row, col=col))
        for s in groups_removed_by_square:
            # If neither player can win any groups at this square, this square is indifferent.
            if (self.square_types[s.row][s.col] != SquareType.Empty) and \
                    (not self.groups_by_square_by_player[0][s.row][s.col]) and \
                    (not self.groups_by_square_by_player[1][s.row][s.col]):
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
        assert self.groups_removed_by_squares_by_move
        assert self.previous_square_types_by_move

        # Switch play.
        opponent = self.player
        self.player = 1 - self.player

        groups_removed_by_squares = self.groups_removed_by_squares_by_move.pop()
        for square in groups_removed_by_squares:
            for group in groups_removed_by_squares[square]:
                self.groups_by_square_by_player[opponent][square.row][square.col].add(group)

        previous_square_types = self.previous_square_types_by_move.pop()
        for square in previous_square_types:
            self.square_types[square.row][square.col] = previous_square_types[square]

    def get_square_types(self) -> List[List[SquareType]]:
        """Retrieves the square types.

        Returns:
            square_types (List[List[SquareType]]): 2D array of SquareTypes summarizing the current state.
        """
        pass
