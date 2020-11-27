import unittest

import gym
import numpy as np

from connect_four.agents import FlatMonteCarlo
from connect_four.envs.connect_four_env import ConnectFourEnv


class TestFlatMonteCarlo(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 4
        ConnectFourEnv.N = 4
        ConnectFourEnv.action_space = 4
        self.env.reset()

    def test_immediate_winning_action_selected(self):
        # Assumes env.step() only evaluates the win condition based
        # on the most recent move.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, ],
                [0, 0, 0, 1, ],
                [0, 0, 0, 1, ],
                [0, 0, 0, 1, ],
            ],
            [
                [1, 1, 1, 0, ],
                [1, 1, 1, 0, ],
                [1, 1, 1, 0, ],
                [1, 1, 1, 0, ],
            ],
        ])
        agent = FlatMonteCarlo(num_rollouts=100)
        action = agent.action(env=self.env)
        self.assertEqual(3, action)

    def test_immediate_drawing_action_selected(self):
        # Assumes env.step() only evaluates the win condition based
        # on the most recent move.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
            ],
            [
                [1, 1, 1, 0, ],
                [1, 1, 1, 1, ],
                [1, 1, 1, 1, ],
                [1, 1, 1, 1, ],
            ],
        ])
        agent = FlatMonteCarlo(num_rollouts=100)
        action = agent.action(env=self.env)
        self.assertEqual(3, action)

    def test_drawing_action_one_move_away_chosen(self):
        # Assumes env.step() only evaluates the win condition based
        # on the most recent move.
        self.env.state = np.array([
            [
                [0, 0, 1, 0, ],
                [0, 0, 1, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
            ],
            [
                [1, 1, 0, 0, ],
                [1, 1, 0, 0, ],
                [1, 1, 1, 1, ],
                [1, 1, 1, 1, ],
            ],
        ])
        agent = FlatMonteCarlo(num_rollouts=100)
        action = agent.action(env=self.env)
        self.assertEqual(3, action)


if __name__ == '__main__':
    unittest.main()
