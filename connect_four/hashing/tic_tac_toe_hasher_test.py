import gym
import unittest

import numpy as np

from connect_four.hashing import TicTacToeHasher
from connect_four.hashing.tic_tac_toe_hasher import Square
from connect_four.hashing.tic_tac_toe_hasher import Group
from connect_four.hashing.tic_tac_toe_hasher import SquareType


class TestTicTacToeHasher(unittest.TestCase):
    GROUP_00_TO_02 = Group(squares=frozenset([Square(row=0, col=0), Square(row=0, col=1), Square(row=0, col=2)]))
    GROUP_10_TO_12 = Group(squares=frozenset([Square(row=1, col=0), Square(row=1, col=1), Square(row=1, col=2)]))
    GROUP_20_TO_22 = Group(squares=frozenset([Square(row=2, col=0), Square(row=2, col=1), Square(row=2, col=2)]))
    GROUP_00_TO_20 = Group(squares=frozenset([Square(row=0, col=0), Square(row=1, col=0), Square(row=2, col=0)]))
    GROUP_01_TO_21 = Group(squares=frozenset([Square(row=0, col=1), Square(row=1, col=1), Square(row=2, col=1)]))
    GROUP_02_TO_22 = Group(squares=frozenset([Square(row=0, col=2), Square(row=1, col=2), Square(row=2, col=2)]))
    GROUP_00_TO_22 = Group(squares=frozenset([Square(row=0, col=0), Square(row=1, col=1), Square(row=2, col=2)]))
    GROUP_20_TO_02 = Group(squares=frozenset([Square(row=2, col=0), Square(row=1, col=1), Square(row=0, col=2)]))

    def setUp(self) -> None:
        self.env = gym.make('tic_tac_toe-v0')
        self.hasher = TicTacToeHasher(env=self.env)

    def test_init_initial_state(self):
        # Validate expected groups.
        want_player_0_groups_at_00 = {
            TestTicTacToeHasher.GROUP_00_TO_02,
            TestTicTacToeHasher.GROUP_00_TO_22,
            TestTicTacToeHasher.GROUP_00_TO_20,
        }
        got_player_0_groups_at_00 = self.hasher.groups_by_square_by_player[0][0][0]
        self.assertEqual(want_player_0_groups_at_00, got_player_0_groups_at_00)

        want_player_0_groups_at_11 = {
            TestTicTacToeHasher.GROUP_00_TO_22,
            TestTicTacToeHasher.GROUP_01_TO_21,
            TestTicTacToeHasher.GROUP_10_TO_12,
            TestTicTacToeHasher.GROUP_20_TO_02,
        }
        got_player_0_groups_at_11 = self.hasher.groups_by_square_by_player[0][1][1]
        self.assertEqual(want_player_0_groups_at_11, got_player_0_groups_at_11)

        # Validate expected square types.
        self.assertEqual(SquareType.Empty, self.hasher.square_types[0][0])

        # Validate current player.
        self.assertEqual(0, self.hasher.player)

    def test_play_square(self):
        self.hasher = TicTacToeHasher(env=self.env)
        # Since no squares have been played, it is possible for Player 2 to win using Group 00-02.
        self.assertIn(TestTicTacToeHasher.GROUP_00_TO_02, self.hasher.groups_by_square_by_player[1][0][2])
        self.hasher._play_square(player=0, row=0, col=0)
        # Since Player 1 has played at 00, it is not possible for Player 2 to win using Group 00-02.
        self.assertNotIn(TestTicTacToeHasher.GROUP_00_TO_02, self.hasher.groups_by_square_by_player[1][0][2])

    def test_play_square_initial_state(self):
        self.hasher = TicTacToeHasher(env=self.env)
        want_groups_removed_by_square = {
            Square(row=0, col=0): {
                TestTicTacToeHasher.GROUP_00_TO_02,
                TestTicTacToeHasher.GROUP_00_TO_22,
                TestTicTacToeHasher.GROUP_00_TO_20,
            },
            Square(row=0, col=1): {
                TestTicTacToeHasher.GROUP_00_TO_02,
            },
            Square(row=0, col=2): {
                TestTicTacToeHasher.GROUP_00_TO_02,
            },
            Square(row=1, col=1): {
                TestTicTacToeHasher.GROUP_00_TO_22,
            },
            Square(row=2, col=2): {
                TestTicTacToeHasher.GROUP_00_TO_22,
            },
            Square(row=1, col=0): {
                TestTicTacToeHasher.GROUP_00_TO_20,
            },
            Square(row=2, col=0): {
                TestTicTacToeHasher.GROUP_00_TO_20,
            },
        }
        want_previous_square_types = {
            Square(row=0, col=0): SquareType.Empty,
        }
        got_groups_removed_by_square, got_previous_square_types = self.hasher._play_square(player=0, row=0, col=0)
        self.assertEqual(want_groups_removed_by_square, got_groups_removed_by_square)
        self.assertEqual(want_previous_square_types, got_previous_square_types)

    def test_play_square_groups_removed_by_square_groups_already_removed(self):
        self.env.state = np.array([
            [
                [1, 0, 0, ],
                [0, 0, 0, ],
                [0, 0, 0, ],
            ],
            [
                [0, 0, 0, ],
                [0, 0, 1, ],
                [0, 0, 0, ],
            ],
        ])
        self.hasher = TicTacToeHasher(env=self.env)

        # Since Player 1 has played at 00, Player 2 cannot win Group 00-22.
        # This should already be reflected at 22.
        self.assertNotIn(TestTicTacToeHasher.GROUP_00_TO_22, self.hasher.groups_by_square_by_player[1][2][2])

        # Make Player 1 play in the center square.
        got_groups_removed_by_square, _ = self.hasher._play_square(player=0, row=1, col=1)

        # Since Group 00-22 was already not winnable before, Square 22 should not be in got_groups_removed_by_square.
        self.assertNotIn(Square(row=2, col=2), got_groups_removed_by_square)

    def test_play_square_previous_square_types_indifferent_squares(self):
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

        # Player 1 plays in the bottom-middle square.
        _, got_previous_square_types = self.hasher._play_square(player=0, row=2, col=1)
        want_previous_square_types = {
            Square(row=0, col=1): SquareType.Player2,  # top-middle
            Square(row=1, col=1): SquareType.Player2,  # center
            Square(row=2, col=0): SquareType.Player2,  # bottom-left
            Square(row=2, col=1): SquareType.Empty,
        }
        self.assertEqual(want_previous_square_types, got_previous_square_types)

    def test_init_with_indifferent_squares(self):
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

        # Validate expected groups at 00. Neither player should be able to win.
        self.assertFalse(self.hasher.groups_by_square_by_player[0][0][0])
        self.assertEqual(SquareType.Indifferent, self.hasher.square_types[0][0])

        # Validate expected groups at 01. Player 2 should be able to win 01-21.
        self.assertIn(TestTicTacToeHasher.GROUP_01_TO_21, self.hasher.groups_by_square_by_player[1][0][1])
        self.assertEqual(SquareType.Player2, self.hasher.square_types[0][1])

    def test_move(self):
        # Since no squares have been played, it is possible for Player 2 to win using Group 00-02.
        self.assertIn(TestTicTacToeHasher.GROUP_00_TO_02, self.hasher.groups_by_square_by_player[1][0][2])
        self.hasher.move(action=0)
        # Since Player 1 has played at 00, it is not possible for Player 2 to win using Group 00-02.
        self.assertNotIn(TestTicTacToeHasher.GROUP_00_TO_02, self.hasher.groups_by_square_by_player[1][0][2])
        # It should now be Player 2's turn.
        self.assertEqual(1, self.hasher.player)

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
        got_transposition_arr = self.hasher._convert_square_types_to_transposition_arr(square_types=self.hasher.square_types)
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
        got_transposition = self.hasher._get_transposition(transposition_arr=transposition_arr)
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
        self.hasher = TicTacToeHasher(self.env)
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
        self.hasher = TicTacToeHasher(self.env)
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
        self.hasher = TicTacToeHasher(self.env)
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
        self.hasher = TicTacToeHasher(self.env)
        transposition_of_flipped = self.hasher.hash()
        self.assertEqual(transposition_of_original, transposition_of_flipped)

    def test_play_move_undo_move_initial_state(self):
        self.hasher.move(action=0)
        self.assertTrue(self.hasher.groups_removed_by_squares_by_move)
        self.assertTrue(self.hasher.previous_square_types_by_move)
        self.hasher.undo_move()
        self.assertFalse(self.hasher.groups_removed_by_squares_by_move)
        self.assertFalse(self.hasher.previous_square_types_by_move)

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
