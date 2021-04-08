import unittest

from connect_four.evaluation.victor.game import Square
from connect_four.evaluation.victor.game import Group

from connect_four.evaluation.victor.rules import Claimeven
from connect_four.evaluation.victor.rules import Baseinverse
from connect_four.evaluation.victor.rules import Vertical
from connect_four.evaluation.victor.rules import Aftereven
from connect_four.evaluation.victor.rules import Before
from connect_four.evaluation.victor.rules import Specialbefore

from connect_four.evaluation.victor.threat_hunter import Threat
from connect_four.evaluation.victor.threat_hunter import ThreatCombination
from connect_four.evaluation.victor.threat_hunter import ThreatCombinationType

from connect_four.evaluation.victor.planning import simple_plan


class TestSimplePlan(unittest.TestCase):
    def test_from_claimeven(self):
        # Example from Diagram 5.4.
        square_e3 = Square(row=3, col=4)
        square_e4 = Square(row=2, col=4)
        claimeven_e3_e4 = Claimeven(upper=square_e4, lower=square_e3)
        want_plan = simple_plan.SimplePlan(
            responses={
                square_e3: square_e4,
            },
        )
        got_plan = simple_plan.from_claimeven(claimeven=claimeven_e3_e4)
        self.assertEqual(want_plan, got_plan)

    def test_from_baseinverse(self):
        # Example from Diagram 6.2.
        square_a1 = Square(row=5, col=0)
        square_b1 = Square(row=5, col=1)
        baseinverse_a1_b1 = Baseinverse(playable1=square_a1, playable2=square_b1)
        want_plan = simple_plan.SimplePlan(
            responses={
                square_a1: square_b1,
                square_b1: square_a1,
            }
        )
        got_plan = simple_plan.from_baseinverse(baseinverse=baseinverse_a1_b1)
        self.assertEqual(want_plan, got_plan)

    def test_from_vertical(self):
        # Example from Diagram 6.3.
        square_e4 = Square(row=2, col=4)
        square_e5 = Square(row=1, col=4)
        vertical_e4_e5 = Vertical(upper=square_e5, lower=square_e4)
        want_plan = simple_plan.SimplePlan(
            responses={
                square_e4: square_e5,
            },
            availabilities={square_e4, square_e5},
        )
        got_plan = simple_plan.from_vertical(vertical=vertical_e4_e5)
        self.assertEqual(want_plan, got_plan)

    def test_from_aftereven(self):
        # Example from Diagram 6.5.
        square_f1 = Square(row=5, col=5)
        square_f2 = Square(row=4, col=5)
        square_g1 = Square(row=5, col=6)
        square_g2 = Square(row=4, col=6)
        aftereven_d2_g2 = Aftereven(
            group=Group(player=1, start=Square(row=4, col=3), end=Square(row=4, col=6)),  # d2-g2
            claimevens=[
                Claimeven(upper=square_f2, lower=square_f1),  # Claimeven f1-f2
                Claimeven(upper=square_g2, lower=square_g1),  # Claimeven g1-g2
            ],
        )
        want_plan = simple_plan.SimplePlan(
            responses={
                square_f1: square_f2,
                square_g1: square_g2,
            }
        )
        got_plan = simple_plan.from_aftereven(aftereven=aftereven_d2_g2)
        self.assertEqual(want_plan, got_plan)

    def test_from_before(self):
        # Example from Diagram 6.9.
        square_b3 = Square(row=3, col=1)
        square_b4 = Square(row=2, col=1)
        square_e1 = Square(row=5, col=4)
        square_e2 = Square(row=4, col=4)
        vertical_e1_e2 = Vertical(upper=square_e2, lower=square_e1)
        claimeven_b3_b4 = Claimeven(upper=square_b4, lower=square_b3)
        before_b4_e1 = Before(
            group=Group(player=1, start=Square(row=2, col=1), end=Square(row=5, col=4)),  # Group b4-e1
            verticals=[vertical_e1_e2],
            claimevens=[claimeven_b3_b4],
        )
        want_plan = simple_plan.SimplePlanBuilder([
            simple_plan.from_vertical(vertical=vertical_e1_e2),
            simple_plan.from_claimeven(claimeven=claimeven_b3_b4),
        ]).build()
        got_plan = simple_plan.from_before(before=before_b4_e1)
        self.assertEqual(want_plan, got_plan)

    def test_from_specialbefore(self):
        # Example from Diagram 6.10.
        internal_directly_playable_square_e2 = Square(row=4, col=4)
        square_e3 = Square(row=3, col=4)
        square_f1 = Square(row=5, col=5)
        square_f2 = Square(row=4, col=5)
        square_g1 = Square(row=5, col=6)
        square_g2 = Square(row=4, col=6)
        external_directly_playable_square_d3 = Square(row=3, col=3)

        # Verticals/Claimevens which are part of the Before.
        vertical_e2_e3 = Vertical(upper=square_e3, lower=internal_directly_playable_square_e2)  # Vertical e2-e3.
        claimeven_f1_f2 = Claimeven(upper=square_f2, lower=square_f1)  # Claimeven f1-f2.
        claimeven_g1_g2 = Claimeven(upper=square_g2, lower=square_g1)  # Claimeven g1-g2.

        # Before d2-g2.
        before_d2_g2 = Before(
            group=Group(player=1, start=Square(row=4, col=3), end=Square(row=4, col=6)),  # d2-g2
            verticals=[vertical_e2_e3],
            claimevens=[claimeven_f1_f2, claimeven_g1_g2],
        )
        # Specialbefore d2-g2.
        specialbefore_d2_g2 = Specialbefore(
            before=before_d2_g2,
            internal_directly_playable_square=internal_directly_playable_square_e2,  # e2
            external_directly_playable_square=external_directly_playable_square_d3,  # d3
        )

        want_plan = simple_plan.SimplePlanBuilder([
            simple_plan.from_baseinverse(
                baseinverse=Baseinverse(
                    playable1=internal_directly_playable_square_e2,
                    playable2=external_directly_playable_square_d3,
                )),
            simple_plan.from_claimeven(claimeven=claimeven_f1_f2),
            simple_plan.from_claimeven(claimeven=claimeven_g1_g2),
        ]).build()
        got_plan = simple_plan.from_specialbefore(specialbefore=specialbefore_d2_g2)
        self.assertEqual(want_plan, got_plan)

    def test_from_odd_threat(self):
        # Example from Diagram 8.2.
        square_a1 = Square(row=5, col=0)
        square_a2 = Square(row=4, col=0)
        square_a3 = Square(row=3, col=0)

        # Odd Threat a3-d3.
        odd_threat_a3_d3 = Threat(
            group=Group(player=0, start=square_a3, end=Square(row=3, col=3)),
            empty_square=square_a3,
        )

        want_plan = simple_plan.SimplePlanBuilder([
            square_a1,
            {square_a2: square_a3},
        ]).build()
        got_plan = simple_plan.from_odd_threat(
            odd_threat=odd_threat_a3_d3,
            directly_playable_square=square_a1,
        )
        self.assertEqual(want_plan, got_plan)

    def test_from_threat_combination(self):
        # Example from Diagram 8.3.
        square_f1 = Square(row=5, col=5)
        square_f2 = Square(row=4, col=5)
        square_f3 = Square(row=3, col=5)
        square_f4 = Square(row=2, col=5)
        square_f5 = Square(row=1, col=5)
        square_f6 = Square(row=0, col=5)
        square_g2 = Square(row=4, col=6)
        square_g3 = Square(row=3, col=6)
        square_g4 = Square(row=2, col=6)
        square_g5 = Square(row=1, col=6)
        square_g6 = Square(row=0, col=6)

        # ThreatCombination {d1-g4, d3-g3}.
        threat_combination_d1_g4_d3_g3 = ThreatCombination(
            even_group=Group(player=0, start=Square(row=5, col=3), end=square_g4),  # d1-g4
            odd_group=Group(player=0, start=Square(row=3, col=3), end=square_g3),  # d3-g3
            shared_square=Square(row=3, col=5),  # f3
            even_square=square_g4,
            odd_square=square_g3,
            threat_combination_type=ThreatCombinationType.EvenAboveOdd,
        )
        want_plan = simple_plan.SimplePlanBuilder([
            # Directly playable odd square in the crossing column.
            square_f1,
            # Even squares in crossing column force the odd square above it.
            {
                square_f2: square_f3,
                square_f4: square_f5,
            },
            # Top even square is an availability.
            square_f6,
            # Every empty square in the stacked column forces the square above it.
            {
                square_g2: square_g3,
                square_g3: square_g4,
                square_g4: square_g5,
                square_g5: square_g6,
            },
        ]).build()
        got_plan = simple_plan.from_threat_combination(
            threat_combination=threat_combination_d1_g4_d3_g3,
            directly_playable_crossing_square=square_f1,
            directly_playable_stacked_square=square_g2,
        )
        self.assertEqual(want_plan, got_plan)


if __name__ == '__main__':
    unittest.main()
