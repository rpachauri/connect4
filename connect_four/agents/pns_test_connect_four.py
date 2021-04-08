import gym
import unittest

import numpy as np

from connect_four.agents import PNS
from connect_four.evaluation.victor_evaluator import Victor


class TestPNSConnectFour(unittest.TestCase):
    """
    TestPNSTicTacToe tests the Proof-Number Search algorithm for the Connect Four environment.
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
        pns = PNS(evaluator=evaluator)

        # Conduct Proof-Number Search.
        pns.proof_number_search()

        got_proof_number = pns.root.proof
        self.assertEqual(0, got_proof_number)


if __name__ == '__main__':
    unittest.main()
