import gym
import unittest

import numpy as np

from connect_four.agents.victor.game import Board
from connect_four.agents.victor.game import Square
from connect_four.agents.victor.game import Group

from connect_four.agents.victor.threat import threat

from connect_four.envs.connect_four_env import ConnectFourEnv


class TestThreat(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 7
        self.env.reset()

    def test_no_odd_threat_exists(self):
        # There is no odd Threat for an empty Board.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        got_threat = threat.find_odd_threat(board=board)
        self.assertIsNone(got_threat)

    def test_find_odd_threat(self):
        # This test is based on Diagram 8.1 from the original paper.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 1, 1, 1, 0, 0, 0, ],
                [0, 1, 0, 0, 0, 0, 0, ],
                [1, 0, 1, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 0, 1, 1, 1, 0, 0, ],
                [0, 1, 0, 0, 1, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        want_threat = threat.Threat(
            group=Group(player=0, start=Square(row=3, col=0), end=Square(row=3, col=3)),  # a3-d3
            empty_square=Square(row=3, col=0),  # a3
        )
        got_threat = threat.find_odd_threat(board=board)
        self.assertEqual(want_threat, got_threat)

    def test_find_odd_threat_when_multiple_exist(self):
        # This test is based on Diagram 3.9 from the original paper.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 1, 1, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        possible_threats = [
            threat.Threat(
                group=Group(player=0, start=Square(row=5, col=1), end=Square(row=5, col=4)),  # b1-e1
                empty_square=Square(row=5, col=1),  # b1
            ),
            threat.Threat(
                group=Group(player=0, start=Square(row=5, col=2), end=Square(row=5, col=5)),  # c1-f1
                empty_square=Square(row=5, col=5),  # f1
            ),
        ]
        got_threat = threat.find_odd_threat(board=board)
        self.assertIn(got_threat, possible_threats)


if __name__ == '__main__':
    unittest.main()
