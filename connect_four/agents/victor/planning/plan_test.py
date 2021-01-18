import unittest

from connect_four.agents.victor.game import Square

from connect_four.agents.victor.rules import Claimeven
from connect_four.agents.victor.rules import Baseinverse
from connect_four.agents.victor.rules import Vertical

from connect_four.agents.victor.planning import plan


class TestPlan(unittest.TestCase):
    def test_from_claimeven(self):
        square_e3 = Square(row=3, col=4)
        square_e4 = Square(row=2, col=4)
        claimeven_2_4 = Claimeven(upper=square_e4, lower=square_e3)
        want_plan = plan.Plan(
            responses={
                square_e3: square_e4,
            },
        )
        got_plan = plan.from_claimeven(claimeven=claimeven_2_4)
        self.assertEqual(want_plan, got_plan)

        want_plan_after_execution = plan.Plan()
        got_response = got_plan.execute(square_e3)
        self.assertEqual(square_e4, got_response)
        self.assertEqual(want_plan_after_execution, got_plan)

    def test_from_baseinverse(self):
        square_a1 = Square(row=5, col=0)
        square_a2 = Square(row=5, col=1)
        baseinverse_a1_b1 = Baseinverse(playable1=square_a1, playable2=square_a2)
        want_plan = plan.Plan(
            responses={
                square_a1: square_a2,
                square_a2: square_a1,
            }
        )
        got_plan = plan.from_baseinverse(baseinverse=baseinverse_a1_b1)
        self.assertEqual(want_plan, got_plan)

        want_plan_after_execution = plan.Plan()
        got_response = got_plan.execute(square_a1)
        self.assertEqual(square_a2, got_response)
        self.assertEqual(want_plan_after_execution, got_plan)

    def test_from_vertical(self):
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


if __name__ == '__main__':
    unittest.main()
