import unittest

import gym
import numpy as np

from connect_four.envs import ConnectFourEnv
from connect_four.evaluation.victor.graph.graph_manager import GraphManager
from connect_four.evaluation.victor.rules import Claimeven, OddThreat, Baseinverse, Before, Vertical
from connect_four.evaluation.victor.solution import solution2, VictorSolutionManager
from connect_four.evaluation.victor.solution.fake_solution_manager import FakeSolutionManager
from connect_four.game import Square
from connect_four.problem import ConnectFourProblemManager, Group as Problem


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
        self.assertTrue(problem_manager.get_current_problems().issubset(got_solved_problems))

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
        self.assertEqual(69, len(problem_manager.get_current_problems()))
        print("number of solutions =", len(solution_manager.get_solutions()))

        gm = GraphManager(player=0, problem_manager=problem_manager, solution_manager=solution_manager)
        print("number of useful solutions =", len(gm.solution_to_problems))
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

    def test_find_chosen_set_diagram_8_1(self):
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

        # Define all Solutions using Claimevens.
        # A subset of these Claimevens can refute all of Black's groups not in the 0th column.
        claimeven_b5_b6 = solution2.from_claimeven(
            claimeven=Claimeven(lower=Square(row=1, col=1), upper=Square(row=0, col=1)),
        )
        claimeven_c5_c6 = solution2.from_claimeven(
            claimeven=Claimeven(lower=Square(row=1, col=2), upper=Square(row=0, col=2)),
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
        claimeven_g3_g4 = solution2.from_claimeven(
            claimeven=Claimeven(lower=Square(row=3, col=6), upper=Square(row=2, col=6)),
        )
        claimeven_g5_g6 = solution2.from_claimeven(
            claimeven=Claimeven(lower=Square(row=1, col=6), upper=Square(row=0, col=6)),
        )
        baseinverse_d5_e5 = solution2.from_baseinverse(
            baseinverse=Baseinverse(playable1=Square(row=1, col=3), playable2=Square(row=1, col=4)),
        )
        odd_threat_a3_d3 = solution2.from_odd_threat(
            odd_threat=OddThreat(
                group=Problem(player=0, start=Square(row=3, col=0), end=Square(row=3, col=3)),  # a3-d3
                empty_square=Square(row=3, col=0),  # a3
                directly_playable_square=Square(row=4, col=0),  # a2
            )
        )

        # Note that typically, for a given set of Solutions, there may be multiple subsets of Solutions that
        # solve all groups.
        # In this test case, the given Solution set is the desired set so there is exactly one subset.
        solutions = {
            claimeven_b5_b6,
            claimeven_c5_c6,
            claimeven_f1_f2,
            claimeven_f3_f4,
            claimeven_f5_f6,
            claimeven_g3_g4,
            claimeven_g5_g6,
            baseinverse_d5_e5,
            odd_threat_a3_d3,
        }

        problem_manager = ConnectFourProblemManager(env_variables=self.env.env_variables)
        fake_solution_manager = FakeSolutionManager(solutions=solutions, win_conditions={odd_threat_a3_d3})

        gm = GraphManager(player=1, problem_manager=problem_manager, solution_manager=fake_solution_manager)
        got_solutions = gm.evaluate()
        self.assertIsNotNone(got_solutions)
        self.assertTrue(got_solutions.issubset(solutions))

        got_solved_problems = set()
        for sol in got_solutions:
            got_solved_problems.update(gm.solution_to_problems[sol])

        # The used Solutions may also solve Problems that belong to the other player.
        # The minimum requirement is that the found Solutions solves all
        # Problems that need to be solved in this position.
        self.assertTrue(problem_manager.get_current_problems().issubset(got_solved_problems))

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

        gm = GraphManager(player=1, problem_manager=problem_manager, solution_manager=solution_manager)
        got_evaluation = gm.evaluate()
        self.assertIsNotNone(got_evaluation)

    def test_evaluate_6x7_11_1_a1_a2(self):
        # This test case is a modified version of on Diagram 11.1.
        # White has played a1 and Black has responded with a2.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [1, 0, 1, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [1, 0, 1, 1, 1, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
            ],
        ])
        problem_manager = ConnectFourProblemManager(env_variables=self.env.env_variables)
        solution_manager = VictorSolutionManager(env_variables=self.env.env_variables)

        # Catches the case when there exists a Problem that cannot be solved by any Solutions.
        gm = GraphManager(player=0, problem_manager=problem_manager, solution_manager=solution_manager)
        got_evaluation = gm.evaluate()
        self.assertIsNone(got_evaluation)

    def test_move(self):
        problem_manager = ConnectFourProblemManager(env_variables=self.env.env_variables)
        solution_manager = VictorSolutionManager(env_variables=self.env.env_variables)

        gm1 = GraphManager(player=0, problem_manager=problem_manager, solution_manager=solution_manager)
        gm1.move(row=5, col=0)

        # Initialize a second GraphManager at the moved state.
        gm2 = GraphManager(player=1, problem_manager=problem_manager, solution_manager=solution_manager)
        self.assertEqual(gm1.problem_to_solutions, gm2.problem_to_solutions)
        self.assertEqual(gm1.solution_to_problems, gm2.solution_to_problems)
        self.assertEqual(len(gm1.solution_to_solutions), len(gm2.solution_to_solutions))
        counter = 0
        for solution in gm1.solution_to_solutions:
            counter += 1
            print(counter, "of", len(gm1.solution_to_solutions))
            self.assertIn(solution, gm2.solution_to_solutions)
            self.assertEqual(gm1.solution_to_solutions[solution], gm2.solution_to_solutions[solution])

    def test_move_undo_move(self):
        problem_manager = ConnectFourProblemManager(env_variables=self.env.env_variables)
        solution_manager = VictorSolutionManager(env_variables=self.env.env_variables)

        gm1 = GraphManager(player=0, problem_manager=problem_manager, solution_manager=solution_manager)

        gm1.move(row=5, col=3)
        self.assertEqual(1, gm1.player)

        gm1.undo_move()

        gm2 = GraphManager(
            player=0,
            problem_manager=ConnectFourProblemManager(env_variables=self.env.env_variables),
            solution_manager=VictorSolutionManager(env_variables=self.env.env_variables),
        )

        for problem in gm1.problem_to_solutions:
            self.assertEqual(gm1.problem_to_solutions[problem], gm2.problem_to_solutions[problem])
        self.assertEqual(gm1.solution_to_problems, gm2.solution_to_problems)
        self.assertEqual(len(gm1.solution_to_solutions), len(gm2.solution_to_solutions))
        counter = 0
        for solution in gm1.solution_to_solutions:
            counter += 1
            print(counter, "of", len(gm1.solution_to_solutions))
            self.assertIn(solution, gm2.solution_to_solutions)
            self.assertEqual(gm1.solution_to_solutions[solution], gm2.solution_to_solutions[solution])


if __name__ == '__main__':
    unittest.main()
