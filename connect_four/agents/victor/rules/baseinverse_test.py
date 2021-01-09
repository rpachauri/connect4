import gym
import unittest

import numpy as np

from connect_four.agents.victor.game import Board
from connect_four.agents.victor.game import Square

from connect_four.agents.victor.rules import Baseinverse
from connect_four.agents.victor.rules import find_all_baseinverses

from connect_four.envs.connect_four_env import ConnectFourEnv


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


if __name__ == '__main__':
    unittest.main()
