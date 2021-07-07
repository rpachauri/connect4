import unittest

from connect_four.evaluation.victor.rules import Claimeven, Baseinverse, Vertical, Aftereven, Lowinverse, Highinverse, \
    Baseclaim, Before, Specialbefore, Oddthreat
from connect_four.evaluation.victor.rules.highinverse import HighinverseColumn
from connect_four.evaluation.incremental_victor.solution import victor_solution
from connect_four.evaluation.incremental_victor.solution.solution import SolutionType
from connect_four.game import Square
from connect_four.problem import Group


class TestSolution(unittest.TestCase):
    def test_from_claimeven(self):
        claimeven_2_4 = Claimeven(upper=Square(row=2, col=4), lower=Square(row=3, col=4))
        want_solution = victor_solution.VictorSolution(
            rule_instance=claimeven_2_4,
            squares=[claimeven_2_4.upper, claimeven_2_4.lower],
            solution_type=SolutionType.SHARED,
            claimeven_bottom_squares=[claimeven_2_4.lower],
        )
        got_solution = victor_solution.from_claimeven(claimeven=claimeven_2_4)
        self.assertEqual(want_solution, got_solution)

    def test_from_baseinverse(self):
        baseinverse_a1_b1 = Baseinverse(playable1=Square(row=5, col=0), playable2=Square(row=5, col=1))

        got_solution = victor_solution.from_baseinverse(baseinverse=baseinverse_a1_b1)
        want_solution = victor_solution.VictorSolution(
            rule_instance=baseinverse_a1_b1,
            solution_type=SolutionType.SHARED,
            squares=frozenset(baseinverse_a1_b1.squares),
        )
        self.assertEqual(want_solution, got_solution)

    def test_from_vertical(self):
        vertical_e4_e5 = Vertical(upper=Square(row=2, col=4), lower=Square(row=1, col=4))

        got_solution = victor_solution.from_vertical(vertical_e4_e5)
        want_solution = victor_solution.VictorSolution(
            rule_instance=vertical_e4_e5,
            solution_type=SolutionType.SHARED,
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

        got_solution = victor_solution.from_aftereven(aftereven_d2_g2)
        want_solution = victor_solution.VictorSolution(
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
            solution_type=SolutionType.BLACK,
        )
        self.assertEqual(want_solution, got_solution)

    def test_from_lowinverse(self):
        lowinverse_c2_c3_d2_d3 = Lowinverse(
            first_vertical=Vertical(upper=Square(row=3, col=2), lower=Square(row=4, col=2)),  # c2-c3
            second_vertical=Vertical(upper=Square(row=3, col=3), lower=Square(row=4, col=3)),  # d2-d3
        )

        got_solution = victor_solution.from_lowinverse(lowinverse_c2_c3_d2_d3)
        want_solution = victor_solution.VictorSolution(
            rule_instance=lowinverse_c2_c3_d2_d3,
            squares=frozenset([
                Square(row=3, col=2),
                Square(row=4, col=2),
                Square(row=3, col=3),
                Square(row=4, col=3),
            ]),
            solution_type=SolutionType.SHARED,
        )
        self.assertEqual(want_solution, got_solution)

    def test_from_highinverse_using_highinverse_columns(self):
        highinverse_c2_c3_c4_d2_d3_d4 = Highinverse(
            columns={
                HighinverseColumn(
                    upper=Square(row=2, col=2),  # c4
                    middle=Square(row=3, col=2),  # c3
                    lower=Square(row=4, col=2),  # c2
                    directly_playable=False,
                ),
                HighinverseColumn(
                    upper=Square(row=2, col=3),  # d4
                    middle=Square(row=3, col=3),  # d3
                    lower=Square(row=4, col=3),  # d2
                    directly_playable=False,
                ),
            }
        )
        want_solution = victor_solution.VictorSolution(
            rule_instance=highinverse_c2_c3_c4_d2_d3_d4,
            squares=frozenset([
                Square(row=2, col=2),  # c4
                Square(row=3, col=2),  # c3
                Square(row=4, col=2),  # c2
                Square(row=2, col=3),  # d4
                Square(row=3, col=3),  # d3
                Square(row=4, col=3),  # d2
            ]),
            solution_type=SolutionType.SHARED,
        )
        got_solution = victor_solution.from_highinverse(
            highinverse=highinverse_c2_c3_c4_d2_d3_d4,
        )
        self.assertEqual(want_solution, got_solution)

    def test_from_baseclaim(self):
        baseclaim_b1_c1_c2_f1 = Baseclaim(
            first=Square(row=5, col=1),  # b1
            second=Square(row=5, col=2),  # c1
            third=Square(row=5, col=4),  # e1
        )

        got_solution = victor_solution.from_baseclaim(
            baseclaim=baseclaim_b1_c1_c2_f1,
        )
        want_solution = victor_solution.VictorSolution(
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
            solution_type=SolutionType.SHARED,
        )
        self.assertEqual(want_solution, got_solution)

    def test_from_before(self):
        before_b4_e1 = Before(
            group=Group(player=1, start=Square(row=2, col=1), end=Square(row=5, col=4)),  # Group b4-e1
            verticals=[
                Vertical(upper=Square(row=4, col=4), lower=Square(row=5, col=4)),  # Vertical e1-e2
            ],
            claimevens=[
                Claimeven(upper=Square(row=2, col=1), lower=Square(row=3, col=1))  # Claimeven b3-b4
            ]
        )

        got_solution = victor_solution.from_before(before_b4_e1)
        want_solution = victor_solution.VictorSolution(
            rule_instance=before_b4_e1,
            squares=frozenset([
                # Empty squares part of the Before group.
                Square(row=2, col=1),  # b4
                Square(row=5, col=4),  # e1
                # Squares part of Claimevens/Verticals not part of the Before group.
                Square(row=3, col=1),  # b3
                Square(row=4, col=4),  # e2
            ]),
            claimeven_bottom_squares=[
                Square(row=3, col=1),  # b3
            ],
            solution_type=SolutionType.BLACK,
        )
        self.assertEqual(want_solution, got_solution)

    def test_from_specialbefore(self):
        # Verticals/Claimevens which are part of the Before.
        vertical_e2_e3 = Vertical(upper=Square(row=3, col=4), lower=Square(row=4, col=4))  # Vertical e2-e3.
        claimeven_f1_f2 = Claimeven(upper=Square(row=4, col=5), lower=Square(row=5, col=5))  # Claimeven f1-f2.
        claimeven_g1_g2 = Claimeven(upper=Square(row=4, col=6), lower=Square(row=5, col=6))  # Claimeven g1-g2.

        # Before d2-g2.
        before_d2_g2 = Before(
            group=Group(player=1, start=Square(row=4, col=3), end=Square(row=4, col=6)),  # d2-g2
            verticals=[vertical_e2_e3],
            claimevens=[claimeven_f1_f2, claimeven_g1_g2],
        )
        # Specialbefore d2-g2.
        specialbefore_d2_g2 = Specialbefore(
            before=before_d2_g2,
            internal_directly_playable_square=Square(row=4, col=4),  # e2
            external_directly_playable_square=Square(row=3, col=3),  # d3
        )

        got_solution = victor_solution.from_specialbefore(
            specialbefore=specialbefore_d2_g2,
        )
        want_solution = victor_solution.VictorSolution(
            rule_instance=specialbefore_d2_g2,
            squares=frozenset([
                # Empty squares part of the Specialbefore group.
                Square(row=4, col=4),  # e2. Note that this is the internal directly playable square.
                Square(row=4, col=5),  # f2
                Square(row=4, col=6),  # g2
                # Squares not part of the Specialbefore group but are
                # part of Verticals/Claimevens which are part of the Specialbefore.
                # Square(row=3, col=4),  # e3 is the upper Square of Vertical e2-e3 and does not get used.
                Square(row=5, col=5),  # f1 is the lower Square of Claimeven f1-f2.
                Square(row=5, col=6),  # g1 is the lower Square of Claimeven g1-g2.
                # Directly playable square not part of the Specialbefore group.
                Square(row=3, col=3),  # d3
            ]),
            claimeven_bottom_squares=[
                Square(row=5, col=5),  # f1 is the lower Square of Claimeven f1-f2.
                Square(row=5, col=6),  # g1 is the lower Square of Claimeven g1-g2.
            ],
            solution_type=SolutionType.BLACK,
        )
        self.assertEqual(want_solution, got_solution)

    def test_from_odd_threat(self):
        odd_threat_a3_d3 = Oddthreat(
            group=Group(player=0, start=Square(row=3, col=0), end=Square(row=3, col=3)),  # a3-d3
            empty_square=Square(row=3, col=0),  # a3
            directly_playable_square=Square(row=5, col=0),  # a1
        )

        got_solution = victor_solution.from_odd_threat(odd_threat=odd_threat_a3_d3)
        want_solution = victor_solution.VictorSolution(
            rule_instance=odd_threat_a3_d3,
            squares=[Square(row=3, col=0)],  # a3
            solution_type=SolutionType.WHITE,
        )
        self.assertEqual(want_solution, got_solution)


if __name__ == '__main__':
    unittest.main()
