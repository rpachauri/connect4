import unittest

from connect_four.evaluation.victor.rules import Claimeven, Baseinverse, Vertical, Aftereven, Lowinverse, Highinverse, \
    Baseclaim
from connect_four.evaluation.victor.solution import solution2
from connect_four.game import Square
from connect_four.problem import Group


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
        baseinverse_a1_b1 = Baseinverse(playable1=Square(row=5, col=0), playable2=Square(row=5, col=1))

        got_solution = solution2.from_baseinverse(baseinverse=baseinverse_a1_b1)
        want_solution = solution2.Solution(
            rule_instance=baseinverse_a1_b1,
            squares=frozenset(baseinverse_a1_b1.squares),
        )
        self.assertEqual(want_solution, got_solution)

    def test_from_vertical(self):
        vertical_e4_e5 = Vertical(upper=Square(row=2, col=4), lower=Square(row=1, col=4))

        got_solution = solution2.from_vertical(vertical_e4_e5)
        want_solution = solution2.Solution(
            rule_instance=vertical_e4_e5,
            squares=frozenset([vertical_e4_e5.upper, vertical_e4_e5.lower]),
        )
        self.assertEqual(want_solution, got_solution)

    def test_from_aftereven(self):
        aftereven_d2_g2 = Aftereven(
            group=Group(player=1, start=Square(row=4, col=3), end=Square(row=4, col=6)),  # d2-g2
            claimevens=[
                Claimeven(upper=Square(row=4, col=5), lower=Square(row=5, col=5)),  # Claimeven f1-f2
                Claimeven(upper=Square(row=4, col=6), lower=Square(row=5, col=6)),  # Claimeven g1-g2
            ],
        )

        got_solution = solution2.from_aftereven(aftereven_d2_g2)
        want_solution = solution2.Solution(
            squares=frozenset([
                # Squares from d2-g2.
                Square(row=4, col=3),
                Square(row=4, col=4),
                Square(row=4, col=5),
                Square(row=4, col=6),
                # Lower squares of Claimevens.
                Square(row=5, col=5),
                Square(row=5, col=6),
            ]),
            claimeven_bottom_squares=[
                # Lower squares of Claimevens.
                Square(row=5, col=5),
                Square(row=5, col=6),
            ],
            rule_instance=aftereven_d2_g2,
        )
        self.assertEqual(want_solution, got_solution)

    def test_from_lowinverse(self):
        lowinverse_c2_c3_d2_d3 = Lowinverse(
            first_vertical=Vertical(upper=Square(row=3, col=2), lower=Square(row=4, col=2)),  # c2-c3
            second_vertical=Vertical(upper=Square(row=3, col=3), lower=Square(row=4, col=3)),  # d2-d3
        )

        got_solution = solution2.from_lowinverse(lowinverse_c2_c3_d2_d3)
        want_solution = solution2.Solution(
            rule_instance=lowinverse_c2_c3_d2_d3,
            squares=frozenset([
                Square(row=3, col=2),
                Square(row=4, col=2),
                Square(row=3, col=3),
                Square(row=4, col=3),
            ]),
        )
        self.assertEqual(want_solution, got_solution)

    def test_from_highinverse(self):
        lowinverse_c2_c3_d2_d3 = Lowinverse(
            first_vertical=Vertical(upper=Square(row=3, col=2), lower=Square(row=4, col=2)),  # c2-c3
            second_vertical=Vertical(upper=Square(row=3, col=3), lower=Square(row=4, col=3)),  # d2-d3
        )
        highinverse_c2_c3_c4_d2_d3_d4 = Highinverse(
            lowinverse=lowinverse_c2_c3_d2_d3,
            directly_playable_squares=[Square(row=4, col=2), Square(row=4, col=3)],  # c2 and d2
        )
        want_solution = solution2.Solution(
            rule_instance=highinverse_c2_c3_c4_d2_d3_d4,
            squares=frozenset([
                Square(row=2, col=2),  # c4
                Square(row=3, col=2),  # c3
                Square(row=4, col=2),  # c2
                Square(row=2, col=3),  # d4
                Square(row=3, col=3),  # d3
                Square(row=4, col=3),  # d2
            ]),
        )
        got_solution = solution2.from_highinverse(
            highinverse=highinverse_c2_c3_c4_d2_d3_d4,
        )
        self.assertEqual(want_solution, got_solution)

    def test_from_baseclaim(self):
        baseclaim_b1_c1_c2_f1 = Baseclaim(
            first=Square(row=5, col=1),  # b1
            second=Square(row=5, col=2),  # c1
            third=Square(row=5, col=4),  # e1
        )

        got_solution = solution2.from_baseclaim(
            baseclaim=baseclaim_b1_c1_c2_f1,
        )
        want_solution = solution2.Solution(
            rule_instance=baseclaim_b1_c1_c2_f1,
            squares=frozenset([
                Square(row=5, col=1),  # b1
                Square(row=5, col=2),  # c1
                Square(row=4, col=2),  # c2
                Square(row=5, col=4),  # e1
            ]),
            claimeven_bottom_squares=[
                Square(row=5, col=2),  # c1
            ],
        )
        self.assertEqual(want_solution, got_solution)


if __name__ == '__main__':
    unittest.main()
