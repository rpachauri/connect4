import gym
import unittest

from connect_four.agents import MCPNS
from connect_four.agents.victor import Victor

from connect_four.envs.connect_four_env import ConnectFourEnv


class TestVictor6x7(unittest.TestCase):
    def setUp(self) -> None:
        self.env = gym.make('connect_four-v0')
        ConnectFourEnv.M = 6
        ConnectFourEnv.N = 7
        self.env.reset()

    def test_evaluate_6x7_a1(self):
        # Initialize the agents
        agent1 = MCPNS(num_rollouts=1000)
        agent2 = Victor()

        # This test case is based on Appendix B: Situation after 1. a1.
        _, reward, done, info = self.env.step(0)
        self.env.render()
        _, reward, done, info = self.env.step(1)
        self.env.render()
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


if __name__ == '__main__':
    unittest.main()
