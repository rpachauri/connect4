import gym
import unittest

import numpy as np

from connect_four.envs import ConnectFourEnv
from connect_four.hashing.connect_four_hasher import ConnectFourHasher


class TestConnectFourHasher(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 7
        self.hasher = ConnectFourHasher(env=self.env)

    def test_initialization_initial_state(self):
        want_lowest_empty_squares = [5, 5, 5, 5, 5, 5, 5]
        self.assertEqual(want_lowest_empty_squares, self.hasher.lowest_empty_squares)

    def test_initialization_diagram_6_1(self):
        # This test case is based on Diagram 6.1.
        self.env.state = np.array([
            [
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 1, 0, 0, ],
            ],
        ])
        self.hasher = ConnectFourHasher(env=self.env)
        want_lowest_empty_squares = [5, 5, 4, -1, 4, 5, 5]
        self.assertEqual(want_lowest_empty_squares, self.hasher.lowest_empty_squares)


if __name__ == '__main__':
    unittest.main()
