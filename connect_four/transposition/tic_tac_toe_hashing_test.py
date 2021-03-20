import unittest
import numpy as np

from connect_four.transposition import tic_tac_toe_hashing


class TestTicTacToeHashing(unittest.TestCase):
    def test_get_transposition_initial_state(self):
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
        want_transposition = "000000000"
        got_transposition = tic_tac_toe_hashing.get_transposition(state=state)
        self.assertEqual(want_transposition, got_transposition)

    def test_determine_empty_square_type(self):
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
        got_square_type = tic_tac_toe_hashing.determine_square_type(state=state, row=0, col=0)
        self.assertEqual(tic_tac_toe_hashing.SquareType.Empty, got_square_type)

    def test_is_indifferent_corner_square(self):
        state = np.array([
            [
                [1, 1, 0, ],
                [1, 0, 0, ],
                [0, 0, 0, ],
            ],
            [
                [0, 0, 1, ],
                [0, 0, 0, ],
                [1, 0, 1, ],
            ],
        ])
        self.assertTrue(tic_tac_toe_hashing.is_indifferent(state=state, row=0, col=0))

    def test_not_is_indifferent_corner_square(self):
        state = np.array([
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
        self.assertFalse(tic_tac_toe_hashing.is_indifferent(state=state, row=0, col=0))

    def test_determine_square_type(self):
        state = np.array([
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
        got_square_type = tic_tac_toe_hashing.determine_square_type(state=state, row=0, col=0)
        self.assertEqual(tic_tac_toe_hashing.SquareType.Player1, got_square_type)

        got_square_type = tic_tac_toe_hashing.determine_square_type(state=state, row=1, col=0)
        self.assertEqual(tic_tac_toe_hashing.SquareType.Player1, got_square_type)

        got_square_type = tic_tac_toe_hashing.determine_square_type(state=state, row=2, col=0)
        self.assertEqual(tic_tac_toe_hashing.SquareType.Player2, got_square_type)

        got_square_type = tic_tac_toe_hashing.determine_square_type(state=state, row=2, col=2)
        self.assertEqual(tic_tac_toe_hashing.SquareType.Player2, got_square_type)

    def test_get_transposition_mixed_square_types(self):
        state = np.array([
            [
                [1, 1, 0, ],
                [1, 0, 0, ],
                [0, 0, 0, ],
            ],
            [
                [0, 0, 1, ],
                [0, 0, 0, ],
                [1, 0, 1, ],
            ],
        ])
        want_transposition = "312100202"
        got_transposition = tic_tac_toe_hashing.get_transposition(state=state)
        self.assertEqual(want_transposition, got_transposition)

    def test_hash_position_leaves_state_untouched(self):
        state = np.array([
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
        state_copy = np.copy(state)
        tic_tac_toe_hashing.hash_position(state=state)
        self.assertIsNone(np.testing.assert_array_equal(
            x=state_copy,
            y=state,
        ))

    def test_hash_rotated_position(self):
        state = np.array([
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
        rotated_state = np.array([
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
        self.assertEqual(
            tic_tac_toe_hashing.hash_position(state=state),
            tic_tac_toe_hashing.hash_position(state=rotated_state),
        )

    def test_hash_flipped_position(self):
        state = np.array([
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
        flipped_state = np.array([
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
        self.assertEqual(
            tic_tac_toe_hashing.hash_position(state=state),
            tic_tac_toe_hashing.hash_position(state=flipped_state),
        )


if __name__ == '__main__':
    unittest.main()
