import gym
import unittest

import numpy as np

from connect_four.agents.victor.game import Board
from connect_four.agents.victor.evaluator import evaluator
from connect_four.envs.connect_four_env import ConnectFourEnv


class TestEvaluator4x5(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 4
        ConnectFourEnv.N = 5
        self.env.reset()

    def test_evaluate_4x5(self):
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, ],
            ],
            [
                [0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, ],
            ],
        ])
        board = Board(self.env.env_variables)
        got_solution_set = evaluator.evaluate(board=board)
        self.assertIsNotNone(got_solution_set)


if __name__ == '__main__':
    unittest.main()
