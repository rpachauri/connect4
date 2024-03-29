import gym
import unittest

import numpy as np

from connect_four.game import Square
from connect_four.problem import Group
from connect_four.problem.tic_tac_toe_group_manager import TicTacToeGroupManager


class TestTicTacToeProblemManager(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('tic_tac_toe-v0')

    def test_remove_groups(self):
        pm = TicTacToeGroupManager(env_variables=self.env.env_variables)
        # It should be Player 1's turn.
        self.assertEqual(0, pm.player)

        # In this test case, we're going to remove groups that contain 00 for Player 2.
        group_00_to_02 = Group(player=1, start=Square(row=0, col=0), end=Square(row=0, col=2))
        group_00_to_22 = Group(player=1, start=Square(row=0, col=0), end=Square(row=2, col=2))
        group_00_to_20 = Group(player=1, start=Square(row=0, col=0), end=Square(row=2, col=0))
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
        got_groups_removed_by_square = pm._remove_groups(opponent=1, row=0, col=0)
        self.assertEqual(want_groups_removed_by_square, got_groups_removed_by_square)

    def test_move_groups_removed_by_square_groups_already_removed(self):
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
        pm = TicTacToeGroupManager(env_variables=self.env.env_variables)

        group_00_to_22 = Group(player=1, start=Square(row=0, col=0), end=Square(row=2, col=2))

        # Since Player 1 has played at 00, Player 2 cannot win Group 00-22.
        # This should already be reflected at 22.
        self.assertNotIn(group_00_to_22, pm.groups_by_square_by_player[1][2][2])

        # Player 1 plays in the center square.
        pm.move(
            player=0,
            row=1,
            col=1,
        )

        # Since Group 00-22 was already not winnable before, Square 22 should not be in got_groups_removed_by_square.
        self.assertNotIn(Square(row=2, col=2), pm.groups_removed_by_squares_by_move[-1])

    def test_move(self):
        pm = TicTacToeGroupManager(env_variables=self.env.env_variables)
        pm.move(player=0, row=0, col=0)
        # Validate that the stack of moves is of length 1.
        self.assertEqual(1, len(pm.groups_removed_by_squares_by_move))

    def test_undo_move_raises_assertion_error(self):
        # undo_move() should raise an assertion error if the PM is at the given state.
        pm = TicTacToeGroupManager(env_variables=self.env.env_variables)
        with self.assertRaises(AssertionError):
            pm.undo_move()

    def test_play_move_undo_move_initial_state(self):
        pm = TicTacToeGroupManager(env_variables=self.env.env_variables)

        pm.move(player=0, row=0, col=0)
        self.assertTrue(pm.groups_removed_by_squares_by_move)

        pm.undo_move()
        self.assertFalse(pm.groups_removed_by_squares_by_move)

        pm2 = TicTacToeGroupManager(env_variables=self.env.env_variables)
        self.assertEqual(pm2.groups_removed_by_squares_by_move, pm.groups_removed_by_squares_by_move)


if __name__ == '__main__':
    unittest.main()
