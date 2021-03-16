import unittest

from connect_four.agents.pns import PNSNode
from connect_four.evaluation.evaluator import ProofStatus, NodeType


class TestPNS(unittest.TestCase):
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

    def test_OR_PNSNode_select_most_proving_child(self):
        # select_most_proving_child of an OR node should select the child with the smallest proof number.
        node = PNSNode(NodeType.OR)
        node.children[0] = PNSNode(NodeType.AND)
        node.children[0].proof = 2
        node.children[1] = PNSNode(NodeType.AND)
        node.children[1].proof = 0
        node.children[2] = PNSNode(NodeType.AND)
        node.children[2].proof = 3

        best_action, most_proving_child = node.select_most_proving_child()
        self.assertEqual(1, best_action)
        self.assertEqual(node.children[1], most_proving_child)

    def test_AND_PNSNode_select_most_proving_child(self):
        # select_most_proving_child of an OR node should select the child with the smallest proof number.
        node = PNSNode(NodeType.AND)
        node.children[0] = PNSNode(NodeType.OR)
        node.children[0].disproof = 2
        node.children[1] = PNSNode(NodeType.OR)
        node.children[1].disproof = 0
        node.children[2] = PNSNode(NodeType.OR)
        node.children[2].disproof = 3

        best_action, most_proving_child = node.select_most_proving_child()
        self.assertEqual(1, best_action)
        self.assertEqual(node.children[1], most_proving_child)


if __name__ == '__main__':
    unittest.main()
