import unittest
import gym
import connect_four
import numpy as np

from connect_four.agents.mcts import MCTS
from connect_four.agents.mcts import MCTSNode
from connect_four.envs.connect_four_env import ConnectFourEnv

class TestMCST(unittest.TestCase):

  def setUp(self):
    self.env = gym.make('connect_four-v0')
    ConnectFourEnv.M = 4
    ConnectFourEnv.N = 4
    ConnectFourEnv.action_space = 4
    self.env.reset()

  def test_fully_explore_MCTSNode(self):
    self.env.state = np.array([
      [
        [0, 0, 0, 0,],
        [0, 0, 0, 1,],
        [0, 0, 0, 1,],
        [0, 0, 0, 1,],
      ],
      [
        [1, 1, 1, 0,],
        [1, 1, 1, 0,],
        [1, 1, 1, 0,],
        [1, 1, 1, 0,],
      ],
    ])
    # Player 1 can win by playing action == 3.
    # All other actions result in a loss.
    node = MCTSNode(num_actions=ConnectFourEnv.action_space)

    # MCTSNode should not re-explore terminal states,
    # so we should be guaranteed to have explored
    # all states after 4 iterations.
    for _ in range(ConnectFourEnv.action_space):
      node.update_tree(env=self.env)

    ### Phase 1: Validate a fully-explored node ###
    # Verify that action 3 has the highest total value.
    self.assertEqual(np.argmax(node.action_total_values), 3)
    # Verify each action has been visited exactly once.
    self.assertIsNone(np.testing.assert_array_equal(
      node.action_visits,
      np.ones(ConnectFourEnv.action_space),
    ))
    # Verify each action has been fully explored.
    self.assertTrue(np.all(node.fully_explored))

    ### Phase 2: Verify nothing changes if we call update_tree one more time. ###
    value = node.update_tree(env=self.env)
    # Verify that action 3 has the highest total value.
    self.assertEqual(np.argmax(node.action_total_values), 3)
    # Verify each action has been visited exactly once.
    self.assertIsNone(np.testing.assert_array_equal(
      node.action_visits,
      np.ones(ConnectFourEnv.action_space),
    ))
    # Verify each action has been fully explored.
    self.assertTrue(np.all(node.fully_explored))

  def test_winning_action_chosen_when_available(self):
    self.env.state = np.array([
      [
        [0, 0, 0, 0,],
        [0, 0, 0, 1,],
        [0, 0, 0, 1,],
        [0, 0, 0, 1,],
      ],
      [
        [1, 1, 1, 0,],
        [1, 1, 1, 0,],
        [1, 1, 1, 0,],
        [1, 1, 1, 0,],
      ],
    ])
    # Player 1 can win by playing action == 3.
    # All other actions result in a loss.
    agent = MCTS(num_rollouts=ConnectFourEnv.action_space)
    action = agent.action(self.env, last_action=None)
    self.assertEqual(action, 3)

  def test_take_draw_to_avoid_loss(self):
    # **Note**. This test makes an assumption that env.step(action) only checks
    # if the location of the **new token** results in a win.
    self.env.state = np.array([
      [
        [0, 0, 0, 0,],
        [0, 0, 0, 0,],
        [0, 0, 0, 0,],
        [0, 0, 0, 0,],
      ],
      [
        [1, 1, 0, 1,],
        [1, 1, 1, 1,],
        [1, 1, 1, 1,],
        [1, 1, 1, 1,],
      ],
    ])
    # Player 1 can draw by playing action == 2.
    agent = MCTS(num_rollouts=ConnectFourEnv.action_space)
    action = agent.action(env=self.env, last_action=0)
    self.assertEqual(action, 2)

  def test_guarantee_win_if_possible(self):
    self.env.state = np.array([
      [
        [0, 0, 0, 1,],
        [0, 0, 0, 0,],
        [1, 1, 1, 0,],
        [0, 1, 0, 1,],
      ],
      [
        [0, 0, 1, 0,],
        [1, 0, 1, 1,],
        [0, 0, 0, 1,],
        [1, 0, 1, 0,],
      ],
    ])
    # Player 1 can guarantee a win by playing action == 1.
    # Player 1 should see this if they perform 20 rollouts
    agent = MCTS(num_rollouts=20)
    action = agent.action(env=self.env, last_action=0)
    self.assertEqual(action, 1)

  def test_prevent_opponent_from_winning_full_search(self):
    self.env.state = np.array([
      [
        [0, 0, 1, 1,],
        [0, 0, 1, 0,],
        [0, 0, 0, 1,],
        [1, 0, 1, 0,],
      ],
      [
        [0, 0, 0, 0,],
        [0, 0, 0, 1,],
        [1, 1, 1, 0,],
        [0, 1, 0, 1,],
      ],
    ])
    # Player 1 can prevent a win by playing action == 1.
    # Player 1 should see this if they perform 52 rollouts
    agent = MCTS(num_rollouts=52)
    action = agent.action(env=self.env, last_action=0)
    self.assertEqual(action, 1)

  # def test_prevent_opponent_from_winning_not_full_search(self):
  #   # Test to see if MCTS can find the optimal move without
  #   # searching the entire game tree.
  #   self.env.state = np.array([
  #     [
  #       [0, 0, 0, 0,],
  #       [0, 0, 0, 0,],
  #       [1, 1, 1, 0,],
  #       [0, 0, 0, 0,],
  #     ],
  #     [
  #       [0, 0, 0, 0,],
  #       [0, 0, 0, 0,],
  #       [0, 0, 0, 0,],
  #       [1, 1, 1, 0,],
  #     ],
  #   ])
  #   # Player 1 can prevent a win by playing action == 3.
  #   agent = MCTS(num_rollouts=64)
  #   action = agent.action(env=self.env, last_action=0)
  #   self.assertEqual(action, 3)


if __name__ == '__main__':
  unittest.main()