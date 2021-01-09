import gym
import unittest

import numpy as np

from connect_four.agents.victor import Aftereven
from connect_four.agents.victor import find_all_afterevens
from connect_four.agents.victor import Board
from connect_four.agents.victor import Claimeven
from connect_four.agents.victor import find_all_claimevens
from connect_four.agents.victor.game import Square
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
        got_afterevens = find_all_afterevens(board=board, claimevens=find_all_claimevens(board))

        want_afterevens = {
            Aftereven(
                threat=Threat(player=1, start=Square(row=4, col=1), end=Square(row=4, col=4)),
                claimevens=frozenset([Claimeven(upper=Square(row=4, col=1), lower=Square(row=5, col=1))]),
            ),
            Aftereven(
                threat=Threat(player=1, start=Square(row=4, col=2), end=Square(row=4, col=5)),
                claimevens=frozenset([Claimeven(upper=Square(row=4, col=5), lower=Square(row=5, col=5))]),
            ),
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
        got_afterevens = find_all_afterevens(board=board, claimevens=find_all_claimevens(board))

        want_afterevens = {
            Aftereven(
                threat=Threat(player=1, start=Square(row=4, col=3), end=Square(row=4, col=6)),
                claimevens=frozenset([
                    Claimeven(upper=Square(row=4, col=5), lower=Square(row=5, col=5)),
                    Claimeven(upper=Square(row=4, col=6), lower=Square(row=5, col=6)),
                ]),
            ),
            Aftereven(
                threat=Threat(player=1, start=Square(row=2, col=3), end=Square(row=2, col=6)),
                claimevens=frozenset([
                    Claimeven(upper=Square(row=2, col=5), lower=Square(row=3, col=5)),
                    Claimeven(upper=Square(row=2, col=6), lower=Square(row=3, col=6)),
                ]),
            ),
            Aftereven(
                threat=Threat(player=1, start=Square(row=2, col=2), end=Square(row=2, col=5)),
                claimevens=frozenset([
                    Claimeven(upper=Square(row=2, col=5), lower=Square(row=3, col=5)),
                ]),
            ),
        }
        self.assertEqual(want_afterevens, got_afterevens)


if __name__ == '__main__':
    unittest.main()
