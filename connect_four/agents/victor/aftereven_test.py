import gym
import unittest

import numpy as np

from connect_four.agents.victor import Aftereven
from connect_four.agents.victor import aftereven
from connect_four.agents.victor import Board
from connect_four.agents.victor import claimeven
from connect_four.agents.victor import Square
from connect_four.agents.victor import Threat
from connect_four.envs.connect_four_env import ConnectFourEnv


class TestAftereven(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 7
        self.env.reset()

    def test_aftereven1(self):
        self.env.state = np.array([
            [
                [1, 0, 0, 1, 0, 0, 1, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [1, 0, 1, 0, 1, 0, 1, ],
                [0, 0, 1, 1, 1, 0, 0, ],
                [1, 0, 0, 0, 0, 0, 1, ],
                [0, 0, 1, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 1, 0, 1, 0, 0, ],
                [1, 0, 1, 0, 1, 0, 1, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [1, 0, 0, 0, 0, 0, 1, ],
                [0, 0, 1, 1, 1, 0, 0, ],
                [1, 0, 0, 0, 1, 0, 1, ],
            ],
        ])
        board = Board(self.env.env_variables)
        got_afterevens = aftereven(board=board, claimevens=claimeven(board))

        want_afterevens = {
            Aftereven(threat=Threat(player=1, start=Square(row=4, col=1), end=Square(row=4, col=4)), columns=[1]),
            Aftereven(threat=Threat(player=1, start=Square(row=4, col=2), end=Square(row=4, col=5)), columns=[5]),
        }
        self.assertEqual(want_afterevens, got_afterevens)

    def test_aftereven2(self):
        self.env.state = np.array([
            [
                [1, 0, 1, 0, 0, 0, 0, ],
                [1, 0, 0, 0, 0, 0, 0, ],
                [0, 1, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 1, 1, 0, 0, ],
                [1, 1, 1, 0, 0, 0, 0, ],
                [0, 1, 1, 1, 0, 0, 0, ],
            ],
            [
                [0, 1, 0, 1, 0, 0, 0, ],
                [0, 1, 1, 0, 0, 0, 0, ],
                [1, 0, 1, 1, 1, 0, 0, ],
                [0, 1, 0, 0, 0, 0, 0, ],
                [1, 0, 0, 1, 1, 0, 0, ],
                [1, 0, 0, 0, 1, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        got_afterevens = aftereven(board=board, claimevens=claimeven(board))

        want_afterevens = {
            Aftereven(threat=Threat(player=1, start=Square(row=4, col=3), end=Square(row=4, col=6)), columns=[5, 6]),
            Aftereven(threat=Threat(player=1, start=Square(row=2, col=3), end=Square(row=2, col=6)), columns=[5, 6]),
            Aftereven(threat=Threat(player=1, start=Square(row=2, col=2), end=Square(row=2, col=5)), columns=[5]),
            Aftereven(threat=Threat(player=1, start=Square(row=0, col=3), end=Square(row=0, col=6)), columns=[4, 5, 6]),
        }
        self.assertEqual(want_afterevens, got_afterevens)


if __name__ == '__main__':
    unittest.main()
