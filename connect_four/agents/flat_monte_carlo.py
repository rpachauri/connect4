import numpy as np

from connect_four.agents.agent import Agent

np.seterr(divide='ignore', invalid='ignore')


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


class FlatMonteCarlo(Agent):

    def __init__(self, num_rollouts):
        """

    Args:
      num_rollouts: the number of rollouts we simulate
  """
        self.num_rollouts = num_rollouts

    def action(self, env, last_action):
        """Returns an action.

    Args:
      env: a plannable gym.Env
      last_action: the last_action we took
    Requires:
      - env must implement get_env_variables, which returns a variable that can
        be passed to env.reset() to restore a state (this supports planning agents)
      - env is a deterministic environment.
      - action space of env is finite.
    Returns:
      the best action after performing num_rollouts simulations
  """
        # Perform rollouts.
        env_variables = env.get_env_variables()
        for _ in range(self.num_rollouts):
            # TODO: select an action to rollout with.
            # TODO: perform a rollout with the selected action.
            env.reset(env_variables)

        pass

    def _select_action_for_rollout(self):
        pass
