import unittest

import numpy as np

from connect_four.transposition import tic_tac_toe_simple_transposition_table


class TestTicTacToeSimpleTranspositionTable(unittest.TestCase):
    def test_save_and_retrieve_initial_state_1_and_1(self):
        state = np.array([
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
        tt = tic_tac_toe_simple_transposition_table.TicTacToeSimpleTranspositionTable()
        want_phi, want_delta = 1, 1
        tt.save(state=state, phi=want_phi, delta=want_delta)
        got_phi, got_delta = tt.retrieve(state=state)
        self.assertEqual(want_phi, got_phi)
        self.assertEqual(want_delta, got_delta)

    def test_overwrite_save(self):
        state = np.array([
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
        tt = tic_tac_toe_simple_transposition_table.TicTacToeSimpleTranspositionTable()
        tt.save(state=state, phi=1, delta=1)

        want_phi, want_delta = 2, 2
        tt.save(state=state, phi=want_phi, delta=want_delta)
        got_phi, got_delta = tt.retrieve(state=state)
        self.assertEqual(want_phi, got_phi)
        self.assertEqual(want_delta, got_delta)


if __name__ == '__main__':
    unittest.main()
