import unittest

from connect_four.evaluation.victor.rules import Claimeven, Baseinverse
from connect_four.evaluation.victor.solution import solution2
from connect_four.game import Square


class TestSolution(unittest.TestCase):
    def test_from_claimeven(self):
        claimeven_2_4 = Claimeven(upper=Square(row=2, col=4), lower=Square(row=3, col=4))
        want_solution = solution2.Solution(
            rule_instance=claimeven_2_4,
            squares=[claimeven_2_4.upper, claimeven_2_4.lower],
            claimeven_bottom_squares=[claimeven_2_4.lower],
        )
        got_solution = solution2.from_claimeven(claimeven=claimeven_2_4)
        self.assertEqual(want_solution, got_solution)

    def test_from_baseinverse(self):
        # The Baseinverse a1-b1 solves a1-d1.
        baseinverse_a1_b1 = Baseinverse(playable1=Square(row=5, col=0), playable2=Square(row=5, col=1))

        got_solution = solution2.from_baseinverse(baseinverse=baseinverse_a1_b1)
        want_solution = solution2.Solution(
            rule_instance=baseinverse_a1_b1,
            squares=frozenset(baseinverse_a1_b1.squares),
        )
        self.assertEqual(want_solution, got_solution)


if __name__ == '__main__':
    unittest.main()
