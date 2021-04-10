import unittest

import gym
import numpy as np

from connect_four.envs import ConnectFourEnv
from connect_four.evaluation.victor.board import Board
from connect_four.evaluation.victor.rules import ThreatCombination
from connect_four.evaluation.victor.rules.threat_combination import ThreatCombinationType, find_all_threat_combinations
from connect_four.game import Square
from connect_four.problem import Group


class TestThreatCombination(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 7
        self.env.reset()

    def test_diagram_8_3(self):
        # This test is based on Diagram 8.3 from the original paper.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 1, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 1, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 1, ],
            ],
            [
                [0, 0, 0, 1, 1, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 1, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
            ],
        ])
        self.env.player = 1

        board = Board(self.env.env_variables)

        want_threat_combinations = {
            # This is the Even above Odd Threat combination described in Diagram 8.3.
            ThreatCombination(
                even_group=Group(player=0, start=Square(row=5, col=3), end=Square(row=2, col=6)),  # d1-g4,
                odd_group=Group(player=0, start=Square(row=3, col=3), end=Square(row=3, col=6)),
                shared_square=Square(row=3, col=5),  # f3
                even_square=Square(row=2, col=6),  # g4
                odd_square=Square(row=3, col=6),  # g3
                threat_combination_type=ThreatCombinationType.EvenAboveOdd,
            ),
            # This is an Odd above not directly playable Even Threat Combination.
            # It wasn't talked about in the original paper for the related diagram, but it exists.
            ThreatCombination(
                even_group=Group(player=0, start=Square(row=1, col=1), end=Square(row=4, col=4)),  # b5-e2
                odd_group=Group(player=0, start=Square(row=1, col=1), end=Square(row=1, col=4)),   # b5-e5
                shared_square=Square(row=1, col=1),  # b5
                even_square=Square(row=2, col=2),  # c4
                odd_square=Square(row=1, col=2),  # c5
                threat_combination_type=ThreatCombinationType.OddAboveNotDirectlyPlayableEven,
            ),
        }
        got_threat_combinations = find_all_threat_combinations(board=board)
        self.assertEqual(want_threat_combinations, got_threat_combinations)

    def test_diagram_8_7(self):
        # This test is a modification of Diagram 8.7 from the original paper.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 0, 0, 1, 1, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 1, ],
            ],
        ])
        board = Board(self.env.env_variables)
        want_even_group = Group(player=0, start=Square(row=1, col=3), end=Square(row=4, col=6))  # d5-g2
        want_odd_group = Group(player=0, start=Square(row=3, col=3), end=Square(row=3, col=6))  # d3-d3
        want_threat_combinations = {
            ThreatCombination(
                even_group=want_even_group,
                odd_group=want_odd_group,
                shared_square=Square(row=3, col=5),  # f3
                even_square=Square(row=4, col=6),  # g2
                odd_square=Square(row=3, col=6),  # g3
                threat_combination_type=ThreatCombinationType.OddAboveDirectlyPlayableEven,
            )
        }
        got_threat_combinations = find_all_threat_combinations(board=board)
        self.assertEqual(want_threat_combinations, got_threat_combinations)


if __name__ == '__main__':
    unittest.main()
