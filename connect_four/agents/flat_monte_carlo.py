import numpy as np

from connect_four.agents.agent import Agent

np.seterr(divide='ignore', invalid='ignore')


class FlatMonteCarlo(Agent):

    def __init__(self, num_rollouts):
        """

    Args:
      num_rollouts: the number of rollouts we simulate
  """
        self.num_rollouts = num_rollouts

    def action(self, env, last_action=None):
        """Returns an action.

    Args:
      env: a plannable gym.Env
      last_action: the last_action we took. None by default.
    Requires:
      - env must implement get_env_variables, which returns a variable that can
        be passed to env.reset() to restore a state (this supports planning agents)
      - env is a deterministic environment.
      - action space of env is finite.
    Returns:
      the best action after performing num_rollouts simulations
  """
        action_total_values = np.zeros(env.action_space)
        action_visits = np.zeros(env.action_space)

        # Perform rollouts.
        env_variables = env.get_env_variables()
        for _ in range(self.num_rollouts):
            # Select an action for rollout.
            action = self._select_action_for_rollout(env)

            # Perform a rollout after taking the action.
            value = self.rollout(env, action)

            # Adjust action-value for the action.
            action_total_values[action] += value
            action_visits[action] += 1

            # Reset the environment to the original state.
            env.reset(env_variables)

        # Select action with the highest action-value.
        action_values = np.divide(action_total_values, action_visits)
        best_action = np.nanargmax(action_values)
        return best_action

    @staticmethod
    def _select_action_for_rollout(env):
        # Select a random action from the environment's action space.
        all_actions = np.arange(env.action_space)
        action = np.random.choice(all_actions)
        return action

    @staticmethod
    def rollout(env, action):
        """Obtains a sample estimate of the action-value for the current
        environment's player.

      Args:
        env (gym.Env): a gym.Env object. Note that this function modifies env
                and env will reach a terminal state. Assumes a terminal state
                is reachable through uniform random move selection.
        action (int): The action to obtain a sample estimate of the action-value for.

      Returns:
        value (float): the total return after performing rollout from the state env is in
      """
        _, r, done, _ = env.step(action)
        value = r

        while not done:
            # Inverse the value now that it is the other player's turn.
            value *= -1

            # Select a random action.
            all_actions = np.arange(env.action_space)
            action = np.random.choice(all_actions)
            _, r, done, _ = env.step(action)

            # Increase the reward for the player.
            value += r

        return value
