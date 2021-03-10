import numpy as np

from connect_four.agents.agent import Agent
from connect_four.envs import TwoPlayerGameEnv


class Minimax(Agent):
    """ A Minimax agent applies the Minimax algorithm up to some depth before
  estimating the value of a state.
  """
    # TERMINAL_REWARDS are the reward given upon arriving at a terminal state.
    # assumes that each of these rewards are distinct.
    TERMINAL_REWARDS = {
        TwoPlayerGameEnv.INVALID_MOVE: -1000000,
        TwoPlayerGameEnv.CONNECTED_FOUR: 100000,  # We'd rather let the opponent win than play an invalid move.
        TwoPlayerGameEnv.DRAW: 0,
    }

    def __init__(self, max_depth=4):
        self.max_depth = max_depth
        pass

    def action(self, env, last_action=None):
        # last_action gets ignored
        return self._minimax(env, self.max_depth)[0]

    def _minimax(self, env, depth, gamma=0.99):
        # Get the current state and player.
        env_variables = env.env_variables

        action_values = []

        for action in range(env.action_space):
            # apply move
            _, reward, done, _ = env.step(action)
            if done:
                # makes the assumption that we can determine if the agent has won/lost/drawn based on the reward.
                action_values.append(Minimax.TERMINAL_REWARDS[reward])
            elif depth == 1:
                # reward goes to the current player.
                # self.estimate() is the estimated total return for the other player.
                value_estimate = reward - self._estimate(env)
                action_values.append(value_estimate)
            else:
                # self.minimax() is the estimated total return for the other player.
                _, other_player_value = self._minimax(env, depth - 1)
                # reward goes to the current player.
                value = reward - other_player_value
                action_values.append(value)
            # undo move
            env.reset(env_variables)

        best_action = np.argmax(np.array(action_values))
        # noinspection PyTypeChecker
        return best_action, gamma * action_values[best_action]

    def _estimate(self, env):
        """_estimate returns the estimated value of a state for a particular player.
      This function assumes that it will not be called for a terminal state.

      Args:
        env (TwoPlayerGameEnv): right now, Minimax only supports the
          TwoPlayerGameEnv because the _estimate() function is handwritten for
          each environment.
      Returns:
        estimate (float): an estimate of how valuable the current state is to the current player.
    """
        env_variables = env.env_variables
        obs = env_variables[0]
        current_player = env_variables[1]

        estimate = 0
        for player in range(len(obs)):
            # multiplier is +1 if player is same as current_player
            # multiplier is -1 if player is different from current_player
            multiplier = 2 * abs(player - current_player) - 1

            for row in range(len(obs[0])):
                for col in range(len(obs[0][0])):
                    if obs[player, row, col] == 1:
                        estimate += multiplier * (10 ** self._num_tokens_left_diagonally(obs, player, row, col))
                        estimate += multiplier * (10 ** self._num_tokens_vertically(obs, player, row, col))
                        estimate += multiplier * (10 ** self._num_tokens_right_diagonally(obs, player, row, col))
                        estimate += multiplier * (10 ** self._num_tokens_horizontally(obs, player, row, col))

        return estimate

    def _num_tokens_left_diagonally(self, obs, player, row, col):
        num_tokens_in_pos_direction = self._num_tokens_in_direction(obs, player, row, col, -1, -1)
        num_tokens_in_neg_direction = self._num_tokens_in_direction(obs, player, row, col, 1, 1)
        return num_tokens_in_pos_direction + 1 + num_tokens_in_neg_direction

    def _num_tokens_vertically(self, obs, player, row, col):
        num_tokens_in_pos_direction = self._num_tokens_in_direction(obs, player, row, col, -1, 0)
        num_tokens_in_neg_direction = self._num_tokens_in_direction(obs, player, row, col, 1, 0)
        return num_tokens_in_pos_direction + 1 + num_tokens_in_neg_direction

    def _num_tokens_right_diagonally(self, obs, player, row, col):
        num_tokens_in_pos_direction = self._num_tokens_in_direction(obs, player, row, col, 1, -1)
        num_tokens_in_neg_direction = self._num_tokens_in_direction(obs, player, row, col, -1, 1)
        return num_tokens_in_pos_direction + 1 + num_tokens_in_neg_direction

    def _num_tokens_horizontally(self, obs, player, row, col):
        num_tokens_in_pos_direction = self._num_tokens_in_direction(obs, player, row, col, 0, 1)
        num_tokens_in_neg_direction = self._num_tokens_in_direction(obs, player, row, col, 0, -1)
        return num_tokens_in_pos_direction + 1 + num_tokens_in_neg_direction

    @staticmethod
    def _num_tokens_in_direction(obs, player, row, col, row_add, col_add):
        """ Finds the number of tokens belonging to the given player starting
          from the given location and continuing in the given direction.

      Args:
        player (int): 0 or 1. The player we are checking.
        row (int): the starting row
        col (int): the starting column
        row_add (int): the increment for row
        col_add (int): the increment for col

      Returns:
        The number of tokens belonging to the player in the given direction.
        The starting location is not included.
        E.g. If there is only 1 token belonging to the player
             adjacent to the given location, returns 1.
    """
        player_tokens = obs[player]
        r, c = row, col
        num_tokens = -1

        # while we are still in bounds and the location belongs to the player.
        while (0 <= r < len(player_tokens) and 0 <= c < len(player_tokens[0]) and
               player_tokens[r, c] == 1):
            r += row_add
            c += col_add
            num_tokens += 1
        return num_tokens
