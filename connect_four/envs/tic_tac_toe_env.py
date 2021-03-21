import numpy as np

from typing import Sequence

from connect_four.envs import TwoPlayerGameEnv
from connect_four.envs import TwoPlayerGameEnvVariables
from connect_four.envs import connect_utils


class TicTacToeEnv(TwoPlayerGameEnv):
    """Implements the gym.Env interface.

        https://github.com/openai/gym/blob/master/gym/core.py.
        """
    # Dimension of the ConnectFour environment.
    M = 3
    N = 3

    action_space = M * N

    def __init__(self):
        self.reset()
        pass

    def step(self, action: int):
        """

        Args:
          action (int):
        """
        if action not in self.actions():
            raise ValueError(action, "not in", self.actions())

        # Convert the action to a row and col in the TicTacToeEnv.
        row, col = self._action_to_square(action=action)

        # # Placing a token in a square that already contains a token is an invalid move.
        # if self._contains_token(row=row, col=col):
        #     return self.state.copy(), TwoPlayerGameEnv.INVALID_MOVE, True, None

        # Place a token.
        self.state[self.player_turn, row, col] = 1

        # Check if the player has connected three.
        if self._connected_three(row=row, col=col):
            return self.state.copy(), TwoPlayerGameEnv.CONNECTED, True, None

        # If all locations have been used and neither player has won,
        # this results in a draw.
        if self._is_full():
            return self.state.copy(), TwoPlayerGameEnv.DRAW, True, None

        # Continue play with it now being the other player's turn.
        self.player_turn = 1 - self.player_turn
        return self.state.copy(), TwoPlayerGameEnv.DEFAULT_REWARD, False, None

    @staticmethod
    def _action_to_square(action: int) -> (int, int):
        """
        Raises:
            ValueError: if not 0 ≤ action ≤ 8.

        Args:
            action (int): 0 ≤ action ≤ 8.

        Returns:
            row (int): 0 ≤ row ≤ 2.
            col (int): 0 ≤ col ≤ 2.
        """
        if action < 0 or 9 <= action:
            raise ValueError("0 ≤ action < 9 must be true, received:", action)
        return action // 3, action % 3

    def _contains_token(self, row: int, col: int) -> bool:
        """
        Args:
            row (int): 0 ≤ row ≤ 2.
            col (int): 0 ≤ col ≤ 2.

        Returns:
            contains_token (bool): whether or not a token already belongs to either player at the given row and column.
        """
        return self.state[0][row][col] == 1 or self.state[1][row][col] == 1

    def _connected_three(self, row: int, col: int) -> bool:
        """
        Args:
            row (int): the starting row
            col (int): the starting column

        Requires:
            self.state[player, row, col] == 1

        Returns:
            connected_three (bool): True if the player connected three using (row, col);
                               otherwise, False
        """
        return connect_utils.connected(state=self.state, num_to_connect=3, player=self.player_turn, row=row, col=col)

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
            self.state = np.zeros(shape=(2, TicTacToeEnv.M, TicTacToeEnv.N))
            self.player_turn = 0

        return self.state.copy()

    def render(self, mode='human'):
        """Renders the current state of the environment.

        Args:
          mode (str): Supported modes: {'human'}
        """
        print(self._create_horizontal_row(row=0) + self._create_horizontal_divider() +
              self._create_horizontal_row(row=1) + self._create_horizontal_divider() +
              self._create_horizontal_row(row=2))

    def _create_horizontal_row(self, row: int):
        return self._create_square(row=row, col=0) + "|" + \
               self._create_square(row=row, col=1) + "|" + \
               self._create_square(row=row, col=2) + "\n"

    def _create_square(self, row: int, col: int):
        # Assumes a square belongs to at most one player.
        if self.state[0][row][col] == 1:
            return "x"
        if self.state[1][row][col] == 1:
            return "o"
        return " "

    @staticmethod
    def _create_horizontal_divider():
        return "-*-*-\n"

    def actions(self) -> Sequence[int]:
        list_of_actions = []
        for row in range(len(self.state[0])):
            for col in range(len(self.state[0][0])):
                if self.state[0][row][col] == 0 and self.state[1][row][col] == 0:
                    list_of_actions.append(row * 3 + col)
        return list_of_actions
