import gym
import unittest

import numpy as np

from connect_four.agents.victor import Board
from connect_four.agents.victor import Square
from connect_four.envs.connect_four_env import ConnectFourEnv


class TestBoard(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 4
        ConnectFourEnv.N = 4
        self.env.reset()

    def test_is_empty(self):
        self.env.state = np.array([
            [
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 1, ],
            ],
            [
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 1, 0, ],
            ],
        ])
        state, _ = self.env.get_env_variables()
        board = Board(state)
        self.assertTrue(board.is_empty(Square(0, 0)))
        self.assertFalse(board.is_empty(Square(3, 3)))
        self.assertFalse(board.is_empty(Square(3, 2)))

    def test_playable_square(self):
        self.env.state = np.array([
            [
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 1, ],
            ],
            [
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 1, 0, ],
            ],
        ])
        state, _ = self.env.get_env_variables()
        board = Board(state)
        self.assertEqual(Square(3, 0), board.playable_square(0))

    def test_playable_squares(self):
        self.env.state = np.array([
            [
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 1, ],
            ],
            [
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 1, 0, ],
            ],
        ])
        state, _ = self.env.get_env_variables()
        board = Board(state)
        want_squares = {
            Square(3, 0),
            Square(3, 1),
            Square(2, 2),
            Square(2, 3),
        }
        self.assertEqual(want_squares, board.playable_squares())


if __name__ == '__main__':
    unittest.main()