import gym
import unittest

import numpy as np

from connect_four.agents.victor.game import Board
from connect_four.agents.victor.game import Square
from connect_four.agents.victor.rules import Claimeven
from connect_four.agents.victor.evaluator import evaluator
from connect_four.agents.victor.solution import solution
from connect_four.envs.connect_four_env import ConnectFourEnv

class TestEvaluator6x7(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 7
        self.env.reset()

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
        board = Board(self.env.env_variables)
        got_solution_set = evaluator.evaluate(board=board)
        self.assertIsNone(got_solution_set)

    def test_evaluate_6x7_a1(self):
        # This test case is based on Appendix B: Situation after 1. a1.
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
        board = Board(self.env.env_variables)
        got_solution_set = evaluator.evaluate(board=board)
        self.assertIsNotNone(got_solution_set)

    def test_evaluate_6x7_b1(self):
        # This test case is based on Appendix B: Situation after 1. b1.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 1, 0, 0, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 0, 0, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        got_solution_set = evaluator.evaluate(board=board)
        self.assertIsNotNone(got_solution_set)

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
        board = Board(self.env.env_variables)
        got_solution_set = evaluator.evaluate(board=board)
        self.assertIsNotNone(got_solution_set)

    def test_evaluate_diagram_6_1(self):
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
        white_threats = board.potential_threats(0)
        square_to_threats = board.potential_threats_by_square()

        # Define all Claimevens that will be converted into Solutions.
        # The set of all of these Claimevens can refute all of white_threats.
        claimeven_a1_a2 = solution.from_claimeven(
            claimeven=Claimeven(lower=Square(row=5, col=0), upper=Square(row=4, col=0)),
            square_to_threats=square_to_threats,
        )
        claimeven_a3_a4 = solution.from_claimeven(
            claimeven=Claimeven(lower=Square(row=3, col=0), upper=Square(row=2, col=0)),
            square_to_threats=square_to_threats,
        )
        claimeven_a5_a6 = solution.from_claimeven(
            claimeven=Claimeven(lower=Square(row=1, col=0), upper=Square(row=0, col=0)),
            square_to_threats=square_to_threats,
        )
        claimeven_b1_b2 = solution.from_claimeven(
            claimeven=Claimeven(lower=Square(row=5, col=1), upper=Square(row=4, col=1)),
            square_to_threats=square_to_threats,
        )
        claimeven_b3_b4 = solution.from_claimeven(
            claimeven=Claimeven(lower=Square(row=3, col=1), upper=Square(row=2, col=1)),
            square_to_threats=square_to_threats,
        )
        claimeven_b5_b6 = solution.from_claimeven(
            claimeven=Claimeven(lower=Square(row=1, col=1), upper=Square(row=0, col=1)),
            square_to_threats=square_to_threats,
        )
        claimeven_c3_c4 = solution.from_claimeven(
            claimeven=Claimeven(lower=Square(row=3, col=2), upper=Square(row=2, col=2)),
            square_to_threats=square_to_threats,
        )
        claimeven_c5_c6 = solution.from_claimeven(
            claimeven=Claimeven(lower=Square(row=1, col=2), upper=Square(row=0, col=2)),
            square_to_threats=square_to_threats,
        )
        claimeven_e3_e4 = solution.from_claimeven(
            claimeven=Claimeven(lower=Square(row=3, col=4), upper=Square(row=2, col=4)),
            square_to_threats=square_to_threats,
        )
        claimeven_e5_e6 = solution.from_claimeven(
            claimeven=Claimeven(lower=Square(row=1, col=4), upper=Square(row=0, col=4)),
            square_to_threats=square_to_threats,
        )
        claimeven_f1_f2 = solution.from_claimeven(
            claimeven=Claimeven(lower=Square(row=5, col=5), upper=Square(row=4, col=5)),
            square_to_threats=square_to_threats,
        )
        claimeven_f3_f4 = solution.from_claimeven(
            claimeven=Claimeven(lower=Square(row=3, col=5), upper=Square(row=2, col=5)),
            square_to_threats=square_to_threats,
        )
        claimeven_f5_f6 = solution.from_claimeven(
            claimeven=Claimeven(lower=Square(row=1, col=5), upper=Square(row=0, col=5)),
            square_to_threats=square_to_threats,
        )
        claimeven_g1_g2 = solution.from_claimeven(
            claimeven=Claimeven(lower=Square(row=5, col=6), upper=Square(row=4, col=6)),
            square_to_threats=square_to_threats,
        )
        claimeven_g3_g4 = solution.from_claimeven(
            claimeven=Claimeven(lower=Square(row=3, col=6), upper=Square(row=2, col=6)),
            square_to_threats=square_to_threats,
        )
        claimeven_g5_g6 = solution.from_claimeven(
            claimeven=Claimeven(lower=Square(row=1, col=6), upper=Square(row=0, col=6)),
            square_to_threats=square_to_threats,
        )

        # Note that typically, for a given set of Solutions, there may be multiple subsets of Solutions that
        # solve all Threats.
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
        node_graph = evaluator.create_node_graph(solutions=solutions)
        got_solutions = evaluator.find_chosen_set(
            node_graph=node_graph,
            problems=white_threats,
            allowed_solutions=solutions,
            used_solutions=set()
        )
        self.assertIsNotNone(got_solutions)
        self.assertTrue(got_solutions.issubset(solutions))

        solved_threats = set()
        for sol in got_solutions:
            solved_threats.update(sol.threats)
        self.assertEqual(white_threats, solved_threats)


if __name__ == '__main__':
    unittest.main()
