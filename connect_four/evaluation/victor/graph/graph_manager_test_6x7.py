import unittest

import gym
import numpy as np

from connect_four.envs import ConnectFourEnv
from connect_four.evaluation.victor.graph.graph_manager import GraphManager
from connect_four.evaluation.victor.rules import Claimeven
from connect_four.evaluation.victor.solution import solution2, VictorSolutionManager
from connect_four.evaluation.victor.solution.fake_solution_manager import FakeSolutionManager
from connect_four.game import Square
from connect_four.problem import ConnectFourProblemManager


class TestGraphManager6x7(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 6
        self.env.reset()

    def test_find_chosen_set_diagram_6_1(self):
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

        # Define all Solutions using Claimevens.
        # A subset of these Claimevens can refute all of white_groups.
        claimeven_a1_a2 = solution2.from_claimeven(
            claimeven=Claimeven(lower=Square(row=5, col=0), upper=Square(row=4, col=0)),
        )
        claimeven_a3_a4 = solution2.from_claimeven(
            claimeven=Claimeven(lower=Square(row=3, col=0), upper=Square(row=2, col=0)),
        )
        claimeven_a5_a6 = solution2.from_claimeven(
            claimeven=Claimeven(lower=Square(row=1, col=0), upper=Square(row=0, col=0)),
        )
        claimeven_b1_b2 = solution2.from_claimeven(
            claimeven=Claimeven(lower=Square(row=5, col=1), upper=Square(row=4, col=1)),
        )
        claimeven_b3_b4 = solution2.from_claimeven(
            claimeven=Claimeven(lower=Square(row=3, col=1), upper=Square(row=2, col=1)),
        )
        claimeven_b5_b6 = solution2.from_claimeven(
            claimeven=Claimeven(lower=Square(row=1, col=1), upper=Square(row=0, col=1)),
        )
        claimeven_c3_c4 = solution2.from_claimeven(
            claimeven=Claimeven(lower=Square(row=3, col=2), upper=Square(row=2, col=2)),
        )
        claimeven_c5_c6 = solution2.from_claimeven(
            claimeven=Claimeven(lower=Square(row=1, col=2), upper=Square(row=0, col=2)),
        )
        claimeven_e3_e4 = solution2.from_claimeven(
            claimeven=Claimeven(lower=Square(row=3, col=4), upper=Square(row=2, col=4)),
        )
        claimeven_e5_e6 = solution2.from_claimeven(
            claimeven=Claimeven(lower=Square(row=1, col=4), upper=Square(row=0, col=4)),
        )
        claimeven_f1_f2 = solution2.from_claimeven(
            claimeven=Claimeven(lower=Square(row=5, col=5), upper=Square(row=4, col=5)),
        )
        claimeven_f3_f4 = solution2.from_claimeven(
            claimeven=Claimeven(lower=Square(row=3, col=5), upper=Square(row=2, col=5)),
        )
        claimeven_f5_f6 = solution2.from_claimeven(
            claimeven=Claimeven(lower=Square(row=1, col=5), upper=Square(row=0, col=5)),
        )
        claimeven_g1_g2 = solution2.from_claimeven(
            claimeven=Claimeven(lower=Square(row=5, col=6), upper=Square(row=4, col=6)),
        )
        claimeven_g3_g4 = solution2.from_claimeven(
            claimeven=Claimeven(lower=Square(row=3, col=6), upper=Square(row=2, col=6)),
        )
        claimeven_g5_g6 = solution2.from_claimeven(
            claimeven=Claimeven(lower=Square(row=1, col=6), upper=Square(row=0, col=6)),
        )

        # Note that typically, for a given set of Solutions, there may be multiple subsets of Solutions that
        # solve all groups.
        # In this test case, the given Solution set is the desired set so there is exactly one subset.
        solutions = {
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

        problem_manager = ConnectFourProblemManager(env_variables=self.env.env_variables)
        fake_solution_manager = FakeSolutionManager(solutions=solutions)

        gm = GraphManager(player=0, problem_manager=problem_manager, solution_manager=fake_solution_manager)
        got_solutions = gm.evaluate()
        self.assertIsNotNone(got_solutions)
        self.assertTrue(got_solutions.issubset(solutions))

        got_solved_problems = set()
        for sol in got_solutions:
            got_solved_problems.update(gm.solution_to_problems[sol])

        # The used Solutions may also solve Problems that belong to the other player.
        # The minimum requirement is that the found Solutions solves all
        # Problems that need to be solved in this position.
        self.assertTrue(problem_manager.get_problems().issubset(got_solved_problems))

    def test_evaluate_6x7(self):
        # The empty 6x7 board has no solution set for Black because White is guaranteed to win.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
            ],
        ])
        problem_manager = ConnectFourProblemManager(env_variables=self.env.env_variables)
        solution_manager = VictorSolutionManager(env_variables=self.env.env_variables)

        # There should be exactly 69 problems that need solving.
        self.assertEqual(69, len(problem_manager.get_problems()))

        gm = GraphManager(player=0, problem_manager=problem_manager, solution_manager=solution_manager)
        got_evaluation = gm.evaluate()
        self.assertIsNone(got_evaluation)

    def test_evaluate_6x7_a1_b1(self):
        # This test case is based on Appendix B: Situation after 1. a1. b1.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [1, 0, 0, 0, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 1, 0, 0, 0, 0, 0, ],
            ],
        ])
        problem_manager = ConnectFourProblemManager(env_variables=self.env.env_variables)
        solution_manager = VictorSolutionManager(env_variables=self.env.env_variables)

        gm = GraphManager(player=0, problem_manager=problem_manager, solution_manager=solution_manager)
        got_evaluation = gm.evaluate()
        self.assertIsNotNone(got_evaluation)

    def test_evaluate_6x7_c1(self):
        # This test case is based on Appendix B: Situation after 1. c1.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
            ],
        ])
        problem_manager = ConnectFourProblemManager(env_variables=self.env.env_variables)
        solution_manager = VictorSolutionManager(env_variables=self.env.env_variables)

        gm = GraphManager(player=0, problem_manager=problem_manager, solution_manager=solution_manager)
        got_evaluation = gm.evaluate()
        self.assertIsNotNone(got_evaluation)

    def test_evaluate_6x7_8_1(self):
        # This test case is based on Diagram 8.1.
        # Black is to move and White has an odd threat at a3.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 1, 1, 1, 0, 0, 0, ],
                [0, 1, 0, 0, 0, 0, 0, ],
                [1, 0, 1, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
                [0, 0, 1, 1, 1, 0, 0, ],
                [0, 1, 0, 0, 1, 0, 0, ],
            ],
        ])
        self.env.player_turn = 1  # Black to move.
        problem_manager = ConnectFourProblemManager(env_variables=self.env.env_variables)
        solution_manager = VictorSolutionManager(env_variables=self.env.env_variables)

        gm = GraphManager(player=0, problem_manager=problem_manager, solution_manager=solution_manager)
        got_evaluation = gm.evaluate()
        self.assertIsNotNone(got_evaluation)


if __name__ == '__main__':
    unittest.main()
