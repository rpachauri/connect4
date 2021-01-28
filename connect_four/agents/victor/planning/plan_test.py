import unittest

from connect_four.agents.victor.game import Square

from connect_four.agents.victor.rules import Claimeven
from connect_four.agents.victor.rules import Baseinverse
from connect_four.agents.victor.rules import Vertical

from connect_four.agents.victor.planning import plan


class TestPlan(unittest.TestCase):
    def test_evaluate_diagram_6_1(self):
        # This test case is based on Diagram 6.1.

        # Define all Squares that will be used in Claimevens.
        square_a1 = Square(row=5, col=0)
        square_a2 = Square(row=4, col=0)
        square_a5 = Square(row=1, col=0)
        square_a6 = Square(row=0, col=0)
        square_b1 = Square(row=5, col=1)
        square_b2 = Square(row=4, col=1)
        square_b3 = Square(row=3, col=1)
        square_b4 = Square(row=2, col=1)
        square_b5 = Square(row=1, col=1)
        square_b6 = Square(row=0, col=1)
        square_c3 = Square(row=3, col=2)
        square_c4 = Square(row=2, col=2)
        square_e3 = Square(row=3, col=4)
        square_e4 = Square(row=2, col=4)
        square_f1 = Square(row=5, col=5)
        square_f2 = Square(row=4, col=5)
        square_f3 = Square(row=3, col=5)
        square_f4 = Square(row=2, col=5)
        square_f5 = Square(row=1, col=5)
        square_f6 = Square(row=0, col=5)
        square_g1 = Square(row=5, col=6)
        square_g2 = Square(row=4, col=6)
        square_g5 = Square(row=1, col=6)
        square_g6 = Square(row=0, col=6)

        # Define the Claimevens.
        claimeven_a1_a2 = Claimeven(lower=square_a1, upper=square_a2)
        claimeven_a5_a6 = Claimeven(lower=square_a5, upper=square_a6)
        claimeven_b1_b2 = Claimeven(lower=square_b1, upper=square_b2)
        claimeven_b3_b4 = Claimeven(lower=square_b3, upper=square_b4)
        claimeven_b5_b6 = Claimeven(lower=square_b5, upper=square_b6)
        claimeven_c3_c4 = Claimeven(lower=square_c3, upper=square_c4)
        claimeven_e3_e4 = Claimeven(lower=square_e3, upper=square_e4)
        claimeven_f1_f2 = Claimeven(lower=square_f1, upper=square_f2)
        claimeven_f3_f4 = Claimeven(lower=square_f3, upper=square_f4)
        claimeven_f5_f6 = Claimeven(lower=square_f5, upper=square_f6)
        claimeven_g1_g2 = Claimeven(lower=square_g1, upper=square_g2)
        claimeven_g5_g6 = Claimeven(lower=square_g5, upper=square_g6)

        # Combine the Claimevens into an iterable of Rule applications.
        rule_applications = [
            claimeven_a1_a2,
            claimeven_a5_a6,
            claimeven_b1_b2,
            claimeven_b3_b4,
            claimeven_b5_b6,
            claimeven_c3_c4,
            claimeven_e3_e4,
            claimeven_f1_f2,
            claimeven_f3_f4,
            claimeven_f5_f6,
            claimeven_g1_g2,
            claimeven_g5_g6,
        ]
        pure_claimeven_plan = plan.Plan(rule_applications=rule_applications)

        # Verify that the upper of a Claimeven is the response to the lower of a Claimeven even
        # when there are no other directly playable squares.
        got_response = pure_claimeven_plan.execute(square=square_a1, directly_playable_squares={})
        self.assertEqual(square_a2, got_response)

    def test_evaluate_diagram_6_2(self):
        # This test case is based on Diagram 6.2.

        # Define all the Squares that will be used in Baseinverses.
        square_a1 = Square(row=5, col=0)
        square_b1 = Square(row=5, col=1)
        square_c4 = Square(row=2, col=2)
        square_d3 = Square(row=3, col=3)
        square_e2 = Square(row=4, col=4)
        square_f1 = Square(row=5, col=5)
        square_g1 = Square(row=5, col=6)
        square_g2 = Square(row=4, col=5)

        directly_playable_squares = {
            square_a1,
            square_b1,
            square_c4,
            square_d3,
            square_e2,
            square_f1,
            square_g1,
        }

        # Define a set of Baseinverses that can be used together.
        baseinverse_a1_b1 = Baseinverse(playable1=square_a1, playable2=square_b1)
        baseinverse_c4_d3 = Baseinverse(playable1=square_c4, playable2=square_d3)
        baseinverse_e2_f1 = Baseinverse(playable1=square_e2, playable2=square_f1)

        # Combine the Baseinverses into an iterable of Rule applications.
        rule_applications = [
            baseinverse_a1_b1,
            baseinverse_c4_d3,
            baseinverse_e2_f1,
        ]
        pure_baseinverse_plan = plan.Plan(rule_applications=rule_applications, availabilities={square_g1, square_g2})

        # Verify that g2 is the response when g1 is played because all squares part of the Baseinverses are forbidden.
        got_response = pure_baseinverse_plan.execute(
            square=square_g1,
            directly_playable_squares={
                square_a1,
                square_b1,
                square_c4,
                square_d3,
                square_e2,
                square_f1,
                square_g2,
            },
        )
        self.assertEqual(square_g2, got_response)

        # Verify that one of the Squares of a Baseinverse is the response to the other Square of the Baseinverse.
        got_response = pure_baseinverse_plan.execute(
            square=square_a1,
            directly_playable_squares=[
                square_b1,
                square_c4,
                square_d3,
                square_e2,
                square_f1,
            ])
        self.assertEqual(square_b1, got_response)

    def test_evaluate_diagram_6_3(self):
        # This test case is based on Diagram 6.3.

        # Define all the Squares that will be used in Verticals
        square_c6 = Square(row=0, col=2)
        square_e4 = Square(row=2, col=4)
        square_e5 = Square(row=1, col=4)

        # Define the Verticals.
        vertical_e4_e5 = Vertical(lower=square_e4, upper=square_e5)

        # Verify that when the lower square is given, the Plan responds with the upper square.
        play_upper_plan = plan.Plan(rule_applications={vertical_e4_e5})
        got_response = play_upper_plan.execute(square=square_e4, directly_playable_squares=[square_e5, square_c6])
        self.assertEqual(square_e5, got_response)

        # Verify that if no other squares are available, the Plan responds with the lower square.
        play_lower_plan = plan.Plan(rule_applications={vertical_e4_e5}, availabilities=[square_c6])
        got_response = play_lower_plan.execute(square=square_c6, directly_playable_squares=[square_e4])
        self.assertEqual(square_e4, got_response)


if __name__ == '__main__':
    unittest.main()
