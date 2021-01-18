import unittest

from connect_four.agents.victor.game import Square
from connect_four.agents.victor.planning import plan
from connect_four.agents.victor.rules import Rule
from connect_four.agents.victor.rules import Claimeven
from connect_four.agents.victor.solution import Solution
from connect_four.agents.victor.evaluator import planner


class TestPlanner(unittest.TestCase):
    def test_evaluate_diagram_6_1(self):
        # This test case is based on Diagram 6.1.

        # Define all Claimevens that will be converted into Solutions.
        # The set of all of these Claimevens can refute all of white_threats.
        claimeven_a1_a2 = Claimeven(lower=Square(row=5, col=0), upper=Square(row=4, col=0))
        claimeven_a5_a6 = Claimeven(lower=Square(row=1, col=0), upper=Square(row=0, col=0))
        claimeven_b1_b2 = Claimeven(lower=Square(row=5, col=1), upper=Square(row=4, col=1))
        claimeven_b3_b4 = Claimeven(lower=Square(row=3, col=1), upper=Square(row=2, col=1))
        claimeven_b5_b6 = Claimeven(lower=Square(row=1, col=1), upper=Square(row=0, col=1))
        claimeven_c3_c4 = Claimeven(lower=Square(row=3, col=2), upper=Square(row=2, col=2))
        claimeven_e3_e4 = Claimeven(lower=Square(row=3, col=4), upper=Square(row=2, col=4))
        claimeven_f1_f2 = Claimeven(lower=Square(row=5, col=5), upper=Square(row=4, col=5))
        claimeven_f3_f4 = Claimeven(lower=Square(row=3, col=5), upper=Square(row=2, col=5))
        claimeven_f5_f6 = Claimeven(lower=Square(row=1, col=5), upper=Square(row=0, col=5))
        claimeven_g1_g2 = Claimeven(lower=Square(row=5, col=6), upper=Square(row=4, col=6))
        claimeven_g5_g6 = Claimeven(lower=Square(row=1, col=6), upper=Square(row=0, col=6))

        claimevens = [
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

        responses = dict()
        for claimeven in claimevens:
            responses[claimeven.lower] = claimeven.upper

        claimeven_solution_a1_a2 = Solution(
            rule=Rule.Claimeven,
            squares=[claimeven_a1_a2.lower, claimeven_a1_a2.upper],
            solution_plan=plan.from_claimeven(claimeven=claimeven_a1_a2),
        )
        self.assertIsNotNone(claimeven_solution_a1_a2)
        self.assertIsNotNone(claimeven_solution_a1_a2.plan)
        self.assertIsNotNone(claimeven_solution_a1_a2.plan.responses)
        claimeven_solution_a5_a6 = Solution(
            rule=Rule.Claimeven,
            squares=[claimeven_a5_a6.lower, claimeven_a5_a6.upper],
            solution_plan=plan.from_claimeven(claimeven=claimeven_a5_a6),
        )
        claimeven_solution_b1_b2 = Solution(
            rule=Rule.Claimeven,
            squares=[claimeven_b1_b2.lower, claimeven_b1_b2.upper],
            solution_plan=plan.from_claimeven(claimeven=claimeven_b1_b2),
        )
        claimeven_solution_b3_b4 = Solution(
            rule=Rule.Claimeven,
            squares=[claimeven_b3_b4.lower, claimeven_b3_b4.upper],
            solution_plan=plan.from_claimeven(claimeven=claimeven_b3_b4),
        )
        claimeven_solution_b5_b6 = Solution(
            rule=Rule.Claimeven,
            squares=[claimeven_b5_b6.lower, claimeven_b5_b6.upper],
            solution_plan=plan.from_claimeven(claimeven=claimeven_b5_b6),
        )
        claimeven_solution_c3_c4 = Solution(
            rule=Rule.Claimeven,
            squares=[claimeven_c3_c4.lower, claimeven_c3_c4.upper],
            solution_plan=plan.from_claimeven(claimeven=claimeven_c3_c4),
        )
        claimeven_solution_e3_e4 = Solution(
            rule=Rule.Claimeven,
            squares=[claimeven_e3_e4.lower, claimeven_e3_e4.upper],
            solution_plan=plan.from_claimeven(claimeven=claimeven_e3_e4),
        )
        claimeven_solution_f1_f2 = Solution(
            rule=Rule.Claimeven,
            squares=[claimeven_f1_f2.lower, claimeven_f1_f2.upper],
            solution_plan=plan.from_claimeven(claimeven=claimeven_f1_f2),
        )
        claimeven_solution_f3_f4 = Solution(
            rule=Rule.Claimeven,
            squares=[claimeven_f3_f4.lower, claimeven_f3_f4.upper],
            solution_plan=plan.from_claimeven(claimeven=claimeven_f3_f4),
        )
        claimeven_solution_f5_f6 = Solution(
            rule=Rule.Claimeven,
            squares=[claimeven_f5_f6.lower, claimeven_f5_f6.upper],
            solution_plan=plan.from_claimeven(claimeven=claimeven_f5_f6),
        )
        claimeven_solution_g1_g2 = Solution(
            rule=Rule.Claimeven,
            squares=[claimeven_g1_g2.lower, claimeven_g1_g2.upper],
            solution_plan=plan.from_claimeven(claimeven=claimeven_g1_g2),
        )
        claimeven_solution_g5_g6 = Solution(
            rule=Rule.Claimeven,
            squares=[claimeven_g5_g6.lower, claimeven_g5_g6.upper],
            solution_plan=plan.from_claimeven(claimeven=claimeven_g5_g6),
        )

        solutions = set()
        solutions.add(claimeven_solution_a1_a2)
        solutions.add(claimeven_solution_a5_a6)
        solutions.add(claimeven_solution_b1_b2)
        solutions.add(claimeven_solution_b3_b4)
        solutions.add(claimeven_solution_b5_b6)
        solutions.add(claimeven_solution_c3_c4)
        solutions.add(claimeven_solution_e3_e4)
        solutions.add(claimeven_solution_f1_f2)
        solutions.add(claimeven_solution_f3_f4)
        solutions.add(claimeven_solution_f5_f6)
        solutions.add(claimeven_solution_g1_g2)
        solutions.add(claimeven_solution_g5_g6)

        want_plan = plan.Plan(responses=responses)
        got_plan = planner.convert(solutions=solutions)
        self.assertEqual(want_plan, got_plan)


if __name__ == '__main__':
    unittest.main()
