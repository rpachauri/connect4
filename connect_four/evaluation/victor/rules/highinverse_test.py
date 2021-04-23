import gym
import unittest

import numpy as np

from connect_four.evaluation.victor.rules.highinverse import HighinverseManager
from connect_four.evaluation.victor.rules.vertical import VerticalManager
from connect_four.game import Square
from connect_four.evaluation.victor.board import Board

from connect_four.evaluation.victor.rules import Vertical
from connect_four.evaluation.victor.rules import find_all_verticals
from connect_four.evaluation.victor.rules import Lowinverse
from connect_four.evaluation.victor.rules import find_all_lowinverses
from connect_four.evaluation.victor.rules import Highinverse
from connect_four.evaluation.victor.rules import find_all_highinverses

from connect_four.envs.connect_four_env import ConnectFourEnv
from connect_four.problem import Group
from connect_four.problem import ConnectFourProblemManager


class TestHighinverse(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 7
        self.env.reset()

    def test_highinverse(self):
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
        got_highinverses = find_all_highinverses(
            board=board,
            lowinverses=find_all_lowinverses(
                verticals=find_all_verticals(board=board),
            ),
        )

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

        want_highinverses = {
            # All Lowinverses with vertical_1_0.
            Highinverse(Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_1_1)),
            Highinverse(Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_3_1)),
            Highinverse(Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_1_2)),
            Highinverse(Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_3_2),
                        directly_playable_squares=[Square(row=4, col=2)]),
            Highinverse(Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_1_3)),
            Highinverse(Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_3_3),
                        directly_playable_squares=[Square(row=4, col=3)]),
            Highinverse(Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_1_4)),
            Highinverse(Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_3_4)),
            Highinverse(Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_1_5)),
            Highinverse(Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_3_5)),
            Highinverse(Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_1_6)),
            Highinverse(Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_3_6)),
            # All Lowinverses with vertical_3_0.
            Highinverse(Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_1_1)),
            Highinverse(Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_3_1)),
            Highinverse(Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_1_2)),
            Highinverse(Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_3_2),
                        directly_playable_squares=[Square(row=4, col=2)]),
            Highinverse(Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_1_3)),
            Highinverse(Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_3_3),
                        directly_playable_squares=[Square(row=4, col=3)]),
            Highinverse(Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_1_4)),
            Highinverse(Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_3_4)),
            Highinverse(Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_1_5)),
            Highinverse(Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_3_5)),
            Highinverse(Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_1_6)),
            Highinverse(Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_3_6)),
            # All Lowinverses with vertical_1_1.
            Highinverse(Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_1_2)),
            Highinverse(Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_3_2),
                        directly_playable_squares=[Square(row=4, col=2)]),
            Highinverse(Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_1_3)),
            Highinverse(Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_3_3),
                        directly_playable_squares=[Square(row=4, col=3)]),
            Highinverse(Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_1_4)),
            Highinverse(Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_3_4)),
            Highinverse(Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_1_5)),
            Highinverse(Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_3_5)),
            Highinverse(Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_1_6)),
            Highinverse(Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_3_6)),
            # All Lowinverses with vertical_3_1.
            Highinverse(Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_1_2)),
            Highinverse(Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_3_2),
                        directly_playable_squares=[Square(row=4, col=2)]),
            Highinverse(Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_1_3)),
            Highinverse(Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_3_3),
                        directly_playable_squares=[Square(row=4, col=3)]),
            Highinverse(Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_1_4)),
            Highinverse(Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_3_4)),
            Highinverse(Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_1_5)),
            Highinverse(Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_3_5)),
            Highinverse(Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_1_6)),
            Highinverse(Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_3_6)),
            # All Lowinverses with vertical_1_2.
            Highinverse(Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_1_3)),
            Highinverse(Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_3_3),
                        directly_playable_squares=[Square(row=4, col=3)]),
            Highinverse(Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_1_4)),
            Highinverse(Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_3_4)),
            Highinverse(Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_1_5)),
            Highinverse(Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_3_5)),
            Highinverse(Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_1_6)),
            Highinverse(Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_3_6)),
            # All Lowinverses with vertical_3_2.
            Highinverse(Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_1_3),
                        directly_playable_squares=[Square(row=4, col=2)]),
            Highinverse(Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_3_3),
                        directly_playable_squares=[Square(row=4, col=2), Square(row=4, col=3)]),
            Highinverse(Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_1_4),
                        directly_playable_squares=[Square(row=4, col=2)]),
            Highinverse(Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_3_4),
                        directly_playable_squares=[Square(row=4, col=2)]),
            Highinverse(Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_1_5),
                        directly_playable_squares=[Square(row=4, col=2)]),
            Highinverse(Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_3_5),
                        directly_playable_squares=[Square(row=4, col=2)]),
            Highinverse(Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_1_6),
                        directly_playable_squares=[Square(row=4, col=2)]),
            Highinverse(Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_3_6),
                        directly_playable_squares=[Square(row=4, col=2)]),
            # All Lowinverses with vertical_1_3.
            Highinverse(Lowinverse(first_vertical=vertical_1_3, second_vertical=vertical_1_4)),
            Highinverse(Lowinverse(first_vertical=vertical_1_3, second_vertical=vertical_3_4)),
            Highinverse(Lowinverse(first_vertical=vertical_1_3, second_vertical=vertical_1_5)),
            Highinverse(Lowinverse(first_vertical=vertical_1_3, second_vertical=vertical_3_5)),
            Highinverse(Lowinverse(first_vertical=vertical_1_3, second_vertical=vertical_1_6)),
            Highinverse(Lowinverse(first_vertical=vertical_1_3, second_vertical=vertical_3_6)),
            # All Lowinverses with vertical_3_3.
            Highinverse(Lowinverse(first_vertical=vertical_3_3, second_vertical=vertical_1_4),
                        directly_playable_squares=[Square(row=4, col=3)]),
            Highinverse(Lowinverse(first_vertical=vertical_3_3, second_vertical=vertical_3_4),
                        directly_playable_squares=[Square(row=4, col=3)]),
            Highinverse(Lowinverse(first_vertical=vertical_3_3, second_vertical=vertical_1_5),
                        directly_playable_squares=[Square(row=4, col=3)]),
            Highinverse(Lowinverse(first_vertical=vertical_3_3, second_vertical=vertical_3_5),
                        directly_playable_squares=[Square(row=4, col=3)]),
            Highinverse(Lowinverse(first_vertical=vertical_3_3, second_vertical=vertical_1_6),
                        directly_playable_squares=[Square(row=4, col=3)]),
            Highinverse(Lowinverse(first_vertical=vertical_3_3, second_vertical=vertical_3_6),
                        directly_playable_squares=[Square(row=4, col=3)]),
            # All Lowinverses with vertical_1_4.
            Highinverse(Lowinverse(first_vertical=vertical_1_4, second_vertical=vertical_1_5)),
            Highinverse(Lowinverse(first_vertical=vertical_1_4, second_vertical=vertical_3_5)),
            Highinverse(Lowinverse(first_vertical=vertical_1_4, second_vertical=vertical_1_6)),
            Highinverse(Lowinverse(first_vertical=vertical_1_4, second_vertical=vertical_3_6)),
            # All Lowinverses with vertical_3_4.
            Highinverse(Lowinverse(first_vertical=vertical_3_4, second_vertical=vertical_1_5)),
            Highinverse(Lowinverse(first_vertical=vertical_3_4, second_vertical=vertical_3_5)),
            Highinverse(Lowinverse(first_vertical=vertical_3_4, second_vertical=vertical_1_6)),
            Highinverse(Lowinverse(first_vertical=vertical_3_4, second_vertical=vertical_3_6)),
            # All Lowinverses with vertical_1_5.
            Highinverse(Lowinverse(first_vertical=vertical_1_5, second_vertical=vertical_1_6)),
            Highinverse(Lowinverse(first_vertical=vertical_1_5, second_vertical=vertical_3_6)),
            # All Lowinverses with vertical_3_5.
            Highinverse(Lowinverse(first_vertical=vertical_3_5, second_vertical=vertical_1_6)),
            Highinverse(Lowinverse(first_vertical=vertical_3_5, second_vertical=vertical_3_6)),
            # All Lowinverses with vertical_1_6.
        }
        self.assertEqual(want_highinverses, got_highinverses)

    def test_highinverse_manager_initialization(self):
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
        hm = HighinverseManager(
            board=board,
            lowinverses=find_all_lowinverses(verticals=find_all_verticals(board=board)),
        )
        got_highinverses = hm.highinverses

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

        want_highinverses = {
            # All Lowinverses with vertical_1_0.
            Highinverse(Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_1_1)),
            Highinverse(Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_3_1)),
            Highinverse(Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_1_2)),
            Highinverse(Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_3_2),
                        directly_playable_squares=[Square(row=4, col=2)]),
            Highinverse(Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_1_3)),
            Highinverse(Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_3_3),
                        directly_playable_squares=[Square(row=4, col=3)]),
            Highinverse(Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_1_4)),
            Highinverse(Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_3_4)),
            Highinverse(Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_1_5)),
            Highinverse(Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_3_5)),
            Highinverse(Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_1_6)),
            Highinverse(Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_3_6)),
            # All Lowinverses with vertical_3_0.
            Highinverse(Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_1_1)),
            Highinverse(Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_3_1)),
            Highinverse(Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_1_2)),
            Highinverse(Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_3_2),
                        directly_playable_squares=[Square(row=4, col=2)]),
            Highinverse(Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_1_3)),
            Highinverse(Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_3_3),
                        directly_playable_squares=[Square(row=4, col=3)]),
            Highinverse(Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_1_4)),
            Highinverse(Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_3_4)),
            Highinverse(Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_1_5)),
            Highinverse(Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_3_5)),
            Highinverse(Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_1_6)),
            Highinverse(Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_3_6)),
            # All Lowinverses with vertical_1_1.
            Highinverse(Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_1_2)),
            Highinverse(Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_3_2),
                        directly_playable_squares=[Square(row=4, col=2)]),
            Highinverse(Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_1_3)),
            Highinverse(Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_3_3),
                        directly_playable_squares=[Square(row=4, col=3)]),
            Highinverse(Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_1_4)),
            Highinverse(Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_3_4)),
            Highinverse(Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_1_5)),
            Highinverse(Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_3_5)),
            Highinverse(Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_1_6)),
            Highinverse(Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_3_6)),
            # All Lowinverses with vertical_3_1.
            Highinverse(Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_1_2)),
            Highinverse(Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_3_2),
                        directly_playable_squares=[Square(row=4, col=2)]),
            Highinverse(Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_1_3)),
            Highinverse(Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_3_3),
                        directly_playable_squares=[Square(row=4, col=3)]),
            Highinverse(Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_1_4)),
            Highinverse(Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_3_4)),
            Highinverse(Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_1_5)),
            Highinverse(Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_3_5)),
            Highinverse(Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_1_6)),
            Highinverse(Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_3_6)),
            # All Lowinverses with vertical_1_2.
            Highinverse(Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_1_3)),
            Highinverse(Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_3_3),
                        directly_playable_squares=[Square(row=4, col=3)]),
            Highinverse(Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_1_4)),
            Highinverse(Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_3_4)),
            Highinverse(Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_1_5)),
            Highinverse(Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_3_5)),
            Highinverse(Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_1_6)),
            Highinverse(Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_3_6)),
            # All Lowinverses with vertical_3_2.
            Highinverse(Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_1_3),
                        directly_playable_squares=[Square(row=4, col=2)]),
            Highinverse(Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_3_3),
                        directly_playable_squares=[Square(row=4, col=2), Square(row=4, col=3)]),
            Highinverse(Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_1_4),
                        directly_playable_squares=[Square(row=4, col=2)]),
            Highinverse(Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_3_4),
                        directly_playable_squares=[Square(row=4, col=2)]),
            Highinverse(Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_1_5),
                        directly_playable_squares=[Square(row=4, col=2)]),
            Highinverse(Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_3_5),
                        directly_playable_squares=[Square(row=4, col=2)]),
            Highinverse(Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_1_6),
                        directly_playable_squares=[Square(row=4, col=2)]),
            Highinverse(Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_3_6),
                        directly_playable_squares=[Square(row=4, col=2)]),
            # All Lowinverses with vertical_1_3.
            Highinverse(Lowinverse(first_vertical=vertical_1_3, second_vertical=vertical_1_4)),
            Highinverse(Lowinverse(first_vertical=vertical_1_3, second_vertical=vertical_3_4)),
            Highinverse(Lowinverse(first_vertical=vertical_1_3, second_vertical=vertical_1_5)),
            Highinverse(Lowinverse(first_vertical=vertical_1_3, second_vertical=vertical_3_5)),
            Highinverse(Lowinverse(first_vertical=vertical_1_3, second_vertical=vertical_1_6)),
            Highinverse(Lowinverse(first_vertical=vertical_1_3, second_vertical=vertical_3_6)),
            # All Lowinverses with vertical_3_3.
            Highinverse(Lowinverse(first_vertical=vertical_3_3, second_vertical=vertical_1_4),
                        directly_playable_squares=[Square(row=4, col=3)]),
            Highinverse(Lowinverse(first_vertical=vertical_3_3, second_vertical=vertical_3_4),
                        directly_playable_squares=[Square(row=4, col=3)]),
            Highinverse(Lowinverse(first_vertical=vertical_3_3, second_vertical=vertical_1_5),
                        directly_playable_squares=[Square(row=4, col=3)]),
            Highinverse(Lowinverse(first_vertical=vertical_3_3, second_vertical=vertical_3_5),
                        directly_playable_squares=[Square(row=4, col=3)]),
            Highinverse(Lowinverse(first_vertical=vertical_3_3, second_vertical=vertical_1_6),
                        directly_playable_squares=[Square(row=4, col=3)]),
            Highinverse(Lowinverse(first_vertical=vertical_3_3, second_vertical=vertical_3_6),
                        directly_playable_squares=[Square(row=4, col=3)]),
            # All Lowinverses with vertical_1_4.
            Highinverse(Lowinverse(first_vertical=vertical_1_4, second_vertical=vertical_1_5)),
            Highinverse(Lowinverse(first_vertical=vertical_1_4, second_vertical=vertical_3_5)),
            Highinverse(Lowinverse(first_vertical=vertical_1_4, second_vertical=vertical_1_6)),
            Highinverse(Lowinverse(first_vertical=vertical_1_4, second_vertical=vertical_3_6)),
            # All Lowinverses with vertical_3_4.
            Highinverse(Lowinverse(first_vertical=vertical_3_4, second_vertical=vertical_1_5)),
            Highinverse(Lowinverse(first_vertical=vertical_3_4, second_vertical=vertical_3_5)),
            Highinverse(Lowinverse(first_vertical=vertical_3_4, second_vertical=vertical_1_6)),
            Highinverse(Lowinverse(first_vertical=vertical_3_4, second_vertical=vertical_3_6)),
            # All Lowinverses with vertical_1_5.
            Highinverse(Lowinverse(first_vertical=vertical_1_5, second_vertical=vertical_1_6)),
            Highinverse(Lowinverse(first_vertical=vertical_1_5, second_vertical=vertical_3_6)),
            # All Lowinverses with vertical_3_5.
            Highinverse(Lowinverse(first_vertical=vertical_3_5, second_vertical=vertical_1_6)),
            Highinverse(Lowinverse(first_vertical=vertical_3_5, second_vertical=vertical_3_6)),
            # All Lowinverses with vertical_1_6.
        }
        self.assertEqual(want_highinverses, got_highinverses)

    def test_find_problems_solved_for_player(self):
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
        pm = ConnectFourProblemManager(env_variables=self.env.env_variables)

        # Lowinverse c2-c3-d2-d3 guarantees that Black will get at least one square
        # out of each of three pairs of squares:
        # 1. The squares in the first column (c2-c3).
        # 2. The squares in the other column (d2-d3).
        # 3. The upper two squares (c3-d3).
        lowinverse_c2_c3_d2_d3 = Lowinverse(
            first_vertical=Vertical(upper=Square(row=3, col=2), lower=Square(row=4, col=2)),  # c2-c3
            second_vertical=Vertical(upper=Square(row=3, col=3), lower=Square(row=4, col=3)),  # d2-d3
        )
        # Highinverse c2-c3-c4-d2-d3-d4 guarantees that Black will get at least one square
        # out of each of four pairs of squares:
        # 1. The upper two squares in the first column (c3-c4).
        # 2. The upper two squares in the second column (d3-d4).
        # 3. The middle squares from both columns (c3-d3).
        # 4. The upper squares from both columns (c4-d4).
        highinverse_c2_c3_c4_d2_d3_d4 = Highinverse(
            lowinverse=lowinverse_c2_c3_d2_d3,
            directly_playable_squares=[Square(row=4, col=2), Square(row=4, col=3)],  # c2 and d2
        )
        want_problems_solved_for_player_0 = {
            # White problems.
            # groups which contain the upper squares of both columns.
            Group(player=0, start=Square(row=2, col=0), end=Square(row=2, col=3)),  # a4-d4
            Group(player=0, start=Square(row=2, col=1), end=Square(row=2, col=4)),  # b4-e4
            Group(player=0, start=Square(row=2, col=2), end=Square(row=2, col=5)),  # c4-f4
            # groups which contain the middle squares of both columns.
            Group(player=0, start=Square(row=3, col=0), end=Square(row=3, col=3)),  # a3-d3
            Group(player=0, start=Square(row=3, col=1), end=Square(row=3, col=4)),  # b3-e3
            Group(player=0, start=Square(row=3, col=2), end=Square(row=3, col=5)),  # c3-f3
            # groups refuted by Vertical c3-c4.
            Group(player=0, start=Square(row=0, col=2), end=Square(row=3, col=2)),  # c3-c6
            Group(player=0, start=Square(row=1, col=2), end=Square(row=4, col=2)),  # c2-c5
            # Note that c1-c4 does not need to be refuted because Black already occupies c1.
            # groups refuted by Vertical d3-d4.
            Group(player=0, start=Square(row=0, col=3), end=Square(row=3, col=3)),  # d3-d6
            Group(player=0, start=Square(row=1, col=3), end=Square(row=4, col=3)),  # d2-d5
            Group(player=0, start=Square(row=2, col=3), end=Square(row=5, col=3)),  # d1-d4
        }
        got_problems_solved_for_player_0 = highinverse_c2_c3_c4_d2_d3_d4.find_problems_solved_for_player(
            groups_by_square=pm.groups_by_square_by_player[0],
        )
        self.assertEqual(want_problems_solved_for_player_0, got_problems_solved_for_player_0)

    def test_diagram_7_2(self):
        # This test case is based on Diagram 7.2 of the original paper.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 1, 1, ],
                [0, 0, 1, 1, 0, 1, 0, ],
                [0, 0, 0, 0, 1, 1, 1, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 1, 1, 1, 0, 0, 1, ],
                [0, 0, 0, 1, 1, 1, 0, ],
            ],
            [
                [0, 0, 1, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 1, ],
                [0, 0, 1, 1, 0, 0, 0, ],
                [0, 1, 1, 1, 0, 1, 1, ],
                [0, 0, 0, 0, 1, 1, 0, ],
                [0, 1, 1, 0, 0, 0, 1, ],
            ],
        ])
        board = Board(self.env.env_variables)

        # Create Verticals for Lowinverses.
        vertical_a4_a5 = Vertical(
            upper=Square(row=1, col=0),  # a5
            lower=Square(row=2, col=0),  # a4
        )
        vertical_a2_a3 = Vertical(
            upper=Square(row=3, col=0),  # a3
            lower=Square(row=4, col=0),  # a2
        )
        vertical_b4_b5 = Vertical(
            upper=Square(row=1, col=1),  # b5
            lower=Square(row=2, col=1),  # b4
        )
        # Create Lowinverses for Highinverses.
        lowinverse_a4_a5_b4_b5 = Lowinverse(
            first_vertical=vertical_a4_a5,
            second_vertical=vertical_b4_b5,
        )
        lowinverse_a2_a3_b4_b5 = Lowinverse(
            first_vertical=vertical_a2_a3,
            second_vertical=vertical_b4_b5,
        )

        want_highinverses = {
            Highinverse(
                lowinverse=lowinverse_a4_a5_b4_b5,
                directly_playable_squares=[Square(row=2, col=1)],  # b4
            ),
            Highinverse(
                lowinverse=lowinverse_a2_a3_b4_b5,
                directly_playable_squares=[Square(row=2, col=1)],  # b4
            ),
        }
        got_highinverses = find_all_highinverses(
            board=board,
            lowinverses=find_all_lowinverses(
                verticals=find_all_verticals(board=board),
            ),
        )
        self.assertEqual(want_highinverses, got_highinverses)

    def test_diagram_7_2_highinverse_manager_initialization(self):
        # This test case is based on Diagram 7.2 of the original paper.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 1, 1, ],
                [0, 0, 1, 1, 0, 1, 0, ],
                [0, 0, 0, 0, 1, 1, 1, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 1, 1, 1, 0, 0, 1, ],
                [0, 0, 0, 1, 1, 1, 0, ],
            ],
            [
                [0, 0, 1, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 1, ],
                [0, 0, 1, 1, 0, 0, 0, ],
                [0, 1, 1, 1, 0, 1, 1, ],
                [0, 0, 0, 0, 1, 1, 0, ],
                [0, 1, 1, 0, 0, 0, 1, ],
            ],
        ])
        board = Board(self.env.env_variables)
        hm = HighinverseManager(
            board=board,
            lowinverses=find_all_lowinverses(verticals=find_all_verticals(board=board)),
        )
        got_highinverses = hm.highinverses

        # Create Verticals for Lowinverses.
        vertical_a4_a5 = Vertical(
            upper=Square(row=1, col=0),  # a5
            lower=Square(row=2, col=0),  # a4
        )
        vertical_a2_a3 = Vertical(
            upper=Square(row=3, col=0),  # a3
            lower=Square(row=4, col=0),  # a2
        )
        vertical_b4_b5 = Vertical(
            upper=Square(row=1, col=1),  # b5
            lower=Square(row=2, col=1),  # b4
        )
        # Create Lowinverses for Highinverses.
        lowinverse_a4_a5_b4_b5 = Lowinverse(
            first_vertical=vertical_a4_a5,
            second_vertical=vertical_b4_b5,
        )
        lowinverse_a2_a3_b4_b5 = Lowinverse(
            first_vertical=vertical_a2_a3,
            second_vertical=vertical_b4_b5,
        )

        want_highinverses = {
            Highinverse(
                lowinverse=lowinverse_a4_a5_b4_b5,
                directly_playable_squares=[Square(row=2, col=1)],  # b4
            ),
            Highinverse(
                lowinverse=lowinverse_a2_a3_b4_b5,
                directly_playable_squares=[Square(row=2, col=1)],  # b4
            ),
        }
        self.assertEqual(want_highinverses, got_highinverses)

    def test_highinverse_given_lowinverses(self):
        # This test case is based on Diagram 7.2 of the original paper.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 1, 1, ],
                [0, 0, 1, 1, 0, 1, 0, ],
                [0, 0, 0, 0, 1, 1, 1, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 1, 1, 1, 0, 0, 1, ],
                [0, 0, 0, 1, 1, 1, 0, ],
            ],
            [
                [0, 0, 1, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 1, ],
                [0, 0, 1, 1, 0, 0, 0, ],
                [0, 1, 1, 1, 0, 1, 1, ],
                [0, 0, 0, 0, 1, 1, 0, ],
                [0, 1, 1, 0, 0, 0, 1, ],
            ],
        ])
        board = Board(self.env.env_variables)

        # Create Verticals for Lowinverses.
        vertical_a2_a3 = Vertical(
            upper=Square(row=3, col=0),  # a3
            lower=Square(row=4, col=0),  # a2
        )
        vertical_b4_b5 = Vertical(
            upper=Square(row=1, col=1),  # b5
            lower=Square(row=2, col=1),  # b4
        )
        # Create Lowinverses for Highinverses.
        lowinverse_a2_a3_b4_b5 = Lowinverse(
            first_vertical=vertical_a2_a3,
            second_vertical=vertical_b4_b5,
        )
        want_highinverses = {
            Highinverse(
                lowinverse=lowinverse_a2_a3_b4_b5,
                directly_playable_squares=[Square(row=2, col=1)],  # b4
            ),
        }

        got_highinverses = HighinverseManager._highinverse_given_lowinverses(
            lowinverses={lowinverse_a2_a3_b4_b5},
            directly_playable_squares=board.playable_squares(),
        )
        self.assertEqual(want_highinverses, got_highinverses)

    def test_directly_playable_highinverse_changes(self):
        # This test case is based on Diagram 7.2 of the original paper.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 1, 1, ],
                [0, 0, 1, 1, 0, 1, 0, ],
                [0, 0, 0, 0, 1, 1, 1, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 1, 1, 1, 0, 0, 1, ],
                [0, 0, 0, 1, 1, 1, 0, ],
            ],
            [
                [0, 0, 1, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 1, ],
                [0, 0, 1, 1, 0, 0, 0, ],
                [0, 1, 1, 1, 0, 1, 1, ],
                [0, 0, 0, 0, 1, 1, 0, ],
                [0, 1, 1, 0, 0, 0, 1, ],
            ],
        ])
        board = Board(self.env.env_variables)
        # If a1 is played, then Vertical a2-a3 becomes directly playable.
        # Thus, only Highinverses containing the Vertical a2-a3 should be affected.

        # Create Verticals for Lowinverses.
        vertical_a2_a3 = Vertical(
            upper=Square(row=3, col=0),  # a3
            lower=Square(row=4, col=0),  # a2
        )
        vertical_b4_b5 = Vertical(
            upper=Square(row=1, col=1),  # b5
            lower=Square(row=2, col=1),  # b4
        )
        # Create Lowinverses for Highinverses.
        lowinverse_a2_a3_b4_b5 = Lowinverse(
            first_vertical=vertical_a2_a3,
            second_vertical=vertical_b4_b5,
        )

        want_removed_highinverses = {
            Highinverse(
                lowinverse=lowinverse_a2_a3_b4_b5,
                directly_playable_squares={
                    Square(row=2, col=1),  # b4
                },
            ),
        }
        want_added_highinverses = {
            Highinverse(
                lowinverse=lowinverse_a2_a3_b4_b5,
                directly_playable_squares={
                    Square(row=4, col=0),  # a2
                    Square(row=2, col=1),  # b4
                },
            ),
        }

        # If a1 is played, then vertical_a2_a3 becomes directly playable.
        got_removed_highinverses, got_added_highinverses = HighinverseManager._directly_playable_highinverse_changes(
            vertical=vertical_a2_a3,
            verticals=VerticalManager(board=board).verticals,
            directly_playable_squares=board.playable_squares(),
        )
        self.assertEqual(want_removed_highinverses, got_removed_highinverses)
        self.assertEqual(want_added_highinverses, got_added_highinverses)


if __name__ == '__main__':
    unittest.main()
