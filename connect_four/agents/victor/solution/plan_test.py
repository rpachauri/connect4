import unittest

from connect_four.agents.victor.game import Square

from connect_four.agents.victor.rules import Claimeven

from connect_four.agents.victor.solution import plan


class TestPlan(unittest.TestCase):
    def test_from_claimeven(self):
        square_e3 = Square(row=3, col=4)
        square_e4 = Square(row=2, col=4)
        claimeven_2_4 = Claimeven(upper=square_e4, lower=square_e3)
        want_plan = plan.Plan(
            follow_up_plans={
                square_e3: square_e4,
            },
        )
        got_plan = plan.from_claimeven(claimeven=claimeven_2_4)
        self.assertEqual(want_plan, got_plan)


if __name__ == '__main__':
    unittest.main()
