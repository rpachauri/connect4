import gym

import numpy as np

from connect_four.envs.connect_four_env import ConnectFourEnv

class MCTSNode():
  # TERMINAL_REWARDS are the reward given upon arriving at a terminal state.
  # assumes that each of these rewards are distinct.
  TERMINAL_REWARDS = {
    # We'd rather let the opponent win than play an invalid move.
    ConnectFourEnv.INVALID_MOVE: -1000000,
    ConnectFourEnv.CONNECTED_FOUR: 100000,
    ConnectFourEnv.DRAW: 0,
  }

  def __init__(self, num_actions=7):
    self.children = {} # dictionary of moves to MCTSNodes

    self.action_total_values = np.zeros(num_actions)
    self.action_visits = np.zeros(num_actions)
    # fully_explored[action] indicates if all paths have been found
    # for that child/
    # If fully_explored[action], then action_total_values[action] must be set
    # to a TERMINAL_REWARDS value.
    self.fully_explored = np.zeros(num_actions, dtype=bool)


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
    all_actions = np.arange(env.action_space)
    # Only select from actions that are not fully explored.
    actions_left_to_explore = all_actions[np.logical_not(self.fully_explored)]

    if len(actions_left_to_explore) == 0:
      # We've fully explored this node.
      return np.max(self.action_total_values)

    action = np.random.choice(actions_left_to_explore)
    _, reward, done, _ = env.step(action)  # env is now at child.
    self.action_visits[action] += 1

    # Base case
    if done:
      # Makes the assumption that we can determine if
      # the agent has won/lost/drawn based on the reward.
      self.action_total_values[action] = MCTSNode.TERMINAL_REWARDS[reward]
      # We found a terminal state so this action has been fully explored.
      self.fully_explored[action] = True
      # We return reward and not MCTSNode.TERMINAL_REWARDS[reward] because it
      # would skew the action-values of parent nodes. This could be a
      # problem if another trajectory has an earlier guaranteed win.
      return reward
    
    if action not in self.children:
      # EXPANSION
      self.children[action] = MCTSNode(env.action_space)
      value = reward - self.children[action].rollout(env, done)
      self.action_total_values[action] += value
      return value
    
    # Recursive case
    value = reward - self.children[action].update_tree(env)
    self.action_total_values[action] += value

    # BACKUP
    self.adjust_action_value(action, value)
    return value


  def adjust_action_value(self, action, value):
    child = self.children[action]

    if np.all(child.fully_explored):
      # all of child's actions have been fully explored
      self.action_total_values[action] = -np.max(child.action_total_values)
      self.fully_explored[action] = True
    else:
      # this action has already been fully explored
      self.action_total_values[action] += value


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
    for _ in range(self.num_rollouts):
      self.root.update_tree(env)
      self.root_num_visits += 1
      env.reset(env_variables)

    # Select action with the highest action-value.
    action_values = np.divide(self.root.action_total_values, self.root.action_visits)
    # print("action_values =", action_values)
    # print("self.root.children[0].action_values =", self.root.children[0].action_total_values)
    # print("self.root.children[1].action_values =", self.root.children[1].action_total_values)
    # print("self.root.children[2].action_values =", self.root.children[2].action_total_values)
    # print("self.root.children[3].action_values =", self.root.children[3].action_total_values)
    best_action = np.nanargmax(action_values)

    self._move_root_to_action(best_action)
    return best_action


  def _move_root_to_action(self, child):
    # Move this tree to the state resulting from action.
    self.root_num_visits = self.root.action_visits[child]
    self.root = self.root.children[child] if child in self.root.children else MCTSNode()
    return child
    