import gym
import unittest

from connect_four.agents.pns import PNSNode
from connect_four.evaluation.evaluator import ProofStatus
from connect_four.evaluation.tic_tac_toe_simple_evaluator import NodeType
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
        self.assertEqual(evaluator.action_space, len(node.children))
        # Any created children should be AND Nodes.
        self.assertEqual(node.children[0], PNSNode(node_type=NodeType.AND))

    def test_OR_PNSNode_update_tree_base_case(self):
        # The TicTacToeSimpleEvaluator should return ProofStatus.Unknown for all children of the root.
        # This means we'll need a child node for every action in the action space.
        evaluator = TicTacToeSimpleEvaluator(model=self.env, node_type=NodeType.OR)
        node = PNSNode(node_type=NodeType.OR)

        node.update_tree(evaluator=evaluator)

        # There should be a child for every action in the action space.
        self.assertEqual(evaluator.action_space, len(node.children))

        # Since all children were just created, they should each have a proof and disproof number of 1.
        # The proof number of an OR node is the smallest proof number of any child.
        self.assertEqual(1, node.proof)
        # The disproof number of an OR node is the sum disproof number of all children.
        self.assertEqual(evaluator.action_space, node.disproof)


if __name__ == '__main__':
    unittest.main()
