import gym
import unittest

import numpy as np

from connect_four.evaluation.victor import Board
from connect_four.evaluation.victor import Square

from connect_four.evaluation.victor.rules import Claimeven
from connect_four.evaluation.victor.rules import find_all_claimevens

from connect_four.envs.connect_four_env import ConnectFourEnv


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


if __name__ == '__main__':
    unittest.main()
