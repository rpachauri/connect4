import gym
import unittest

import numpy as np

from connect_four.evaluation.victor import Board
from connect_four.evaluation.victor import Square
from connect_four.evaluation.victor import Group

from connect_four.evaluation.victor import threat

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
        # There are two odd Threats in the 3rd row from the bottom.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 1, 1, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 0, 1, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        possible_threats = [
            threat.Threat(
                group=Group(player=0, start=Square(row=3, col=1), end=Square(row=3, col=4)),  # b3-e3
                empty_square=Square(row=3, col=1),  # b3
            ),
            threat.Threat(
                group=Group(player=0, start=Square(row=3, col=2), end=Square(row=3, col=5)),  # c3-f3
                empty_square=Square(row=3, col=5),  # f3
            ),
        ]
        got_threat = threat.find_odd_threat(board=board)
        self.assertIn(got_threat, possible_threats)

    def test_threat_columns(self):
        threat_b3_e3 = threat.Threat(
            group=Group(player=0, start=Square(row=3, col=1), end=Square(row=3, col=4)),  # b3-e3
            empty_square=Square(row=3, col=1),  # b3
        )
        want_columns = {1}
        got_columns = threat_b3_e3.columns()
        self.assertEqual(want_columns, got_columns)


if __name__ == '__main__':
    unittest.main()
