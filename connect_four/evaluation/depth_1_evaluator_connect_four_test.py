import unittest

import gym
import numpy as np

from connect_four.envs import ConnectFourEnv
from connect_four.evaluation import ProofStatus
from connect_four.evaluation.depth_1_evaluator import Depth1Evaluator


class TestDepth1EvaluatorConnectFour(unittest.TestCase):
    def setUp(self) -> None:
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 7

        self.diagram_11_1_env = gym.make('connect_four-v0')
        self.diagram_11_1_env.reset()
        self.diagram_11_1_env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 1, 1, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
            ],
        ])
        self.evaluator = Depth1Evaluator(model=self.diagram_11_1_env)

    def test_diagram_11_1_move_5(self):
        # Move 5.
        self.evaluator.move(action=0)  # White plays a1.
        self.evaluator.move(action=0)  # Black plays a2.

        # Since White can win by playing b1, this node should be easily proven.
        got_evaluation = self.evaluator.evaluate()
        # Evaluation should return Proven.
        self.assertEqual(ProofStatus.Proven, got_evaluation)

    def test_diagram_11_1_move_6(self):
        # Move 5.
        self.evaluator.move(action=0)  # White plays a1.
        self.evaluator.move(action=1)  # Black plays b1.
        self.evaluator.move(action=0)  # White plays a2.

        # Since Black can win by playing b2, this node should be easily disproven.
        got_evaluation = self.evaluator.evaluate()
        # Evaluation should return Proven.
        self.assertEqual(ProofStatus.Disproven, got_evaluation)


if __name__ == '__main__':
    unittest.main()
