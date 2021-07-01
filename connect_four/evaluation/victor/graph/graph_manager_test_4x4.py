import gym
import unittest

import numpy as np

from connect_four.envs.connect_four_env import ConnectFourEnv
from connect_four.evaluation.victor.graph.graph_manager import GraphManager
from connect_four.evaluation.victor.solution import VictorSolutionManager
from connect_four.problem import ConnectFourGroupManager


class TestGraphManager4x4(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 4
        ConnectFourEnv.N = 4
        self.env.reset()

    def test_evaluate_4x4(self):
        self.env.state = np.array([
            [
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
            ],
        ])
        problem_manager = ConnectFourGroupManager(env_variables=self.env.env_variables)
        solution_manager = VictorSolutionManager(env_variables=self.env.env_variables)

        gm = GraphManager(player=0, problem_manager=problem_manager, solution_manager=solution_manager)
        got_evaluation = gm.evaluate()
        self.assertIsNotNone(got_evaluation)


if __name__ == '__main__':
    unittest.main()
