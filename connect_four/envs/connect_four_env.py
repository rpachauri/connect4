import gym
import numpy as np

class ConnectFourEnv(gym.Env):
  """Implements the gym.Env interface.
  
  https://github.com/openai/gym/blob/master/gym/core.py.
  """
  # Dimension of the ConnectFour environment.
  M = 6
  N = 7

  def __init__(self):
    pass

  def step(self, action):
    pass

  def reset(self):
    """Resets the state of the environment and returns an initial observation.

      Returns:
        observation (object): the initial observation.
    """
    self.done = False
    self.agent_turn = 0 # 0 means that it is Player 1's turn.

    self.state = np.zeros(shape=(2, ConnectFourEnv.M, ConnectFourEnv.N))

    return self.state

  def render(self, mode='human'):
    pass
