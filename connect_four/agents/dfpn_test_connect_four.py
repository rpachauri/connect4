import gym
import unittest

import numpy as np

from connect_four.agents import DFPN
from connect_four.evaluation.victor_evaluator import Victor
from connect_four.hashing import ConnectFourHasher
from connect_four.transposition.simple_transposition_table import SimpleTranspositionTable


class TestDFPNConnectFour(unittest.TestCase):
    """
    TestDFPNTicTacToe tests the df-pn search algorithm for the Connect Four environment.
    """
    def setUp(self):
        self.env = gym.make('connect_four-v0')

    def test_prove_diagram_11_1(self):
        # This test case is based on Diagram 11.1.
        # White can win by playing a1.
        self.env.state = np.array([
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
        evaluator = Victor(model=self.env)
        hasher = ConnectFourHasher(env=self.env)
        tt = SimpleTranspositionTable()
        agent = DFPN(evaluator, hasher, tt)

        # The given node should be easily proven even with phi/delta thresholds of 1.
        phi, delta = agent.multiple_iterative_deepening(env=self.env, phi_threshold=DFPN.INF, delta_threshold=DFPN.INF)

        # Since we are currently at an OR node and this node should have been proven,
        # phi should be 0.
        self.assertEqual(0, phi)
        # Since we are currently at an OR node and this node should have been disproven,
        # delta should be at least INF.
        self.assertGreaterEqual(delta, DFPN.INF)


if __name__ == '__main__':
    unittest.main()
