import unittest

from connect_four.evaluation.victor.rules import Claimeven
from connect_four.evaluation.victor.solution.solution2 import Solution
from connect_four.game import Square


class TestSolution(unittest.TestCase):
    def test_from_claimeven(self):
        claimeven_2_4 = Claimeven(upper=Square(row=2, col=4), lower=Square(row=3, col=4))
        solution = Solution(rule_instance=claimeven_2_4)

        # Validate Solution fields.
        self.assertEqual(claimeven_2_4, solution.rule_instance)
        self.assertEqual(frozenset([claimeven_2_4.upper, claimeven_2_4.lower]), solution.squares)
        self.assertEqual(frozenset(claimeven_2_4.lower), solution.claimeven_bottom_squares)


if __name__ == '__main__':
    unittest.main()
