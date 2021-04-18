import gym
import unittest

import numpy as np

from connect_four.evaluation.victor.rules.baseinverse import BaseinverseManager
from connect_four.game import Square
from connect_four.evaluation.victor.board import Board

from connect_four.evaluation.victor.rules import Baseinverse
from connect_four.evaluation.victor.rules import find_all_baseinverses

from connect_four.envs.connect_four_env import ConnectFourEnv
from connect_four.problem import Group
from connect_four.problem import ConnectFourProblemManager


class TestBaseinverse(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 7
        self.env.reset()

    def test_baseinverse(self):
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 1, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        got_baseinverses = find_all_baseinverses(board)

        want_baseinverses = {
            # All matches with Square(5, 0).
            Baseinverse(Square(5, 0), Square(5, 1)),
            Baseinverse(Square(5, 0), Square(2, 2)),
            Baseinverse(Square(5, 0), Square(3, 3)),
            Baseinverse(Square(5, 0), Square(4, 4)),
            Baseinverse(Square(5, 0), Square(5, 5)),
            Baseinverse(Square(5, 0), Square(5, 6)),
            # All matches with Square(5, 1).
            Baseinverse(Square(5, 1), Square(2, 2)),
            Baseinverse(Square(5, 1), Square(3, 3)),
            Baseinverse(Square(5, 1), Square(4, 4)),
            Baseinverse(Square(5, 1), Square(5, 5)),
            Baseinverse(Square(5, 1), Square(5, 6)),
            # All matches with Square(2, 2).
            Baseinverse(Square(2, 2), Square(3, 3)),
            Baseinverse(Square(2, 2), Square(4, 4)),
            Baseinverse(Square(2, 2), Square(5, 5)),
            Baseinverse(Square(2, 2), Square(5, 6)),
            # All matches with Square(3, 3).
            Baseinverse(Square(3, 3), Square(4, 4)),
            Baseinverse(Square(3, 3), Square(5, 5)),
            Baseinverse(Square(3, 3), Square(5, 6)),
            # All matches with Square(4, 4).
            Baseinverse(Square(4, 4), Square(5, 5)),
            Baseinverse(Square(4, 4), Square(5, 6)),
            # All matches with Square(5, 5).
            Baseinverse(Square(5, 5), Square(5, 6)),
        }
        self.assertEqual(want_baseinverses, got_baseinverses)

    def test_baseinverse_manager_initialization(self):
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 1, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        bm = BaseinverseManager(board=board)
        got_baseinverses = bm.baseinverses

        want_baseinverses = {
            # All matches with Square(5, 0).
            Baseinverse(Square(5, 0), Square(5, 1)),
            Baseinverse(Square(5, 0), Square(2, 2)),
            Baseinverse(Square(5, 0), Square(3, 3)),
            Baseinverse(Square(5, 0), Square(4, 4)),
            Baseinverse(Square(5, 0), Square(5, 5)),
            Baseinverse(Square(5, 0), Square(5, 6)),
            # All matches with Square(5, 1).
            Baseinverse(Square(5, 1), Square(2, 2)),
            Baseinverse(Square(5, 1), Square(3, 3)),
            Baseinverse(Square(5, 1), Square(4, 4)),
            Baseinverse(Square(5, 1), Square(5, 5)),
            Baseinverse(Square(5, 1), Square(5, 6)),
            # All matches with Square(2, 2).
            Baseinverse(Square(2, 2), Square(3, 3)),
            Baseinverse(Square(2, 2), Square(4, 4)),
            Baseinverse(Square(2, 2), Square(5, 5)),
            Baseinverse(Square(2, 2), Square(5, 6)),
            # All matches with Square(3, 3).
            Baseinverse(Square(3, 3), Square(4, 4)),
            Baseinverse(Square(3, 3), Square(5, 5)),
            Baseinverse(Square(3, 3), Square(5, 6)),
            # All matches with Square(4, 4).
            Baseinverse(Square(4, 4), Square(5, 5)),
            Baseinverse(Square(4, 4), Square(5, 6)),
            # All matches with Square(5, 5).
            Baseinverse(Square(5, 5), Square(5, 6)),
        }
        self.assertEqual(want_baseinverses, got_baseinverses)

    def test_find_problems_solved(self):
        # This board is from Diagram 6.2 of the original paper.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 1, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
            ],
        ])
        pm = ConnectFourProblemManager(env_variables=self.env.env_variables)

        # The Baseinverse a1-b1 solves a1-d1.
        baseinverse_a1_b1 = Baseinverse(playable1=Square(row=5, col=0), playable2=Square(row=5, col=1))

        want_problems_solved = {
            # Groups that belong to White. These were included in the original paper.
            Group(player=0, start=Square(row=5, col=0), end=Square(row=5, col=3)),  # a1-d1
            # There are no Groups that belong to Black the baseinverse solves.
        }
        got_problems_solved = baseinverse_a1_b1.find_problems_solved(
            groups_by_square_by_player=pm.groups_by_square_by_player,
        )
        self.assertEqual(want_problems_solved, got_problems_solved)

        # As stated in the original paper, the Baseinverse a1-c4 is possible but useless.
        # Thus, it should solve no problems.
        baseinverse_a1_c4 = Baseinverse(playable1=Square(row=5, col=0), playable2=Square(row=2, col=2))
        self.assertFalse(baseinverse_a1_c4.find_problems_solved(
            groups_by_square_by_player=pm.groups_by_square_by_player,
        ))


if __name__ == '__main__':
    unittest.main()
