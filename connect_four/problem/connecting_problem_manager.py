from typing import List, Set, Dict

from connect_four.envs import TwoPlayerGameEnvVariables
from connect_four.game import Square
from connect_four.problem import Group as Problem
from connect_four.problem.problem_manager import ProblemManager


class ConnectingProblemManager(ProblemManager):
    def __init__(self, env_variables: TwoPlayerGameEnvVariables, num_to_connect: int):
        """Initializes the ConnectingProblemManager with the given env_variables.

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

        # Play squares that have already been played.
        # Change self.groups_by_square_by_player accordingly.
        # Note that the order of the play does not matter because groups in self.groups_by_square_by_player() can only
        # be removed by self._play_square().
        for player in range(len(state)):
            for row in range(len(state[0])):
                for col in range(len(state[0][0])):
                    if state[player][row][col] == 1:
                        self._play_square(player=player, row=row, col=col)

        self.groups_removed_by_squares_by_move = []

    @staticmethod
    def _create_all_groups(num_rows: int, num_cols: int, num_to_connect: int) -> Set[Problem]:
        """Creates a set of all Problems for an empty board with the given number of rows and columns.

        Args:
            num_rows (int): The number of rows there are in the board.
            num_cols (int): The number of columns there are in the board.
            num_to_connect (int): The number of squares that need to be connected for a win.

        Returns:
            all_groups (Set[Problem]): the set of all Problems that can be used by either player in an empty board.
        """
        directions = [
            (-1, 1),  # up-right diagonal
            (0, 1),  # horizontal
            (1, 1),  # down-right diagonal
            (1, 0),  # vertical
        ]
        all_groups = set()
        for player in range(2):
            for start_row in range(num_rows):
                for start_col in range(num_cols):
                    for direction in directions:
                        end_row = start_row + (num_to_connect - 1) * direction[0]
                        end_col = start_col + (num_to_connect - 1) * direction[1]
                        if ConnectingProblemManager._is_valid(
                                row=end_row, col=end_col, num_rows=num_rows, num_cols=num_cols):
                            all_groups.add(Problem(
                                player=player,
                                start=Square(row=start_row, col=start_col),
                                end=Square(row=end_row, col=end_col),
                            ))
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
            num_rows: int, num_cols: int, all_groups: Set[Problem]) -> List[List[List[Set[Problem]]]]:
        """

        Args:
            num_rows (int): the number of rows in the board.
            num_cols (int): the number of columns in the board.
            all_groups (Set[Problem]): the set of all Groups that can be used by either player in an empty board.

        Returns:
            groups_by_square_by_player (List[List[List[Set[Problem]]]]): a 3D array of a Set of Groups.
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
                        if player == group.player and square in group.squares:
                            groups_at_square.add(group)
                    rows.append(groups_at_square)
                player_squares.append(rows)
            groups_by_square_by_player.append(player_squares)
        return groups_by_square_by_player

    def _play_square(self, player: int, row: int, col: int) -> Dict[Square, Set[Problem]]:
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
            groups_removed_by_squares (Dict[Square, Set[Problem]]):
                A Dictionary mapping Squares to the Set of Problems that were removed from that Square.
                For every square in groups_removed_by_squares, the opponent can no longer win using that Group.
        """
        opponent = 1 - player
        groups_removed_by_square = self._remove_groups(opponent=opponent, row=row, col=col)
        return groups_removed_by_square

    def _remove_groups(self, opponent: int, row: int, col: int) -> Dict[Square, Set[Problem]]:
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
            groups_removed_by_square (Dict[Square, Set[Problems]]):
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

    def move(self, player: int, row: int, col: int) -> Set[Square]:
        """Plays a move at the given row and column for the given player.

        Assumptions:
            1.  The internal state of the ConnectingProblemManager is not at a terminal state.

        Args:
            player (int): the player making the move.
            row (int): the row to play
            col (int): the column to play

        Returns:
            affected_squares (Set[Square]): all squares which had a Problem removed.
        """
        groups_removed_by_square = self._play_square(player=player, row=row, col=col)
        self.groups_removed_by_squares_by_move.append(groups_removed_by_square)
        return set(groups_removed_by_square.keys())

    def undo_move(self) -> Set[Problem]:
        """Undoes the most recent move.

        Raises:
            (AssertionError): if the internal state of the ConnectingProblemManager is
                at the state given upon initialization.

        Returns:
            added_problems (Set[Problem]): the Problems that were added after undoing the most recent move.
        """
        assert self.groups_removed_by_squares_by_move

        added_problems = set()
        groups_removed_by_squares = self.groups_removed_by_squares_by_move.pop()
        for square in groups_removed_by_squares:
            for group in groups_removed_by_squares[square]:
                self.groups_by_square_by_player[group.player][square.row][square.col].add(group)
                added_problems.add(group)

        return added_problems

    def get_problems_by_square_by_player(self) -> List[List[List[Set[Problem]]]]:
        """
        Returns:
            groups_by_square_by_player (List[List[List[Set[Problem]]]]): a 3D array of a Set of Groups.
                1. The first dimension is the player.
                2. The second dimension is the row.
                3. The third dimension is the col.

                For a given player and a given Square, you can retrieve all Problems
                that player can win from that Square with:
                    set_of_possible_winning_groups_at_player_row_col = groups_by_square_by_player[player][row][col]
        """
        return self.groups_by_square_by_player

    def get_current_problems(self) -> Set[Problem]:
        """

        Returns:
            problems (Set[Problem]): a set of all Problems that belong to the current player.
        """
        problems = set()
        for row in range(len(self.groups_by_square_by_player[self.player])):
            for col in range(len(self.groups_by_square_by_player[self.player][row])):
                problems.update(self.groups_by_square_by_player[self.player][row][col])
        return problems

    def get_all_problems(self) -> Set[Problem]:
        """

        Returns:
            problems (Set[Problem]): a set of all Problems that belong to the either player.
        """
        problems = set()
        for player in range(len(self.groups_by_square_by_player)):
            for row in range(len(self.groups_by_square_by_player[player])):
                for col in range(len(self.groups_by_square_by_player[player][row])):
                    problems.update(self.groups_by_square_by_player[player][row][col])
        return problems
