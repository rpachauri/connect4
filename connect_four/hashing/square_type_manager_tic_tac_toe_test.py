import gym
import unittest

import numpy as np

from connect_four.hashing.data_structures import Group, Square, SquareType
from connect_four.hashing.square_type_manager import SquareTypeManager


class TestSquareTypeManagerTicTacToe(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('tic_tac_toe-v0')

    def test_remove_groups(self):
        stm = SquareTypeManager(env_variables=self.env.env_variables, num_to_connect=3)
        # It should be Player 1's turn.
        self.assertEqual(0, stm.player)

        # In this test case, we're going to remove groups that contain 00 for Player 2.
        group_00_to_02 = Group(squares=frozenset([Square(row=0, col=0), Square(row=0, col=1), Square(row=0, col=2)]))
        group_00_to_22 = Group(squares=frozenset([Square(row=0, col=0), Square(row=1, col=1), Square(row=2, col=2)]))
        group_00_to_20 = Group(squares=frozenset([Square(row=0, col=0), Square(row=1, col=0), Square(row=2, col=0)]))
        want_groups_removed_by_square = {
            Square(row=0, col=0): {group_00_to_02, group_00_to_22, group_00_to_20},
            Square(row=0, col=1): {group_00_to_02},
            Square(row=0, col=2): {group_00_to_02},
            Square(row=1, col=1): {group_00_to_22},
            Square(row=2, col=2): {group_00_to_22},
            Square(row=1, col=0): {group_00_to_20},
            Square(row=2, col=0): {group_00_to_20},
        }

        # Remove groups that contain 00 for Player 2.
        got_groups_removed_by_square = stm._remove_groups(opponent=1, row=0, col=0)
        self.assertEqual(want_groups_removed_by_square, got_groups_removed_by_square)

    def test_find_indifferent_squares(self):
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
        stm = SquareTypeManager(env_variables=self.env.env_variables, num_to_connect=3)

        # Player 1 plays in the bottom-middle square.
        # Remove groups that contain 21 for Player 2.
        groups_removed_by_square = stm._remove_groups(opponent=1, row=2, col=1)

        want_indifferent_squares = {
            Square(row=0, col=1),  # top-middle
            Square(row=1, col=1),  # center
            Square(row=2, col=0),  # bottom-left
            Square(row=2, col=1),  # bottom-middle
        }
        got_indifferent_squares = stm._find_indifferent_squares(
            player=0,
            row=2,
            col=1,
            groups_removed_by_square=groups_removed_by_square,
        )
        self.assertEqual(want_indifferent_squares, got_indifferent_squares)

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
        stm = SquareTypeManager(env_variables=self.env.env_variables, num_to_connect=3)

        # Player 1 plays in the bottom-middle square.
        _, got_previous_square_types = stm._play_square(
            player=0,
            row=2,
            col=1,
        )
        want_previous_square_types = {
            Square(row=0, col=1): SquareType.Player2,  # top-middle
            Square(row=1, col=1): SquareType.Player2,  # center
            Square(row=2, col=0): SquareType.Player2,  # bottom-left
            Square(row=2, col=1): SquareType.Empty,
        }
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
        stm = SquareTypeManager(env_variables=self.env.env_variables, num_to_connect=3)

        group_00_to_22 = Group(squares=frozenset([Square(row=0, col=0), Square(row=1, col=1), Square(row=2, col=2)]))

        # Since Player 1 has played at 00, Player 2 cannot win Group 00-22.
        # This should already be reflected at 22.
        self.assertNotIn(group_00_to_22, stm.groups_by_square_by_player[1][2][2])

        # Player 1 plays in the center square.
        got_groups_removed_by_square, _ = stm._play_square(
            player=0,
            row=1,
            col=1,
        )

        # Since Group 00-22 was already not winnable before, Square 22 should not be in got_groups_removed_by_square.
        self.assertNotIn(Square(row=2, col=2), got_groups_removed_by_square)

    def test_move(self):
        stm = SquareTypeManager(env_variables=self.env.env_variables, num_to_connect=3)
        stm.move(row=0, col=0)
        # Validate that play has switched to the opponent.
        self.assertEqual(1, stm.player)
        # Validate that the stack of moves is of length 1.
        self.assertEqual(1, len(stm.groups_removed_by_squares_by_move))
        self.assertEqual(1, len(stm.previous_square_types_by_move))

    def test_undo_move_raises_assertion_error(self):
        # undo_move() should raise an assertion error if the STM is at the given state.
        stm = SquareTypeManager(env_variables=self.env.env_variables, num_to_connect=3)
        with self.assertRaises(AssertionError):
            stm.undo_move()

    def test_play_move_undo_move_initial_state(self):
        stm = SquareTypeManager(env_variables=self.env.env_variables, num_to_connect=3)

        stm.move(row=0, col=0)
        self.assertEqual(1, stm.player)
        self.assertTrue(stm.groups_removed_by_squares_by_move)
        self.assertTrue(stm.previous_square_types_by_move)

        stm.undo_move()
        self.assertEqual(0, stm.player)
        self.assertFalse(stm.groups_removed_by_squares_by_move)
        self.assertFalse(stm.previous_square_types_by_move)


if __name__ == '__main__':
    unittest.main()
