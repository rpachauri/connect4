import gym
import unittest

import numpy as np

from connect_four.game import Square
from connect_four.evaluation.victor.board import Board
from connect_four.evaluation.victor.rules import Vertical
from connect_four.evaluation.victor.rules import find_all_verticals
from connect_four.envs.connect_four_env import ConnectFourEnv
from connect_four.problem import Group
from connect_four.problem.problem_manager import ProblemManager


class TestVertical(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 7
        self.env.reset()

    def test_vertical(self):
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 0, 1, 0, 1, 0, 0, ],
                [0, 0, 1, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        got_verticals = find_all_verticals(board)

        want_verticals = {
            # First column.
            Vertical(Square(1, 0), Square(2, 0)),
            Vertical(Square(3, 0), Square(4, 0)),
            # Second column.
            Vertical(Square(1, 1), Square(2, 1)),
            Vertical(Square(3, 1), Square(4, 1)),
            # Fourth column.
            Vertical(Square(1, 3), Square(2, 3)),
            # Fifth column.
            Vertical(Square(1, 4), Square(2, 4)),
            # Sixth column.
            Vertical(Square(1, 5), Square(2, 5)),
            Vertical(Square(3, 5), Square(4, 5)),
            # Seventh column.
            Vertical(Square(1, 6), Square(2, 6)),
            Vertical(Square(3, 6), Square(4, 6)),
        }
        self.assertEqual(want_verticals, got_verticals)

    def test_find_problems_solved(self):
        # This board is from Diagram 6.3 of the original paper.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 0, 1, 0, 1, 0, 0, ],
                [0, 0, 1, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
            ],
        ])
        pm = ProblemManager(env_variables=self.env.env_variables, num_to_connect=4)

        # The Vertical e4-e5 solves e2-e5 and e3-e6.
        vertical_e4_e5 = Vertical(upper=Square(row=2, col=4), lower=Square(row=1, col=4))

        want_problems_solved = {
            # Groups that belong to White. These were included in the original paper.
            Group(player=0, start=Square(row=4, col=4), end=Square(row=1, col=4)),  # e2-e5
            Group(player=0, start=Square(row=3, col=4), end=Square(row=0, col=4)),  # e3-e6
            # There are no Groups that belong to Black this vertical solves.
        }
        got_problems_solved = vertical_e4_e5.find_problems_solved(
            groups_by_square_by_player=pm.groups_by_square_by_player,
        )
        self.assertEqual(want_problems_solved, got_problems_solved)


if __name__ == '__main__':
    unittest.main()
