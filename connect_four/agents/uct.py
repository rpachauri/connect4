import numpy as np

from connect_four.agents.agent import Agent


class UCTNode:
    EXPLORATION_CONSTANT = 4

    def __init__(self, num_actions=7):
        self.children = {}  # dictionary of moves to UCTNodes

        self.action_total_values = np.zeros(num_actions)
        self.action_visits = np.zeros(num_actions)

    def update_tree(self, env):
        """Performs UCT for this node and all children of this node.

      Args:
       - env is a "plannable" OpenAI gym environment.
      Requires:
       - env's state is at the current node
      Effects:
       - Creates a new leaf node.
       - Updates the value estimate for each node along this path
      Returns:
       - the value of the new leaf node
      """
        # SELECTION
        # Select an action using Upper Confidence Bounds.
        action = self.select_action_for_rollout()

        _, reward, done, _ = env.step(action)  # env is now at child.
        self.action_visits[action] += 1

        if action not in self.children:
            # Base case
            # EXPANSION
            self.children[action] = UCTNode(env.action_space)

            if done:  # action leads to a terminal state
                return reward
            else:  # action needs to be explored further.
                return reward - self.rollout(env, done)

        # Recursive case
        # value is the action-value.
        # (the reward minus the state-value of the state resulting from action)
        value = reward - self.children[action].update_tree(env)

        # BACKUP
        # If the child status is still exploring, add to the estimate.
        self.action_total_values[action] += value

        return value

    def select_action_for_rollout(self):
        # Select an action from the environment's action space using bandit-based selection.
        action_values = np.divide(self.action_total_values, self.action_visits)
        exploration_values = UCTNode.EXPLORATION_CONSTANT * np.sqrt(2 * np.log(np.sum(self.action_visits)) / self.action_visits)
        return np.argmax(action_values + exploration_values)

    @staticmethod
    def rollout(env, done):
        """

      Args:
        env (gym.Env):
        done (bool):

      Returns:
        value (float): the total return after performing rollout from the state env is in
      """
        value = 0
        while not done:
            all_actions = np.arange(env.action_space)
            action = np.random.choice(all_actions)
            _, r, done, _ = env.step(action)
            value += r
            # inverse the value now that it is the other player's turn
            value *= -1
        return value


class UCT(Agent):

    def __init__(self, num_rollouts):
        """

    Args:
      num_rollouts: the number of rollouts we simulate
  """
        self.root = None
        self.num_rollouts = num_rollouts
        self.root_num_visits = 1  # number of times we've visited the root node

    def action(self, env, last_action=None):
        """Returns an action.

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
  """
        if self.root is None:
            # Initialize tree if this is the first time action() is being called.
            self.root = UCTNode(env.action_space)
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

        # Uncomment below line to see the number of times each action was visited.
        print("self.root.action_visits =", self.root.action_visits, "=>", np.sum(self.root.action_visits))

        # Select action with the highest number of visits.
        most_visited_action = np.argmax(self.root.action_visits)

        self._move_root_to_action(most_visited_action)
        return most_visited_action

    def _move_root_to_action(self, child):
        # Move the root node of this tree to the state resulting from action.
        self.root_num_visits = self.root.action_visits[child]
        self.root = self.root.children[child] if child in self.root.children else UCTNode()
        return child
