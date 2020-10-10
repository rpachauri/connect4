import gym
import numpy as np

class ConnectFourEnv(gym.Env):
  """Implements the gym.Env interface.
  
  https://github.com/openai/gym/blob/master/gym/core.py.
  """
  # Dimension of the ConnectFour environment.
  M = 6
  N = 7

  INVALID_MOVE = -1
  CONNECTED_FOUR = 1

  def __init__(self):
    self.reset()
    pass

  def step(self, action):
    # Find the highest token in the given column.
    highest_token = self._find_highest_token(action)
    # The location of the new token will be one above the highest token.
    new_token_row = highest_token - 1

    # Placing a token in a full column is an invalid move.
    if new_token_row == -1:
      return self.state, ConnectFourEnv.INVALID_MOVE, True, None

    # Place a token.
    self.state[self.player_turn, new_token_row, action] = 1

    # Check if the player has connected four.
    if self._connected_four(self.player_turn, new_token_row, action):
      return self.state, ConnectFourEnv.CONNECTED_FOUR, True, None
    pass

  def _find_highest_token(self, column):
    """ Finds the highest token belonging to either player in the selected column.

      Args:
        column (int): 0 ≤ column < ConnectFourEnv.N
      Returns:
        row (int): 0 ≤ row < ConnectFourEnv.M if there exist at least 1 token belonging to either player.
                   -1 if there are no tokens in the column
    """
    # mask is a boolean array. It is true if there is a token in the given column and false otherwise.
    mask = (self.state[:,:, column] != 0).any(axis=0)
    # get the highest row in the given column belonging to either player.
    return np.where(mask.any(axis=0), mask.argmax(axis=0), -1)

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
      (-1, 0), # up
      (-1, 1), # up-right
      (0, 1), # right
      (1, 1), # down-right
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
    while (r >= 0 and r < len(player_tokens) and
          c >= 0 and c < len(player_tokens[0]) and
          player_tokens[r, c] == 1):
      r += row_add
      c += col_add
      num_tokens += 1
    return num_tokens

  def reset(self):
    """Resets the state of the environment and returns an initial observation.

      Returns:
        observation (object): the initial observation.
    """
    self.player_turn = 0 # 0 means that it is Player 1's turn.

    self.state = np.zeros(shape=(2, ConnectFourEnv.M, ConnectFourEnv.N))

    return self.state

  def render(self, mode='human'):
    pass
