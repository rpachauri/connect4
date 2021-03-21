import unittest

from connect_four.agents import DFPN
from connect_four.evaluation import ProofStatus, NodeType


class TestDFPN(unittest.TestCase):
    def test_determine_phi_delta_OR_Proven(self):
        got_phi, got_delta = DFPN.determine_phi_delta(node_type=NodeType.OR, status=ProofStatus.Proven)
        self.assertEqual(0, got_phi)
        self.assertEqual(float('inf'), got_delta)

    def test_determine_phi_delta_OR_Disproven(self):
        got_phi, got_delta = DFPN.determine_phi_delta(node_type=NodeType.OR, status=ProofStatus.Disproven)
        self.assertEqual(float('inf'), got_phi)
        self.assertEqual(0, got_delta)

    def test_determine_phi_delta_AND_Proven(self):
        got_phi, got_delta = DFPN.determine_phi_delta(node_type=NodeType.AND, status=ProofStatus.Proven)
        self.assertEqual(float('inf'), got_phi)
        self.assertEqual(0, got_delta)

    def test_determine_phi_delta_AND_Disproven(self):
        got_phi, got_delta = DFPN.determine_phi_delta(node_type=NodeType.AND, status=ProofStatus.Disproven)
        self.assertEqual(0, got_phi)
        self.assertEqual(float('inf'), got_delta)


if __name__ == '__main__':
    unittest.main()
