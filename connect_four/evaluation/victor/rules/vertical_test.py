import gym
import unittest

import numpy as np

from connect_four.evaluation.victor.game import Board
from connect_four.evaluation.victor.game import Square
from connect_four.evaluation.victor.rules import Vertical
from connect_four.evaluation.victor.rules import find_all_verticals
from connect_four.envs.connect_four_env import ConnectFourEnv


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


if __name__ == '__main__':
    unittest.main()
