from abc import ABC, abstractmethod
from enum import Enum


class ProofStatus(Enum):
    Unknown = 0
    Proven = 1
    Disproven = 2


class NodeType(Enum):
    OR = 0
    AND = 1


class Evaluator(ABC):

    @abstractmethod
    def __init__(self, node_type: NodeType):
        self.node_type = node_type

    def move(self, action: int):
        self._switch_play()

    def undo_move(self):
        self._switch_play()

    def _switch_play(self):
        if self.node_type == NodeType.OR:
            self.node_type = NodeType.AND
        else:  # self.node_type == NodeType.AND
            self.node_type = NodeType.OR

    @abstractmethod
    def evaluate(self) -> ProofStatus:
        pass

    @property
    @abstractmethod
    def action_space(self) -> int:
        pass

