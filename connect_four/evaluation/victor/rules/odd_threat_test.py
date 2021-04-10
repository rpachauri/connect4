import unittest

import gym
import numpy as np

from connect_four.envs import ConnectFourEnv
from connect_four.evaluation.victor.board import Board
from connect_four.evaluation.victor.rules import OddThreat
from connect_four.evaluation.victor.rules import find_all_odd_threats
from connect_four.game import Square
from connect_four.problem import Group


class TestOddThreat(unittest.TestCase):
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
        got_odd_threats = find_all_odd_threats(board=board)
        self.assertFalse(got_odd_threats)

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
        want_odd_threats = {
            OddThreat(
                group=Group(player=0, start=Square(row=3, col=0), end=Square(row=3, col=3)),  # a3-d3
                empty_square=Square(row=3, col=0),  # a3
            ),
        }
        got_odd_threats = find_all_odd_threats(board=board)
        self.assertEqual(want_odd_threats, got_odd_threats)

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
        want_odd_threats = {
            OddThreat(
                group=Group(player=0, start=Square(row=3, col=1), end=Square(row=3, col=4)),  # b3-e3
                empty_square=Square(row=3, col=1),  # b3
            ),
            OddThreat(
                group=Group(player=0, start=Square(row=3, col=2), end=Square(row=3, col=5)),  # c3-f3
                empty_square=Square(row=3, col=5),  # f3
            ),
        }
        got_odd_threats = find_all_odd_threats(board=board)
        self.assertEqual(want_odd_threats, got_odd_threats)


if __name__ == '__main__':
    unittest.main()
