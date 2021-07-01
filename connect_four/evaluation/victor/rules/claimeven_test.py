import gym
import unittest

import numpy as np

from connect_four.evaluation.victor.rules.claimeven import ClaimevenManager
from connect_four.game import Square
from connect_four.evaluation.victor.board import Board

from connect_four.evaluation.victor.rules import Claimeven
from connect_four.evaluation.victor.rules import find_all_claimevens

from connect_four.envs.connect_four_env import ConnectFourEnv
from connect_four.problem import Group
from connect_four.problem import ConnectFourGroupManager


class TestClaimeven(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 7
        self.env.reset()

    def test_claimeven(self):
        self.env.state = np.array([
            [
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 1, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        got_claimevens = find_all_claimevens(board)

        want_claimevens = {
            Claimeven(Square(0, 0), Square(1, 0)),
            Claimeven(Square(2, 0), Square(3, 0)),
            Claimeven(Square(4, 0), Square(5, 0)),
            Claimeven(Square(0, 1), Square(1, 1)),
            Claimeven(Square(2, 1), Square(3, 1)),
            Claimeven(Square(4, 1), Square(5, 1)),
            Claimeven(Square(0, 2), Square(1, 2)),
            Claimeven(Square(2, 2), Square(3, 2)),
            Claimeven(Square(0, 4), Square(1, 4)),
            Claimeven(Square(2, 4), Square(3, 4)),
            Claimeven(Square(0, 5), Square(1, 5)),
            Claimeven(Square(2, 5), Square(3, 5)),
            Claimeven(Square(4, 5), Square(5, 5)),
            Claimeven(Square(0, 6), Square(1, 6)),
            Claimeven(Square(2, 6), Square(3, 6)),
            Claimeven(Square(4, 6), Square(5, 6)),
        }
        self.assertEqual(want_claimevens, got_claimevens)

    def test_claimeven_manager_initialization(self):
        self.env.state = np.array([
            [
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 1, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        cm = ClaimevenManager(board=board)
        got_claimevens = cm.claimevens

        want_claimevens = {
            Claimeven(Square(0, 0), Square(1, 0)),
            Claimeven(Square(2, 0), Square(3, 0)),
            Claimeven(Square(4, 0), Square(5, 0)),
            Claimeven(Square(0, 1), Square(1, 1)),
            Claimeven(Square(2, 1), Square(3, 1)),
            Claimeven(Square(4, 1), Square(5, 1)),
            Claimeven(Square(0, 2), Square(1, 2)),
            Claimeven(Square(2, 2), Square(3, 2)),
            Claimeven(Square(0, 4), Square(1, 4)),
            Claimeven(Square(2, 4), Square(3, 4)),
            Claimeven(Square(0, 5), Square(1, 5)),
            Claimeven(Square(2, 5), Square(3, 5)),
            Claimeven(Square(4, 5), Square(5, 5)),
            Claimeven(Square(0, 6), Square(1, 6)),
            Claimeven(Square(2, 6), Square(3, 6)),
            Claimeven(Square(4, 6), Square(5, 6)),
        }
        self.assertEqual(want_claimevens, got_claimevens)

    def test_claimeven_manager_move_undo_move(self):
        self.env.state = np.array([
            [
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 1, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        cm = ClaimevenManager(board=board)

        # Move (5, 0).
        claimeven = Claimeven(lower=Square(row=5, col=0), upper=Square(row=4, col=0))
        got_removed_claimeven = cm.move(row=5, col=0)
        self.assertEqual(claimeven, got_removed_claimeven)

        # Move (4, 0).
        got_removed_claimeven = cm.move(row=4, col=0)
        self.assertIsNone(got_removed_claimeven)

        # Undo (4, 0).
        got_added_claimeven = cm.undo_move()
        self.assertIsNone(got_added_claimeven)

        # Undo (5, 0).
        got_added_claimeven = cm.undo_move()
        self.assertEqual(claimeven, got_added_claimeven)

    def test_find_problems_solved(self):
        # This board is from Diagram 5.4 of the original paper.
        self.env.state = np.array([
            [
                [0, 0, 1, 1, 0, 0, 1, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 1, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 1, ],
                [0, 0, 1, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 1, 0, 0, 1, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 1, ],
                [0, 0, 0, 1, 1, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 1, ],
            ],
        ])
        pm = ConnectFourGroupManager(env_variables=self.env.env_variables)

        # We're using the Claimeven with the upper square being e4.
        # In the example from the original paper, this refutes the groups in (4):
        # d3-g6, c2-f5, b1-e4, e3-e6
        claimeven_2_4 = Claimeven(upper=Square(row=2, col=4), lower=Square(row=3, col=4))  # e3, e4

        want_problems_solved = {
            # Groups that belong to White. These were included in the original paper.
            Group(player=0, start=Square(row=3, col=3), end=Square(row=0, col=6)),  # d3-g6
            Group(player=0, start=Square(row=4, col=2), end=Square(row=1, col=5)),  # c2-f5
            Group(player=0, start=Square(row=5, col=1), end=Square(row=2, col=4)),  # b1-e4
            Group(player=0, start=Square(row=3, col=4), end=Square(row=0, col=4)),  # e3-e6
            # Groups that belong to Black.
            Group(player=1, start=Square(row=3, col=4), end=Square(row=0, col=4)),  # e3-e6
            Group(player=1, start=Square(row=4, col=4), end=Square(row=1, col=4)),  # e2-e5
            Group(player=1, start=Square(row=5, col=4), end=Square(row=2, col=4)),  # e1-e4
        }
        got_problems_solved = claimeven_2_4.find_problems_solved(
            groups_by_square_by_player=pm.groups_by_square_by_player,
        )
        self.assertEqual(want_problems_solved, got_problems_solved)


if __name__ == '__main__':
    unittest.main()
