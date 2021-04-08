import unittest

from connect_four.evaluation.victor.game import Square
from connect_four.evaluation.victor.game import Group
from connect_four.evaluation.victor.rules import Rule
from connect_four.evaluation.victor.solution import Solution

from connect_four.evaluation.victor.evaluator.evaluator import create_node_graph


class TestEvaluator(unittest.TestCase):
    def test_create_node_graph(self):
        # Note that a Board is not required for create_node_graph().
        # Also note that the Solutions below are not exhaustive
        # (i.e. the Solutions could probably refute more groups),
        # but it is not necessary for the Solutions to be exhaustive for this test.
        group_0_0_to_0_3 = Group(player=0, start=Square(row=0, col=0), end=Square(row=0, col=3))
        solution1 = Solution(
            rule=Rule.Claimeven,
            squares=[
                Square(row=0, col=0),
                Square(row=1, col=0),
            ],
            groups=[group_0_0_to_0_3],
            claimeven_bottom_squares=[Square(row=1, col=0)],
        )
        group_1_0_to_4_0 = Group(player=0, start=Square(row=1, col=0), end=Square(row=4, col=0))
        solution2 = Solution(
            rule=Rule.Vertical,
            squares=[
                Square(row=1, col=0),
                Square(row=2, col=0),
            ],
            groups=[group_1_0_to_4_0],
        )
        group_0_1_to_3_4 = Group(player=1, start=Square(row=0, col=1), end=Square(row=3, col=4))
        solution3 = Solution(
            rule=Rule.Vertical,
            squares=[
                Square(row=0, col=1),
                Square(row=1, col=1),
            ],
            groups=[group_0_1_to_3_4],
            claimeven_bottom_squares=[Square(row=1, col=1)],
        )
        want_node_graph = {
            group_0_0_to_0_3: {solution1},
            group_1_0_to_4_0: {solution2},
            group_0_1_to_3_4: {solution3},
            solution1: {solution1, solution2},
            solution2: {solution1, solution2},
            solution3: {solution3},
        }
        got_node_graph = create_node_graph({solution1, solution2, solution3})
        self.assertEqual(want_node_graph, got_node_graph)


if __name__ == '__main__':
    unittest.main()
