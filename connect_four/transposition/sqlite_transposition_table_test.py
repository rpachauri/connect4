import unittest

import gym
import numpy as np

from connect_four.hashing import TicTacToeHasher
from connect_four.transposition.sqlite_transposition_table import SQLiteTranspositionTable


class TestSQLiteTranspositionTable(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('tic_tac_toe-v0')

    def test_save_and_retrieve(self):
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
        tt = SQLiteTranspositionTable(database_file=":memory:")
        want_phi, want_delta = 1, 1
        tt.save(transposition=transposition, phi=want_phi, delta=want_delta)
        self.assertIn(transposition, tt)
        got_phi, got_delta = tt.retrieve(transposition=transposition)
        self.assertEqual(want_phi, got_phi)
        self.assertEqual(want_delta, got_delta)

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
        tt = SQLiteTranspositionTable(database_file=":memory:")
        tt.save(transposition=transposition, phi=1, delta=1)

        want_phi, want_delta = 2, 2
        tt.save(transposition=transposition, phi=want_phi, delta=want_delta)
        got_phi, got_delta = tt.retrieve(transposition=transposition)
        self.assertEqual(want_phi, got_phi)
        self.assertEqual(want_delta, got_delta)

    def test_close_and_reload(self):
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
        tt = SQLiteTranspositionTable(database_file="sqlite_test.db")
        tt.save(transposition=transposition, phi=1, delta=1)
        tt.close()

        tt2 = SQLiteTranspositionTable(database_file="sqlite_test.db")
        self.assertIn(transposition, tt2)
        tt2.close()


if __name__ == '__main__':
    unittest.main()
