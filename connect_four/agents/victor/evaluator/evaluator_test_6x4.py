import gym
import unittest

import numpy as np

from connect_four.agents.victor.game import Board, Group, Square
from connect_four.agents.victor.evaluator import evaluator
from connect_four.agents.victor.threat_hunter import threat_combination
from connect_four.envs.connect_four_env import ConnectFourEnv


class TestEvaluator6x4(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 4
        self.env.reset()

    def test_evaluate_6x4(self):
        self.env.state = np.array([
            [
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        got_evaluation = evaluator.evaluate(board=board)
        self.assertIsNotNone(got_evaluation)

    def test_evaluate_6x4_odd_above_even_threat_combination(self):
        # This test case is based on Diagram 8.3. The left 3 columns are removed.
        # Black is to move and White has a ThreatCombination at a1-d4 and a3-d3.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, ],
                [1, 1, 0, 0, ],
                [0, 0, 0, 0, ],
                [1, 1, 0, 0, ],
                [0, 1, 0, 0, ],
                [1, 0, 0, 1, ],
            ],
            [
                [1, 1, 0, 0, ],
                [0, 0, 0, 0, ],
                [1, 1, 0, 0, ],
                [0, 0, 0, 0, ],
                [1, 0, 0, 0, ],
                [0, 1, 0, 0, ],
            ],
        ])
        self.env.player_turn = 1  # Black to move.
        board = Board(self.env.env_variables)
        got_evaluation = evaluator.evaluate(board=board)
        self.assertIsNotNone(got_evaluation)

        want_odd_threat_guarantor = threat_combination.ThreatCombination(
            even_threat=Group(player=0, start=Square(row=5, col=0), end=Square(row=2, col=3)),  # a1-d4
            odd_threat=Group(player=0, start=Square(row=3, col=0), end=Square(row=3, col=3)),  # a3-d3
            shared_square=Square(row=3, col=2),  # c3
            even_square=Square(row=2, col=3),  # d4
            odd_square=Square(row=3, col=3),  # d3
            threat_combination_type=threat_combination.ThreatCombinationType.EvenAboveOdd,
        )
        self.assertEqual(want_odd_threat_guarantor, got_evaluation.odd_threat_guarantor)


if __name__ == '__main__':
    unittest.main()
