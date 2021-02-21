from connect_four.agents.victor.game import Square
from connect_four.agents.victor.game import Group
from connect_four.envs import ConnectFourEnvVariables


class Board:
    """Board is essentially a wrapper around the state of a ConnectFourEnv. It does not keep in sync with the
    environment's board. This means that if the state of the environment changes, this board will be out of date.
    """
    def __init__(self, env_variables: ConnectFourEnvVariables):
        """

        Args:
            env_variables (ConnectFourEnvVariables): an instance of the ConnectFourEnv.env_variables property.
                It must contain the following variables:

                state (np.array): a 2 x M x N np.array, where:
                    M is the number of rows in the board.
                    N is the number of columns in the board.
                player (int): The player whose turn it is in this state (0 or 1).
        """
        self.state, self.player = env_variables.state.copy(), env_variables.player_turn

    def is_valid(self, square: Square):
        return 0 <= square.row < len(self.state[0]) and 0 <= square.col < len(self.state[0][0])

    def is_empty(self, square: Square):
        """Returns whether or not the given square is empty on this board.

        Args:
            square: a Square. Assumes that the given square is within this board.

        Returns:
            True if the given square on this board is empty.
            False if the given square is occupied by either player.
        """
        return self.state[0][square.row][square.col] == 0 and self.state[1][square.row][square.col] == 0

    def playable_squares(self):
        """Returns a set of playable squares on this board.

        Returns:
            squares: a set of playable squares. empty if there are none.
        """
        squares = set()
        for col in range(len(self.state[0][0])):
            square = self.playable_square(col)
            if square is not None:
                squares.add(square)
        return squares

    def playable_square(self, col) -> Square:
        """Returns a playable square in this column if it exists.

        Args:
            col: (int) the column to find a playable square.

        Returns:
            square: (Square) the only playable square in this column if there is one.
                    If there is no playable square, returns None.
        """
        for row in reversed(range(len(self.state[0]))):
            square = Square(row, col)
            if self.is_empty(square):
                return square

    def potential_groups(self, player):
        """Returns a set of potential groups that this player has in this board state.

        Args:
            player (int): a player (0 or 1). groups must belong to this player.

        Returns:
            groups (set<Group>): a set of Group instances. Each group belongs to the given player.
        """
        directions = [
            (-1, 1),  # up-right diagonal
            (0, 1),  # horizontal
            (1, 1),  # down-right diagonal
            (1, 0),  # vertical
        ]
        groups = set()

        for row in range(len(self.state[0])):
            for col in range(len(self.state[0][0])):
                for row_diff, col_diff in directions:
                    if self.is_potential_group(player, row, col, row_diff, col_diff):
                        groups.add(Group(
                            player,
                            start=Square(row, col),
                            end=Square(row + 3 * row_diff, col + 3 * col_diff),
                        ))

        return groups

    def is_potential_group(self, player: int, row: int, col: int, row_diff: int, col_diff: int):
        """Returns whether or not the given group is a group that belongs to the player.

        Args:
            player (int): a player (0 or 1). Is the group a group that belongs to this player?
            row (int): starting row
            col (int): starting column
            row_diff (int): direction in which to increment the row (-1, 0 or 1)
            col_diff (int): direction in which to increment the col (-1, 0 or 1)

        Returns:
            is_group (bool): True if the group is a valid potential group that belongs to the player.
                              Otherwise, false.
        """
        opponent = 1 - player
        for _ in range(4):
            square = Square(row, col)
            if not self.is_valid(square):
                return False
            if self.state[opponent][row][col]:
                # If there is a token that belongs to the opponent in this group,
                # then this group is not a potential group that belongs to the given player.
                return False
            row, col = row + row_diff, col + col_diff
        return True

    def potential_groups_by_square(self):
        """Returns a dictionary of Squares to all groups that contain that Square.
        Every Group is a potential Group that the current player has in this board state.

        Returns:
            square_to_groups (Map<Square, Set<Group>>):
                A dictionary mapping each Square to all groups that contain that Square.
                Every Square in Board will be in the key set.
        """
        square_to_groups = {}
        for row in range(len(self.state[0])):
            for col in range(len(self.state[0][0])):
                square_to_groups[Square(row=row, col=col)] = set()

        groups = self.potential_groups(self.player)
        for group in groups:
            for square in group.squares:
                square_to_groups[square].add(group)

        return square_to_groups

    def empty_squares(self):
        """Returns a set of empty squares in this board state.

        Returns:
            squares (Set<Square>): A set of squares.
        """
        squares = set()
        for row in range(len(self.state[0])):
            for col in range(len(self.state[0][0])):
                if self.state[0][row][col] == 0 and self.state[1][row][col] == 0:
                    squares.add(Square(row=row, col=col))
        return squares
