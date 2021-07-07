import gym
import unittest

import numpy as np

from connect_four.envs.connect_four_env import ConnectFourEnv
from connect_four.evaluation.incremental_victor.graph.graph_manager import GraphManager
from connect_four.evaluation.victor.solution import VictorSolutionManager
from connect_four.problem import ConnectFourGroupManager


@unittest.skip("deprecated")
class TestGraphManager6x4(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 4
        ConnectFourEnv.N = 5
        self.env.reset()

    def test_evaluate_4x6(self):
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, ],
            ],
        ])
        problem_manager = ConnectFourGroupManager(env_variables=self.env.env_variables)
        solution_manager = VictorSolutionManager(env_variables=self.env.env_variables)

        gm = GraphManager(player=0, problem_manager=problem_manager, solution_manager=solution_manager)
        got_evaluation = gm.evaluate()
        self.assertIsNotNone(got_evaluation)

    @unittest.skip("threat combinations not implemented yet")
    def test_evaluate_6x4_odd_above_even_threat_combination(self):
        # This test case is based on Diagram 8.3. The left 3 columns are removed.
        # Black is to move and White has a ThreatCombination at a1-d4 and a3-d3.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, ],
                [1, 1, 0, 0, ],
                [0, 0, 0, 0, ],
                [1, 1, 0, 0, ],
                [0, 1, 0, 0, ],
                [1, 0, 0, 1, ],
            ],
            [
                [1, 1, 0, 0, ],
                [0, 0, 0, 0, ],
                [1, 1, 0, 0, ],
                [0, 0, 0, 0, ],
                [1, 0, 0, 0, ],
                [0, 1, 0, 0, ],
            ],
        ])
        self.env.player_turn = 1  # Black to move.

        problem_manager = ConnectFourGroupManager(env_variables=self.env.env_variables)
        solution_manager = VictorSolutionManager(env_variables=self.env.env_variables)

        gm = GraphManager(player=1, problem_manager=problem_manager, solution_manager=solution_manager)
        got_evaluation = gm.evaluate()
        self.assertIsNotNone(got_evaluation)

    @unittest.skip("threat combinations not implemented yet")
    def test_evaluate_6x7_odd_above_not_directly_playable_even_threat_combination(self):
        # This test case is a modified version of Diagram 8.7.
        # The even square of the ThreatCombination is NOT directly playable.
        # Black is to move and White has a ThreatCombination at a5-d2 and a3-d3.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, ],
                [1, 0, 0, 0, ],
                [0, 1, 0, 0, ],
                [1, 1, 0, 0, ],
                [1, 0, 0, 0, ],
                [1, 0, 0, 0, ],
            ],
            [
                [1, 0, 0, 0, ],
                [0, 1, 0, 0, ],
                [1, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 1, 0, 0, ],
                [0, 1, 0, 0, ],
            ],
        ])
        self.env.player_turn = 1  # Black to move.

        problem_manager = ConnectFourGroupManager(env_variables=self.env.env_variables)
        solution_manager = VictorSolutionManager(env_variables=self.env.env_variables)

        gm = GraphManager(player=1, problem_manager=problem_manager, solution_manager=solution_manager)
        got_evaluation = gm.evaluate()
        self.assertIsNotNone(got_evaluation)


if __name__ == '__main__':
    unittest.main()
