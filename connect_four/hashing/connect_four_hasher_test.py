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
        self.assertEqual(want_lowest_empty_squares, self.hasher.lowest_empty_row_by_col)

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
        self.assertEqual(want_lowest_empty_squares, self.hasher.lowest_empty_row_by_col)

    def test_move_undo_move(self):
        self.hasher.move(action=0)
        want_columns_played_by_move = [0]
        self.assertEqual(want_columns_played_by_move, self.hasher.columns_played_by_move)

        self.hasher.undo_move()
        self.assertFalse(self.hasher.columns_played_by_move)

    def test_hash_flipped_position(self):
        # This test case is based on Diagram 12.2.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
            ],
        ])
        self.hasher = ConnectFourHasher(env=self.env)
        transposition_of_original = self.hasher.hash()

        # Initialize state to a flipped version of the above position.
        # See Diagram 12.7.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 1, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
            ],
        ])
        self.hasher = ConnectFourHasher(env=self.env)
        transposition_of_flipped = self.hasher.hash()
        self.assertEqual(transposition_of_original, transposition_of_flipped)


if __name__ == '__main__':
    unittest.main()
