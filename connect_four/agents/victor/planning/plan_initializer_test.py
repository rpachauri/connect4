import gym
import unittest

import numpy as np

from connect_four.agents.victor.game import Board
from connect_four.agents.victor.game import Square
from connect_four.agents.victor.planning.plan_initializer import PlanInitializer

from connect_four.agents.victor.rules import Claimeven

from connect_four.agents.victor.solution import solution
from connect_four.agents.victor.evaluator import evaluator

from connect_four.envs.connect_four_env import ConnectFourEnv


class TestPlanInitializer(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 7
        self.env.reset()

    def test_initialize_diagram_6_1(self):
        # This test case is based on Diagram 6.1.
        self.env.state = np.array([
            [
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 1, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        square_to_groups = board.potential_groups_by_square()

        # Define all Claimevens.
        claimeven_a1_a2 = Claimeven(lower=Square(row=5, col=0), upper=Square(row=4, col=0))
        claimeven_a3_a4 = Claimeven(lower=Square(row=3, col=0), upper=Square(row=2, col=0))
        claimeven_a5_a6 = Claimeven(lower=Square(row=1, col=0), upper=Square(row=0, col=0))
        claimeven_b1_b2 = Claimeven(lower=Square(row=5, col=1), upper=Square(row=4, col=1))
        claimeven_b3_b4 = Claimeven(lower=Square(row=3, col=1), upper=Square(row=2, col=1))
        claimeven_b5_b6 = Claimeven(lower=Square(row=1, col=1), upper=Square(row=0, col=1))
        claimeven_c3_c4 = Claimeven(lower=Square(row=3, col=2), upper=Square(row=2, col=2))
        claimeven_c5_c6 = Claimeven(lower=Square(row=1, col=2), upper=Square(row=0, col=2))
        claimeven_e3_e4 = Claimeven(lower=Square(row=3, col=4), upper=Square(row=2, col=4))
        claimeven_e5_e6 = Claimeven(lower=Square(row=1, col=4), upper=Square(row=0, col=4))
        claimeven_f1_f2 = Claimeven(lower=Square(row=5, col=5), upper=Square(row=4, col=5))
        claimeven_f3_f4 = Claimeven(lower=Square(row=3, col=5), upper=Square(row=2, col=5))
        claimeven_f5_f6 = Claimeven(lower=Square(row=1, col=5), upper=Square(row=0, col=5))
        claimeven_g1_g2 = Claimeven(lower=Square(row=5, col=6), upper=Square(row=4, col=6))
        claimeven_g3_g4 = Claimeven(lower=Square(row=3, col=6), upper=Square(row=2, col=6))
        claimeven_g5_g6 = Claimeven(lower=Square(row=1, col=6), upper=Square(row=0, col=6))

        # Define all Solutions using Claimevens.
        # A subset of these Claimevens can refute all of white_groups.
        claimeven_a1_a2_solution = solution.from_claimeven(
            claimeven=claimeven_a1_a2,
            square_to_groups=square_to_groups,
        )
        claimeven_a3_a4_solution = solution.from_claimeven(
            claimeven=claimeven_a3_a4,
            square_to_groups=square_to_groups,
        )
        claimeven_a5_a6_solution = solution.from_claimeven(
            claimeven=claimeven_a5_a6,
            square_to_groups=square_to_groups,
        )
        claimeven_b1_b2_solution = solution.from_claimeven(
            claimeven=claimeven_b1_b2,
            square_to_groups=square_to_groups,
        )
        claimeven_b3_b4_solution = solution.from_claimeven(
            claimeven=claimeven_b3_b4,
            square_to_groups=square_to_groups,
        )
        claimeven_b5_b6_solution = solution.from_claimeven(
            claimeven=claimeven_b5_b6,
            square_to_groups=square_to_groups,
        )
        claimeven_c3_c4_solution = solution.from_claimeven(
            claimeven=claimeven_c3_c4,
            square_to_groups=square_to_groups,
        )
        claimeven_c5_c6_solution = solution.from_claimeven(
            claimeven=claimeven_c5_c6,
            square_to_groups=square_to_groups,
        )
        claimeven_e3_e4_solution = solution.from_claimeven(
            claimeven=claimeven_e3_e4,
            square_to_groups=square_to_groups,
        )
        claimeven_e5_e6_solution = solution.from_claimeven(
            claimeven=claimeven_e5_e6,
            square_to_groups=square_to_groups,
        )
        claimeven_f1_f2_solution = solution.from_claimeven(
            claimeven=claimeven_f1_f2,
            square_to_groups=square_to_groups,
        )
        claimeven_f3_f4_solution = solution.from_claimeven(
            claimeven=claimeven_f3_f4,
            square_to_groups=square_to_groups,
        )
        claimeven_f5_f6_solution = solution.from_claimeven(
            claimeven=claimeven_f5_f6,
            square_to_groups=square_to_groups,
        )
        claimeven_g1_g2_solution = solution.from_claimeven(
            claimeven=claimeven_g1_g2,
            square_to_groups=square_to_groups,
        )
        claimeven_g3_g4_solution = solution.from_claimeven(
            claimeven=claimeven_g3_g4,
            square_to_groups=square_to_groups,
        )
        claimeven_g5_g6_solution = solution.from_claimeven(
            claimeven=claimeven_g5_g6,
            square_to_groups=square_to_groups,
        )

        # Note that typically, for a given set of Solutions, there may be multiple subsets of Solutions that
        # solve all groups.
        # In this test case, the given Solution set is the desired set so there is exactly one subset.
        solutions = {
            claimeven_a1_a2_solution,
            claimeven_a3_a4_solution,
            claimeven_a5_a6_solution,
            claimeven_b1_b2_solution,
            claimeven_b3_b4_solution,
            claimeven_b5_b6_solution,
            claimeven_c3_c4_solution,
            claimeven_c5_c6_solution,
            claimeven_e3_e4_solution,
            claimeven_e5_e6_solution,
            claimeven_f1_f2_solution,
            claimeven_f3_f4_solution,
            claimeven_f5_f6_solution,
            claimeven_g1_g2_solution,
            claimeven_g3_g4_solution,
            claimeven_g5_g6_solution,
        }

        want_rule_applications = {
            claimeven_a1_a2,
            claimeven_a3_a4,
            claimeven_a5_a6,
            claimeven_b1_b2,
            claimeven_b3_b4,
            claimeven_b5_b6,
            claimeven_c3_c4,
            claimeven_c5_c6,
            claimeven_e3_e4,
            claimeven_e5_e6,
            claimeven_f1_f2,
            claimeven_f3_f4,
            claimeven_f5_f6,
            claimeven_g1_g2,
            claimeven_g3_g4,
            claimeven_g5_g6,
        }
        want_availabilities = {
            Square(row=4, col=2),  # c2
            Square(row=4, col=4),  # e2
        }

        plan_initializer = PlanInitializer(
            board=board,
            evaluation=evaluator.Evaluation(
                chosen_set=solutions,
                odd_threat_guarantor=None,
            ),
        )
        self.assertEqual(want_rule_applications, plan_initializer.rule_applications)
        self.assertEqual(want_availabilities, plan_initializer.availabilities)
        self.assertIsNone(plan_initializer.odd_group_guarantor)
        self.assertEqual(board.playable_squares(), plan_initializer.directly_playable_squares)


if __name__ == '__main__':
    unittest.main()
