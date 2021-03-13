import gym
import unittest

from connect_four.envs import TwoPlayerGameEnv
from connect_four.evaluation.tic_tac_toe_simple_evaluator import NodeType
from connect_four.evaluation.tic_tac_toe_simple_evaluator import TicTacToeSimpleEvaluator


class TestTicTacToeSimpleEvaluator(unittest.TestCase):
    def setUp(self):
        self.env = gym.make('tic_tac_toe-v0')
        self.env.reset()

    def test_init(self):
        # TicTacToeSimpleEvaluator requires that model IS NOT at a terminal state when given.
        evaluator = TicTacToeSimpleEvaluator(model=self.env, node_type=NodeType.OR)

        # Since we know the given state is not a terminal state, the reward should just be the default reward.
        self.assertEqual(TwoPlayerGameEnv.DEFAULT_REWARD, evaluator.reward)
        # Since we know the given state is not a terminal state, the game should not have ended.
        self.assertFalse(evaluator.done)
        # The NodeType should be the given NodeType.
        self.assertEqual(NodeType.OR, evaluator.node_type)

    def test_single_move(self):
        evaluator = TicTacToeSimpleEvaluator(model=self.env, node_type=NodeType.OR)

        # A single move is made. X plays in the top-left corner.
        evaluator.move(action=0)

        # The reward should just be the default reward.
        self.assertEqual(TwoPlayerGameEnv.DEFAULT_REWARD, evaluator.reward)
        # If the only step is that X plays in the top-left corner, the game should not end.
        self.assertFalse(evaluator.done)
        # Play should always switch to the opponent.
        self.assertEqual(NodeType.AND, evaluator.node_type)

    def test_undo_move(self):
        evaluator = TicTacToeSimpleEvaluator(model=self.env, node_type=NodeType.OR)

        # A single move is made. X plays in the top-left corner.
        evaluator.move(action=0)
        # Undo that move.
        evaluator.undo_move()

        # The evaluator's internal model should be at the initial state.
        # Since we know the given state is not a terminal state, the reward should just be the default reward.
        self.assertEqual(TwoPlayerGameEnv.DEFAULT_REWARD, evaluator.reward)
        # Since we know the given state is not a terminal state, the game should not have ended.
        self.assertFalse(evaluator.done)
        # The NodeType should be the given NodeType.
        self.assertEqual(NodeType.OR, evaluator.node_type)


if __name__ == '__main__':
    unittest.main()
