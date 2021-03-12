import gym

from abc import ABC, abstractmethod
from collections import namedtuple

TwoPlayerGameEnvVariables = namedtuple("TicTacToeEnvVariables", ["state", "player_turn"])


class TwoPlayerGameEnv(gym.Env, ABC):
    INVALID_MOVE = -1
    CONNECTED = 1
    DRAW = 0
    DEFAULT_REWARD = 0

    @property
    @abstractmethod
    def env_variables(self) -> TwoPlayerGameEnvVariables:
        pass

    @abstractmethod
    def reset(self, env_variables: TwoPlayerGameEnvVariables = None):
        pass
