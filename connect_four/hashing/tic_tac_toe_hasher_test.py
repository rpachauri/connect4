import gym
import unittest

import numpy as np

from connect_four.hashing import hasher_hash_utils
from connect_four.hashing import TicTacToeHasher


class TestTicTacToeHasher(unittest.TestCase):

    def setUp(self) -> None:
        self.env = gym.make('tic_tac_toe-v0')
        self.hasher = TicTacToeHasher(env=self.env)

    def test_convert_square_types_to_transposition_arr(self):
        self.env.state = np.array([
            [
                [1, 0, 1, ],
                [1, 0, 0, ],
                [0, 0, 0, ],
            ],
            [
                [0, 1, 0, ],
                [0, 1, 0, ],
                [1, 0, 0, ],
            ],
        ])
        self.hasher = TicTacToeHasher(env=self.env)

        want_transposition_arr = np.array([
            ["3", "2", "1", ],
            ["3", "2", "0", ],
            ["2", "0", "0", ],
        ])
        got_transposition_arr = hasher_hash_utils.convert_square_types_to_transposition_arr(
            square_types=self.hasher.stm.square_types,
        )
        self.assertIsNone(np.testing.assert_array_equal(
            want_transposition_arr,
            got_transposition_arr,
        ))

    def test_get_transposition(self):
        transposition_arr = np.array([
            ["3", "2", "1", ],
            ["3", "2", "0", ],
            ["2", "0", "0", ],
        ])
        want_transposition = "321320200"
        got_transposition = hasher_hash_utils.get_transposition(transposition_arr=transposition_arr)
        self.assertEqual(want_transposition, got_transposition)

    def test_hash_rotated_position(self):
        self.env.state = np.array([
            [
                [1, 0, 0, ],
                [1, 0, 0, ],
                [0, 0, 0, ],
            ],
            [
                [0, 0, 0, ],
                [0, 0, 0, ],
                [1, 0, 1, ],
            ],
        ])
        self.hasher = TicTacToeHasher(env=self.env)
        transposition_of_original = self.hasher.hash()

        # Initialize state to a rotated version of the above position.
        self.env.state = np.array([
            [
                [0, 0, 0, ],
                [0, 0, 0, ],
                [1, 1, 0, ],
            ],
            [
                [0, 0, 1, ],
                [0, 0, 0, ],
                [0, 0, 1, ],
            ],
        ])
        self.hasher = TicTacToeHasher(env=self.env)
        transposition_of_rotated = self.hasher.hash()
        self.assertEqual(transposition_of_original, transposition_of_rotated)

    def test_hash_flipped_position(self):
        self.env.state = np.array([
            [
                [1, 0, 0, ],
                [1, 0, 0, ],
                [0, 0, 0, ],
            ],
            [
                [0, 0, 0, ],
                [0, 0, 0, ],
                [1, 0, 1, ],
            ],
        ])
        self.hasher = TicTacToeHasher(env=self.env)
        transposition_of_original = self.hasher.hash()

        # Initialize state to a flipped version of the above position.
        self.env.state = np.array([
            [
                [0, 0, 1, ],
                [0, 0, 1, ],
                [0, 0, 0, ],
            ],
            [
                [0, 0, 0, ],
                [0, 0, 0, ],
                [1, 0, 1, ],
            ],
        ])
        self.hasher = TicTacToeHasher(env=self.env)
        transposition_of_flipped = self.hasher.hash()
        self.assertEqual(transposition_of_original, transposition_of_flipped)

    def test_move_to_drawn_terminal_state(self):
        self.env.state = np.array([
            [
                [1, 1, 0, ],
                [0, 0, 1, ],
                [1, 0, 0, ],
            ],
            [
                [0, 0, 1, ],
                [1, 0, 0, ],
                [0, 1, 1, ],
            ],
        ])
        self.hasher = TicTacToeHasher(env=self.env)

        want_transposition = "333303333"
        got_transposition = self.hasher.hash()
        self.assertEqual(want_transposition, got_transposition)

        self.hasher.move(action=4)
        want_transposition = "333333333"
        got_transposition = self.hasher.hash()
        self.assertEqual(want_transposition, got_transposition)


if __name__ == '__main__':
    unittest.main()
