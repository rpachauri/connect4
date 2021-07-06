import unittest

import gym
import numpy as np

from connect_four.envs import ConnectFourEnv
from connect_four.evaluation.victor.graph.graph_manager import GraphManager
from connect_four.evaluation.victor.solution import VictorSolutionManager
from connect_four.problem import ConnectFourGroupManager


@unittest.skip("deprecated")
class TestGraphManagerDiagram11_1(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 7
        self.env.reset()

        self.diagram_8_1_env = gym.make('connect_four-v0')
        self.diagram_8_1_env.reset()
        self.diagram_8_1_env.state = np.array([
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
        self.diagram_8_1_env.player_turn = 1  # Black to move.

        self.diagram_11_1_env = gym.make('connect_four-v0')
        self.diagram_11_1_env.reset()
        self.diagram_11_1_env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 1, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 1, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 1, 1, 1, 0, 0, ],
                [0, 0, 0, 0, 1, 0, 0, ],
            ],
        ])

    def test_evaluate_6x7_8_1(self):
        # This test case is based on Diagram 8.1.
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
        problem_manager = ConnectFourGroupManager(env_variables=self.env.env_variables)
        solution_manager = VictorSolutionManager(env_variables=self.env.env_variables)

        # White can win in this position.
        gm = GraphManager(player=1, problem_manager=problem_manager, solution_manager=solution_manager)
        got_evaluation = gm.evaluate()
        self.assertIsNotNone(got_evaluation)

    def test_move_from_11_1_to_8_1(self):
        gm = GraphManager(
            player=0,
            problem_manager=ConnectFourGroupManager(env_variables=self.diagram_11_1_env.env_variables),
            solution_manager=VictorSolutionManager(env_variables=self.diagram_11_1_env.env_variables),
        )
        gm.move(row=5, col=0)  # White plays a1
        gm.move(row=5, col=1)  # Black plays b1
        gm.move(row=4, col=1)  # White plays b2
        gm.move(row=2, col=3)  # Black plays d4
        gm.move(row=3, col=1)  # White plays b3
        gm.move(row=3, col=4)  # Black plays e3
        gm.move(row=2, col=4)  # White plays e4
        want_gm = GraphManager(
            player=1,
            problem_manager=ConnectFourGroupManager(env_variables=self.diagram_8_1_env.env_variables),
            solution_manager=VictorSolutionManager(env_variables=self.diagram_8_1_env.env_variables),
        )
        self.assertEqual(want_gm.problem_to_solutions, gm.problem_to_solutions)
        self.assertEqual(want_gm.solution_to_problems, gm.solution_to_problems)
        self.assertEqual(want_gm.solution_to_solutions, gm.solution_to_solutions)

        gm.undo_move()
        gm.undo_move()
        gm.undo_move()
        gm.undo_move()
        gm.undo_move()
        gm.undo_move()
        gm.undo_move()
        want_gm = GraphManager(
            player=0,
            problem_manager=ConnectFourGroupManager(env_variables=self.diagram_11_1_env.env_variables),
            solution_manager=VictorSolutionManager(env_variables=self.diagram_11_1_env.env_variables),
        )
        self.assertEqual(want_gm.problem_to_solutions, gm.problem_to_solutions)
        self.assertEqual(want_gm.solution_to_problems, gm.solution_to_problems)
        self.assertEqual(want_gm.solution_to_solutions, gm.solution_to_solutions)


if __name__ == '__main__':
    unittest.main()
