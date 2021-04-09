import gym
import unittest

from connect_four.game import Square
from connect_four.problem import Group
from connect_four.problem.problem_manager import ProblemManager


class TestProblemManagerTicTacToe(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('tic_tac_toe-v0')

    def test_remove_groups(self):
        pm = ProblemManager(env_variables=self.env.env_variables, num_to_connect=3)
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


if __name__ == '__main__':
    unittest.main()