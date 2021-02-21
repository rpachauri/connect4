import gym
import unittest

import numpy as np

from connect_four.agents.victor.game import Board
from connect_four.agents.victor.game import Square
from connect_four.agents.victor.game import Group

from connect_four.agents.victor.threat_hunter.threat_combination import ThreatCombination
from connect_four.agents.victor.threat_hunter.threat_combination import ThreatCombinationType
from connect_four.agents.victor.threat_hunter.threat_combination import find_threat_combination

from connect_four.envs.connect_four_env import ConnectFourEnv


class TestThreatCombination(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 7
        self.env.reset()

    def test_even_above_odd_threat_combination(self):
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
        board = Board(self.env.env_variables)
        want_even_threat = Group(player=0, start=Square(row=5, col=3), end=Square(row=2, col=6))  # d1-g4
        want_odd_threat = Group(player=0, start=Square(row=3, col=3), end=Square(row=3, col=6))  # d3-g3
        want_threat_combination = ThreatCombination(
            even_group=want_even_threat,
            odd_group=want_odd_threat,
            shared_square=Square(row=3, col=5),  # f3
            even_square=Square(row=2, col=6),  # g4
            odd_square=Square(row=3, col=6),  # g3
            threat_combination_type=ThreatCombinationType.EvenAboveOdd,
        )
        got_threat_combination = find_threat_combination(board=board)
        self.assertEqual(want_threat_combination, got_threat_combination)

    def test_odd_above_even_threat_combination(self):
        # This test is based on Diagram 8.7 from the original paper.
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
                [0, 0, 1, 0, 1, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        want_even_group = Group(player=0, start=Square(row=1, col=3), end=Square(row=4, col=6))  # d5-g2
        want_odd_group = Group(player=0, start=Square(row=3, col=3), end=Square(row=3, col=6))  # d3-d3
        want_threat_combination = ThreatCombination(
            even_group=want_even_group,
            odd_group=want_odd_group,
            shared_square=Square(row=3, col=5),  # f3
            even_square=Square(row=4, col=6),  # g2
            odd_square=Square(row=3, col=6),  # g3
            threat_combination_type=ThreatCombinationType.OddAboveNotDirectlyPlayableEven,
        )
        got_threat_combination = find_threat_combination(board=board)
        self.assertEqual(want_threat_combination, got_threat_combination)

    def test_threat_combination_columns(self):
        group_d5_g2 = Group(player=0, start=Square(row=1, col=3), end=Square(row=4, col=6))  # d5-g2
        group_d3_g3 = Group(player=0, start=Square(row=3, col=3), end=Square(row=3, col=6))  # d3-d3
        threat_combination_d5_g2_and_d3_g3 = ThreatCombination(
            even_group=group_d5_g2,
            odd_group=group_d3_g3,
            shared_square=Square(row=3, col=5),  # f3
            even_square=Square(row=4, col=6),  # g2
            odd_square=Square(row=3, col=6),  # g3
            threat_combination_type=ThreatCombinationType.OddAboveNotDirectlyPlayableEven,
        )
        want_columns = {5, 6}
        got_columns = threat_combination_d5_g2_and_d3_g3.columns()
        self.assertEqual(want_columns, got_columns)


if __name__ == '__main__':
    unittest.main()
