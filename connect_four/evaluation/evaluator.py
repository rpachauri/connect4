from abc import ABC, abstractmethod
from enum import Enum

from connect_four.envs import TwoPlayerGameEnv


class ProofType(Enum):
    Unknown = 0
    Proven = 1
    Disproven = 2


class Evaluator(ABC):

    @abstractmethod
    def __init__(self, model: TwoPlayerGameEnv):
        pass

    @abstractmethod
    def move(self, action: int):
        pass

    @abstractmethod
    def undo_move(self):
        pass

    @abstractmethod
    def evaluate(self) -> ProofType:
        pass
