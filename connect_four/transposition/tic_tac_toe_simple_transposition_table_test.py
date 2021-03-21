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
        want_proof, want_disproof = 1, 1
        tt.save(state=state, proof=want_proof, disproof=want_disproof)
        got_proof, got_disproof = tt.retrieve(state=state)
        self.assertEqual(want_proof, got_proof)
        self.assertEqual(want_disproof, got_disproof)

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
        tt.save(state=state, proof=1, disproof=1)

        want_proof, want_disproof = 2, 2
        tt.save(state=state, proof=want_proof, disproof=want_disproof)
        got_proof, got_disproof = tt.retrieve(state=state)
        self.assertEqual(want_proof, got_proof)
        self.assertEqual(want_disproof, got_disproof)


if __name__ == '__main__':
    unittest.main()
