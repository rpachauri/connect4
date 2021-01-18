import unittest

from connect_four.agents.victor.game import Square
from connect_four.agents.victor.game import Threat
from connect_four.agents.victor.rules import Rule
from connect_four.agents.victor.solution import Solution

from connect_four.agents.victor.evaluator.evaluator import create_node_graph


class TestEvaluator(unittest.TestCase):
    def test_create_node_graph(self):
        # Note that a Board is not required for create_node_graph().
        # Also note that the Solutions below are not exhaustive
        # (i.e. the Solutions could probably refute more Threats),
        # but it is not necessary for the Solutions to be exhaustive for this test.
        threat_0_0_to_0_3 = Threat(player=0, start=Square(row=0, col=0), end=Square(row=0, col=3))
        solution1 = Solution(
            rule=Rule.Claimeven,
            squares=[
                Square(row=0, col=0),
                Square(row=1, col=0),
            ],
            threats=[threat_0_0_to_0_3],
            claimeven_bottom_squares=[Square(row=1, col=0)],
        )
        threat_1_0_to_4_0 = Threat(player=0, start=Square(row=1, col=0), end=Square(row=4, col=0))
        solution2 = Solution(
            rule=Rule.Vertical,
            squares=[
                Square(row=1, col=0),
                Square(row=2, col=0),
            ],
            threats=[threat_1_0_to_4_0],
        )
        threat_0_1_to_3_4 = Threat(player=1, start=Square(row=0, col=1), end=Square(row=3, col=4))
        solution3 = Solution(
            rule=Rule.Vertical,
            squares=[
                Square(row=0, col=1),
                Square(row=1, col=1),
            ],
            threats=[threat_0_1_to_3_4],
            claimeven_bottom_squares=[Square(row=1, col=1)],
        )
        want_node_graph = {
            threat_0_0_to_0_3: {solution1},
            threat_1_0_to_4_0: {solution2},
            threat_0_1_to_3_4: {solution3},
            solution1: {solution1, solution2},
            solution2: {solution1, solution2},
            solution3: {solution3},
        }
        got_node_graph = create_node_graph({solution1, solution2, solution3})
        self.assertEqual(want_node_graph, got_node_graph)


if __name__ == '__main__':
    unittest.main()
