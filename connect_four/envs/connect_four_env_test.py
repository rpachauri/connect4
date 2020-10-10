import unittest
import gym
import connect_four
import numpy as np

from connect_four.envs.connect_four_env import ConnectFourEnv

class TestConnectFourEnv(unittest.TestCase):

  def setUp(self):
    self.env = gym.make('connect_four-v0')
    ConnectFourEnv.M = 6
    ConnectFourEnv.N = 7
    self.env.reset()

  def test_reset(self):
    obs = self.env.reset()
    # upon initialization, environment should not be done.
    self.assertFalse(self.env.done)
    # upon initialization, it should be Player 1's turn.
    self.assertEqual(self.env.agent_turn, 0)
    # upon initialization, board should be full of 0s.
    self.assertIsNone(np.testing.assert_array_equal(
      obs,
      np.zeros(shape=(2, ConnectFourEnv.M, ConnectFourEnv.N)),
    ))


if __name__ == '__main__':
  unittest.main()