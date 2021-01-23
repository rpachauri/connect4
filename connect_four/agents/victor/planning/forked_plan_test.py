import unittest

from connect_four.agents.victor.game import Square

from connect_four.agents.victor.rules import Claimeven
from connect_four.agents.victor.rules import Baseinverse
from connect_four.agents.victor.rules import Vertical
from connect_four.agents.victor.rules import Lowinverse
from connect_four.agents.victor.rules import Highinverse

from connect_four.agents.victor.planning import simple_plan
from connect_four.agents.victor.planning import forked_plan


class TestForkedPlan(unittest.TestCase):
    def test_from_lowinverse(self):
        square_c2 = Square(row=4, col=2)
        square_c3 = Square(row=3, col=2)
        square_d2 = Square(row=4, col=3)
        square_d3 = Square(row=3, col=3)
        vertical_c2_c3 = Vertical(upper=square_c3, lower=square_c2)  # c2-c3
        vertical_d2_d3 = Vertical(upper=square_d3, lower=square_d2)  # d2-d3
        lowinverse_c2_c3_d2_d3 = Lowinverse(
            first_vertical=vertical_c2_c3,
            second_vertical=vertical_d2_d3,
        )
        want_plan = forked_plan.Fork(
            branches={
                square_c2: forked_plan.Branch(
                    forced_square=square_c3,
                    simple_plan=simple_plan.from_vertical(vertical_d2_d3),
                ),
                square_d2: forked_plan.Branch(
                    forced_square=square_d3,
                    simple_plan=simple_plan.from_vertical(vertical_c2_c3),
                ),
            },
        )
        got_plan = forked_plan.from_lowinverse(lowinverse=lowinverse_c2_c3_d2_d3)
        self.assertEqual(want_plan, got_plan)

    def test_from_highinverse(self):
        square_c2 = Square(row=4, col=2)
        square_c3 = Square(row=3, col=2)
        square_c4 = Square(row=2, col=2)
        square_d2 = Square(row=4, col=3)
        square_d3 = Square(row=3, col=3)
        square_d4 = Square(row=2, col=3)
        vertical_c2_c3 = Vertical(upper=square_c3, lower=square_c2)  # c2-c3
        vertical_d2_d3 = Vertical(upper=square_d3, lower=square_d2)  # d2-d3
        lowinverse_c2_c3_d2_d3 = Lowinverse(
            first_vertical=vertical_c2_c3,
            second_vertical=vertical_d2_d3,
        )
        highinverse_c2_c3_c4_d2_d3_d4 = Highinverse(
            lowinverse=lowinverse_c2_c3_d2_d3,
            directly_playable_squares=[square_c2],  # c2 will be directly playable. d2 will not.
        )
        want_plan = forked_plan.Fork(
            branches={
                square_c2: forked_plan.Branch(
                    forced_square=square_c3,
                    simple_plan=simple_plan.SimplePlanBuilder([
                        simple_plan.from_claimeven(
                            claimeven=Claimeven(upper=square_d4, lower=square_d3),
                        ),
                        square_d2,  # available square.
                        square_c4,  # available square.
                    ]).build(),
                ),
                square_d2: forked_plan.Branch(
                    forced_square=square_d3,
                    simple_plan=simple_plan.SimplePlanBuilder([
                        simple_plan.from_claimeven(
                            claimeven=Claimeven(upper=square_c4, lower=square_c3),
                        ),
                        simple_plan.from_baseinverse(
                            baseinverse=Baseinverse(playable1=square_c2, playable2=square_d4),
                        )
                    ]).build(),
                ),
            },
        )
        got_plan = forked_plan.from_highinverse(highinverse=highinverse_c2_c3_c4_d2_d3_d4)
        self.assertEqual(want_plan, got_plan)


if __name__ == '__main__':
    unittest.main()
