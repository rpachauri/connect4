import unittest

import gym
import numpy as np

from connect_four.agents.minimax import Minimax
from connect_four.envs.connect_four_env import ConnectFourEnv


class TestMinimax(unittest.TestCase):

    def setUp(self):
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 4
        ConnectFourEnv.N = 4
        ConnectFourEnv.action_space = 4
        self.env.reset()

    def test_winning_action_chosen_when_available(self):
        self.env.state = np.array([
            [
                [0, 0, 0, 0, ],
                [0, 0, 0, 1, ],
                [0, 0, 0, 1, ],
                [0, 0, 0, 1, ],
            ],
            [
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 1, 0, 0, ],
                [0, 1, 1, 0, ],
            ],
        ])
        # Player 1 can win by playing action == 3.
        agent = Minimax(max_depth=1)
        action = agent.action(env=self.env, last_action=0)
        self.assertEqual(action, 3)

    def test_take_draw_to_avoid_loss(self):
        # **Note**. This test makes an assumption that env.step(action) only checks
        # if the location of the **new token** results in a win.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
            ],
            [
                [1, 1, 0, 1, ],
                [1, 1, 1, 1, ],
                [1, 1, 1, 1, ],
                [1, 1, 1, 1, ],
            ],
        ])
        # Player 1 can draw by playing action == 2.
        agent = Minimax(max_depth=1)
        action = agent.action(env=self.env, last_action=0)
        self.assertEqual(action, 2)

    def test_prevent_opponent_from_winning(self):
        self.env.state = np.array([
            [
                [0, 0, 0, 0, ],
                [0, 0, 0, 0, ],
                [0, 1, 0, 0, ],
                [0, 1, 1, 0, ],
            ],
            [
                [0, 0, 0, 0, ],
                [0, 0, 0, 1, ],
                [0, 0, 0, 1, ],
                [0, 0, 0, 1, ],
            ],
        ])
        # Player 2 can win by playing action == 3.
        # Since it's Player 1's turn, they should play action == 3 to prevent that.
        agent = Minimax(max_depth=1)
        action = agent.action(env=self.env, last_action=0)
        self.assertEqual(action, 3)

    def test_guarantee_win_if_possible(self):
        self.env.state = np.array([
            [
                [0, 0, 0, 1, ],
                [0, 0, 0, 0, ],
                [1, 1, 1, 0, ],
                [0, 1, 0, 1, ],
            ],
            [
                [0, 0, 1, 0, ],
                [1, 0, 1, 1, ],
                [0, 0, 0, 1, ],
                [1, 0, 1, 0, ],
            ],
        ])
        # Player 1 can guarantee a win by playing action == 1.
        # Player 1 should see this if they look 3 steps ahead.
        agent = Minimax(max_depth=3)
        action = agent.action(env=self.env, last_action=0)
        self.assertEqual(action, 1)


if __name__ == '__main__':
    unittest.main()
