import gym
import unittest

import numpy as np

from connect_four.agents import MCPNS
from connect_four.agents.victor import Victor

from connect_four.envs.connect_four_env import ConnectFourEnv


class TestVictor6x7(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 7
        self.env.reset()

    def test_action_6x7_a1_b1(self):
        # In this test case, Black is guaranteed at least a draw.
        # Initialize the agents
        agent1 = MCPNS(num_rollouts=100)
        agent2 = Victor()

        # This test case is based on Appendix B: Situation after 1. a1.
        _, reward, done, info = self.env.step(0)
        # self.env.render()
        _, reward, done, info = self.env.step(1)
        # self.env.render()
        last_action = 1

        while not done:
            # Let the agent whose turn it is select an action.
            if self.env.player_turn == 0:
                last_action = agent1.action(self.env, last_action)
            else:
                last_action = agent2.action(self.env, last_action)

            # print("Player", (self.env.player_turn + 1), "is placing a token in column:", last_action)
            _, reward, done, info = self.env.step(last_action)
            # self.env.render()

        if self.env.player_turn == 0:
            # If the game ends with White as the last move, White should have lost.
            self.assertEqual(reward, ConnectFourEnv.INVALID_MOVE)

        if self.env.player_turn == 1:
            # If the game ends with Black as the last move, Black could have either won or drawn.
            self.assertIn(reward, [ConnectFourEnv.DRAW, ConnectFourEnv.CONNECTED_FOUR])

    def test_action_6x7_diagram_8_1(self):
        # In this test case, White is guaranteed a win.
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

        # Initialize the agents
        agent1 = Victor()
        agent2 = MCPNS(num_rollouts=100)

        reward = 0
        done = False
        last_action = -1

        while not done:
            # Let the agent whose turn it is select an action.
            if self.env.player_turn == 0:
                last_action = agent1.action(self.env, last_action)
            else:
                last_action = agent2.action(self.env, last_action)

            # print("Player", (self.env.player_turn + 1), "is placing a token in column:", last_action)
            _, reward, done, info = self.env.step(last_action)
            # self.env.render()

        # The game mst end with White winning.
        self.assertEqual(reward, ConnectFourEnv.CONNECTED_FOUR)

    def test_action_6x7_diagram_8_1_proof_number_search(self):
        # In this test case, White is guaranteed a win, but needs to search the game tree.
        # This test case is based on Diagram 8.1, except e4 has not yet been played by White.
        # White is to move and White has an odd threat at a3.
        self.env.state = np.array([
            [
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
                [0, 0, 0, 0, 0, 0, 0, ],
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

        # Initialize the agents
        agent1 = Victor()
        agent2 = MCPNS(num_rollouts=1000)

        reward = 0
        done = False
        last_action = 4

        while not done:
            # Let the agent whose turn it is select an action.
            if self.env.player_turn == 0:
                last_action = agent1.action(self.env, last_action)
            else:
                last_action = agent2.action(self.env, last_action)

            # print("Player", (self.env.player_turn + 1), "is placing a token in column:", last_action)
            _, reward, done, info = self.env.step(last_action)
            # self.env.render()

        # The game mst end with White winning.
        self.assertEqual(reward, ConnectFourEnv.CONNECTED_FOUR)


if __name__ == '__main__':
    unittest.main()
