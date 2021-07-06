import gym
import unittest

import numpy as np

from connect_four.game import Square
from connect_four.problem import Group
from connect_four.evaluation.victor.board import Board
from connect_four.evaluation.victor.evaluator import evaluator
from connect_four.evaluation.victor.threat_hunter import threat_combination
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

    @unittest.skip("threat combination not yet implemented")
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
            even_group=Group(player=0, start=Square(row=5, col=0), end=Square(row=2, col=3)),  # a1-d4
            odd_group=Group(player=0, start=Square(row=3, col=0), end=Square(row=3, col=3)),  # a3-d3
            shared_square=Square(row=3, col=2),  # c3
            even_square=Square(row=2, col=3),  # d4
            odd_square=Square(row=3, col=3),  # d3
            threat_combination_type=threat_combination.ThreatCombinationType.EvenAboveOdd,
        )
        self.assertEqual(want_odd_threat_guarantor, got_evaluation.odd_threat_guarantor)

    @unittest.skip("threat combination not yet implemented")
    def test_evaluate_6x7_odd_above_not_directly_playable_even_threat_combination(self):
        # This test case is a modified version of Diagram 8.7.
        # The even square of the ThreatCombination is NOT directly playable.
        # Black is to move and White has a ThreatCombination at a5-d2 and a3-d3.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, ],
                [1, 0, 0, 0, ],
                [0, 1, 0, 0, ],
                [1, 1, 0, 0, ],
                [1, 0, 0, 0, ],
                [1, 0, 0, 0, ],
            ],
            [
                [1, 0, 0, 0, ],
                [0, 1, 0, 0, ],
                [1, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 1, 0, 0, ],
                [0, 1, 0, 0, ],
            ],
        ])
        self.env.player_turn = 1  # Black to move.
        board = Board(self.env.env_variables)
        got_evaluation = evaluator.evaluate(board=board)
        self.assertIsNotNone(got_evaluation)

        want_odd_threat_guarantor = threat_combination.ThreatCombination(
            even_group=Group(player=0, start=Square(row=1, col=0), end=Square(row=4, col=3)),  # a5-d2
            odd_group=Group(player=0, start=Square(row=3, col=0), end=Square(row=3, col=3)),  # a3-d3
            shared_square=Square(row=3, col=2),  # c3
            even_square=Square(row=4, col=3),  # d2
            odd_square=Square(row=3, col=3),  # d3
            threat_combination_type=threat_combination.ThreatCombinationType.OddAboveNotDirectlyPlayableEven,
        )
        self.assertEqual(want_odd_threat_guarantor, got_evaluation.odd_threat_guarantor)


if __name__ == '__main__':
    unittest.main()
