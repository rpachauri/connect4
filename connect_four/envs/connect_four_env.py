from typing import Sequence

import numpy as np

from connect_four.envs import TwoPlayerGameEnv
from connect_four.envs import TwoPlayerGameEnvVariables
from connect_four.envs import connect_utils


class ConnectFourEnv(TwoPlayerGameEnv):
    """Implements the gym.Env interface.
  
    https://github.com/openai/gym/blob/master/gym/core.py.
    """

    # Dimension of the ConnectFour environment.
    M = 6
    N = 7

    action_space = N

    def __init__(self):
        self.reset()
        pass

    def step(self, action: int):
        """

        Args:
          action (int): 
        """
        # Find the highest token in the given column.
        highest_token = self._find_highest_token(action)
        # The location of the new token will be one above the highest token.
        new_token_row = highest_token - 1

        # Placing a token in a full column is an invalid move.
        if new_token_row == -1:
            return self.state.copy(), TwoPlayerGameEnv.INVALID_MOVE, True, None

        # Place a token.
        self.state[self.player_turn, new_token_row, action] = 1

        # Check if the player has connected four.
        if self._connected_four(row=new_token_row, col=action):
            return self.state.copy(), TwoPlayerGameEnv.CONNECTED, True, None

        # If all locations have been used and neither player has won,
        # this results in a draw.
        if self._is_full():
            return self.state.copy(), TwoPlayerGameEnv.DRAW, True, None

        # Continue play with it now being the other player's turn.
        self.player_turn = 1 - self.player_turn
        return self.state.copy(), TwoPlayerGameEnv.DEFAULT_REWARD, False, None

    def _find_highest_token(self, column) -> int:
        """ Finds the highest token belonging to either player in the selected column.

        Args:
            column (int): 0 ≤ column < ConnectFourEnv.N
        Returns:
            row (int): 0 ≤ row < ConnectFourEnv.M if there exist at least 1 token belonging to either player.
                ConnectFourEnv.M if there are no tokens in the column
        """
        # mask is a boolean array. It is true if there is a token in the given column and false otherwise.
        mask = (self.state[:, :, column] != 0).any(axis=0)
        # get the highest row in the given column belonging to either player.
        return int(np.where(mask.any(axis=0), mask.argmax(axis=0), ConnectFourEnv.M))

    def _connected_four(self, row: int, col: int) -> bool:
        """
        Args:
            row (int): the starting row
            col (int): the starting column

        Requires:
            self.state[player, row, col] == 1

        Returns:
            connected_four (bool): True if the player connected at least 4 using (row, col);
                               otherwise, False
        """
        return connect_utils.connected(state=self.state, num_to_connect=4, player=self.player_turn, row=row, col=col)

    def _is_full(self):
        """
        Returns:
            True if there is a token belonging to either player for every possible location.
        """
        return (self.state != 0).any(axis=0).all()

    @property
    def env_variables(self) -> TwoPlayerGameEnvVariables:
        """
        Returns:
            env_variables (tuple): a tuple that can be passed to reset() to restore a state.
            - env_variables[0] contains "obs", the observable variable for that state.
            - env_variables[1] contains "player_turn", indicating whose turn it is in that state.
        """
        return TwoPlayerGameEnvVariables(self.state.copy(), self.player_turn)

    def reset(self, env_variables=None):
        """Resets the state of the environment and returns an initial observation.

        Args:
            env_variables (tuple) (optional):
                env_variables[0] (ndarray): should be a a numpy ndarray of shape (2, M, N)
                env_variables[1] (int): whose turn it should be (0 or 1)

        Example Usage:
            env_variables = env.env_variables()
            env.step(action)
            .
            .
            .
            env.reset(env_variables)

        Returns:
            observation (object): the initial observation.
        """
        if env_variables is not None:
            self.state = env_variables[0].copy()
            self.player_turn = env_variables[1]
        else:
            self.state = np.zeros(shape=(2, ConnectFourEnv.M, ConnectFourEnv.N))
            self.player_turn = 0

        return self.state.copy()

    def undo_last_action(self, action):
        """ TODO Deprecate.

        Args:
            action (int): an Action

        Raises:
            ValuerError if:
            1. The environment is in the initial state.
            2. There must be at least one token in the given column (i.e. action)
            3. The top token in the given column must belong to the opponent of the current player.

        Modifies:
            - this ConnectFourEnv instance will have undone the given action.
        """
        # If there are no tokens in the state:
        if np.sum(self.state) == 0:
            raise ValueError("Cannot undo action for initial state")

        # Find the highest token that belongs to either player in the given column.
        highest_row = self._find_highest_token(column=action)

        # If the given column is empty:
        if highest_row == ConnectFourEnv.M:
            raise ValueError("Cannot undo action for empty column")

        # If the highest token belongs to the current player:
        if self.state[self.player_turn][highest_row][action] == 1:
            raise ValueError("Cannot undo action that belongs to the current player")

        # Remove the token and switch play to the other player.
        self.state[1 - self.player_turn, highest_row, action] = 0
        self.player_turn = 1 - self.player_turn

    def render(self, mode='human'):
        """Renders the current state of the environment.

        Args:
          mode (str): Supported modes: {'human'}
        """
        horizontal_wall = self._create_horizontal_wall()
        print(horizontal_wall)

        # plot the environment.
        for m in range(ConnectFourEnv.M):
            line = "|"
            for n in range(ConnectFourEnv.N):
                if self.state[0, m, n] == 1:  # token belongs to Player 1
                    line += "x"
                elif self.state[1, m, n] == 1:  # token belongs to Player 2
                    line += "o"
                else:  # location belongs to neither player
                    line += " "
            print(line + "|")

        print(horizontal_wall)

    @staticmethod
    def _create_horizontal_wall():
        """Used to help render the top or bottom wall in human mode.
        Returns:
          str: a string that can be printed when rendering in human mode.
        """
        wall = "*"
        for i in range(ConnectFourEnv.N):
            wall += "="
        return wall + "*"

    def actions(self) -> Sequence[int]:
        available_actions = []
        for col in range(ConnectFourEnv.N):
            if self._find_highest_token(column=col) > 0:
                available_actions.append(col)
        return available_actions
