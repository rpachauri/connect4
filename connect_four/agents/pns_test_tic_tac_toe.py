import gym
import unittest

import numpy as np

from connect_four.agents.pns import PNSNode
from connect_four.agents.pns import PNS
from connect_four.evaluation.evaluator import NodeType
from connect_four.evaluation.tic_tac_toe_simple_evaluator import TicTacToeSimpleEvaluator


class TestPNSTicTacToe(unittest.TestCase):
    """
    TestPNSTicTacToe tests the Proof-Number Search algorithm for the TicTacToe environment.
    """
    def setUp(self):
        self.env = gym.make('tic_tac_toe-v0')
        self.env.reset()

    def test_PNSNode_expand_all_children(self):
        # The TicTacToeSimpleEvaluator should return ProofStatus.Unknown for all children of the root.
        # This means we'll need a child node for every action in the action space.
        evaluator = TicTacToeSimpleEvaluator(model=self.env, node_type=NodeType.OR)
        node = PNSNode(node_type=NodeType.OR)

        node.expand(evaluator=evaluator)

        # There should be a child for every action in the action space.
        self.assertEqual(len(evaluator.actions()), len(node.children))
        # Any created children should be AND Nodes.
        self.assertEqual(node.children[0], PNSNode(node_type=NodeType.AND))

    def test_OR_PNSNode_update_tree_base_case_initial_state(self):
        # The TicTacToeSimpleEvaluator should return ProofStatus.Unknown for all children of the root.
        # This means we'll need a child node for every action in the action space.
        evaluator = TicTacToeSimpleEvaluator(model=self.env, node_type=NodeType.OR)
        node = PNSNode(node_type=NodeType.OR)

        node.update_tree(evaluator=evaluator)

        # There should be a child for every action in the action space.
        self.assertEqual(len(evaluator.actions()), len(node.children))

        # Since all children were just created, they should each have a proof and disproof number of 1.
        # The proof number of an OR node is the smallest proof number of any child.
        self.assertEqual(1, node.proof)
        # The disproof number of an OR node is the sum disproof number of all children.
        self.assertEqual(len(evaluator.actions()), node.disproof)

    def test_OR_PNSNode_update_tree_base_case_02_11_20_22(self):
        self.env.state = np.array([
            [
                [0, 0, 1, ],
                [0, 0, 0, ],
                [1, 0, 0, ],
            ],
            [
                [0, 0, 0, ],
                [0, 1, 0, ],
                [0, 0, 1, ],
            ],
        ])
        # X can win by playing 0.
        evaluator = TicTacToeSimpleEvaluator(model=self.env, node_type=NodeType.OR)
        node = PNSNode(node_type=NodeType.OR)

        node.update_tree(evaluator=evaluator)

        # The proof number of an OR node is the smallest proof number of any child.
        # Since all children were just created, they should each have a proof number of 1.
        self.assertEqual(1, node.proof)
        # The disproof number of an OR node is the sum disproof number of all children.
        # 4 of the children would be INVALID_MOVES for OR, so they should have a disproof number of 0.
        self.assertEqual(5, node.disproof)

    def test_AND_PNSNode_update_tree_02_11_20_22_00(self):
        # This position is a guaranteed win for OR.
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
        evaluator = TicTacToeSimpleEvaluator(model=self.env, node_type=NodeType.AND)
        node = PNSNode(node_type=NodeType.AND)

        node.update_tree(evaluator=evaluator)

        # The proof number of an AND node is the sum proof number of all children.
        # 5 of the children would be INVALID_MOVES for AND, so they should have a proof number of 0.
        self.assertEqual(4, node.proof)
        # The disproof number of an AND node is the smallest disproof number of any child.
        # Since all children were just created, they should each have a disproof number of 1.
        self.assertEqual(1, node.disproof)

        # Since we know this position is a guaranteed win for OR, we know that either:
        # 1. The proof number will decrease
        # or
        # 2. The disproof number will increase.
        node.update_tree(evaluator=evaluator)
        self.assertTrue(4 >= node.proof)
        self.assertTrue(1 <= node.disproof)

    def test_PNS_Proven_action_last_action_is_None(self):
        self.env.state = np.array([
            [
                [0, 0, 1, ],
                [0, 0, 0, ],
                [1, 0, 0, ],
            ],
            [
                [0, 0, 0, ],
                [0, 1, 0, ],
                [0, 0, 1, ],
            ],
        ])
        # X can win by playing 0.
        evaluator = TicTacToeSimpleEvaluator(model=self.env, node_type=NodeType.OR)
        pns = PNS(evaluator=evaluator)

        action = pns.action(env=self.env)
        self.assertEqual(0, action)

    def test_PNS_Proven_action_last_action_is_not_None(self):
        self.env.state = np.array([
            [
                [0, 0, 1, ],
                [0, 0, 0, ],
                [1, 0, 0, ],
            ],
            [
                [0, 0, 0, ],
                [0, 1, 0, ],
                [0, 0, 0, ],
            ],
        ])
        self.env.player_turn = 1
        evaluator = TicTacToeSimpleEvaluator(model=self.env, node_type=NodeType.AND)
        pns = PNS(evaluator=evaluator)

        # O plays in the bottom-right corner.
        self.env.step(action=8)

        # X can win by playing 0.
        action = pns.action(env=self.env, last_action=8)
        self.assertEqual(0, action)


if __name__ == '__main__':
    unittest.main()
