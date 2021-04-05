import gym
import unittest

import numpy as np

from connect_four.agents import DFPN
from connect_four.evaluation.tic_tac_toe_simple_evaluator import TicTacToeSimpleEvaluator
from connect_four.hashing import TicTacToeHasher
from connect_four.transposition.simple_transposition_table import SimpleTranspositionTable


class TestDFPNTicTacToe(unittest.TestCase):
    """
    TestDFPNTicTacToe tests the df-pn search algorithm for the TicTacToe environment.
    """
    def setUp(self):
        self.env = gym.make('tic_tac_toe-v0')
        self.env.reset()

    def test_generate_children_initial_state(self):
        evaluator = TicTacToeSimpleEvaluator(model=self.env)
        hasher = TicTacToeHasher(env=self.env)
        tt = SimpleTranspositionTable()
        agent = DFPN(evaluator, hasher, tt)

        agent.generate_children()
        # Make sure at least one of the children is in the TT.
        # Looping isn't ideal for testing and manually testing all 9 children would lead to a long test.
        hasher.move(action=0)
        phi, delta = tt.retrieve(transposition=hasher.hash())
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
        evaluator = TicTacToeSimpleEvaluator(model=self.env)
        hasher = TicTacToeHasher(env=self.env)
        tt = SimpleTranspositionTable()
        agent = DFPN(evaluator, hasher, tt)

        agent.generate_children()

        # Note that the test cases might be counter-intuitive. Recall that the child nodes are AND nodes,
        # so their phi/delta numbers will be the opposite of what you'd expect for an OR node.

        # Verify that any moves that lead to X winning will be considered "Proven".
        hasher.move(action=2)
        phi, delta = tt.retrieve(transposition=hasher.hash())
        hasher.undo_move()
        # Since child_2 is an AND node, the phi number is INF because it is impossible to disprove the node.
        self.assertEqual(DFPN.INF, phi)
        self.assertEqual(0, delta)

        # Verify that any moves that allow the game to continue will be considered "Unknown".
        hasher.move(action=5)
        phi, delta = tt.retrieve(transposition=hasher.hash())
        # Since child_2 is an AND node, the phi number is 0 because it disproved the node.
        self.assertEqual(1, phi)
        self.assertEqual(1, delta)

    def test_calculate_phi_delta_initial_state(self):
        evaluator = TicTacToeSimpleEvaluator(model=self.env)
        hasher = TicTacToeHasher(env=self.env)
        tt = SimpleTranspositionTable()
        agent = DFPN(evaluator, hasher, tt)

        agent.generate_children()
        untouched_env_variables = self.env.env_variables
        phi, delta = agent.calculate_phi_delta()

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
        evaluator = TicTacToeSimpleEvaluator(model=self.env)
        hasher = TicTacToeHasher(env=self.env)
        tt = SimpleTranspositionTable()
        agent = DFPN(evaluator, hasher, tt)

        agent.generate_children()
        phi, delta = agent.calculate_phi_delta()
        # The phi number should be the smallest delta number of all of node's children.
        # Child 2 should have a delta number of 0 because X wins in that state.
        # This means the phi number of the OR node should be 0.
        self.assertEqual(0, phi)
        # The delta number should be sum of the phi numbers of all of node's children.
        # Child 2 should have a phi number of INF.
        # This means the delta number of the OR node should be at least INF.
        self.assertGreaterEqual(delta, DFPN.INF)

    def test_multiple_iterative_deepening_proving_OR(self):
        # This test case should validate the termination condition works for a node
        # that can be immediately proved.
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
        # OR is X and AND is O. The above state should be easily proved.
        # Any moves that lead to X winning will be considered "Proven".
        # Any moves that cause X to lose or draw the game will be considered "Disproven".
        # Any moves that allow the game to continue will be considered "Unknown".
        evaluator = TicTacToeSimpleEvaluator(model=self.env)
        hasher = TicTacToeHasher(env=self.env)
        tt = SimpleTranspositionTable()
        agent = DFPN(evaluator, hasher, tt)

        # The given node should be easily proven even with phi/delta thresholds of 1.
        phi, delta = agent.multiple_iterative_deepening(env=self.env, phi_threshold=1, delta_threshold=1)

        # The phi number should be the smallest delta number of all of node's children.
        # Child 2 should have a delta number of 0 because X wins in that state.
        # This means the phi number of the OR node should be 0.
        self.assertEqual(0, phi)
        # The delta number should be sum of the phi numbers of all of node's children.
        # Child 2 should have a phi number of INF.
        # This means the delta number of the OR node should be at least INF.
        self.assertGreaterEqual(delta, DFPN.INF)

    def test_multiple_iterative_deepening_AND_Proven_02_11_20_22_00(self):
        # This position is a guaranteed win for OR, so it should be Proven.
        self.env.state = np.array([
            [
                [1, 0, 1, ],
                [0, 0, 0, ],
                [1, 0, 0, ],
            ],
            [
                [0, 0, 0, ],
                [0, 1, 0, ],
                [0, 0, 1, ],
            ],
        ])
        self.env.player_turn = 1
        evaluator = TicTacToeSimpleEvaluator(model=self.env)
        hasher = TicTacToeHasher(env=self.env)
        tt = SimpleTranspositionTable()
        agent = DFPN(evaluator, hasher, tt)

        # The given node should be easily proven even with phi/delta thresholds of 1.
        phi, delta = agent.multiple_iterative_deepening(env=self.env, phi_threshold=DFPN.INF, delta_threshold=DFPN.INF)

        # Since we are currently at an AND node and this node should have been proven,
        # phi should be at least INF.
        self.assertGreaterEqual(phi, DFPN.INF)
        # Since we are currently at an AND node and this node should have been proven,
        # delta should be 0.
        self.assertEqual(0, delta)

    def test_multiple_iterative_deepening_OR_Disproven_initial_state(self):
        # The initial state of Tic-Tac-Toe is a known draw, which means it is disproven for OR.
        evaluator = TicTacToeSimpleEvaluator(model=self.env)
        hasher = TicTacToeHasher(env=self.env)
        tt = SimpleTranspositionTable()
        agent = DFPN(evaluator, hasher, tt)

        # The given node should be easily proven even with phi/delta thresholds of 1.
        phi, delta = agent.multiple_iterative_deepening(env=self.env, phi_threshold=DFPN.INF, delta_threshold=DFPN.INF)

        # Since we are currently at an OR node and this node should have been disproven,
        # phi should be at least INF.
        self.assertGreaterEqual(phi, DFPN.INF)
        # Since we are currently at an OR node and this node should have been disproven,
        # delta should be 0.
        self.assertEqual(0, delta)

    def test_multiple_iterative_deepening_AND_Disproven_near_terminal_state(self):
        # In this state, AND is to move but the game is a draw.
        self.env.state = np.array([
            [
                [1, 1, 0, ],
                [0, 0, 1, ],
                [1, 0, 0, ],
            ],
            [
                [0, 0, 1, ],
                [0, 0, 0, ],
                [0, 1, 1, ],
            ],
        ])
        self.env.player_turn = 1
        evaluator = TicTacToeSimpleEvaluator(model=self.env)
        hasher = TicTacToeHasher(env=self.env)
        tt = SimpleTranspositionTable()
        agent = DFPN(evaluator, hasher, tt)

        # The given node should be disproven with phi/delta thresholds of 4.
        phi, delta = agent.multiple_iterative_deepening(env=self.env, phi_threshold=4, delta_threshold=4)

        # Since we are currently at an AND node and this node should have been disproven,
        # phi should be 0.
        self.assertEqual(0, phi)
        # Since we are currently at an OR node and this node should have been disproven,
        # delta should be at least INF.
        self.assertGreaterEqual(delta, DFPN.INF)


if __name__ == '__main__':
    unittest.main()
