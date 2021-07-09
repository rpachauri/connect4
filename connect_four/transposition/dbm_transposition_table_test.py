import unittest

import gym
import numpy as np

from connect_four.hashing import TicTacToeHasher
from connect_four.transposition.dbm_transposition_table import DBMTranspositionTable


class TestDBMTranspositionTable(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('tic_tac_toe-v0')

    def test_save_and_retrieve_initial_state_1_and_1(self):
        self.env.state = np.array([
            [
                [0, 0, 0, ],
                [0, 0, 0, ],
                [0, 0, 0, ],
            ],
            [
                [0, 0, 0, ],
                [0, 0, 0, ],
                [0, 0, 0, ],
            ],
        ])
        transposition = TicTacToeHasher(self.env).hash()
        tt = DBMTranspositionTable(phi_file="test_tic_tac_toe_phi", delta_file="test_tic_tac_toe_delta")
        want_phi, want_delta = 1, 1
        tt.save(transposition=transposition, phi=want_phi, delta=want_delta)
        got_phi, got_delta = tt.retrieve(transposition=transposition)
        self.assertEqual(want_phi, got_phi)
        self.assertEqual(want_delta, got_delta)
        self.assertIn(transposition, tt)

    def test_overwrite_save(self):
        self.env.state = np.array([
            [
                [0, 0, 0, ],
                [0, 0, 0, ],
                [0, 0, 0, ],
            ],
            [
                [0, 0, 0, ],
                [0, 0, 0, ],
                [0, 0, 0, ],
            ],
        ])
        transposition = TicTacToeHasher(self.env).hash()
        tt = DBMTranspositionTable(phi_file="test_tic_tac_toe_phi", delta_file="test_tic_tac_toe_delta")
        tt.save(transposition=transposition, phi=1, delta=1)

        want_phi, want_delta = 2, 2
        tt.save(transposition=transposition, phi=want_phi, delta=want_delta)
        got_phi, got_delta = tt.retrieve(transposition=transposition)
        self.assertEqual(want_phi, got_phi)
        self.assertEqual(want_delta, got_delta)


if __name__ == '__main__':
    unittest.main()
