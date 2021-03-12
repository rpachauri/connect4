import gym
import unittest

import numpy as np

from connect_four.envs import TwoPlayerGameEnv
from connect_four.envs import TicTacToeEnv


class TestTicTacToeEnv(unittest.TestCase):
    def setUp(self):
        self.env = gym.make('tic_tac_toe-v0')
        self.env.reset()

    def test_reset(self):
        obs = self.env.reset()
        # upon initialization, it should be Player 1's turn.
        self.assertEqual(self.env.player_turn, 0)
        # upon initialization, board should be full of 0s.
        self.assertIsNone(np.testing.assert_array_equal(
            obs,
            np.zeros(shape=(2, TicTacToeEnv.M, TicTacToeEnv.N)),
        ))

    def test_is_full(self):
        # Place a token for Player 1 in the first column.
        self.env.state[0, -1, 0] = 1
        self.assertFalse(self.env._is_full())

        # Cover the entire state with tokens from Player 1.
        self.env.state[0, :, :] = 1
        self.assertTrue(self.env._is_full())

    def test_action_to_square(self):
        row, col = self.env._action_to_square(7)
        self.assertEqual(2, row)
        self.assertEqual(1, col)

    def test_contains_token(self):
        # Place a token for Player 1 in the top-left corner.
        self.env.state[0, 0, 0] = 1
        self.assertTrue(self.env._contains_token(row=0, col=0))
        self.assertFalse(self.env._contains_token(row=1, col=0))

    def test_step_invalid_move(self):
        _, reward, done, _ = self.env.step(action=0)
        self.assertEqual(TwoPlayerGameEnv.DEFAULT_REWARD, reward)
        self.assertFalse(done)

        _, reward, done, _ = self.env.step(action=0)
        self.assertEqual(TwoPlayerGameEnv.INVALID_MOVE, reward)
        self.assertTrue(done)

    def test_step_connected_three(self):
        self.env.state = np.array([
            [
                [1, 1, 0, ],
                [0, 0, 0, ],
                [0, 0, 0, ],
            ],
            [
                [0, 0, 0, ],
                [1, 1, 0, ],
                [0, 0, 0, ],
            ],
        ])
        _, reward, done, _ = self.env.step(action=2)
        self.assertEqual(TwoPlayerGameEnv.CONNECTED, reward)
        self.assertTrue(done)


if __name__ == '__main__':
    unittest.main()
