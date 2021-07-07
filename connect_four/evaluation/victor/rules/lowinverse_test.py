import gym
import unittest

import numpy as np

from connect_four.evaluation.victor.rules.lowinverse import LowinverseManager
from connect_four.game import Square
from connect_four.evaluation.board import Board

from connect_four.evaluation.victor.rules import Vertical
from connect_four.evaluation.victor.rules import find_all_verticals
from connect_four.evaluation.victor.rules import Lowinverse
from connect_four.evaluation.victor.rules import find_all_lowinverses

from connect_four.envs.connect_four_env import ConnectFourEnv
from connect_four.problem import Group
from connect_four.problem import ConnectFourGroupManager


class TestLowinverse(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 7
        self.env.reset()

    def test_lowinverse(self):
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        got_lowinverses = find_all_lowinverses(verticals=find_all_verticals(board))

        # Verticals in the first column.
        vertical_1_0 = Vertical(upper=Square(row=1, col=0), lower=Square(row=2, col=0))
        vertical_3_0 = Vertical(upper=Square(row=3, col=0), lower=Square(row=4, col=0))
        # Verticals in the second column.
        vertical_1_1 = Vertical(upper=Square(row=1, col=1), lower=Square(row=2, col=1))
        vertical_3_1 = Vertical(upper=Square(row=3, col=1), lower=Square(row=4, col=1))
        # Verticals in the third column
        vertical_1_2 = Vertical(upper=Square(row=1, col=2), lower=Square(row=2, col=2))
        vertical_3_2 = Vertical(upper=Square(row=3, col=2), lower=Square(row=4, col=2))
        # Verticals in the fourth column
        vertical_1_3 = Vertical(upper=Square(row=1, col=3), lower=Square(row=2, col=3))
        vertical_3_3 = Vertical(upper=Square(row=3, col=3), lower=Square(row=4, col=3))
        # Verticals in the fifth column
        vertical_1_4 = Vertical(upper=Square(row=1, col=4), lower=Square(row=2, col=4))
        vertical_3_4 = Vertical(upper=Square(row=3, col=4), lower=Square(row=4, col=4))
        # Verticals in the sixth column
        vertical_1_5 = Vertical(upper=Square(row=1, col=5), lower=Square(row=2, col=5))
        vertical_3_5 = Vertical(upper=Square(row=3, col=5), lower=Square(row=4, col=5))
        # Verticals in the seventh column
        vertical_1_6 = Vertical(upper=Square(row=1, col=6), lower=Square(row=2, col=6))
        vertical_3_6 = Vertical(upper=Square(row=3, col=6), lower=Square(row=4, col=6))

        want_lowinverses = {
            # All Lowinverses with vertical_1_0.
            Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_1_1),
            # Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_3_1),
            Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_1_2),
            Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_3_2),
            Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_1_3),
            # Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_3_3),
            # Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_1_4),
            # Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_3_4),
            # Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_1_5),
            # Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_3_5),
            # Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_1_6),
            # Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_3_0.
            # Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_1_1),
            Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_3_1),
            Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_1_2),
            Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_3_2),
            # Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_1_3),
            Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_3_3),
            # Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_1_4),
            # Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_3_4),
            # Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_1_5),
            # Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_3_5),
            # Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_1_6),
            # Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_1_1.
            Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_1_2),
            # Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_3_2),
            Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_1_3),
            Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_3_3),
            Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_1_4),
            # Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_3_4),
            # Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_1_5),
            # Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_3_5),
            # Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_1_6),
            # Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_3_1.
            # Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_1_2),
            Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_3_2),
            Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_1_3),
            Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_3_3),
            # Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_1_4),
            Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_3_4),
            # Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_1_5),
            # Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_3_5),
            # Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_1_6),
            # Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_1_2.
            Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_1_3),
            # Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_3_3),
            Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_1_4),
            Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_3_4),
            Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_1_5),
            # Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_3_5),
            # Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_1_6),
            # Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_3_2.
            # Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_1_3),
            Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_3_3),
            Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_1_4),
            Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_3_4),
            # Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_1_5),
            Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_3_5),
            # Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_1_6),
            # Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_1_3.
            Lowinverse(first_vertical=vertical_1_3, second_vertical=vertical_1_4),
            # Lowinverse(first_vertical=vertical_1_3, second_vertical=vertical_3_4),
            Lowinverse(first_vertical=vertical_1_3, second_vertical=vertical_1_5),
            Lowinverse(first_vertical=vertical_1_3, second_vertical=vertical_3_5),
            Lowinverse(first_vertical=vertical_1_3, second_vertical=vertical_1_6),
            # Lowinverse(first_vertical=vertical_1_3, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_3_3.
            # Lowinverse(first_vertical=vertical_3_3, second_vertical=vertical_1_4),
            Lowinverse(first_vertical=vertical_3_3, second_vertical=vertical_3_4),
            Lowinverse(first_vertical=vertical_3_3, second_vertical=vertical_1_5),
            Lowinverse(first_vertical=vertical_3_3, second_vertical=vertical_3_5),
            # Lowinverse(first_vertical=vertical_3_3, second_vertical=vertical_1_6),
            Lowinverse(first_vertical=vertical_3_3, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_1_4.
            Lowinverse(first_vertical=vertical_1_4, second_vertical=vertical_1_5),
            # Lowinverse(first_vertical=vertical_1_4, second_vertical=vertical_3_5),
            Lowinverse(first_vertical=vertical_1_4, second_vertical=vertical_1_6),
            Lowinverse(first_vertical=vertical_1_4, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_3_4.
            # Lowinverse(first_vertical=vertical_3_4, second_vertical=vertical_1_5),
            Lowinverse(first_vertical=vertical_3_4, second_vertical=vertical_3_5),
            Lowinverse(first_vertical=vertical_3_4, second_vertical=vertical_1_6),
            Lowinverse(first_vertical=vertical_3_4, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_1_5.
            Lowinverse(first_vertical=vertical_1_5, second_vertical=vertical_1_6),
            # Lowinverse(first_vertical=vertical_1_5, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_3_5.
            # Lowinverse(first_vertical=vertical_3_5, second_vertical=vertical_1_6),
            Lowinverse(first_vertical=vertical_3_5, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_1_6.
        }
        self.assertEqual(want_lowinverses, got_lowinverses)

    def test_lowinverse_manager_initialization(self):
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        lm = LowinverseManager(verticals=find_all_verticals(board=board))
        got_lowinverses = lm.lowinverses

        # Verticals in the first column.
        vertical_1_0 = Vertical(upper=Square(row=1, col=0), lower=Square(row=2, col=0))
        vertical_3_0 = Vertical(upper=Square(row=3, col=0), lower=Square(row=4, col=0))
        # Verticals in the second column.
        vertical_1_1 = Vertical(upper=Square(row=1, col=1), lower=Square(row=2, col=1))
        vertical_3_1 = Vertical(upper=Square(row=3, col=1), lower=Square(row=4, col=1))
        # Verticals in the third column
        vertical_1_2 = Vertical(upper=Square(row=1, col=2), lower=Square(row=2, col=2))
        vertical_3_2 = Vertical(upper=Square(row=3, col=2), lower=Square(row=4, col=2))
        # Verticals in the fourth column
        vertical_1_3 = Vertical(upper=Square(row=1, col=3), lower=Square(row=2, col=3))
        vertical_3_3 = Vertical(upper=Square(row=3, col=3), lower=Square(row=4, col=3))
        # Verticals in the fifth column
        vertical_1_4 = Vertical(upper=Square(row=1, col=4), lower=Square(row=2, col=4))
        vertical_3_4 = Vertical(upper=Square(row=3, col=4), lower=Square(row=4, col=4))
        # Verticals in the sixth column
        vertical_1_5 = Vertical(upper=Square(row=1, col=5), lower=Square(row=2, col=5))
        vertical_3_5 = Vertical(upper=Square(row=3, col=5), lower=Square(row=4, col=5))
        # Verticals in the seventh column
        vertical_1_6 = Vertical(upper=Square(row=1, col=6), lower=Square(row=2, col=6))
        vertical_3_6 = Vertical(upper=Square(row=3, col=6), lower=Square(row=4, col=6))

        want_lowinverses = {
            # All Lowinverses with vertical_1_0.
            Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_1_1),
            # Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_3_1),
            Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_1_2),
            Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_3_2),
            Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_1_3),
            # Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_3_3),
            # Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_1_4),
            # Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_3_4),
            # Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_1_5),
            # Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_3_5),
            # Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_1_6),
            # Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_3_0.
            # Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_1_1),
            Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_3_1),
            Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_1_2),
            Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_3_2),
            # Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_1_3),
            Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_3_3),
            # Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_1_4),
            # Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_3_4),
            # Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_1_5),
            # Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_3_5),
            # Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_1_6),
            # Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_1_1.
            Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_1_2),
            # Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_3_2),
            Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_1_3),
            Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_3_3),
            Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_1_4),
            # Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_3_4),
            # Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_1_5),
            # Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_3_5),
            # Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_1_6),
            # Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_3_1.
            # Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_1_2),
            Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_3_2),
            Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_1_3),
            Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_3_3),
            # Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_1_4),
            Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_3_4),
            # Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_1_5),
            # Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_3_5),
            # Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_1_6),
            # Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_1_2.
            Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_1_3),
            # Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_3_3),
            Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_1_4),
            Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_3_4),
            Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_1_5),
            # Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_3_5),
            # Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_1_6),
            # Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_3_2.
            # Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_1_3),
            Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_3_3),
            Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_1_4),
            Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_3_4),
            # Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_1_5),
            Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_3_5),
            # Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_1_6),
            # Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_1_3.
            Lowinverse(first_vertical=vertical_1_3, second_vertical=vertical_1_4),
            # Lowinverse(first_vertical=vertical_1_3, second_vertical=vertical_3_4),
            Lowinverse(first_vertical=vertical_1_3, second_vertical=vertical_1_5),
            Lowinverse(first_vertical=vertical_1_3, second_vertical=vertical_3_5),
            Lowinverse(first_vertical=vertical_1_3, second_vertical=vertical_1_6),
            # Lowinverse(first_vertical=vertical_1_3, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_3_3.
            # Lowinverse(first_vertical=vertical_3_3, second_vertical=vertical_1_4),
            Lowinverse(first_vertical=vertical_3_3, second_vertical=vertical_3_4),
            Lowinverse(first_vertical=vertical_3_3, second_vertical=vertical_1_5),
            Lowinverse(first_vertical=vertical_3_3, second_vertical=vertical_3_5),
            # Lowinverse(first_vertical=vertical_3_3, second_vertical=vertical_1_6),
            Lowinverse(first_vertical=vertical_3_3, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_1_4.
            Lowinverse(first_vertical=vertical_1_4, second_vertical=vertical_1_5),
            # Lowinverse(first_vertical=vertical_1_4, second_vertical=vertical_3_5),
            Lowinverse(first_vertical=vertical_1_4, second_vertical=vertical_1_6),
            Lowinverse(first_vertical=vertical_1_4, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_3_4.
            # Lowinverse(first_vertical=vertical_3_4, second_vertical=vertical_1_5),
            Lowinverse(first_vertical=vertical_3_4, second_vertical=vertical_3_5),
            Lowinverse(first_vertical=vertical_3_4, second_vertical=vertical_1_6),
            Lowinverse(first_vertical=vertical_3_4, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_1_5.
            Lowinverse(first_vertical=vertical_1_5, second_vertical=vertical_1_6),
            # Lowinverse(first_vertical=vertical_1_5, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_3_5.
            # Lowinverse(first_vertical=vertical_3_5, second_vertical=vertical_1_6),
            Lowinverse(first_vertical=vertical_3_5, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_1_6.
        }
        self.assertEqual(want_lowinverses, got_lowinverses)

    def test_find_affected_lowinverses(self):
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)

        # Verticals in the first column.
        vertical_1_0 = Vertical(upper=Square(row=1, col=0), lower=Square(row=2, col=0))
        vertical_3_0 = Vertical(upper=Square(row=3, col=0), lower=Square(row=4, col=0))
        # Verticals in the second column.
        vertical_1_1 = Vertical(upper=Square(row=1, col=1), lower=Square(row=2, col=1))
        vertical_3_1 = Vertical(upper=Square(row=3, col=1), lower=Square(row=4, col=1))
        # Verticals in the third column
        # vertical_1_2 = Vertical(upper=Square(row=1, col=2), lower=Square(row=2, col=2))  Not needed
        vertical_3_2 = Vertical(upper=Square(row=3, col=2), lower=Square(row=4, col=2))
        # Verticals in the fourth column
        vertical_1_3 = Vertical(upper=Square(row=1, col=3), lower=Square(row=2, col=3))
        vertical_3_3 = Vertical(upper=Square(row=3, col=3), lower=Square(row=4, col=3))
        # Verticals in the fifth column
        vertical_1_4 = Vertical(upper=Square(row=1, col=4), lower=Square(row=2, col=4))
        vertical_3_4 = Vertical(upper=Square(row=3, col=4), lower=Square(row=4, col=4))
        # Verticals in the sixth column
        vertical_1_5 = Vertical(upper=Square(row=1, col=5), lower=Square(row=2, col=5))
        vertical_3_5 = Vertical(upper=Square(row=3, col=5), lower=Square(row=4, col=5))
        # Verticals in the seventh column
        vertical_1_6 = Vertical(upper=Square(row=1, col=6), lower=Square(row=2, col=6))
        vertical_3_6 = Vertical(upper=Square(row=3, col=6), lower=Square(row=4, col=6))

        # If White plays at c2, then any Lowinverse that contains Vertical c2-c3 would be affected.

        want_affected_lowinverses = {
            # All Lowinverses with vertical_3_2.
            Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_1_0),
            Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_3_0),
            # Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_1_1),
            Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_3_1),
            # Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_1_3),
            Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_3_3),
            Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_1_4),
            Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_3_4),
            # Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_1_5),
            Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_3_5),
            # Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_1_6),
            # Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_3_6),
        }

        got_affected_lowinverses = LowinverseManager._find_affected_lowinverses(
            vertical=vertical_3_2,
            verticals=find_all_verticals(board=board),
        )
        self.assertEqual(want_affected_lowinverses, got_affected_lowinverses)

    def test_find_problems_solved(self):
        # This board is from Diagram 6.6 of the original paper.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
            ],
        ])
        pm = ConnectFourGroupManager(env_variables=self.env.env_variables)

        # Lowinverse c2-c3-d2-d3 guarantees that Black will get at least one square
        # out of each of three pairs of squares:
        # 1. The squares in the first column (c2-c3).
        # 2. The squares in the other column (d2-d3).
        # 3. The upper two squares (c3-d3).
        lowinverse_c2_c3_d2_d3 = Lowinverse(
            first_vertical=Vertical(upper=Square(row=3, col=2), lower=Square(row=4, col=2)),  # c2-c3
            second_vertical=Vertical(upper=Square(row=3, col=3), lower=Square(row=4, col=3)),  # d2-d3
        )

        want_problems_solved = {
            # White groups.
            # groups which contain both upper squares of the Verticals.
            Group(player=0, start=Square(row=3, col=0), end=Square(row=3, col=3)),  # a3-d3
            Group(player=0, start=Square(row=3, col=1), end=Square(row=3, col=4)),  # b3-e3
            Group(player=0, start=Square(row=3, col=2), end=Square(row=3, col=5)),  # c3-f3
            # groups refuted by Vertical c2-c3.
            Group(player=0, start=Square(row=1, col=2), end=Square(row=4, col=2)),  # c2-c5
            # Note that c1-c4 does not need to be refuted because Black already occupies c1.
            # groups refuted by Vertical d2-d3.
            Group(player=0, start=Square(row=1, col=3), end=Square(row=4, col=3)),  # d2-d5
            Group(player=0, start=Square(row=2, col=3), end=Square(row=5, col=3)),  # d1-d4
            # Black groups.
            # groups which contain both upper squares of the Verticals.
            Group(player=1, start=Square(row=3, col=0), end=Square(row=3, col=3)),  # a3-d3
            Group(player=1, start=Square(row=3, col=1), end=Square(row=3, col=4)),  # b3-e3
            Group(player=1, start=Square(row=3, col=2), end=Square(row=3, col=5)),  # c3-f3
            # groups refuted by Vertical c2-c3.
            Group(player=1, start=Square(row=1, col=2), end=Square(row=4, col=2)),  # c2-c5
            Group(player=1, start=Square(row=2, col=2), end=Square(row=5, col=2)),  # c1-c4
            # groups refuted by Vertical d2-d3.
            Group(player=1, start=Square(row=1, col=3), end=Square(row=4, col=3)),  # d2-d5
            # Note that d1-d4 does not need to be refuted because White already occupies d1.
        }
        got_problems_solved = lowinverse_c2_c3_d2_d3.find_problems_solved(
            groups_by_square_by_player=pm.groups_by_square_by_player,
        )
        self.assertEqual(want_problems_solved, got_problems_solved)

    def test_solves(self):
        # Lowinverse c2-c3-d2-d3 guarantees that Black will get at least one square
        # out of each of three pairs of squares:
        # 1. The squares in the first column (c2-c3).
        # 2. The squares in the other column (d2-d3).
        # 3. The upper two squares (c3-d3).
        lowinverse_c2_c3_d2_d3 = Lowinverse(
            first_vertical=Vertical(upper=Square(row=3, col=2), lower=Square(row=4, col=2)),  # c2-c3
            second_vertical=Vertical(upper=Square(row=3, col=3), lower=Square(row=4, col=3)),  # d2-d3
        )

        # a3-d3 is a Group that contains both upper squares of both Verticals.
        white_group_a3_d3 = Group(player=0, start=Square(row=3, col=0), end=Square(row=3, col=3))  # a3-d3
        self.assertTrue(lowinverse_c2_c3_d2_d3.solves(group=white_group_a3_d3))
        # groups refuted by Vertical c2-c3.
        white_group_c2_c5 = Group(player=0, start=Square(row=1, col=2), end=Square(row=4, col=2))  # c2-c5
        self.assertTrue(lowinverse_c2_c3_d2_d3.solves(group=white_group_c2_c5))
        # groups refuted by Vertical d2-d3.
        white_group_d2_d5 = Group(player=0, start=Square(row=1, col=3), end=Square(row=4, col=3))  # d2-d5
        self.assertTrue(lowinverse_c2_c3_d2_d3.solves(group=white_group_d2_d5))
        # The Lowinverse makes no guarantee about solving groups that contain the two lower squares of both Verticals.
        white_group_a2_d2 = Group(player=0, start=Square(row=4, col=0), end=Square(row=4, col=3))  # a2-d2
        self.assertFalse(lowinverse_c2_c3_d2_d3.solves(group=white_group_a2_d2))

    def test_is_useful(self):
        # Lowinverse c2-c3-d2-d3 guarantees that Black will get at least one square
        # out of each of three pairs of squares:
        # 1. The squares in the first column (c2-c3).
        # 2. The squares in the other column (d2-d3).
        # 3. The upper two squares (c3-d3).

        # Since the two Verticals that make it up already solve #1 and #2, the Lowinverse is only useful if
        # it solves a group that satisfies #3.
        lowinverse_c2_c3_d2_d3 = Lowinverse(
            first_vertical=Vertical(upper=Square(row=3, col=2), lower=Square(row=4, col=2)),  # c2-c3
            second_vertical=Vertical(upper=Square(row=3, col=3), lower=Square(row=4, col=3)),  # d2-d3
        )

        # a3-d3 is a Group that contains both upper squares of both Verticals.
        white_group_a3_d3 = Group(player=0, start=Square(row=3, col=0), end=Square(row=3, col=3))  # a3-d3
        # groups refuted by Vertical c2-c3.
        white_group_c2_c5 = Group(player=0, start=Square(row=1, col=2), end=Square(row=4, col=2))  # c2-c5
        # groups refuted by Vertical d2-d3.
        white_group_d2_d5 = Group(player=0, start=Square(row=1, col=3), end=Square(row=4, col=3))  # d2-d5

        self.assertTrue(lowinverse_c2_c3_d2_d3.is_useful(
            groups={white_group_a3_d3, white_group_c2_c5, white_group_d2_d5},
        ))
        self.assertFalse(lowinverse_c2_c3_d2_d3.is_useful(
            groups={white_group_c2_c5, white_group_d2_d5},
        ))


if __name__ == '__main__':
    unittest.main()
