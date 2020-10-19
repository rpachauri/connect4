import gym

import numpy as np
np.seterr(divide='ignore', invalid='ignore')
from connect_four.envs.connect_four_env import ConnectFourEnv
from enum import Enum

class MCTSNodeStatus(Enum):
  exploring = 0
  winning = 1
  drawing = 2
  losing = 3
  terminal = 4

# TERMINAL_REWARDS are the reward given upon arriving at a terminal state.
# assumes that each of these rewards are distinct.
TERMINAL_REWARDS_TO_STATUSES = {
  ConnectFourEnv.INVALID_MOVE: MCTSNodeStatus.losing,
  ConnectFourEnv.CONNECTED_FOUR: MCTSNodeStatus.winning,
  ConnectFourEnv.DRAW: MCTSNodeStatus.drawing,
}

STATUSES_TO_VALUES = {
  MCTSNodeStatus.losing: -1000,
  MCTSNodeStatus.winning: 100,
  MCTSNodeStatus.drawing: 0,
}

class MCTSNode():

  def __init__(self, num_actions=7):
    self.children = {} # dictionary of moves to MCTSNodes

    self.action_total_values = np.zeros(num_actions)
    self.action_visits = np.zeros(num_actions)

    # Every node is initialized with a status of exploring.
    self.status = MCTSNodeStatus.exploring

  def update_tree(self, env):
    '''Performs MCTS for this node and all children of this node.
    
      Args:
       - env is a "plannable" OpenAI gym environment.
      Requires:
       - env's state is at the current node
      Effects:
       - Creates a new leaf node.
       - Updates the value estimate for each node along this path
      Returns:
       - the value of the new leaf node
    '''
    # SELECTION
    # Only select from actions that are not fully explored.
    actions_left_to_explore = self.get_actions_left_to_explore(env)
    # print("actions_left_to_explore =", actions_left_to_explore)

    if len(actions_left_to_explore) == 0:
      # We've fully explored this node.
      return max(self.action_total_values)

    # Select a random action that still needs exploring.
    action = np.random.choice(np.array(actions_left_to_explore))
    # print("taking action", action)
    _, reward, done, _ = env.step(action)  # env is now at child.
    self.action_visits[action] += 1

    # EXPANSION
    # Base case
    if action not in self.children:
      
      self.children[action] = MCTSNode(env.action_space)

      if done:
        # Makes the assumption that we can determine if
        # the agent has won/lost/drawn based on the reward.
        self.children[action].status = TERMINAL_REWARDS_TO_STATUSES[reward]
        self.status = self.get_new_status(env)
        self.action_total_values[action] = STATUSES_TO_VALUES[self.children[action].status]
        return reward

      value = reward - self.children[action].rollout(env, done)
      self.action_total_values[action] += value
      return value

    # Recursive case
    value = reward - self.children[action].update_tree(env)    

    # BACKUP
    # Change the status of this node based on the child nodes.
    self.status = self.get_new_status(env)

    if self.children[action].status == MCTSNodeStatus.exploring:
      # If the child status is still exploring, add to the estimate.
      self.action_total_values[action] += value
    else:
      # If the child status is no longer exploring, hardcode the action value.
      self.action_total_values[action] = STATUSES_TO_VALUES[self.children[action].status]
    return value

  def get_actions_left_to_explore(self, env):
    # Only return actions for which there is no node or
    # the existing node is still exploring.
    actions_left_to_explore = []
    for action in range(env.action_space):
      if action not in self.children or self.children[action].status == MCTSNodeStatus.exploring:
        actions_left_to_explore.append(action)
      elif self.children[action].status == MCTSNodeStatus.winning:
         # If this node has a winning action, there is no need to explore anymore.
        return []
    return actions_left_to_explore

  def rollout(self, env, done):
    value = 0
    while not done:
      all_actions = np.arange(env.action_space)
      action = np.random.choice(all_actions)
      _, r, done, _ = env.step(action)
      value += r
      # inverse the value now that it is the other player's turn
      value *= -1
    return value

  def get_new_status(self, env):
    # If there is a winning action, this node is losing.
    # Child statuses can be one of [exploring, winning, drawing, losing]
    for action in self.children:
      child = self.children[action]
      if child.status == MCTSNodeStatus.winning:
        # self.action_total_values[action] = STATUSES_TO_VALUES[MCTSNodeStatus.winning]
        return MCTSNodeStatus.losing

    # If we're missing a child, this node is still exploring.
    if len(self.children) < env.action_space:
      return MCTSNodeStatus.exploring

    # If there is an action that still needs to be explored, this node is exploring.
    # Possible child statuses can be one of [exploring, drawing, losing]
    for action in self.children:
      child = self.children[action]
      if child.status == MCTSNodeStatus.exploring:
        return MCTSNodeStatus.exploring

    # If we can only draw or lose, this node is drawing.
    # Possible child statuses can be one of [drawing, losing]
    for action in self.children:
      child = self.children[action]
      if child.status == MCTSNodeStatus.drawing:
        # self.action_total_values[action] = STATUSES_TO_VALUES[MCTSNodeStatus.drawing]
        return MCTSNodeStatus.drawing

    # All child statuses must be losing, so this node is winning.
    # self.action_total_values[action] = STATUSES_TO_VALUES[MCTSNodeStatus.losing]
    return MCTSNodeStatus.winning

class MCTS():

  def __init__(self, num_rollouts):
    '''

      Args:
        num_rollouts: the number of rollouts we simulate
    '''
    self.root = None
    self.num_rollouts = num_rollouts

  def action(self, env, last_action):
    '''Returns an action.
      
      Args:
        env: a plannable gym.Env
        last_action: the last_action we took
      Requires:
        - env must implement get_env_variables, which returns a variable that can
          be passed to env.reset() to restore a state (this supports planning agents)
        - env is a deterministic environment.
        - action space of env is finite.
        - current state of env MUST match one of self.root.children
      Effects:
        - performs a number of rollouts
        - selects an action and moves this tree's root to the resulting state
        - the original environment is restored if modified
      Returns:
        the best action after performing num_rollouts simulations
    '''
    if self.root is None:
      # Initialize tree if this is the first time action() is being called.
      self.root = MCTSNode(env.action_space)
      self.root_num_visits = 1  # number of times we've visited the root node
    elif last_action is not None:
      # Move down a node to record the opponent's move.
      # If this tree has just been initialized, pass since there is no node to move to.
      self._move_root_to_action(last_action)

    # Perform rollouts.
    env_variables = env.get_env_variables()
    for i in range(self.num_rollouts):
      self.root.update_tree(env)
      self.root_num_visits += 1
      env.reset(env_variables)

    # Otherwise, select action with the highest action-value.
    action_values = np.divide(self.root.action_total_values, self.root.action_visits)
    best_action = np.nanargmax(action_values)

    self._move_root_to_action(best_action)
    return best_action


  def _move_root_to_action(self, child):
    # Move this tree to the state resulting from action.
    self.root_num_visits = self.root.action_visits[child]
    self.root = self.root.children[child] if child in self.root.children else MCTSNode()
    return child
    