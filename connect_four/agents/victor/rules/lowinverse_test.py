import gym
import unittest

import numpy as np


from connect_four.agents.victor.game import Board
from connect_four.agents.victor.game import Square

from connect_four.agents.victor.rules import Vertical
from connect_four.agents.victor.rules import find_all_verticals
from connect_four.agents.victor.rules import Lowinverse
from connect_four.agents.victor.rules import find_all_lowinverses

from connect_four.envs.connect_four_env import ConnectFourEnv


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
            # TODO a Lowinverse with both verticals in the same column doesn't make sense.
            Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_3_0),
            Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_1_1),
            Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_3_1),
            Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_1_2),
            Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_3_2),
            Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_1_3),
            Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_3_3),
            Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_1_4),
            Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_3_4),
            Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_1_5),
            Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_3_5),
            Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_1_6),
            Lowinverse(first_vertical=vertical_1_0, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_3_0.
            Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_1_1),
            Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_3_1),
            Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_1_2),
            Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_3_2),
            Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_1_3),
            Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_3_3),
            Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_1_4),
            Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_3_4),
            Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_1_5),
            Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_3_5),
            Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_1_6),
            Lowinverse(first_vertical=vertical_3_0, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_1_1.
            Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_3_1),
            Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_1_2),
            Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_3_2),
            Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_1_3),
            Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_3_3),
            Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_1_4),
            Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_3_4),
            Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_1_5),
            Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_3_5),
            Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_1_6),
            Lowinverse(first_vertical=vertical_1_1, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_3_1.
            Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_1_2),
            Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_3_2),
            Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_1_3),
            Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_3_3),
            Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_1_4),
            Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_3_4),
            Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_1_5),
            Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_3_5),
            Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_1_6),
            Lowinverse(first_vertical=vertical_3_1, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_1_2.
            Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_3_2),
            Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_1_3),
            Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_3_3),
            Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_1_4),
            Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_3_4),
            Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_1_5),
            Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_3_5),
            Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_1_6),
            Lowinverse(first_vertical=vertical_1_2, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_3_2.
            Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_1_3),
            Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_3_3),
            Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_1_4),
            Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_3_4),
            Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_1_5),
            Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_3_5),
            Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_1_6),
            Lowinverse(first_vertical=vertical_3_2, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_1_3.
            Lowinverse(first_vertical=vertical_1_3, second_vertical=vertical_3_3),
            Lowinverse(first_vertical=vertical_1_3, second_vertical=vertical_1_4),
            Lowinverse(first_vertical=vertical_1_3, second_vertical=vertical_3_4),
            Lowinverse(first_vertical=vertical_1_3, second_vertical=vertical_1_5),
            Lowinverse(first_vertical=vertical_1_3, second_vertical=vertical_3_5),
            Lowinverse(first_vertical=vertical_1_3, second_vertical=vertical_1_6),
            Lowinverse(first_vertical=vertical_1_3, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_3_3.
            Lowinverse(first_vertical=vertical_3_3, second_vertical=vertical_1_4),
            Lowinverse(first_vertical=vertical_3_3, second_vertical=vertical_3_4),
            Lowinverse(first_vertical=vertical_3_3, second_vertical=vertical_1_5),
            Lowinverse(first_vertical=vertical_3_3, second_vertical=vertical_3_5),
            Lowinverse(first_vertical=vertical_3_3, second_vertical=vertical_1_6),
            Lowinverse(first_vertical=vertical_3_3, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_1_4.
            Lowinverse(first_vertical=vertical_1_4, second_vertical=vertical_3_4),
            Lowinverse(first_vertical=vertical_1_4, second_vertical=vertical_1_5),
            Lowinverse(first_vertical=vertical_1_4, second_vertical=vertical_3_5),
            Lowinverse(first_vertical=vertical_1_4, second_vertical=vertical_1_6),
            Lowinverse(first_vertical=vertical_1_4, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_3_4.
            Lowinverse(first_vertical=vertical_3_4, second_vertical=vertical_1_5),
            Lowinverse(first_vertical=vertical_3_4, second_vertical=vertical_3_5),
            Lowinverse(first_vertical=vertical_3_4, second_vertical=vertical_1_6),
            Lowinverse(first_vertical=vertical_3_4, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_1_5.
            Lowinverse(first_vertical=vertical_1_5, second_vertical=vertical_3_5),
            Lowinverse(first_vertical=vertical_1_5, second_vertical=vertical_1_6),
            Lowinverse(first_vertical=vertical_1_5, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_3_5.
            Lowinverse(first_vertical=vertical_3_5, second_vertical=vertical_1_6),
            Lowinverse(first_vertical=vertical_3_5, second_vertical=vertical_3_6),
            # All Lowinverses with vertical_1_6.
            Lowinverse(first_vertical=vertical_1_6, second_vertical=vertical_3_6),
        }
        self.assertEqual(want_lowinverses, got_lowinverses)


if __name__ == '__main__':
    unittest.main()
