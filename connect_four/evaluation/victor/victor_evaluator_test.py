import gym
import unittest

import numpy as np

from connect_four.envs import ConnectFourEnv
from connect_four.evaluation import ProofStatus
from connect_four.evaluation.victor.victor_evaluator import Victor


class TestVictor(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 7
        self.evaluator = Victor(model=self.env)

    def test_initial_state(self):
        # In the initial state, Victor is not able to find a chosen set.
        # Thus, it should return Unknown.
        got_status = self.evaluator.evaluate()
        self.assertEqual(ProofStatus.Unknown, got_status)

    def test_evaluate_upon_initialization_works_for_disproving_diagram_6_1(self):
        # This test case is based on Diagram 6.1.
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
        self.evaluator = Victor(model=self.env)

        # It is currently White's turn and White is OR.
        # However, Victor should show that this position is a draw
        # so this node should be disproven.
        got_status = self.evaluator.evaluate()
        self.assertEqual(ProofStatus.Disproven, got_status)

    def test_evaluate_upon_initialization_works_for_disproving_diagram_8_1(self):
        # This test case is based on Diagram 8.1.
        # Black is to move and White has an odd threat at a3.
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
        self.env.player_turn = 1  # Black to move.
        self.evaluator = Victor(model=self.env)

        # It is currently White's turn and White is OR.
        # However, Victor should show that this position is a draw
        # so this node should be disproven.
        got_status = self.evaluator.evaluate()
        self.assertEqual(ProofStatus.Proven, got_status)


if __name__ == '__main__':
    unittest.main()
