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
    self.assertEqual(self.env.player_turn, 0)
    # upon initialization, board should be full of 0s.
    self.assertIsNone(np.testing.assert_array_equal(
      obs,
      np.zeros(shape=(2, ConnectFourEnv.M, ConnectFourEnv.N)),
    ))

  def test_find_highest_token(self):
    # place a token for Player 1 in the first column.
    self.env.state[0, -1, 0] = 1
    # fill the entire 2nd column with tokens belonging to Player 2.
    self.env.state[1, :, 1] = np.ones(ConnectFourEnv.M)

    # when there is only 1 token in the column,
    # the highest token should be at the lowest row.
    self.assertEqual(self.env._find_highest_token(0), ConnectFourEnv.M - 1)
    # when the column is full,
    # the highest token should be at the highest row.
    self.assertEqual(self.env._find_highest_token(1), 0)
    # when the column is empty,
    # the highest token should be -1.
    self.assertEqual(self.env._find_highest_token(2), -1)

  def test_place_token_in_full_column(self):
    # fill the entire 2nd column with tokens belonging to Player 2.
    self.env.state[1, :, 1] = np.ones(ConnectFourEnv.M)
    state_copy = self.env.state.copy()

    obs, reward, done, _ = self.env.step(1)
    # verify that the state has not changed.
    self.assertIsNone(np.testing.assert_array_equal(
      obs,
      state_copy,
    ))
    # verify the expected reward.
    self.assertEqual(reward, ConnectFourEnv.INVALID_MOVE)
    # verify the environment is done.
    self.assertTrue(done)


if __name__ == '__main__':
  unittest.main()