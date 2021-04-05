from abc import ABC, abstractmethod
from enum import Enum
from typing import Sequence


class ProofStatus(Enum):
    Unknown = 0
    Proven = 1
    Disproven = 2


class NodeType(Enum):
    OR = 0
    AND = 1


class Evaluator(ABC):

    @abstractmethod
    def move(self, action: int):
        pass

    @abstractmethod
    def undo_move(self):
        pass

    @abstractmethod
    def evaluate(self) -> ProofStatus:
        pass

    @abstractmethod
    def actions(self) -> Sequence[int]:
        pass

    @property
    @abstractmethod
    def state(self) -> int:
        pass
