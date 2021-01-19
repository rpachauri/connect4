import unittest

from connect_four.agents.victor.game import Square
from connect_four.agents.victor.game import Threat

from connect_four.agents.victor.rules import Claimeven
from connect_four.agents.victor.rules import Baseinverse
from connect_four.agents.victor.rules import Vertical
from connect_four.agents.victor.rules import Aftereven
from connect_four.agents.victor.rules import Lowinverse

from connect_four.agents.victor.planning import plan


class TestPlan(unittest.TestCase):
    def test_from_claimeven(self):
        # Example from Diagram 5.4.
        square_e3 = Square(row=3, col=4)
        square_e4 = Square(row=2, col=4)
        claimeven_e3_e4 = Claimeven(upper=square_e4, lower=square_e3)
        want_plan = plan.Plan(
            responses={
                square_e3: square_e4,
            },
        )
        got_plan = plan.from_claimeven(claimeven=claimeven_e3_e4)
        self.assertEqual(want_plan, got_plan)

        want_plan_after_execution = plan.Plan()
        got_response = got_plan.execute(square_e3)
        self.assertEqual(square_e4, got_response)
        self.assertEqual(want_plan_after_execution, got_plan)

    def test_merge_claimeven(self):
        square_e3 = Square(row=3, col=4)
        square_e4 = Square(row=2, col=4)
        claimeven_plan_e3_e4 = plan.from_claimeven(
            claimeven=Claimeven(upper=square_e4, lower=square_e3),
        )
        square_a1 = Square(row=5, col=0)
        square_a2 = Square(row=4, col=0)
        claimeven_plan_a1_a2 = plan.from_claimeven(
            claimeven=Claimeven(upper=square_a2, lower=square_a1),
        )

        want_plan_after_merging = plan.Plan(
            responses={
                square_e3: square_e4,
                square_a1: square_a2,
            },
        )
        claimeven_plan_e3_e4.merge(plan=claimeven_plan_a1_a2)
        self.assertEqual(want_plan_after_merging, claimeven_plan_e3_e4)

    def test_from_baseinverse(self):
        # Example from Diagram 6.2.
        square_a1 = Square(row=5, col=0)
        square_b1 = Square(row=5, col=1)
        baseinverse_a1_b1 = Baseinverse(playable1=square_a1, playable2=square_b1)
        want_plan = plan.Plan(
            responses={
                square_a1: square_b1,
                square_b1: square_a1,
            }
        )
        got_plan = plan.from_baseinverse(baseinverse=baseinverse_a1_b1)
        self.assertEqual(want_plan, got_plan)

        want_plan_after_execution = plan.Plan()
        got_response = got_plan.execute(square_a1)
        self.assertEqual(square_b1, got_response)
        self.assertEqual(want_plan_after_execution, got_plan)

    def test_impossible_merge(self):
        # Example from Diagram 6.7.
        square_c1 = Square(row=5, col=2)
        square_c2 = Square(row=4, col=2)
        claimeven_c1_c2 = Claimeven(upper=square_c2, lower=square_c1)
        square_e1 = Square(row=5, col=4)
        baseinverse_c1_e1 = Baseinverse(playable1=square_c1, playable2=square_e1)

        claimeven_plan_c1_c2 = plan.from_claimeven(claimeven=claimeven_c1_c2)
        baseinverse_plan_c1_e1 = plan.from_baseinverse(baseinverse=baseinverse_c1_e1)

        raises = False
        try:
            claimeven_plan_c1_c2.merge(baseinverse_plan_c1_e1)
        except ValueError:
            raises = True
        self.assertTrue(raises)

    def test_from_vertical(self):
        # Example from Diagram 6.3.
        square_e4 = Square(row=2, col=4)
        square_e5 = Square(row=1, col=4)
        vertical_e4_e5 = Vertical(upper=square_e5, lower=square_e4)
        want_plan = plan.Plan(
            responses={
                square_e4: square_e5,
            },
            availabilities={square_e4},
        )
        got_plan = plan.from_vertical(vertical=vertical_e4_e5)
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
        want_plan = plan.Plan(
            responses={
                square_f1: square_f2,
                square_g1: square_g2,
            }
        )
        got_plan = plan.from_aftereven(aftereven=aftereven_d2_g2)
        self.assertEqual(want_plan, got_plan)

        want_plan_after_execution = plan.Plan(
            responses={
                square_g1: square_g2,
            }
        )
        got_response = got_plan.execute(square=square_f1)
        self.assertEqual(square_f2, got_response)
        self.assertEqual(want_plan_after_execution, got_plan)

    def test_from_lowinverse(self):
        square_c2 = Square(row=4, col=2)
        square_c3 = Square(row=3, col=2)
        square_d2 = Square(row=4, col=3)
        square_d3 = Square(row=3, col=3)
        lowinverse_c2_c3_d2_d3 = Lowinverse(
            first_vertical=Vertical(upper=square_c3, lower=square_c2),  # c2-c3
            second_vertical=Vertical(upper=square_d3, lower=square_d2),  # d2-d3
        )
        want_plan = plan.Plan(
            responses={
                square_c2: plan.Plan(
                    forced_square=square_c3,
                    responses={
                        square_d2: plan.Plan(
                            forced_square=square_d3,
                        )
                    },
                    availabilities={square_d2},
                ),
                square_d2: plan.Plan(
                    forced_square=square_d3,
                    responses={
                        square_c2: plan.Plan(
                            forced_square=square_c3,
                        )
                    },
                    availabilities={square_c2},
                ),
            },
        )
        got_plan = plan.from_lowinverse(lowinverse=lowinverse_c2_c3_d2_d3)
        self.assertEqual(want_plan, got_plan)


if __name__ == '__main__':
    unittest.main()
