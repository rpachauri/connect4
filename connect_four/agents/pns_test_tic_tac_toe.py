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

    def test_PNSNode_initialization(self):
        node = PNSNode(NodeType.OR)
        self.assertEqual(1, node.proof)
        self.assertEqual(1, node.disproof)
        self.assertEqual(ProofStatus.Unknown, node.status)
        self.assertFalse(node.children)  # assert that node.children is empty.

    def test_PNSNode_equals(self):
        self.assertEqual(PNSNode(NodeType.OR), PNSNode(NodeType.OR))

    def test_PNSNode_not_equals(self):
        self.assertNotEqual(PNSNode(NodeType.OR), PNSNode(NodeType.AND))

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


if __name__ == '__main__':
    unittest.main()
