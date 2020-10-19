import unittest
import gym
import connect_four
import numpy as np

from connect_four.agents import mcts
from connect_four.agents.mcts import MCTS
from connect_four.agents.mcts import MCTSNode
from connect_four.agents.mcts import MCTSNodeStatus
from connect_four.envs.connect_four_env import ConnectFourEnv

class TestMCST(unittest.TestCase):

  def setUp(self):
    self.env = gym.make('connect_four-v0')
    ConnectFourEnv.M = 4
    ConnectFourEnv.N = 4
    ConnectFourEnv.action_space = 4
    self.env.reset()

  def test_env_that_is_guaranteed_to_win(self):
    # this test verifies intended functionality of the env for a state
    # used in another test
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

    env_variables = self.env.get_env_variables()
    _, reward, done, _ = self.env.step(0)
    self.assertEqual(reward, ConnectFourEnv.INVALID_MOVE)
    self.assertEqual(mcts.TERMINAL_REWARDS_TO_STATUSES[ConnectFourEnv.INVALID_MOVE], MCTSNodeStatus.losing)

    self.env.reset(env_variables)
    _, reward, done, _ = self.env.step(3)
    self.assertEqual(reward, ConnectFourEnv.CONNECTED_FOUR)
    self.assertEqual(mcts.TERMINAL_REWARDS_TO_STATUSES[ConnectFourEnv.CONNECTED_FOUR], MCTSNodeStatus.winning)

  def test_update_tree(self):
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

    env_variables = self.env.get_env_variables()
    value = node.update_tree(env=self.env)
    self.env.reset(env_variables)

    explored_action = np.argmax(node.action_visits)

    if explored_action != 3:
      # If we found a losing action, keep exploring.
      self.assertEqual(node.status, MCTSNodeStatus.exploring)
    else:
      # If we found a winning action, this node is losing for the opponent.
      self.assertEqual(node.status, MCTSNodeStatus.losing)

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
    env_variables = self.env.get_env_variables()
    for i in range(ConnectFourEnv.action_space):
      node.update_tree(env=self.env)
      self.env.reset(env_variables)

    ### Phase 1: Validate a fully-explored node ###
    # This node is "losing" because it represents the win/loss status of the opponent.
    # self.assertEqual(node.status, MCTSNodeStatus.losing)
    # Verify that selecting action 3 is winning.
    self.assertEqual(node.children[3].status, MCTSNodeStatus.winning)

    # Verify action 3 was visited exactly once.
    # Other actions may not have been visited if we found 3 first.
    self.assertEqual(node.action_visits[3], 1)

    ### Phase 2: Verify nothing changes if we call update_tree one more time. ###
    node.update_tree(env=self.env)
    # This node is "losing" because it represents the win/loss status of the opponent.
    self.assertEqual(node.status, MCTSNodeStatus.losing)
    # Verify that selecting action 3 is winning.
    self.assertEqual(node.children[3].status, MCTSNodeStatus.winning)

    # Verify action 3 was visited exactly once.
    # Other actions may not have been visited if we found 3 first.
    self.assertEqual(node.action_visits[3], 1)

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
    agent = MCTS(num_rollouts=200)
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

  def test_prevent_opponent_from_winning_not_full_search(self):
    # Test to see if MCTS can find the optimal move without
    # searching the entire game tree.
    self.env.state = np.array([
      [
        [0, 0, 0, 0,],
        [0, 0, 0, 0,],
        [1, 1, 1, 0,],
        [0, 0, 0, 0,],
      ],
      [
        [0, 0, 0, 0,],
        [0, 0, 0, 0,],
        [0, 0, 0, 0,],
        [1, 1, 1, 0,],
      ],
    ])
    # Player 1 can prevent a win by playing action == 3.
    agent = MCTS(num_rollouts=64)
    action = agent.action(env=self.env, last_action=0)
    self.assertEqual(action, 3)


if __name__ == '__main__':
  unittest.main()