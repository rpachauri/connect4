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

  def __init__(self):
    self.reset()
    pass

  def step(self, action):
    # 
    highest_token = self._find_highest_token(action)
    # the location of the new token will be one above the highest token.
    new_token_row = highest_token - 1

    # Placing a token in a full column is an invalid move.
    if new_token_row == -1:
      self.done = True
      return self.state, ConnectFourEnv.INVALID_MOVE, self.done, None

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

  def reset(self):
    """Resets the state of the environment and returns an initial observation.

      Returns:
        observation (object): the initial observation.
    """
    self.done = False
    self.player_turn = 0 # 0 means that it is Player 1's turn.

    self.state = np.zeros(shape=(2, ConnectFourEnv.M, ConnectFourEnv.N))

    return self.state

  def render(self, mode='human'):
    pass
