import gym
import unittest

import numpy as np

from connect_four.agents import DFPN
from connect_four.evaluation import NodeType
from connect_four.evaluation.tic_tac_toe_simple_evaluator import TicTacToeSimpleEvaluator
from connect_four.transposition.tic_tac_toe_simple_transposition_table import TicTacToeSimpleTranspositionTable


class TestDFPNTicTacToe(unittest.TestCase):
    """
    TestDFPNTicTacToe tests the df-pn search algorithm for the TicTacToe environment.
    """
    def setUp(self):
        self.env = gym.make('tic_tac_toe-v0')
        self.env.reset()

    def test_multiple_iterative_deepening_base_case_OR_Proven(self):
        # Have to initialize the environment one step before a terminal state because
        # the TicTacToeSimpleEvaluator cannot be instantiated with a terminal state.
        self.env.state = np.array([
            [
                [1, 1, 0, ],
                [0, 0, 0, ],
                [0, 0, 0, ],
            ],
            [
                [0, 0, 0, ],
                [1, 1, 0, ],
                [0, 0, 0, ],
            ],
        ])
        # OR is O and AND is X.
        evaluator = TicTacToeSimpleEvaluator(model=self.env, node_type=NodeType.AND)

        # Move the environment and the evaluator to a terminal state.
        # X plays in the top-left corner.
        self.env.step(action=0)
        evaluator.move(action=0)
        # Evaluator is now at an OR node (O). Since X just lost, it should evaluate() to Proven.

        tt = TicTacToeSimpleTranspositionTable()
        agent = DFPN(evaluator, tt)

        want_phi, want_delta = 0, DFPN.INF
        got_phi, got_delta = agent.multiple_iterative_deepening(
            env=self.env,
            phi_threshold=DFPN.INF,
            delta_threshold=DFPN.INF,
        )
        self.assertEqual(want_phi, got_phi)
        self.assertEqual(want_delta, got_delta)

        got_tt_phi, got_tt_delta = tt.retrieve(self.env.state)
        self.assertEqual(want_phi, got_tt_phi)
        self.assertEqual(want_delta, got_tt_delta)

    def test_multiple_iterative_deepening_base_case_OR_Disproven(self):
        # Have to initialize the environment one step before a terminal state because
        # the TicTacToeSimpleEvaluator cannot be instantiated with a terminal state.
        self.env.state = np.array([
            [
                [1, 1, 0, ],
                [0, 0, 0, ],
                [0, 0, 0, ],
            ],
            [
                [0, 0, 0, ],
                [1, 1, 0, ],
                [0, 0, 0, ],
            ],
        ])
        # AND is X and OR is O.
        evaluator = TicTacToeSimpleEvaluator(model=self.env, node_type=NodeType.AND)

        # Move the environment and the evaluator to a terminal state.
        # X plays in the top-right corner.
        self.env.step(action=2)
        evaluator.move(action=2)
        # Evaluator is now at an OR node (O). Since X just won, it should evaluate() to Disproven.

        tt = TicTacToeSimpleTranspositionTable()
        agent = DFPN(evaluator, tt)

        want_phi, want_delta = DFPN.INF, 0
        got_phi, got_delta = agent.multiple_iterative_deepening(
            env=self.env,
            phi_threshold=DFPN.INF,
            delta_threshold=DFPN.INF,
        )
        self.assertEqual(want_phi, got_phi)
        self.assertEqual(want_delta, got_delta)

        got_tt_phi, got_tt_delta = tt.retrieve(self.env.state)
        self.assertEqual(want_phi, got_tt_phi)
        self.assertEqual(want_delta, got_tt_delta)

    def test_multiple_iterative_deepening_base_case_AND_Proven(self):
        # Have to initialize the environment one step before a terminal state because
        # the TicTacToeSimpleEvaluator cannot be instantiated with a terminal state.
        self.env.state = np.array([
            [
                [1, 1, 0, ],
                [0, 0, 0, ],
                [0, 0, 0, ],
            ],
            [
                [0, 0, 0, ],
                [1, 1, 0, ],
                [0, 0, 0, ],
            ],
        ])
        # OR is X and AND is O.
        evaluator = TicTacToeSimpleEvaluator(model=self.env, node_type=NodeType.OR)

        # Move the environment and the evaluator to a terminal state.
        # X plays in the top-right corner.
        self.env.step(action=2)
        evaluator.move(action=2)
        # Evaluator is now at an AND node (O). Since X just won, it should evaluate() to Proven.

        tt = TicTacToeSimpleTranspositionTable()
        agent = DFPN(evaluator, tt)

        want_phi, want_delta = DFPN.INF, 0
        got_phi, got_delta = agent.multiple_iterative_deepening(
            env=self.env,
            phi_threshold=DFPN.INF,
            delta_threshold=DFPN.INF,
        )
        self.assertEqual(want_phi, got_phi)
        self.assertEqual(want_delta, got_delta)

        got_tt_phi, got_tt_delta = tt.retrieve(self.env.state)
        self.assertEqual(want_phi, got_tt_phi)
        self.assertEqual(want_delta, got_tt_delta)

    def test_multiple_iterative_deepening_base_case_AND_Disproven(self):
        # Have to initialize the environment one step before a terminal state because
        # the TicTacToeSimpleEvaluator cannot be instantiated with a terminal state.
        self.env.state = np.array([
            [
                [1, 1, 0, ],
                [0, 0, 0, ],
                [0, 0, 0, ],
            ],
            [
                [0, 0, 0, ],
                [1, 1, 0, ],
                [0, 0, 0, ],
            ],
        ])
        # OR is X and AND is O.
        evaluator = TicTacToeSimpleEvaluator(model=self.env, node_type=NodeType.OR)

        # Move the environment and the evaluator to a terminal state.
        # X plays in the top-left corner.
        self.env.step(action=0)
        evaluator.move(action=0)
        # Evaluator is now at an AND node (O). Since X just lost, it should evaluate() to Disproven.

        tt = TicTacToeSimpleTranspositionTable()
        agent = DFPN(evaluator, tt)

        want_phi, want_delta = 0, DFPN.INF
        got_phi, got_delta = agent.multiple_iterative_deepening(
            env=self.env,
            phi_threshold=DFPN.INF,
            delta_threshold=DFPN.INF,
        )
        self.assertEqual(want_phi, got_phi)
        self.assertEqual(want_delta, got_delta)

        got_tt_phi, got_tt_delta = tt.retrieve(self.env.state)
        self.assertEqual(want_phi, got_tt_phi)
        self.assertEqual(want_delta, got_tt_delta)


if __name__ == '__main__':
    unittest.main()
