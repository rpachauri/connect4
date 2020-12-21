import gym
import numpy as np

from collections import namedtuple


ConnectFourEnvVariables = namedtuple("ConnectFourEnvVariables", ["state", "player_turn"])


class ConnectFourEnv(gym.Env):
    """Implements the gym.Env interface.
  
  https://github.com/openai/gym/blob/master/gym/core.py.
  """
    # Dimension of the ConnectFour environment.
    M = 6
    N = 7

    action_space = N

    INVALID_MOVE = -1
    CONNECTED_FOUR = 1
    DRAW = 0
    DEFAULT_REWARD = 0

    def __init__(self):
        self.reset()
        pass

    def step(self, action: int):
        """

        Args:
          action (int): 
        """
        # Find the highest token in the given column.
        highest_token = self._find_highest_token(action)
        # The location of the new token will be one above the highest token.
        new_token_row = highest_token - 1

        # Placing a token in a full column is an invalid move.
        if new_token_row == -1:
            return self.state.copy(), ConnectFourEnv.INVALID_MOVE, True, None

        # Place a token.
        self.state[self.player_turn, new_token_row, action] = 1

        # Check if the player has connected four.
        if self._connected_four(self.player_turn, new_token_row, action):
            return self.state.copy(), ConnectFourEnv.CONNECTED_FOUR, True, None

        # If all locations have been used and neither player has won,
        # this results in a draw.
        if self._is_full():
            return self.state.copy(), ConnectFourEnv.DRAW, True, None

        # Continue play with it now being the other player's turn.
        self.player_turn = 1 - self.player_turn
        return self.state.copy(), ConnectFourEnv.DEFAULT_REWARD, False, None

    def _find_highest_token(self, column):
        """ Finds the highest token belonging to either player in the selected column.

      Args:
        column (int): 0 ≤ column < ConnectFourEnv.N
      Returns:
        row (int): 0 ≤ row < ConnectFourEnv.M if there exist at least 1 token belonging to either player.
                   -1 if there are no tokens in the column
    """
        # mask is a boolean array. It is true if there is a token in the given column and false otherwise.
        mask = (self.state[:, :, column] != 0).any(axis=0)
        # get the highest row in the given column belonging to either player.
        return np.where(mask.any(axis=0), mask.argmax(axis=0), ConnectFourEnv.M)

    def _connected_four(self, player, row, col):
        """
      Args:
        player (int): 0 or 1. The player we are checking.
        row (int): the starting row
        col (int): the starting column

      Requires:
        self.state[player, row, col] == 1

      Returns:
        connected_four (bool): True if the player connected at least 4 using (row, col);
                               otherwise, False
    """
        row_and_col_adds = [
            (-1, 0),  # up
            (-1, 1),  # up-right
            (0, 1),  # right
            (1, 1),  # down-right
        ]
        for row_add, col_add in row_and_col_adds:
            num_tokens_in_pos_direction = self._num_tokens_in_direction(player, row, col, row_add, col_add)
            num_tokens_in_neg_direction = self._num_tokens_in_direction(player, row, col, -row_add, -col_add)
            num_tokens_in_line = num_tokens_in_pos_direction + 1 + num_tokens_in_neg_direction

            if num_tokens_in_line >= 4:
                return True

        # Player did not connect four in any direction.
        return False

    def _num_tokens_in_direction(self, player, row, col, row_add, col_add):
        """ Finds the number of tokens belonging to the given player starting
          from the given location and continuing in the given direction.

      Args:
        player (int): 0 or 1. The player we are checking.
        row (int): the starting row
        col (int): the starting column
        row_add (int): the increment for row
        col_add (int): the increment for col

      Returns:
        The number of tokens belonging to the player in the given direction.
        The starting location is not included.
        E.g. If there is only 1 token belonging to the player
             adjacent to the given location, returns 1.
    """
        player_tokens = self.state[player]
        r, c = row, col
        num_tokens = -1

        # while we are still in bounds and the location belongs to the player.
        while (0 <= r < len(player_tokens) and 0 <= c < len(player_tokens[0]) and
               player_tokens[r, c] == 1):
            r += row_add
            c += col_add
            num_tokens += 1
        return num_tokens

    def _is_full(self):
        """
      Returns:
        True if there is a token belonging to either player for every possible location.
    """
        return (self.state != 0).any(axis=0).all()

    @property
    def env_variables(self):
        """
      Returns:
        env_variables (tuple): a tuple that can be passed to reset() to restore a state.
        - env_variables[0] contains "obs", the observable variable for that state.
        - env_variables[1] contains "player_turn", indicating whose turn it is in that state.
    """
        return ConnectFourEnvVariables(self.state.copy(), self.player_turn)

    def reset(self, env_variables=None):
        """Resets the state of the environment and returns an initial observation.

      Args:
        env_variables (tuple) (optional):
          env_variables[0] (ndarray): should be a a numpy ndarray of shape (2, M, N)
          env_variables[1] (int): whose turn it should be (0 or 1)
      Example Usage:
        env_variables = env.env_variables()
        env.step(action)
        .
        .
        .
        env.reset(env_variables)
      Returns:
        observation (object): the initial observation.
    """
        if env_variables is not None:
            self.state = env_variables[0].copy()
            self.player_turn = env_variables[1]
        else:
            self.state = np.zeros(shape=(2, ConnectFourEnv.M, ConnectFourEnv.N))
            self.player_turn = 0

        return self.state.copy()

    def render(self, mode='human'):
        """Renders the current state of the environment.

    Args:
      mode (str): Supported modes: {'human'}
    """
        horizontal_wall = self._create_horizontal_wall()
        print(horizontal_wall)

        # plot the environment.
        for m in range(ConnectFourEnv.M):
            line = "|"
            for n in range(ConnectFourEnv.N):
                if self.state[0, m, n] == 1:  # token belongs to Player 1
                    line += "o"
                elif self.state[1, m, n] == 1:  # token belongs to Player 2
                    line += "x"
                else:  # location belongs to neither player
                    line += " "
            print(line + "|")

        print(horizontal_wall)

    @staticmethod
    def _create_horizontal_wall():
        """Used to help render the top or bottom wall in human mode.
    Returns:
      str: a string that can be printed when rendering in human mode.
    """
        wall = "*"
        for i in range(ConnectFourEnv.N):
            wall += "="
        return wall + "*"
