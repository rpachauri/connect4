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

    # def test_multiple_iterative_deepening_base_case_OR_Proven(self):
    #     # Have to initialize the environment one step before a terminal state because
    #     # the TicTacToeSimpleEvaluator cannot be instantiated with a terminal state.
    #     self.env.state = np.array([
    #         [
    #             [1, 1, 0, ],
    #             [0, 0, 0, ],
    #             [0, 0, 0, ],
    #         ],
    #         [
    #             [0, 0, 0, ],
    #             [1, 1, 0, ],
    #             [0, 0, 0, ],
    #         ],
    #     ])
    #     # OR is O and AND is X.
    #     evaluator = TicTacToeSimpleEvaluator(model=self.env, node_type=NodeType.AND)
    # 
    #     # Move the environment and the evaluator to a terminal state.
    #     # X plays in the top-left corner.
    #     self.env.step(action=0)
    #     evaluator.move(action=0)
    #     # Evaluator is now at an OR node (O). Since X just lost, it should evaluate() to Proven.
    # 
    #     tt = TicTacToeSimpleTranspositionTable()
    #     agent = DFPN(evaluator, tt)
    # 
    #     want_phi, want_delta = 0, DFPN.INF
    #     got_phi, got_delta = agent.multiple_iterative_deepening(
    #         env=self.env,
    #         phi_threshold=DFPN.INF,
    #         delta_threshold=DFPN.INF,
    #     )
    #     self.assertEqual(want_phi, got_phi)
    #     self.assertEqual(want_delta, got_delta)
    # 
    #     got_tt_phi, got_tt_delta = tt.retrieve(self.env.state)
    #     self.assertEqual(want_phi, got_tt_phi)
    #     self.assertEqual(want_delta, got_tt_delta)

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

    # def test_multiple_iterative_deepening_base_case_AND_Disproven(self):
    #     # Have to initialize the environment one step before a terminal state because
    #     # the TicTacToeSimpleEvaluator cannot be instantiated with a terminal state.
    #     self.env.state = np.array([
    #         [
    #             [1, 1, 0, ],
    #             [0, 0, 0, ],
    #             [0, 0, 0, ],
    #         ],
    #         [
    #             [0, 0, 0, ],
    #             [1, 1, 0, ],
    #             [0, 0, 0, ],
    #         ],
    #     ])
    #     # OR is X and AND is O.
    #     evaluator = TicTacToeSimpleEvaluator(model=self.env, node_type=NodeType.OR)
    # 
    #     # Move the environment and the evaluator to a terminal state.
    #     # X plays in the top-left corner.
    #     self.env.step(action=0)
    #     evaluator.move(action=0)
    #     # Evaluator is now at an AND node (O). Since X just lost, it should evaluate() to Disproven.
    # 
    #     tt = TicTacToeSimpleTranspositionTable()
    #     agent = DFPN(evaluator, tt)
    # 
    #     want_phi, want_delta = 0, DFPN.INF
    #     got_phi, got_delta = agent.multiple_iterative_deepening(
    #         env=self.env,
    #         phi_threshold=DFPN.INF,
    #         delta_threshold=DFPN.INF,
    #     )
    #     self.assertEqual(want_phi, got_phi)
    #     self.assertEqual(want_delta, got_delta)
    # 
    #     got_tt_phi, got_tt_delta = tt.retrieve(self.env.state)
    #     self.assertEqual(want_phi, got_tt_phi)
    #     self.assertEqual(want_delta, got_tt_delta)

    def test_generate_children_initial_state(self):
        evaluator = TicTacToeSimpleEvaluator(model=self.env, node_type=NodeType.OR)
        tt = TicTacToeSimpleTranspositionTable()
        agent = DFPN(evaluator, tt)

        agent.generate_children()
        # Make sure at least one of the children is in the TT.
        # Looping isn't ideal for testing and manually testing all 9 children would lead to a long test.
        child_0 = np.array([
            [
                [1, 0, 0, ],
                [0, 0, 0, ],
                [0, 0, 0, ],
            ],
            [
                [0, 0, 0, ],
                [0, 0, 0, ],
                [0, 0, 0, ],
            ],
        ])
        phi, delta = tt.retrieve(state=child_0)
        self.assertEqual(1, phi)
        self.assertEqual(1, delta)

    def test_generate_children_winning_OR(self):
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
        # Any moves that lead to X winning will be considered "Proven".
        # Any moves that cause X to lose or draw the game will be considered "Disproven".
        # Any moves that allow the game to continue will be considered "Unknown".
        evaluator = TicTacToeSimpleEvaluator(model=self.env, node_type=NodeType.OR)
        tt = TicTacToeSimpleTranspositionTable()
        agent = DFPN(evaluator, tt)

        agent.generate_children()

        # Note that the test cases might be counter-intuitive. Recall that the child nodes are AND nodes,
        # so their phi/delta numbers will be the opposite of what you'd expect for an OR node.

        # Verify that any moves that lead to X winning will be considered "Proven".
        child_2 = np.array([
            [
                [1, 1, 1, ],
                [0, 0, 0, ],
                [0, 0, 0, ],
            ],
            [
                [0, 0, 0, ],
                [1, 1, 0, ],
                [0, 0, 0, ],
            ],
        ])
        phi, delta = tt.retrieve(state=child_2)
        # Since child_2 is an AND node, the phi number is INF because it is impossible to disprove the node.
        self.assertEqual(DFPN.INF, phi)
        self.assertEqual(0, delta)

        # Verify that any moves that allow the game to continue will be considered "Unknown".
        child_5 = np.array([
            [
                [1, 1, 0, ],
                [0, 0, 1, ],
                [0, 0, 0, ],
            ],
            [
                [0, 0, 0, ],
                [1, 1, 0, ],
                [0, 0, 0, ],
            ],
        ])
        phi, delta = tt.retrieve(state=child_5)
        # Since child_2 is an AND node, the phi number is 0 because it is impossible to disprove the node.
        self.assertEqual(1, phi)
        self.assertEqual(1, delta)

    def test_calculate_phi_delta_initial_state(self):
        evaluator = TicTacToeSimpleEvaluator(model=self.env, node_type=NodeType.OR)
        tt = TicTacToeSimpleTranspositionTable()
        agent = DFPN(evaluator, tt)

        agent.generate_children()
        untouched_env_variables = self.env.env_variables
        phi, delta = agent.calculate_phi_delta(env=self.env)

        # Verify the environment is reset back to what it was originally.
        self.assertIsNone(np.testing.assert_array_equal(
            untouched_env_variables[0],
            self.env.env_variables[0],
        ))
        self.assertEqual(untouched_env_variables[1], self.env.env_variables[1])

        # The phi number should be the smallest delta number of all of node's children.
        self.assertEqual(1, phi)
        # The delta number should be sum of the phi numbers of all of node's children.
        self.assertEqual(len(evaluator.actions()), delta)

    def test_calculate_phi_delta_proving_OR(self):
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
        # Any moves that lead to X winning will be considered "Proven".
        # Any moves that cause X to lose or draw the game will be considered "Disproven".
        # Any moves that allow the game to continue will be considered "Unknown".
        evaluator = TicTacToeSimpleEvaluator(model=self.env, node_type=NodeType.OR)
        tt = TicTacToeSimpleTranspositionTable()
        agent = DFPN(evaluator, tt)
        agent.generate_children()

        phi, delta = agent.calculate_phi_delta(env=self.env)
        # The phi number should be the smallest delta number of all of node's children.
        # Child 2 should have a delta number of 0 because X wins in that state.
        self.assertEqual(0, phi)
        # The delta number should be sum of the phi numbers of all of node's children.
        # Child 2 should have a phi number of INF, so the delta number should be at least INF.
        self.assertGreaterEqual(delta, DFPN.INF)


if __name__ == '__main__':
    unittest.main()
