import unittest

from connect_four.agents.victor.game import Square
from connect_four.agents.victor.game import Threat

from connect_four.agents.victor.rules import Claimeven
from connect_four.agents.victor.rules import Baseinverse
from connect_four.agents.victor.rules import Vertical
from connect_four.agents.victor.rules import Aftereven
from connect_four.agents.victor.rules import Lowinverse
from connect_four.agents.victor.rules import Highinverse
from connect_four.agents.victor.rules import Baseclaim
from connect_four.agents.victor.rules import Before
from connect_four.agents.victor.rules import Specialbefore

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
        pure_claimeven_plan = plan.Plan(
            rule_applications=rule_applications,
            directly_playable_squares={square_a1},
        )

        # Verify that the upper of a Claimeven is the response to the lower of a Claimeven.
        got_response = pure_claimeven_plan.execute(square=square_a1)
        self.assertEqual(square_a2, got_response)
        self.assertEqual({Square(row=3, col=0)}, pure_claimeven_plan.directly_playable_squares)  # a3

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
        square_g2 = Square(row=4, col=6)

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
        pure_baseinverse_plan = plan.Plan(
            rule_applications=rule_applications,
            availabilities={square_g1, square_g2},
            directly_playable_squares={square_a1, square_b1, square_g1},
        )

        # Verify that g2 is the response when g1 is played because all squares part of the Baseinverses are forbidden.
        got_response = pure_baseinverse_plan.execute(square=square_g1)
        self.assertEqual(square_g2, got_response)

        # Verify that one of the Squares of a Baseinverse is the response to the other Square of the Baseinverse.
        got_response = pure_baseinverse_plan.execute(square=square_a1)
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
        play_upper_plan = plan.Plan(
            rule_applications={vertical_e4_e5},
            directly_playable_squares={square_e4},
        )
        got_response = play_upper_plan.execute(square=square_e4)
        self.assertEqual(square_e5, got_response)

        # Verify that if no other squares are available, the Plan responds with the lower square.
        play_lower_plan = plan.Plan(
            rule_applications={vertical_e4_e5},
            availabilities=[square_c6],
            directly_playable_squares={square_c6, square_e4},
        )
        got_response = play_lower_plan.execute(square=square_c6)
        self.assertEqual(square_e4, got_response)

    def test_evaluate_diagram_6_4(self):
        # This test case is based on Diagram 6.4.

        # Define all the Squares that will be used in Claimevens and Afterevens.
        square_f1 = Square(row=5, col=5)
        square_f2 = Square(row=4, col=5)

        # Define the Claimevens.
        claimeven_f1_f2 = Claimeven(lower=square_f1, upper=square_f2)

        # Define the Afterevens.
        aftereven_c2_f2 = Aftereven(
            threat=Threat(player=1, start=Square(row=5, col=2), end=Square(row=5, col=5)),  # c2-f2
            claimevens=[claimeven_f1_f2],
        )

        # Verify that the upper of a Claimeven is the response to the lower of a Claimeven.
        pure_aftereven_plan = plan.Plan(
            rule_applications=[aftereven_c2_f2],
            availabilities={square_f1, square_f2},
            directly_playable_squares={square_f1},
        )
        got_response = pure_aftereven_plan.execute(square=square_f1)
        self.assertEqual(square_f2, got_response)

    def test_evaluate_diagram_6_6_lowinverse(self):
        # This test case is based on Diagram 6.6.

        # Define all the Squares that will be used in the Lowinverse.
        square_c2 = Square(row=4, col=2)
        square_c3 = Square(row=3, col=2)
        square_d2 = Square(row=4, col=3)
        square_d3 = Square(row=3, col=3)

        # Define the Verticals that will be part of the Lowinverse.
        vertical_c2_c3 = Vertical(upper=square_c3, lower=square_c2)
        vertical_d2_d3 = Vertical(upper=square_d3, lower=square_d2)

        # Define the Lowinverses.
        lowinverse_c2_c3_d2_d3 = Lowinverse(
            first_vertical=vertical_c2_c3,  # c2-c3
            second_vertical=vertical_d2_d3,  # d2-d3
        )

        # Verify that the correct Branch of a Fork is chosen.
        pure_lowinverse_plan = plan.Plan(
            rule_applications=[lowinverse_c2_c3_d2_d3],
            directly_playable_squares={square_c2, square_d2},
        )
        got_response = pure_lowinverse_plan.execute(square=square_c2)
        self.assertEqual(square_c3, got_response)

        # Verify that the upper of a Vertical is the response to the lower of a Vertical.
        got_response = pure_lowinverse_plan.execute(square=square_d2)
        self.assertEqual(square_d3, got_response)

    def test_evaluate_diagram_6_6_highinverse(self):
        # This test case is based on Diagram 6.6.

        # Define all the Squares that will be used in the Highinverse.
        square_c2 = Square(row=4, col=2)
        square_c3 = Square(row=3, col=2)
        square_c4 = Square(row=2, col=2)
        square_d2 = Square(row=4, col=3)
        square_d3 = Square(row=3, col=3)
        square_d4 = Square(row=2, col=3)

        # Define the Verticals that will be part of the Lowinverse.
        vertical_c2_c3 = Vertical(upper=square_c3, lower=square_c2)
        vertical_d2_d3 = Vertical(upper=square_d3, lower=square_d2)

        # Define the Lowinverse.
        lowinverse_c2_c3_d2_d3 = Lowinverse(
            first_vertical=vertical_c2_c3,  # c2-c3
            second_vertical=vertical_d2_d3,  # d2-d3
        )

        # Define the Highinverse.
        highinverse_c2_c3_c4_d2_d3_d4 = Highinverse(
            lowinverse=lowinverse_c2_c3_d2_d3,
            directly_playable_squares=[square_c2, square_d2],  # c2 and d2
        )

        # Verify that the correct Branch of a Fork is chosen.
        pure_highinverse_plan = plan.Plan(
            rule_applications=[highinverse_c2_c3_c4_d2_d3_d4],
            directly_playable_squares={square_c2, square_d2},
        )
        got_response = pure_highinverse_plan.execute(square=square_c2)
        self.assertEqual(square_c3, got_response)

        # Verify that if the bottom square of the column that is not chosen is directly playable,
        # it becomes part of a Baseinverse with the top square of the first column.
        got_response = pure_highinverse_plan.execute(square=square_d2)
        self.assertEqual(square_c4, got_response)

        # Verify that the top two squares of the second column become a Claimeven.
        got_response = pure_highinverse_plan.execute(square=square_d3)
        self.assertEqual(square_d4, got_response)

    def test_evaluate_diagram_6_7(self):
        # This test case is based on Diagram 6.7.

        # Define all the Squares that will be used in the Baseclaim.
        square_b1 = Square(row=5, col=1)
        square_c1 = Square(row=5, col=2)
        square_c2 = Square(row=4, col=2)
        square_e1 = Square(row=5, col=4)

        # Define the Baseclaim.
        baseclaim_b1_c1_c2_f1 = Baseclaim(
            first=square_b1,  # b1
            second=square_c1,  # c1
            third=square_e1,  # e1
        )

        # Verify that the correct Branch of a Fork is chosen.
        pure_baseclaim_plan = plan.Plan(
            rule_applications=[baseclaim_b1_c1_c2_f1],
            directly_playable_squares={square_b1, square_c1, square_e1},
        )
        # Verify that if the first square is played by the opponent, the third square is the response.
        got_response = pure_baseclaim_plan.execute(square=square_b1)
        self.assertEqual(square_e1, got_response)
        # Verify that after the Branch is chosen, a Claimeven is used for the second square.
        got_response = pure_baseclaim_plan.execute(square=square_c1)
        self.assertEqual(square_c2, got_response)

    def test_evaluate_diagram_6_9(self):
        # Define all the Squares that will be used in the Before.
        square_b3 = Square(row=3, col=1)
        square_b4 = Square(row=2, col=1)
        square_e1 = Square(row=5, col=4)
        square_e2 = Square(row=4, col=4)
        square_c4 = Square(row=2, col=2)

        # Define the Before.
        before_b4_e1 = Before(
            threat=Threat(player=1, start=Square(row=2, col=1), end=Square(row=5, col=4)),  # Threat b4-e1
            verticals=[
                Vertical(upper=square_e2, lower=square_e1),  # Vertical e1-e2
            ],
            claimevens=[
                Claimeven(upper=square_b4, lower=square_b3)  # Claimeven b3-b4
            ]
        )

        # Verify that if there are no available squares except the lower of a Vertical, it is chosen.
        pure_before_plan = plan.Plan(
            rule_applications=[before_b4_e1],
            directly_playable_squares={square_b3, square_c4, square_e1},
        )
        got_response = pure_before_plan.execute(square=square_c4)
        self.assertEqual(square_e1, got_response)

    def test_evaluate_diagram_6_10(self):
        square_d3 = Square(row=3, col=3)
        square_e2 = Square(row=4, col=4)
        square_e3 = Square(row=3, col=4)
        square_f1 = Square(row=5, col=5)
        square_f2 = Square(row=4, col=5)
        square_g1 = Square(row=5, col=6)
        square_g2 = Square(row=4, col=6)

        # Verticals/Claimevens which are part of the Before.
        vertical_e2_e3 = Vertical(upper=square_e3, lower=square_e2)  # Vertical e2-e3.
        claimeven_f1_f2 = Claimeven(upper=square_f2, lower=square_f1)  # Claimeven f1-f2.
        claimeven_g1_g2 = Claimeven(upper=square_g2, lower=square_g1)  # Claimeven g1-g2.

        # Define the Before.
        before_d2_g2 = Before(
            threat=Threat(player=1, start=Square(row=4, col=3), end=Square(row=4, col=6)),  # d2-g2
            verticals=[vertical_e2_e3],
            claimevens=[claimeven_f1_f2, claimeven_g1_g2],
        )
        # Define the Specialbefore.
        specialbefore_d2_g2 = Specialbefore(
            before=before_d2_g2,
            internal_directly_playable_square=square_e2,  # e2
            external_directly_playable_square=square_d3,  # d3
        )

        # Verify that even though e2 is the lower of vertical_e2_e3, the response is d3.
        pure_specialbefore_plan = plan.Plan(
            rule_applications=[specialbefore_d2_g2],
            directly_playable_squares={square_d3, square_e2, square_f1, square_g1},
        )
        got_response = pure_specialbefore_plan.execute(square=square_e2)
        self.assertEqual(square_d3, got_response)


if __name__ == '__main__':
    unittest.main()
