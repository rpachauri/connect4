import unittest

from connect_four.agents.victor.game import Square
from connect_four.agents.victor.game import Threat

from connect_four.agents.victor.rules import Claimeven
from connect_four.agents.victor.rules import Baseinverse
from connect_four.agents.victor.rules import Vertical
from connect_four.agents.victor.rules import Aftereven
from connect_four.agents.victor.rules import Before

from connect_four.agents.victor.planning import simple_plan


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
            availabilities={square_e4},
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
            threat=Threat(player=1, start=Square(row=4, col=3), end=Square(row=4, col=6)),  # d2-g2
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
            threat=Threat(player=1, start=Square(row=2, col=1), end=Square(row=5, col=4)),  # Threat b4-e1
            verticals=[vertical_e1_e2],
            claimevens=[claimeven_b3_b4],
        )
        want_plan = simple_plan.SimplePlanBuilder([
            simple_plan.from_vertical(vertical=vertical_e1_e2),
            simple_plan.from_claimeven(claimeven=claimeven_b3_b4),
        ]).build()
        got_plan = simple_plan.from_before(before=before_b4_e1)
        self.assertEqual(want_plan, got_plan)


if __name__ == '__main__':
    unittest.main()
