import gym
import unittest

import numpy as np

from connect_four.envs import TwoPlayerGameEnv
from connect_four.evaluation.evaluator import ProofStatus, NodeType
from connect_four.evaluation.simple_evaluator import SimpleEvaluator


class TestTicTacToeSimpleEvaluator(unittest.TestCase):
    def setUp(self):
        self.env = gym.make('tic_tac_toe-v0')
        self.env.reset()

    def test_init(self):
        # SimpleEvaluator requires that model IS NOT at a terminal state when given.
        evaluator = SimpleEvaluator(model=self.env)

        # Since we know the given state is not a terminal state, the reward should just be the default reward.
        self.assertEqual(TwoPlayerGameEnv.DEFAULT_REWARD, evaluator.reward)
        # Since we know the given state is not a terminal state, the board should not have ended.
        self.assertFalse(evaluator.done)
        # The NodeType should be the given NodeType.
        self.assertEqual(NodeType.OR, evaluator.node_type)
        # Evaluation at initialization should return Unknown.
        self.assertEqual(ProofStatus.Unknown, evaluator.evaluate())

    def test_single_move(self):
        evaluator = SimpleEvaluator(model=self.env)

        # A single move is made. X plays in the top-left corner.
        evaluator.move(action=0)

        # The reward should just be the default reward.
        self.assertEqual(TwoPlayerGameEnv.DEFAULT_REWARD, evaluator.reward)
        # If the only step is that X plays in the top-left corner, the board should not end.
        self.assertFalse(evaluator.done)
        # Play should always switch to the opponent.
        self.assertEqual(NodeType.AND, evaluator.node_type)
        # Evaluation should return Unknown.
        self.assertEqual(ProofStatus.Unknown, evaluator.evaluate())

    def test_undo_move(self):
        evaluator = SimpleEvaluator(model=self.env)

        # A single move is made. X plays in the top-left corner.
        evaluator.move(action=0)
        # Undo that move.
        evaluator.undo_move()

        # The evaluator's internal model should be at the initial state.
        # Since we know the given state is not a terminal state, the reward should just be the default reward.
        self.assertEqual(TwoPlayerGameEnv.DEFAULT_REWARD, evaluator.reward)
        # Since we know the given state is not a terminal state, the board should not have ended.
        self.assertFalse(evaluator.done)
        # The NodeType should be the given NodeType.
        self.assertEqual(NodeType.OR, evaluator.node_type)
        # Evaluation should return Unknown.
        self.assertEqual(ProofStatus.Unknown, evaluator.evaluate())

    ###
    # The following test cases follow somewhat unintuitive naming conventions.
    # {AND, OR} indicates the terminal node.
    # {CONNECTED, DRAW} indicates the reward returned upon arriving at the terminal node.
    # This reward is given to the *opponent* of the player at the terminal node.
    ###

    def test_evaluate_AND_CONNECTED(self):
        # This tests for when OR has connected three.
        # The terminal state will be at AND.
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
        evaluator = SimpleEvaluator(model=self.env)

        # A single move is made. X plays in the top-right corner.
        evaluator.move(action=2)

        # The evaluator's internal model should be at a terminal state.
        # The reward should just be the result of connecting three.
        self.assertEqual(TwoPlayerGameEnv.CONNECTED, evaluator.reward)
        # The board should have ended.
        self.assertTrue(evaluator.done)
        # NodeType should always switch to the opponent.
        self.assertEqual(NodeType.AND, evaluator.node_type)
        # Evaluation should return Proven.
        self.assertEqual(ProofStatus.Proven, evaluator.evaluate())

    def test_evaluate_AND_DRAW(self):
        # This tests for when OR has drawn the board.
        # The terminal state will be at AND.
        self.env.state = np.array([
            [
                [0, 1, 0, ],
                [0, 1, 1, ],
                [1, 0, 0, ],
            ],
            [
                [1, 0, 1, ],
                [1, 0, 0, ],
                [0, 1, 0, ],
            ],
        ])

        evaluator = SimpleEvaluator(model=self.env)

        # A single move is made. X plays in the bottom-right corner.
        evaluator.move(action=8)

        # The evaluator's internal model should be at a terminal state.
        # The reward should just be the result of connecting three.
        self.assertEqual(TwoPlayerGameEnv.DRAW, evaluator.reward)
        # The board should have ended.
        self.assertTrue(evaluator.done)
        # NodeType should always switch to the opponent.
        self.assertEqual(NodeType.AND, evaluator.node_type)
        # Evaluation should return Proven.
        self.assertEqual(ProofStatus.Disproven, evaluator.evaluate())

    def test_evaluate_OR_CONNECTED(self):
        # Note that if AND wins or draws the board, then the node is Disproven because OR has not won the board.
        # For Tic-Tac-Toe, it is not possible for AND to draw the board because only Player 1 can draw the board.
        # This tests for when AND connects three.
        # The terminal state will be at OR.
        self.env.state = np.array([
            [
                [1, 1, 0, ],
                [0, 0, 0, ],
                [1, 0, 0, ],
            ],
            [
                [0, 0, 0, ],
                [1, 1, 0, ],
                [0, 0, 0, ],
            ],
        ])
        self.env.player_turn = 1

        evaluator = SimpleEvaluator(model=self.env)

        # A single move is made. O plays on the right-middle edge.
        evaluator.move(action=5)

        # The evaluator's internal model should be at a terminal state.
        # The reward should just be the result of connecting three.
        self.assertEqual(TwoPlayerGameEnv.CONNECTED, evaluator.reward)
        # The board should have ended.
        self.assertTrue(evaluator.done)
        # NodeType should always switch to the opponent.
        self.assertEqual(NodeType.OR, evaluator.node_type)
        # Evaluation should return Disproven.
        self.assertEqual(ProofStatus.Disproven, evaluator.evaluate())


if __name__ == '__main__':
    unittest.main()
